"""Uses Requests and BeautifulSoup to collect all the links from the front page of reddit.com"""


"""TODO: If a link goes to reddit comments, this html seems to be common to all comment pages:
    <div class="siteTable ...">
        <div class="thumbnail ...">
            <a href=(***link here***)>
        Take the reddit comments link and replace it with the href from the thumbnail.
"""

import requests
from bs4 import BeautifulSoup

#set up BeautifulSoup with website
website = "https://reddit.com/r/all/"
response = requests.get(website)
html = response.content

web_soup = BeautifulSoup(html, 'lxml')

#create a list of links of all the required characteristics
list_of_links = []
for post in web_soup.findAll(attrs={'class':'title'}):
    for link in post.findAll('a'):
        url = link.get('href')
        list_of_links.append(url)

#Remove links not part of any Reddit posts - they contain /domain/ and /r/
for element in list_of_links:
    if "/domain/" in element or '/r/' in element:
        list_of_links.remove(element)

#Change links to only subreddits to full https links
for i in range (1, len(list_of_links)):
    if '/r/' in list_of_links[i]:
        list_of_links[i] = "https://www.reddit.com" + list_of_links[i]

#for links that lead to comment sections, parse again for href
for i in range (1, len(list_of_links)):
    if 'https://www.reddit.com' in list_of_links[i]:
        response2 = requests.get(list_of_links[i])
        html2 = response2.content
        soup2 = BeautifulSoup(html2, 'lxml')

        for post2 in soup2.findAll(attrs={'class':'title'}):
            for link2 in post2.findAll('a'):
                print(link2.prettify())

#print(list_of_links)
#link_file = open('link_list.txt', 'w')
#for link in list_of_links:
    #link_file.write(link + '\n')
