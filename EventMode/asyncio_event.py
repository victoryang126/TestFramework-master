import asyncio

async def main():
    # 创建一个异步任务
    async def worker(name):
        await asyncio.sleep(1)
        print(f"Worker {name} is done")

    tasks = [worker("A"), worker("B"), worker("C")]

    # 启动异步任务
    await asyncio.gather(*tasks)
"""
引入asyncio库。
创建异步函数main，其中定义了异步任务worker。
使用asyncio.gather同时启动多个异步任务。
通过asyncio.run运行main函数"""
if __name__ == "__main__":
    asyncio.run(main())
