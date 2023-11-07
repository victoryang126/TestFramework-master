import asyncio

async def event_handler(event):
    while True:
        print("Waiting for event...")
        await event.wait()
        event.clear()
        print("Event received!")

async def trigger_event(event, delay):
    await asyncio.sleep(delay)
    event.set()
    print("Event triggered!")

async def main():
    event = asyncio.Event()
    event_task = asyncio.create_task(event_handler(event))
    trigger_task = asyncio.create_task(trigger_event(event, 2))

    await asyncio.gather(event_task, trigger_task)

"""
asyncio.Event用于创建事件。event_handler协程等待事件，而trigger_event协程在2"""


if __name__ == "__main__":
    asyncio.run(main())
