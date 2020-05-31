import asyncio
import websockets
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disable tf warnings
import tensorflow as tf

from constants import MASTER_PORT, DATA_TYPE

server_stop_signal = asyncio.Future()  # This is a flag used to close the server when all values are received
received_tensors = []  # Array to save received encrypted tensors from the slaves and slave master


async def handler(websocket: websockets.WebSocketServerProtocol, path: str):
    async for message in websocket:
        serialized_tensor = message  # gets the serialized tensor
        tensor = tf.io.parse_tensor(serialized_tensor, DATA_TYPE)
        received_tensors.append(tensor)

        print(f"received tensor: {tensor}")

        if len(received_tensors) == 2:  # we have 2 slaves in this example
            server_stop_signal.set_result(None)


async def main():
    async with websockets.serve(handler, "localhost", MASTER_PORT):
        await server_stop_signal

    sum_tensor = sum(received_tensors)

    print(f"sum_tensor: {sum_tensor}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
