# Written by Paul Clarke 2020

from bs4 import BeautifulSoup
import requests

def getPlaylistLinks(url,playlist_key):
    '''
    Grab all the video links from a specific playlist

    Args:
        - url (string): The url of a video in the playlist
        - playlist_key (string): each playlist has a particular key that identifies it

    Return:
        - A list of all video links in the playlist

    '''

    page_source = requests.get(url).text
    soup = BeautifulSoup(page_source, 'html.parser')

    video_links = []
    initial_link = 'https://www.youtube.com/embed/'
    links = soup.find_all("a")

    # Go through all the links in the page
    for link in links:
        href = link.get('href')
        # check if the link is long enough to be a video
        if len(href) > 53:           
            key = href[26:53]
            # check if the link is a playlist video link
            if (key == playlist_key):
                # adjust the link for iFrame management and append it
                combo = initial_link + href[9:20]
                if (combo not in video_links):
                    video_links.append(initial_link + href[9:20])

    return video_links
    

links = getPlaylistLinks('https://www.youtube.com/watch?v=koAJ4LZu8eI&list=PLjGNXiulWlOQR1dvAJ8Si8eeZ38_zJ8dm&index=1',"PLjGNXiulWlOQR1dvAJ8Si8eeZ3")

html = open("uqcs_videos.html", mode="r", encoding="utf-8", errors="strict", buffering=1).read()
soup = BeautifulSoup(html, features="lxml")

# determine how many rows/cols are required
num_videos = len(links)
num_cols = 3 # arbitrary value

# Find specific line and append new information
location = soup.find("meta", {"class" : "pointer"})

# if the links already exist, delete them
con = soup.find('div',{'class' : 'appendage-content'})
if con is not None:
    con.decompose()

# initial holding tag
container = soup.new_tag('div')
container['class'] = 'appendage-content'
location.insert_after(container)

breaker = ''
current = ''

#plate up the videos
i = 0
while i < len(links):
    if i % 3 == 0:
        breaker = soup.new_tag('div')
        breaker['class'] = 'columns is-centered row-'+str(i)
        container.insert(1,breaker)
        current = breaker
        
    div = soup.new_tag('div')
    div['class'] = 'column is-4'
    div['style'] = 'display:flex;align-items:center'
    current.insert(1,div)
    
    vid = soup.new_tag('iframe')
    vid['allow'] = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture'
    vid['frameborder'] = '0'
    vid['height'] = '314'
    vid['width'] = '558'
    vid['src'] = links[i]
    div.insert(1,vid)

    i += 1


# rewrite the file with the new information
f = open("uqcs_videos.html", mode="w+", encoding="utf-8", errors="strict", buffering=1)
f.write(str(soup.prettify()))
f.close()

print('Task Completed!')





