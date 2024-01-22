import wikipedia as wk
import wikipediaapi as wkapi
import re
import openai
import tiktoken
from tenacity import retry, wait_exponential, stop_after_attempt
import pycld2 as cld2
from django_main.settings import OPENAI_KEY


openai.api_key = OPENAI_KEY


class Wiki:
    base_agent = ".wikipedia.org"

    langs = [
        "en",
        "ceb",
        "de",
        "sv",
        "fr",
        "nl",
        "ru",
        "es",
        "it",
        "arz",
        "pl",
        "ja",
        "zh",
        "uk",
        "vi",
        "war",
        "ar",
        "pt",
        "fa",
        "ca",
        "sr",
        "id",
        "ko",
        "no",
        "ce",
        "fi",
        "tr",
        "cs",
        "hu",
        "tt",
        "sh",
        "ro",
        "nan",
        "eu",
        "ms",
        "eo",
        "he",
        "hy",
        "da",
        "bg",
        "cy",
        "sk",
        "uz",
        "azb",
        "et",
        "be",
        "kk",
        "min",
        "el",
        "hr",
        "lt",
        "gl",
        "az",
        "ur",
        "sl",
        "lld",
        "ka",
        "nn",
        "hi",
        "th",
        "ta",
        "bn",
        "mk",
        "la",
        "yue",
        "ast",
        "lv",
        "af",
        "tg",
    ]

    SECTIONS_TO_IGNORE = [
        "See also",
        "References",
        "External links",
        "Further reading",
        "Footnotes",
        "Bibliography",
        "Sources",
        "Citations",
        "Literature",
        "Footnotes",
        "Notes and references",
        "Photo gallery",
        "Works cited",
        "Photos",
        "Gallery",
        "Notes",
        "References and sources",
        "References and notes",
    ]

    @classmethod
    def get_langs(cls):
        langs = {}
        for key in cls.langs:
            langs[key] = wk.languages()[key]
        return langs

    @classmethod
    def search(
        cls, title: str, lang: str, n_suggestions: int = 10, summary=False
    ) -> list[dict[str, bool, str]]:
        wk.set_lang(lang)
        suggestions = wk.search(title, results=n_suggestions, suggestion=False)
        if not summary:
            for suggestion in suggestions:
                if suggestion.find("disambiguaton") != -1:
                    suggestions.drop(suggestion)
            return suggestions
        else:
            suggestions_summaries = []
            for suggestion in suggestions:
                try:
                    summary = wk.summary(
                        suggestion, auto_suggest=False, redirect=False)
                    suggestion_summary = {
                        "suggestion": suggestion,
                        "disambiguation": False,
                        "summary": summary,
                    }
                    suggestions_summaries.append(suggestion_summary)
                except wk.exceptions.DisambiguationError as err:
                    suggestion_summary = {
                        "suggestion": suggestion,
                        "disambiguation": True,
                        "summary": err.options,
                    }
                    suggestions_summaries.append(suggestion_summary)
            print(suggestions_summaries)
            return suggestions_summaries

    def summary(page_id):
        summary = wk.summary(page_id, auto_suggest=False, redirect=False)
        return summary

    def get_page(
        title, lang
    ) -> list[dict[str, list[str] | None, list[str], list[int]]]:
        """
        Returns a
        _________
        \n\nparameters:\n
        title: wikiedia page title.
        \nThis function takes a wikipedia page title, and returns a list of dictionaries, each of which contains four keys:
            \n	"section_title" key: the section's title.
            \n	sub_sections" key: contains a list of sub_sections titles or None if there are no sub_sections.
            \n	"content" key: contains a list of contents, one content per sub_section. If there are no sub_sectios then the content belongs directly to the original "section_title".
            \n	"n_tokens": number of tokens per each content calculated with "cl100k_base" encoder.
        """
        wk.set_lang(lang)
        page = wk.WikipediaPage(title=title)
        content = page.content

        content = content.partition("\n\n\n== See also ==")[0]
        sections_txt = "\n\n\n== .* =="
        sections_titles = re.findall(sections_txt, content)
        sections_titles = [
            re.search("= .* =", title)[0][2:-2] for title in sections_titles
        ]
        sections_titles.insert(0, "Introduction")
        sections_contents = re.split(sections_txt, content)

        sub_secs = []
        for content in sections_contents:
            if GPT.gpt3_tokens_calc(content) == 0:
                continue
            if GPT.gpt3_tokens_calc(content) > 2_000:
                sub_sec_txt = "\n\n\n=== .* ==="
                sub_secs_titles = re.findall(sub_sec_txt, content)
                sub_secs_titles = [
                    re.search("= .* =", title)[0][2:-2] for title in sub_secs_titles
                ]
                sub_secs_contents = re.split(sub_sec_txt, content)
                if sub_secs_contents[0] == "":
                    sub_secs_contents.remove(sub_secs_contents[0])
                else:
                    sub_secs_titles.insert(0, "[[intro]]")
                sub_secs.append(
                    {"sub_sections": sub_secs_titles,
                        "contents": sub_secs_contents}
                )
            else:
                sub_secs.append({"sub_sections": None, "contents": [content]})

        page_contents = []
        for sec_title, sub_section in zip(sections_titles, sub_secs):
            page_contents.append(
                {
                    "section_title": sec_title,
                    "sub_sections": sub_section["sub_sections"],
                    "contents": sub_section["contents"],
                    "n_tokens": [
                        GPT.gpt3_tokens_calc(c) for c in sub_section["contents"]
                    ],
                }
            )
        return page_contents

    def page(title, lang, permitted_chars: int = 10_000):
        agent = lang + Wiki.base_agent
        wiki = wkapi.Wikipedia(user_agent=agent, language=lang)
        page = wkapi.WikipediaPage(wiki=wiki, title=title, language=lang)

        if not page.exists:
            raise ValueError(f'Page "{title}" doesn\'t exist.')

        page_contents = []

        def chunk(title, type_, content):
            page_contents.append(
                {"title": title, "type": type_, "content": content})
        chunk(title, "page_title", page.summary)

        def flat_sections(sections):
            for section in sections:
                if section.title in Wiki.SECTIONS_TO_IGNORE:
                    continue
                if len(section.full_text()) < permitted_chars or not section.sections or section.level == 5:
                    chunk(
                        section.title,
                        "heading_" + str(section.level),
                        section.full_text()[len(section.title):]
                    )
                else:
                    chunk(
                        section.title, "heading_" +
                        str(section.level),
                        section.text)
                    flat_sections(section.sections)

        flat_sections(page.sections)

        return page_contents

    def page_section(title: str, section: str, lang):
        agent = lang + Wiki.base_agent
        wiki = wkapi.Wikipedia(user_agent=agent, language=lang)
        page = wkapi.WikipediaPage(wiki=wiki, title=title, language=lang)
        sections = page.section_by_title(title=section)
        return [section.full_text() for section in sections]


