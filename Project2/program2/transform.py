from bs4 import BeautifulSoup
import urllib.request
import csv

web_page = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions')
soup = BeautifulSoup(web_page, "html.parser")
super_bowl_table = soup.find_all('table', {'class': 'wikitable'})[1]

in_file = open("result.csv", 'w')
csv_writer = csv.writer(in_file, delimiter=',')
csv_writer.writerows([["Game number", "year", "winning team", "score", "losing team", "venue"]])

super_bowl_list = []

for row in super_bowl_table.find_all('tr')[1:51]:
    cells = row.find_all('td')
    super_bowl_list = [[cells[0].find('span', {'class': 'sorttext'}).get_text(), cells[1].find_all('span')[1].get_text().split()[2], cells[2].find('span', {'class': 'sortkey'}).get_text().replace(" !", ""), cells[3].find('span', {'class': 'sorttext'}).get_text(), cells[4].find('span', {'class': 'sortkey'}).get_text().replace(" !", ""), cells[5].find('span', {'class': 'sortkey'}).get_text().replace(" !", "")]]
    csv_writer.writerows(super_bowl_list)

