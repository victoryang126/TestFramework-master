import threading

def event_handler(event):
    print("Waiting for event...")
    event.wait()
    print("Event received!")

event = threading.Event()
handler_thread = threading.Thread(target=event_handler, args=(event,))
handler_thread.start()

# 触发事件
event.set()
handler_thread.join()
