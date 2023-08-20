class EventSystem:
    def __init__(self):
        self._events = {}

    def register(self, event_name, handler):
        """注册事件处理程序"""
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(handler)

    def trigger(self, event_name, *args, **kwargs):
        """触发事件"""
        for handler in self._events.get(event_name, []):
            handler(*args, **kwargs)

# 实例化事件系统
events = EventSystem()

# 用户定义的事件处理程序
def custom_handler(message):
    print(f"Handled custom event with message: {message}")

# 注册处理程序
events.register("custom_event", custom_handler)

# 在某些地方触发事件
events.trigger("custom_event", "Hello from the event!")  # 输出: "Handled custom event with message: Hello from the event!"
