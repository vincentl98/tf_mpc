import asyncio
from asyncio import Future
from typing import Tuple, List

import tensorflow as tf
import websockets
import config
from config import TENSOR_SHAPE, DATA_TYPE, SLAVES, RANDOM_PROVIDER
import protocol

ADD = "add"
MUL = "mul"


def generate_random_tensor(begin: int = 0, end: int = 100) -> tf.Tensor:
    return tf.random.uniform(config.get(TENSOR_SHAPE), begin, end, dtype=config.get(DATA_TYPE))


def generate_random_tensors(n: int, begin: int = 0, end: int = 100) -> List[tf.Tensor]:
    return [generate_random_tensor(begin, end) for _ in range(n)]


async def handler(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    async for message in websocket:
        op_type = message  # receives from Bob
        assert op_type in (ADD, MUL)

        if op_type == ADD:
            random_tensor = generate_random_tensor()
            for addr, port in config.get(SLAVES):
                ok = await protocol.send_tensor(random_tensor, f"ws://{addr}:{port}/{ADD}")
                while not ok:
                    ok = await protocol.send_tensor(random_tensor, f"ws://{addr}:{port}/{ADD}")
        else:
            # TODO
            s, t, u, v, w = generate_random_tensors(5)
            s0 = s - u
            s1 = u
            t0 = t - v
            t1 = v
            st0 = s * t - w
            st1 = w

            # alice a les 0

            # step les 1


async def main():
    addr, port = config.get(RANDOM_PROVIDER)
    async with websockets.serve(handler, addr, port):
        print("server ok")
        await Future()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
