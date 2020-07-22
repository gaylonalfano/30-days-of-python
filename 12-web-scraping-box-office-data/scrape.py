import typing as t
import datetime
import requests
from requests_html import HTML

URL = "https://www.boxofficemojo.com/year/world/"

now = datetime.datetime.now()
today = datetime.datetime.today()


def url_to_html(
    url: str, filename: str = f"world-{today}.html", save: bool = False
):
    """
    Download the full HTML of any URL. Can use later with
    scraping to parse and save data for analysis.

    ? - Should I use string sub in default param or in func?
    """
    r = requests.get(URL)
    if r.status_code == 200:
        html_text = r.text
        if save:
            with open(filename, "w") as f:
                f.write(html_text)
        print(f"Request successful: {r.status_code}")
        return html_text
    return


# Save raw HTML text
html_text = url_to_html(URL, save=False)


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

print(table_data[:3])


"""
notes:
    - chrome > dev tools > cmd+shift+p > "disable javascript".
    this helps you get to see raw html without js changing it.
    - the table headers are stored in 'th' elements
    - the individual table cells data are stored in 'td'
"""
