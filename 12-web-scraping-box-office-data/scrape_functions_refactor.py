import os
import typing as t
import datetime
import regex as re
import requests
import pandas as pd
from requests_html import HTML

BASE_DIR = os.path.dirname(__file__)
BASE_URL = "https://www.boxofficemojo.com/year/world/"
NOW = datetime.datetime.now()
YEAR = NOW.year
URL = f"{BASE_URL}{YEAR}/"


def extract_year_from_url(url: str) -> int:
    """
    Parse and extract 'year' value from url.
    """
    if url == URL:
        # 'year' is current year
        year: int = YEAR
    else:
        # Parse 'year' from 'url'
        year_match: str = re.search(r"/(\d{4})/$", url).group(1)
        year: int = int(year_match)

    return year


def url_to_html(
    url: str = URL, prefix: str = "world", save: bool = False
) -> str:
    """
    Download the full HTML of any URL. Can use later with
    scraping to parse and save data for analysis.

    Params:
        url: str -> URL to scrape
        filename: str -> Filename prefix
        save: bool -> Save to file?
    """
    year = extract_year_from_url(url)

    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        if save:
            with open(f"{prefix}-{year}.html", "w") as f:
                f.write(html_text)
        print(f"Request successful: {r.status_code}")
        return html_text
    return None


# def parse_and_extract(url: str, prefix: str = "movies", year: int = YEAR):
#     """
#     Download raw html text from url.
#     Parse and extract data from HTML table.
#     Save data to CSV with filename argument.

#     Params:
#         url: str -> URL to parse
#         filename: str -> Filename prefix
#         year: int -> Year to parse
#     """

#     # Save raw HTML text
#     html_text = url_to_html(url, save=False)

#     # Convert raw HTML to requests_html HTML object
#     r_html = HTML(html=html_text)

#     # Find the specific table element within the HTML
#     table_class: str = ".imdb-scroll-table"
#     # table_class = "#table"  # Same result
#     r_table = r_html.find(table_class)
#     # print(r_table)
#     # [<Element 'div' id='table' class=('a-section', 'imdb-scroll-table', 'mojo-gutter')>]

#     # Extract just the text from the table (similar to r.text)
#     if len(r_table) == 1:
#         # print(r_table[0].text)  # Has data but unstructured
#         parsed_table = r_table[0]
#         rows: t.List = parsed_table.find(
#             "tr"
#         )  # list of [<Element 'tr'>, <Element 'tr'>, ...]
#         # Convert list of Elements to list of Lists
#         header_row = rows[0]  # <Element 'tr' >
#         header_cols = header_row.find("th")
#         # print(header_cols)  # [<Element 'th'> class(...), ...]
#         header_cols_names: t.List[str] = [h.text for h in header_cols]
#         # print(f"header_cols_names: {header_cols_names}")
#         # header_cols_names: ['Rank', 'Release Group', 'Worldwide', 'Domestic', '%', 'Foreign', '%']

#         # Build list of lists for each row aligned with column name
#         # Basically replicating a table view.
#         table_data: t.List[t.List[str]] = []
#         for row in rows[1:]:
#             # Table cells data stored in 'td' elements
#             cols: t.List = row.find("td")
#             # print(cols) # [<Element 'td' class=('a-text-right',...column')>,...]
#             row_data: t.List[str] = []
#             for i, col in enumerate(cols):
#                 # print(i, col.text)
#                 """
#                 0 1
#                 1 Bad Boys for Life
#                 2 $419,074,646
#                 3 $204,417,855
#                 4 48.8%
#                 5 $214,656,791
#                 6 51.2%
#                 """
#                 row_data.append(col.text)
#             table_data.append(row_data)

#     # Store table into Pandas dataframe so can save as CSV
#     df = pd.DataFrame(table_data, columns=header_cols_names)

#     # Set path to 'data' sub-dir; create if doesn't exist
#     path = os.path.join(BASE_DIR, "data")
#     os.makedirs(path, exist_ok=True)

#     # Set final filepath using 'filename' argument with .csv file type
#     filepath = os.path.join(path, f"{prefix}-{year}.csv")

