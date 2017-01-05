"""Uses Requests and BeautifulSoup to collect all the links from the front page of reddit.com"""


import requests
from bs4 import BeautifulSoup
import urllib.request

def get_links():
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

    #For links that lead to comment sections, parse again for href
    for i in range (1, len(list_of_links)):
        if 'https://www.reddit.com' in list_of_links[i]:
            response2 = requests.get(list_of_links[i])
            html2 = response2.content
            soup2 = BeautifulSoup(html2, 'lxml')

            for post2 in soup2.findAll(attrs={'class':'title'}):
                for link2 in post2.findAll('a'):
                    list_of_links[i] = link2.get('data-href-url')

    #Remove any elements of the list that return None.
    for i in range (1, len(list_of_links)):
        if list_of_links[i] == "None":
            list_of_links[i].remove()

    return(list_of_links)

def write_links(list, filename):
    #Write the links to a text file.
    link_file = open(filename, 'w')
    for link in list:
        link_file.write(str(link) + '\n')
    link_file.close()

def get_titles():
    #Set up BeautifulSoup with /r/all
    website = "https://reddit.com/r/all/"
    response = requests.get(website)
    html = response.content

    web_soup = BeautifulSoup(html, 'lxml')

    list_of_titles = []
    for post in web_soup.findAll(attrs={'class':'title'}):
        for title in post.findAll('a', attrs={'class':'title'}):
            list_of_titles.append(title.string)

    return(list_of_titles)

def zip_lists(list1, list2):
    zipped_list = list(zip(list1, list2))
    return(zipped_list)

def download_images(list):
    for x,y in list:
        if "imgur.com" in y:
            extensions = ('.jpeg', '.jpg', '.png', '.gif', '.gifv', '.apng', '.tiff', '.pdf', '.xcf', '.mp4')
            if y.endswith(extensions):
                urllib.request.urlretrieve(y, "Images/%s" %x)



def get_imgur_image(url):
    response = requests.get(url)
    html = response.content

    imgur_soup = BeautifulSoup(html)

    f

#def get_reddit_image(url):
    #function here

download_images(zip_lists(get_titles(), get_links()))
#write_links(get_links(), 'link_list.txt')
