import asyncio
import sys
import tensorflow as tf
import websockets
import config
import protocol
from asyncio import Future
from random_provider import ADD

secret = 200

n = int(sys.argv[1])


async def handler(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    async for message in websocket:
        if path == f"/{ADD}":
            serialized_r = message
            random_tensor = tf.io.parse_tensor(serialized_r, config.get(config.DATA_TYPE))

            if n % 2 == 0:
                random_tensor = -random_tensor

            encrypted_secret = secret + random_tensor

            addr_m, port_m = config.get(config.MASTER)
            ok = await protocol.send_tensor(encrypted_secret, f"ws://{addr_m}:{port_m}")
            while not ok:
                ok = await protocol.send_tensor(encrypted_secret, f"ws://{addr_m}:{port_m}")
        else:
            raise NotImplementedError()


async def main():
    addr, port = config.get(config.SLAVES)[n]
    async with websockets.serve(handler, addr, port):
        await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
