import threading
from queue import Queue
from datetime import datetime
import socket
import sys
myMaxThread=200

def myScan(myPort):
    
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(5)
    try:
        #print(port)
        myConnection = mySocket.connect((myIP,myPort))
        with print_lock:
            print('Port Open',myPort)
        myConnection.close()
    except:
        pass

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        myWorker = myQueue.get()

        # Run the example job with the avail worker in queue (thread)
        myScan(myWorker)

        # completed with the job
        myQueue.task_done()


if len(sys.argv) >= 2:
    myPercentage=0
    print_lock = threading.Lock()
    myTarget = sys.argv[1]
    myPortStart = sys.argv[2]
    myPortEnd = sys.argv[3]
    myIP = socket.gethostbyname(myTarget)
else:
    print("Usage : ",sys.argv[0], " Target StartPort EndPort")
    sys.exit(1)        

# Create the queue and threader 
myQueue = Queue()

# how many threads are we going to allow for
for x in range(myMaxThread):
     myThread = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
     myThread.daemon = True

     # begins, must come after daemon definition
     myThread.start()


t1 = datetime.now()

# Port Scan job
for myPorts in range(int(myPortStart),int(myPortEnd)):
    myQueue.put(myPorts)
    

# wait until the thread terminates.
myQueue.join()
t2 =  datetime.now()
total = t2 - t1
myScanTime = str(total).split(':')
print(myScanTime)
print ("Scanning completed in: ",myScanTime[0]," Hours ",myScanTime[1]," Minutes & ",myScanTime[2]," Seconds.")