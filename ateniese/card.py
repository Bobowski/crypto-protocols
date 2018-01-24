import asyncio
import websockets

from utils import jencode, jdecode
from ateniese import join_0, join_1, join_2, join_3, join_4, sign, verify

Y = None
Key = None

async def get_pk():
    async with websockets.connect('ws://localhost:8765') as websocket:
        print("> Ask for Public Key")

        # Construct and send requrest frame
        frame = {"cmd": "get_pk"}
        await websocket.send(jencode(frame))

        # Await response
        data = await websocket.recv()
        frame = jdecode(data)
        global Y
        Y = frame


async def join():
    async with websockets.connect('ws://localhost:8765') as websocket:
        print("> Ask to join")

        # Prepare parameters
        u = dict(Y)

        # Commit
        out = {'cmd': 'join', 'name': "Piotr"}
        out.update(join_0(u))
        await websocket.send(jencode(out))

        # Await and response
        data = await websocket.recv()
        frame = jdecode(data)
        if frame["status"] != "OK":
            print("JOIN ERROR")
            return
        u.update(frame)

        out = join_2(u)
        await websocket.send(jencode(out))

        # Await
        data = await websocket.recv()
        if frame["status"] != "OK":
            print("JOIN ERROR")
            return
        frame = jdecode(data)
        u.update(frame)
        if join_4(u):
            global Key
            Key = u


async def open_msg():
    async with websockets.connect('ws://localhost:8765') as websocket:
        print("> SIGN")

        msg = "Random message to sign"
        u = dict(Key)
        u.update(Y)
        signature = sign(u, msg)

        # Commit
        out = {'cmd': 'open', 'name': "Adam", "msg": msg, "sign": signature}
        await websocket.send(jencode(out))

        # Await and response
        data = await websocket.recv()
        frame = jdecode(data)
        print(frame)


asyncio.get_event_loop().run_until_complete(get_pk())
asyncio.get_event_loop().run_until_complete(join())
asyncio.get_event_loop().run_until_complete(open_msg())
