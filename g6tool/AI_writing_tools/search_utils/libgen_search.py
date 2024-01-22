# https://pypi.org/project/libgen-api/


from libgen_api import LibgenSearch

libgen = LibgenSearch()


class LibgenBook:
    # result = {
    #     "ID": "241400",
    #     "Author": "H Falcke,F Hehl",
    #     "Title": "The Galactic Black Hole: Studies in High Energy Physics, Cosmology and Gravitation",
    #     "Publisher": "Taylor & Francis, IOP",
    #     "Year": "2002",
    #     "Pages": "359",
    #     "Language": "English",
    #     "Size": "13 Mb",
    #     "Extension": "pdf",
    #     "Mirror_1": "http://library.lol/main/DE69E9C3CF9E2D09CD6EC162BCD4793B",
    #     "Mirror_2": "http://libgen.li/ads.php?md5=DE69E9C3CF9E2D09CD6EC162BCD4793B",
    #     "Mirror_3": "https://library.bz/main/edit/DE69E9C3CF9E2D09CD6EC162BCD4793B",
    # }

    def __init__(self, result: dict):
        self.id = result.get("ID")
        self.title = result.get("Title")
        self.size = result.get("Size")
        self.pages = result.get("Pages")
        self.year = result.get("Year")
        self.language = result.get("Language")
        self.extension = result.get("Extension")
        self.author = result.get("Author")
        self.result = result

    @property
    def pdf_url(self):
        try:
            download_link = libgen.resolve_download_links(self.result)["GET"]
            return download_link
        except:
            return None


def search_in_libgen_pdf_books(query: str) -> list[LibgenBook]:
    title_filters = {"Extension": "pdf"}
    results = libgen.search_title_filtered(query, title_filters, exact_match=False)
    return [LibgenBook(result) for result in results]


if __name__ == "__main__":
    print("########################")
    print("########################")

    results = search_in_libgen_pdf_books("black holes")
    print("########################")
    print(len(results))
    print("########################")
    for result in results:
        print("_______________________")
        print(type(result))
        print(result.title)
        print(result.extension)
        print(result.pages)
        print(result.size)
        # print(result.pdf_url)
        print("*********************************************")

    print("########################")
