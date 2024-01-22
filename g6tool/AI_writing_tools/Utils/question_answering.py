from .ai_utils import GPT
import re
from scipy import spatial
import heapq
import tiktoken


class QuestionAnswering:

    def extract_text():
        pass

    def create_chunks(text, n):
        """Returns successive n-sized chunks from provided text."""
        tokenizer = tiktoken.get_encoding("cl100k_base")
        tokens = tokenizer.encode(text)
        i = 0
        chunks = []
        while i < len(tokens):
            # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
            j = min(i + int(1.5 * n), len(tokens))
            while j > i + int(0.5 * n):
                # Decode the tokens and check for full stop or newline
                chunk = tokenizer.decode(tokens[i:j])
                if chunk.endswith(".") or chunk.endswith("\n"):
                    break
                j -= 1
            # If no end of sentence found, use n tokens as the chunk size
            if j == i + int(0.5 * n):
                j = min(i + n, len(tokens))
            chunks.append(tokenizer.decode(tokens[i:j]))
            i = j
        if GPT.gpt3_tokens_calc(chunk[-1]) < 100:
            chunks[-2] += chunks.pop()
        return chunks

    def divide_and_embed(
        corpus: str,
    ):
        """
        estimated time of execution: 1 second per 5_000 token
        """
        splitted = re.split("\.\n", corpus)
        paragraphs = []
        for elem in splitted:
            if len(elem) < 15:
                continue
            if len(elem) / 3 > 8_000:
                chunks = QuestionAnswering.create_chunks(elem, 1_000)
                for chunk in chunks:
                    paragraphs.append(chunk)
            else:
                paragraphs.append(elem)

        paragraphs = [p + "." for p in paragraphs]
        embeddings = []
        _input = []
        n_avg_tokens = 0
        usage = 0
        for i in range(len(paragraphs)):
            _input.append(paragraphs[i])
            n_avg_tokens += len(paragraphs[i])
            if i != len(paragraphs) - 1:
                if n_avg_tokens + len(paragraphs[i + 1]) < 8_000:
                    continue
            embed_req = GPT.embed(
                _input=_input,
            )
            data = embed_req.data
            for embedding in data:
                embeddings.append(embedding.embedding)
            usage += embed_req.usage.total_tokens
            _input = []
            n_avg_tokens = 0
        data = {
            "paragraphs": paragraphs,
            "embeddings": embeddings,
            "n_tokens": usage
        }
        return data

    def query(
        questions: list[str],
        top_n: int,
        paragraphs,
        embeddings,
        relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y)
    ):
        questions_embeddings = GPT.embed(questions)
        relatedness = [
            [
                relatedness_fn(question_embedding.embedding, embedding) for embedding in embeddings
            ]
            for question_embedding in questions_embeddings.data]
        maxs = [heapq.nlargest(top_n, arr) for arr in relatedness]
        most_related_paragraphs = [None] * len(questions)
        for i in range(len(questions)):
            most_related_paragraphs[i] = [
                paragraphs[relatedness[i].index(_max)] for _max in maxs[i]]
        return most_related_paragraphs, maxs

    def ask_gpt(
        questions: list[str],
        related_paragraphs,
        relatednesses,
    ):
        pass
