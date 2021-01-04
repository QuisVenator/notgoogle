import threading
class InputThread(threading.Thread):
    def __init__(self, threadList):
        threading.Thread.__init__(self)
        self.threadList = threadList
        self.crawlingStopped = False
    
    def run(self):
        while True:
            cmd = input()
            
            if cmd == "status":
                tCompleted = 0
                tWaiting = 0
                for thread in self.threadList:
                    completed = thread.completed
                    waiting = thread.queueCount[thread.threadNum]
                    print("Thread {}:".format(thread.threadNum))
                    print("Completed: {}\nWaiting: {}".format(completed, waiting))
                    tCompleted += completed
                    tWaiting += waiting
                print("\n\nTOTOAL {} completed and {} waiting".format(tCompleted, tWaiting))

            elif cmd == "force-exit":
                print("Killing threads...")
                for thread in self.threadList:
                    thread.terminate()
                print("All crawler threads killed, use stop to terminate programm")
                self.crawlingStopped = True
            
            elif cmd == "stop":
                if self.crawlingStopped:
                    break
                else:
                    print("There are still crawling threads active, please use \"force-exit\" to stop these first!")