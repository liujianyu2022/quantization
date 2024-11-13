from datetime import datetime
from math import ceil

import requests
from bs4 import BeautifulSoup
import mysql.connector as mdb


def obtain_parse_wiki_snp500():
    """
    Download and parse the Wikipedia list of S&P500 
    constituents using requests and BeautifulSoup.

    Returns a list of tuples to add to MySQL.
    """
    # Stores the current time for the created_at record
    now = datetime.utcnow()

    # Use requests and BeautifulSoup to download the 
    # list of S&P500 companies and obtain the symbol table
    response = requests.get(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )
    soup = BeautifulSoup(response.text, "html.parser")

    # This selects the first table, using CSS Selector syntax
    # and then ignores the header row ([1:])
    symbolslist = soup.select('table')[0].select('tr')[1:]

    # Obtain the symbol information for each 
    # row in the S&P500 constituent table
    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(
            (
                tds[0].select('a')[0].text.strip(),  # Ticker
                'stock', 
                tds[1].select('a')[0].text.strip(),  # Name
                tds[3].text.strip(),  # Sector
                'USD', now, now
            ) 
        )
    return symbols


def insert_snp500_symbols(symbols):
    """
    Insert the S&P500 symbols into the MySQL database.
    """
    # Database connection details
    db_host = 'localhost'
    db_user = 'root'
    db_pass = 'liujianyu'
    db_name = 'quantization'
    
    # Establish a connection to the MySQL database
    con = mdb.connect(
        host=db_host, user=db_user, password=db_pass, database=db_name
    )

    # Create the insert strings
    column_str = """ticker, instrument, name, sector, 
                 currency, created_date, last_updated_date
                 """
    insert_str = ("%s, " * 7)[:-2]
    final_str = "INSERT INTO symbol (%s) VALUES (%s)" % \
        (column_str, insert_str)

    # Using the MySQL connection, carry out 
    # an INSERT INTO for every symbol
    with con: 
        cur = con.cursor()
        cur.executemany(final_str, symbols)
        con.commit()


if __name__ == "__main__":
    symbols = obtain_parse_wiki_snp500()
    insert_snp500_symbols(symbols)
    print(f"{len(symbols)} symbols were successfully added.")
