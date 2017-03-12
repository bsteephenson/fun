
import threading
import queue
import time

# Apparently the built-in Queue has everything you need
# (particularly blocking and safe access)

def client(q):
	for i in range(10):
		q.put(i)
		time.sleep(0.25)


def server(q):
	for i in range(10):
		print "Server got: " + str(q.get())

q = queue.Queue()

client = threading.Thread(target = client, args = [q])
server = threading.Thread(target = server, args = [q])

client.start()
server.start()

client.join()
server.join()

# This was not as interesting as I hoped.. Oh well!
