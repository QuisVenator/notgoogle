from InputThread import InputThread
from CrawlerThread import CrawlerThread
from queue import LifoQueue

####Main function
threadCount = 10
queueList = list()
threadList = list()
queueCount = list()
for i in range(threadCount):
    queueList.append(LifoQueue())
    queueCount.append(0)

url = "https://de.wikipedia.org/wiki/Wikipedia:Hauptseite"
queueList[hash(url)%threadCount].put(url)

for i in range(threadCount):
    thread = CrawlerThread(threadCount, queueList, i, queueCount)
    thread.start()
    threadList.append(thread)

print("All {} threads up and running, starting input thread...".format(threadCount))
inputThread = InputThread(threadList)
inputThread.start()
print("Use \"status\" to see progress...")