# Ai tools
class GPT:
    # https://openai.com/blog/new-models-and-developer-products-announced-at-devday
    # https://pypi.org/project/arxiv/
    # https://newspaper.readthedocs.io/en/latest/
    # https://pypi.org/project/nytimesarticle/
    # https://pypi.org/project/scholarly/
    # https://biopython.org/wiki/Documentation
    # https://pypi.org/project/Wikidata/
    # https://newsapi.org/docs
    # Google Books API
    # https://pypi.org/project/gdelt/

    class Models:
        gpt_35_1106 = "gpt-3.5-turbo-1106"
        gpt_4 = "gpt-4"
        gpt_4_turbo = "gpt-4-1106-preview"
        gpt_4_vision = "gpt-4-vision-preview"
        base_model = gpt_35_1106
        embedding_model = "text-embedding-ada-002"

    tokenizer = tiktoken.get_encoding("cl100k_base")

    __improvements = {
        "Grammatics & Semantics": "Address any grammatical or spelling errors.",
        "Engagement": "Use engaging language to make the text more compelling",
        "Clarity": "Rephrase any complex or unclear sections for clarity",
        "Summarization": "Summarize where necessary",
    }

    def embed(_input, model=Models.embedding_model):
        return openai.embeddings.create(input=_input, model=model)

    def response_message(response):
        return [choice["message"]["content"] for choice in response["choices"]]

    def finish_reason(response):
        return [choice["finish_reason"] for choice in response["choices"]]

    def gpt3_tokens_calc(
        argument, chat=False, encoding=tiktoken.get_encoding("cl100k_base")
    ):
        if chat:
            num_tokens = 0
            for message in argument:
                # every message follows <im_start>{role/name}\n{content}<im_end>\n
                num_tokens += 4
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        elif not chat:
            encoded_string = encoding.encode(argument)
            tokens = [encoding.decode([token]) for token in encoded_string]
            return len(tokens)

    def preproc_wiki_page(page):
        streamer = []
        for section in page:
            streamer.append(
                {"chunk": section["section_title"], "type": "section"})
            if section["sub_sections"] is not None:
                for sub, content in zip(section["sub_sections"], section["contents"]):
                    if sub == "[[intro]]":
                        streamer.append({"chunk": content, "type": "content"})
                    else:
                        streamer.append({"chunk": sub, "type": "sub_section"})
                        streamer.append({"chunk": content, "type": "content"})
            else:
                streamer.append(
                    {"chunk": section["contents"][0], "type": "content"})
        return streamer

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=5), stop=stop_after_attempt(5)
    )
    def rewrite_wiki_section(
        content: str, language: str, model=Models.base_model, stream: bool = True
    ):
        """ """
        try:
            language = wk.languages()[language]
            res = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You will be given an article and your goal is to paraphrase it in {language}",
                    },
                    {"role": "user", "content": content},
                ],
                n=1,
                temperature=1,
                max_tokens=8_000,
                stream=stream,
            )
            return res
        except Exception as e:
            print(e)
            raise Exception(e)

    def completion_feed_from_text(text, max_tokens=40):
        mirrored = text[::-1]
        last_paragraph = re.split("\n", mirrored)[0]
        last_paragraph_sentences = re.split("\.", last_paragraph)
        last_sentence = last_paragraph_sentences[0][::-1]
        encoded = GPT.tokenizer.encode(last_sentence)
        if (len(encoded) <= 10) & (len(last_paragraph_sentences) > 1):
            encoded = GPT.tokenizer.encode(
                last_paragraph_sentences[1][::-1]) + encoded
        if len(encoded) >= max_tokens:
            feed = GPT.tokenizer.decode(encoded[-max_tokens:])
        else:
            feed = GPT.tokenizer.decode(encoded)
        return feed

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=5), stop=stop_after_attempt(5)
    )
    def paragraph_completion(
        prompt,
        title,
        description=False,
        sentence=False,
        n=1,
        max_tokens=70,
        model=Models.gpt_35_1106,
        stream: bool = True,
    ):
        messages = [
            {
                "role": "system",
                "content": f"you will be given the start of a paragrah and your goal is to complete it.\n\
                        The paragraph is within an article with the title {title}.",
            },
            {"role": "user", "content": prompt},
        ]

        if description:
            messages[0]["content"] += f"The discription of the article is {description}"

        try:
            res = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                n=n,
                max_tokens=max_tokens,
                stop="." if sentence else "\n",
                temperature=1,
                stream=stream,
            )
            return res
        except Exception as e:
            raise Exception(e)

    def improvement_messages(
        text: str,
        lang,
        instruction: str = "",
    ):
        language = wk.languages()[lang]
        messages = [
            {
                "role": "system",
                "content": f"You will be given a piece of text and your goal is to paraphrase it \
                            and to improve the quality and relevance of it\n\n\
                            please:\n\
                            - Use engaging language to make the text more compelling.\n\
                            - Rephrase any complex or unclear sections for clarity.\n\
                            - USe the same language as the text which is {language}\n\
                            - Return the improved text only without any Brackets.",
            },
            {"role": "user", "content": f"Improve this piece of text: {text}"},
        ]
        if instruction:
            messages[0]["content"] += f"- {instruction},"
        data = {
            "messages": messages,
            "tokens": GPT.gpt3_tokens_calc(messages, chat=True),
        }
        return data

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=5), stop=stop_after_attempt(5)
    )
    def improvement(messages, n=1, model=Models.gpt_35_1106, stream: bool = True):
        try:
            res = openai.ChatCompletion.create(
                model=model, messages=messages, n=n, temperature=1, stream=stream
            )
            return res
        except Exception as e:
            raise Exception(e)

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=5), stop=stop_after_attempt(5)
    )
    def chat(
        messages,
        model=Models.gpt_35_1106,
        max_tokens=1_000,
    ):
        print(model)
        res = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=True,
            max_tokens=max_tokens,
        )
        return res


