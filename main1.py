from pprint import pprint

import asyncio
import websockets
import time

import asyncio


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def f1():
    while True:
        print("F1")
        await asyncio.sleep(1)

async def f2():
    while True:
        print("F2")
        await asyncio.sleep(1)

async def main():
    tasks = []
    task1 = f1()
    task2 = f2()

    tasks.append(task1)
    tasks.append(task2)

    # планируем одновременные вызовы
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    # Запускаем цикл событий
    results = asyncio.run(main())

# async def hello(websocket, path):
#     name = await websocket.recv()
#     print(name)
#
#     greeting = "Hello " + name + "!"
#
#     await websocket.send(greeting)
#     print(greeting)

# async def run():
#     tasks = asyncio.gather(*[f1, f2])
#     await tasks



# asyncio.run(run())


# start_server = websockets.serve(hello, "localhost", 8765)
# eventLoop = asyncio.new_event_loop()
# time.sleep(2)



# print("Run web socket in threaded env")
# TH = threading.Thread(target=startWebSocket, args=[eventLoop, start_server,])
# TH.start()

# async def run():
#     eventLoop.create_task(start_server())
#     eventLoop.run_in_executor(None, f2)


# eventLoop.run_until_complete(run())
