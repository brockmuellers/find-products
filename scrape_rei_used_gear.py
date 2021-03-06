import scrape_utils


REI_USED_SEARCH_URL_FILE = "rei_used_search_urls.csv"
REI_USED_RESULTS_DIR = "results/rei_used/"


# Messy logic, specific to the REI website.
def scrape():
    # Load file of URLs to scrape, which are search result pages
    labeled_urls = scrape_utils.open_search_urls(REI_USED_SEARCH_URL_FILE)

    for labeled_url in labeled_urls:
        # List to collect available products we encounter
        available_products = []

        label = labeled_url["label"]
        url = labeled_url["url"]

        print("\n----------------------------\n")
        print("EXAMINING PRODUCT: " + label)
        print("Search URL: " + url)

        # Load the page and parse out search result items
        search_soup = scrape_utils.get_soup(url)
        items = search_soup.find_all("li", class_="TileItem")

        # The number of search results the page thinks we should have (for validation)
        expected_count_div = search_soup.find("div", class_="count")

        if expected_count_div is None:
            # Nothing was found for this search
            print("No products found.")
            expected_count = 0
        else:
            expected_count = int(expected_count_div.find("span").contents[0])

        # Make sure we have the same number of items the page says we should have
        # This might throw an error if the search results are paginated, and not
        # all are loaded, or if the page structure changes
        if len(items) != expected_count:
            raise AssertionError(
                "Error on page {}: found {} items, but page said there would be {}".format(
                    url, len(items, expected_count)))

        # Handle each individual item, and add to available_products list
        for item in items:
            title = item.find_all("span", class_="title")[0].contents[0]
            print("Found product " + title)

            available_products.append(title)

            # Get the URL in case you want to explore it; this is real brittle
            # item_path = item.find_all("a")[0]['href']
            # item_url = "http://www.rei.com" + item_path

        # Compare to the previous list of products, and save this list for future comparisons..
        scrape_utils.compare_and_save_products(available_products, label, REI_USED_RESULTS_DIR)
