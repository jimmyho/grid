import gevent
import zmq.green as zmq
import gevent.monkey
from gevent.event import Event
import sys
# import zmq

gevent.monkey.patch_all()
port = "5556"
stop = Event()
# Socket to talk to server
context = zmq.Context()
def server(stop):
    socket = context.socket(zmq.SUB)

    print "Collecting updates from weather server..."
    socket.connect ("tcp://localhost:%s" % port)

    if len(sys.argv) > 2:
        socket.connect ("tcp://localhost:%s" % port1)

    # Subscribe to zipcode, default is NYC, 10001
    topicfilter = "10001"
    socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

    # Process 5 updates
    total_value = 0
    for update_nbr in range (115):
        if stop.is_set():
            print 'exit'
            return
        string = socket.recv()
        topic, messagedata = string.split()
        total_value += int(messagedata)
        print topic, messagedata

    print "Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr)


def file_watcher(stop):
    import sys, os
    from fsmonitor import FSMonitor

    m = FSMonitor()
    m.add_dir_watch('.')

    while True:
        for evt in m.read_events():
            stop.set()
            print "%s %s %s" % (evt.action_name, evt.watch.path, evt.name)


server = gevent.spawn(server, stop)
watcher = gevent.spawn(file_watcher, stop)
gevent.joinall([server])
