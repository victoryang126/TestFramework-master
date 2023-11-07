from twisted.internet import reactor, task

def event_handler():
    print("Waiting for event...")

def trigger_event():
    print("Event triggered!")

def main():
    # 使用LoopingCall来定期调用event_handler
    event_call = task.LoopingCall(event_handler)
    event_call.start(1)

    # 使用reactor.callLater来触发事件
    reactor.callLater(3, trigger_event)

    reactor.run()

if __name__ == "__main__":
    main()
