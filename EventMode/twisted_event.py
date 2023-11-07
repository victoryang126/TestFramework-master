from twisted.internet import reactor, defer

def callback(result):
    print(f"Result: {result}")

def errback(error):
    print(f"Error: {error}")

def long_running_task():
    d = defer.Deferred()
    reactor.callLater(2, d.callback, "Task completed")
    return d

def main():
    d = long_running_task()
    d.addCallback(callback)
    d.addErrback(errback)

    reactor.run()

if __name__ == "__main__":
    main()