#     # Export to CSV
#     try:
#         df.to_csv(filepath, index=False)
#         print(f"Saved at: {filepath}")
#     except:
#         print("Export to CSV failed!")


def parse_html_table(html: str) -> pd.DataFrame:
    """
    Parse and extract data from HTML table and save in
    pandas DataFrame object.

    Params:
        html: str -> Raw HTML to parse
    """
    # Save raw HTML text
    html_text = url_to_html()

    # Convert raw HTML to requests_html HTML object
    r_html = HTML(html=html_text)

    # Find the specific table element within the HTML
    table_class: str = ".imdb-scroll-table"
    # table_class = "#table"  # Same result
    r_table = r_html.find(table_class)
    # print(r_table)
    # [<Element 'div' id='table' class=('a-section', 'imdb-scroll-table', 'mojo-gutter')>]

    # Extract just the text from the table (similar to r.text)
    if len(r_table) == 1:
        # print(r_table[0].text)  # Has data but unstructured
        parsed_table = r_table[0]
        rows: t.List = parsed_table.find(
            "tr"
        )  # list of [<Element 'tr'>, <Element 'tr'>, ...]
        # Convert list of Elements to list of Lists
        header_row = rows[0]  # <Element 'tr' >
        header_cols = header_row.find("th")
        # print(header_cols)  # [<Element 'th'> class(...), ...]
        header_cols_names: t.List[str] = [h.text for h in header_cols]
        # print(f"header_cols_names: {header_cols_names}")
        # header_cols_names: ['Rank', 'Release Group', 'Worldwide', 'Domestic', '%', 'Foreign', '%']

        # Build list of lists for each row aligned with column name
        # Basically replicating a table view.
        table_data: t.List[t.List[str]] = []
        for row in rows[1:]:
            # Table cells data stored in 'td' elements
            cols: t.List = row.find("td")
            # print(cols) # [<Element 'td' class=('a-text-right',...column')>,...]
            row_data: t.List[str] = []
            for i, col in enumerate(cols):
                # print(i, col.text)
                """
                0 1
                1 Bad Boys for Life
                2 $419,074,646
                3 $204,417,855
                4 48.8%
                5 $214,656,791
                6 51.2%
                """
                row_data.append(col.text)
            table_data.append(row_data)

    # Store table into Pandas dataframe so can save as CSV
    df = pd.DataFrame(table_data, columns=header_cols_names)

    return df


def save_to_csv(
    url: str, prefix: str = "movies", year: t.Optional[int] = None
) -> None:
    """
    Save scraped data to CSV file format.

    Params:
        prefix: str = "movies"
        year: int = current year
    """
    df = parse_html_table(url)

    # Set path to 'data' sub-dir; create if doesn't exist
    path = os.path.join(BASE_DIR, "data")
    os.makedirs(path, exist_ok=True)

    # Set final filepath using 'filename' argument with .csv file type
    # TODO Consider using extract_year_from_url(url) function to get 'year'
    # value then can construct the final filepath.

    if year is not None:
        filepath = os.path.join(path, f"{prefix}-{year}.csv")
    else:
        filepath = os.path.join(path, f"{prefix}-UNKNOWN_YEAR.csv")

    # Export to CSV
    try:
        df.to_csv(filepath, index=False)
        print(f"Saved at: {filepath}")
    except:
        print("Export to CSV failed!")


def main(
    url: t.Optional[str] = None,
    start_year: t.Optional[int] = None,
    years_ago: int = 0,
    prefix: str = "movies",
):
    """
    First converts a URL to HTML text, which is then parsed for
    box office data and stored in CSV.

    Default is to scrape current year's data plus N years of
    historical data as specified.

    Params:
        start_year: t.Optional[int] = None
        year_ago: int = 0
    """
    if start_year is None:
        now: int = datetime.datetime.now()
        start_year: int = now.year
    assert isinstance(start_year, int)
    assert isinstance(years_ago, int)
    assert len(f"{start_year}") == 4
    parse_and_extract(f"{URL}/{start_year}")


"""
notes:
    - chrome > dev tools > cmd+shift+p > "disable javascript".
    this helps you get to see raw html without js changing it.
    - the table headers are stored in 'th' elements
    - the individual table cells data are stored in 'td'
"""
