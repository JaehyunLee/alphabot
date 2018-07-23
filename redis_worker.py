from rq import Connection, Worker, Queue

with Connection():
    q = Queue()
    Worker(q).work()

