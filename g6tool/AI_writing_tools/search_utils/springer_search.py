import requests
from urllib.parse import urlparse, ParseResult
from bs4 import BeautifulSoup
from django_main.settings import SPRINGER_KEY
from collections import namedtuple

# for more info
# https://dev.springernature.com/adding-constraints
# https://dev.springernature.com

query = "black holes"
springer_api_key = SPRINGER_KEY
base_url_springer = "http://api.springernature.com/openaccess/json"
url_params_springer = {
    "api_key": springer_api_key,
    "start": 1,
    "p": 10,  # num of articles
    # "q": "doi:10.1134/S1063779623060096",
    "q": f'title:"{query}"',
    # "date-facet-mode": "between",
    # "date": "2017-01-01 TO 2019-12-31",
    "facet": "language",
    "facet-language": "en",
}

mathjax_cdn_script_tag = """
                        <script
                            type="text/javascript"
                            id="MathJax-script"
                            async
                            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
                        ></script>
                """


class SpringerArticle:
    def __init__(self, record: dict):
        self.record: dict = record
        self.creators = record.get("creators")
        self.title = record.get("title")
        self.journal = record["publicationName"]
        self.date = record["publicationDate"]
        self.summary = self.get_article_summary()
        self.page_url = self.get_page_url()

    def get_article_summary(self) -> str | None:
        data: dict = self.record.get("abstract", None)
        if data:
            return data.get("p")
        return None

    def get_page_url(self) -> str | None:
        try:
            data: dict = self.record.get("url", None)[0]
            if data:
                return data.get("value")

            return None
        except:
            return None

    @property
    def more_fast_pdf_url(self):
        """
        fetch the pdf download url
        by manipulating with the article url
        (replacing 'article' by 'content/pdf' and '.pdf' to the end)
        """
        try:
            res = requests.get(
                self.page_url,
            )
            res.raise_for_status()

            url = res.url.replace("article", "content/pdf") + ".pdf"
            print("done easy")
            # res1 = requests.get(url)
            # res1.raise_for_status()
            return url
        except:
            print("***************** hard way ******************")
            return self.scrap_pdf_url

    @property
    def pdf_url(self) -> str | None:
        """
        fetch the pdf download url by scrabing the article page
        """

        response = requests.get(self.page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            try:
                html_url = soup.find("meta", {"name": "citation_fulltext_html_url"})[
                    "content"
                ]
                try:
                    pdf_file_path = (
                        soup.find("body")
                        .find("div", class_="c-pdf-download u-clear-both u-mb-16")
                        .find("a", href=True)["href"]
                    )

                except:
                    pdf_file_path = (
                        soup.find("body")
                        .find("div", class_="c-pdf-download u-clear-both")
                        .find("a", href=True)["href"]
                    )

                parsed_html_url: ParseResult = urlparse(html_url)

                full_pdf_url = f"{parsed_html_url.scheme}://{parsed_html_url.netloc}{pdf_file_path}"
                return full_pdf_url
            except Exception as e:
                print(e)
                return None
        else:
            return None

    @property
    def as_html(self):
        """
        return the article content with it's html code
        """
        try:
            res = requests.get(self.page_url)
            res.raise_for_status()
            soup = BeautifulSoup(res.content, "html.parser")
            article_body = soup.find("main").find("div", class_="c-article-body")
            article_sections = article_body.find_all(class_="c-article-section")

            allsecs = ""
            for sec in article_sections:
                allsecs = allsecs + str(sec)

            allsecs = allsecs + mathjax_cdn_script_tag
            with open(
                f"{self.title[:5]}full_artical.html", "w", encoding="utf-8"
            ) as file:
                file.write(allsecs)
            return allsecs
        except:
            return None


def search_in_springer(query: str = query) -> list[SpringerArticle]:
    url_params_springer["q"] = f'title:"{query}"'
    records = requests.get(base_url_springer, params=url_params_springer)
    with open("f.json", "w") as f:
        f.write(records.text)
    records = records.json()["records"]
    print(records)

    return [SpringerArticle(record) for record in records]
