import asyncio
import websockets
import tensorflow as tf
import config
import protocol
import random_provider

server_stop_signal = asyncio.Future()  # This is a flag used to close the server when all values are received
received_tensors = []  # Array to save received encrypted tensors from the slaves and slave master


async def handler(websocket: websockets.WebSocketServerProtocol, path: str):
    async for message in websocket:
        serialized_tensor = message
        tensor = tf.io.parse_tensor(serialized_tensor, config.get(config.DATA_TYPE))
        received_tensors.append(tensor)

        print(f"received tensor: {tensor}")

        if len(received_tensors) == len(config.get(config.SLAVES)):
            server_stop_signal.set_result(None)


async def main():
    addr, port = config.get(config.MASTER)
    addr_rp, port_rp = config.get(config.RANDOM_PROVIDER)

    ok = await protocol.send_str(random_provider.ADD, f"ws://{addr_rp}:{port_rp}")
    while not ok:
        ok = await protocol.send_str(random_provider.ADD, f"ws://{addr_rp}:{port_rp}")

    print("op sent:add")

    async with websockets.serve(handler, addr, port):
        await server_stop_signal

    sum_tensor = sum(received_tensors)

    print(f"sum_tensor: {sum_tensor}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
