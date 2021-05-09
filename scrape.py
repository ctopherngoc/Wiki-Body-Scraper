from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv


class Scrape:
    """
    Wikipedia scrape class
    """

    def __init__(self, link):
        """
        Obtain Wikipedia link from request.
        """
        self.link = link
        body = self.parseURL()
        self.getText(body)

    def parseURL(self):
        """

        """
        # parse web page
        uClient = uReq(self.link)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")

        error = "Wikipedia does not have an article with this exact name"
        if error in page_soup:
            return "error"

        # scrape following html tags
        page_body = page_soup.body.findAll(['h1', 'h2', 'h3', 'h4', 'd1', 'p'])
        return page_body

    def getText(self, body):
        """
        output: wiki text.csv
        Sets csv delimiter = "~" and lineterminator="\n"
        Goes through html element and place headers and p in column A of excel.

        Removes commas from each line.
        """

        # creates writable CSV file
        filename = "text.csv"
        f = csv.writer(open(filename, 'w'), delimiter='~', lineterminator='\n')

        # loop through html element
        for x in body:

            # removes sup html tags
            while x.find('sup'):
                x.find('sup').extract()

            # remove empty html tags
            if len(x.text.strip()) == 0:

                # Remove empty tag
                x.extract()

            # if element has text
            elif x.text:

                # skips if html tag = Contents
                headerList = ["Contents", "Navigation menu", "References", "See also", "External links"]
                if x.text in headerList:
                    pass

                # if other than Contents
                else:
                    # add string to CSV
                    line = x.text

                    # removes all commas then adds to csv
                    line = line.replace(',', '')
                    line = line.encode("ascii", "ignore")
                    line = line.decode()
                    f.writerow([line])

            else:
                pass


# example
# my_url = "https://en.wikipedia.org/wiki/Lego"
# test = Scrape(my_url)
# body = test.parseURL()
# test.getText(body)
