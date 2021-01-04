import threading, time
from dbinterface import DbInterface
from getlinks import getlinks

class CrawlerThread (threading.Thread):
    def __init__(self, threadCount : int, queueList, threadNum : int, queueCount):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.threadCount = threadCount
        self.queueList = queueList
        self.queueCount = queueCount
        self.killed = False
        self.linkMinBufferSize = 50
        self.linkMaxBufferSize = 500
    
    def run(self):
        self.conn = DbInterface("test.db")
        
        threadNum = self.threadNum
        tcount = self.threadCount
        queue = self.queueList[threadNum]
        touched = dict()
        self.completed = 0
        double = 0
        while not self.killed:
            while not queue.empty() and not self.killed:
                url = queue.get()
                if not url in touched:
                    touched[url] = 1
                    newurls = getlinks(url, self.conn)
                    if newurls:
                        for url in newurls:
                            if url in touched:
                                touched[url] += 1
                                double += 1
                            else:
                                index = hash(url)%tcount
                                self.queueList[index].put(url)
                                self.queueCount[index] += 1
                        self.completed += 1
                        self.queueCount[threadNum] += 1
                else:
                    touched[url] += 1
                    double += 1
                if self.queueCount[threadNum] >= self.linkMaxBufferSize:
                    self.dump()
            else:
                time.sleep(10)
    
    def terminate(self) :
        self.killed = True
    
    def dump(self):
        try:
            dumpFile = open("dump{}.txt".format(self.threadNum), "a")
        except:
            print("Error opening file for dumping excess links for thread {}".format(self.threadNum))
            return

        while self.queueCount[self.threadNum] > self.linkMinBufferSize:
            dumpFile.write(self.queueList[self.threadNum].get())
            dumpFile.write("\n")
            self.queueCount[self.threadNum] -= 1
