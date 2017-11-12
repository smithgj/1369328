import time
from threading import Thread
import threading
from pprint import pprint

data = [None,None,None,None,None,None,None,None,None,None]

def myfunc(i):
    if i==3:
        data[i] = ['skip', 0]
        exit("1")
    if i==5:
        s=25
    else:
        s=i
    if i==6:
        raise ValueError('A very specific bad thing happened')
    print ("sleeping " + str(s) + " sec from thread %d" % i)
    time.sleep(s)
    print ("finished sleeping from thread %d" % i)
    data[i] = [i+i, i*i]


for i in range(10):
    my_name = 'thread_' + str(i)
    t = Thread(target=myfunc, args=(i,), name=my_name, daemon=True)
    t.start()


print("out of loop")
print(threading.active_count())
t.join()
print("after join")
print(threading.active_count())
pprint(data)
while threading.active_count() > 1 :
    print(threading.active_count())
    time.sleep(3)
print(threading.active_count())
pprint(data)