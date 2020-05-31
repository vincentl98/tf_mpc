import asyncio
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disable tf warnings

import tensorflow as tf
import websockets

from constants import DATA_TYPE, SLAVE_LEADER_PORT
from slave_common import send_encrypted_tensor

random_tensor = tf.random.uniform((1,), 0, 100, dtype=DATA_TYPE)
print(f"set random tensor: {random_tensor}")

secret = 150
server_stop_signal = asyncio.Future()


async def handler(websocket: websockets.WebSocketServerProtocol, path: str):
    tensor_as_bytes = tf.io.serialize_tensor(random_tensor).numpy()
    await websocket.send(tensor_as_bytes)

    # here we only have 1 slave, so we can stop it on the first request
    server_stop_signal.set_result(None)


async def main():
    async with websockets.serve(handler, "localhost", SLAVE_LEADER_PORT):
        await server_stop_signal

    encrypted_secret = random_tensor + secret

    ok = await send_encrypted_tensor(encrypted_secret)
    while not ok:
        ok = await send_encrypted_tensor(encrypted_secret)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
