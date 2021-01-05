import urllib.request, urllib.parse, urllib.error, re
from dbinterface import DbInterface
from bs4 import BeautifulSoup

def getlinks(url, connection : DbInterface):
    if not "wikipedia.org" in url: return
    
    try :
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    except:
        return
    
    htmlTag = soup.find("html")
    if htmlTag is None or not "de" in htmlTag.get("lang", ""): return False

    links = set()
    words = dict()
    for tag in soup("a"):
        if "href" in tag.attrs:
            parsedurl = urllib.parse.urlparse(tag["href"])
            if parsedurl.scheme in ("http", "https"):
                links.add(tag["href"])
    
    for tag in soup("meta"):
        if "description" in tag.attrs and len(tag.get("content", "")) <= 400:
            description = tag.get("content", "").split()
            for word in description:
                word = re.sub('[^a-z0-9äüöñßáéíóúý]+', '', word.lower(), flags=re.IGNORECASE)
                words[word] = 1
        elif "keywords" in tag.attrs and len(tag.get("content", "")) <= 200:
            keywords = tag.get("content", "").split()
            for word in keywords:
                word = re.sub('[^a-z0-9äüöñßáéíóúý]+', '', word.lower(), flags=re.IGNORECASE)
                words[word] = 1
    try:
        title = soup.find("title").text
        if len(title) <= 200:
            for word in title.split():
                word = re.sub('[^a-z0-9äüöñßáéíóúý]+', ' ', word.lower(), flags=re.IGNORECASE)
                if word in words: words[word] += 0.1
                else: words[word] = 1
    except:
        pass

    #TODO pass a connection and insert all words in database
    connection.insert_data(words, url, links)
    
    return links

#debug function with standard url
#getlinks("https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser")

#url = "https://de.wikipedia.org/wiki/Wikipedia:Hauptseite"
#for link in getlinks(url, None):
#    print(link)