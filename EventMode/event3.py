event_flag = False

def event_handler():
    global event_flag
    print("Waiting for event...")
    while not event_flag:
        pass
    print("Event received!")

# 触发事件
event_flag = True
event_handler()
