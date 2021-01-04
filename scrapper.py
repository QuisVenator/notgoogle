from getlinks import getlinks
from queue import LifoQueue

startingPoint = "https://de.wikipedia.org/wiki/Wikipedia:Hauptseite"

completed = 0
waiting = 0
touched = dict()
urlqueue = LifoQueue()
urlqueue.put(startingPoint)

while not urlqueue.empty():
    url = urlqueue.get()
    touched[url] = 1
    newurls = getlinks(url)
    if newurls is None: continue
    for url in newurls:
        if url in touched:
            touched[url] += 1
        else:
            waiting += 1
            urlqueue.put(url)
    completed += 1

    print("Waiting: {}".format(waiting), "Completed: {}".format(completed))