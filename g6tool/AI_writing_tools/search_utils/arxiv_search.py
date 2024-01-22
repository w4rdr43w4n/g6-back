# https://lukasschwab.me/arxiv.py/arxiv.html
# https://poe.com/chat/2t4f2epll96yl0li4gn

import arxiv


def search_in_arxiv(query: str, max_results: int = 10):
    client = arxiv.Client(page_size=100, delay_seconds=1.0, num_retries=3)

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )

    all_results = list(client.results(search))
    return all_results


if __name__ == "__main__":
    for r in search_in_arxiv("Quantum Gravity"):
        print("* * * * * * ")
        print(r.title)
        print(r.pdf_url)
        for l in r.links:
            if l.title == "doi":
                print(l)

        print("* * * * * * \n")
# print(all_results[0].summary)

# ...or exhaust it into a list. Careful: this is slow for large results sets.
# print([r.title for r in all_results])