class AIUtils:
    def detect_lang(
        text,
    ):
        """
        Only use with meaningful sentences with at least 3 words containing 3 litters each
        """
        detection = cld2.detect(text, returnVectors=True)
        if detection[0]:
            detected_languages = detection[2]
            top_language = detected_languages[0][1]
            return top_language


# from Bio import Entrez

# def search(query):
#     Entrez.email = 'your.email@example.com' # Always tell NCBI who you are
#     handle = Entrez.esearch(db='pubmed', sort='relevance', retmax='50', retmode='xml', term=query)
#     results = Entrez.read(handle)
#     return results

# def fetch_details(id_list):
#     ids = ','.join(id_list)
#     Entrez.email = 'your.email@example.com'
#     handle = Entrez.efetch(db='pubmed', retmode='xml', id=ids)
#     results = Entrez.read(handle)
#     return results

# if __name__ == '__main__':
#     results = search('fever')
#     id_list = results['IdList']
#     papers = fetch_details(id_list)
#     for i, paper in enumerate(papers['PubmedArticle']): print("%d) %s" % (i+1, paper['MedlineCitation']['Article']['ArticleTitle']))

# Replace `'your.email@example.com'` with your actual email address. NCBI uses the email field to track usage and to send warning messages if a script is misbehaving. Also replace `'fever'` with the keyword you want to search.

# This script will return the titles of up to 50 recent papers related to fever, with most relevant papers first.
