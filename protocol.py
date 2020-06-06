from asyncio import Future

import tensorflow as tf
import websockets

CONNECTION_ERRORS = (OSError, ConnectionRefusedError, ConnectionAbortedError)  # All types of connection errors


async def send_tensor(tensor: tf.Tensor, uri: str) -> bool:
    tensor_as_bytes = tf.io.serialize_tensor(tensor).numpy()

    try:
        async with websockets.connect(uri) as ws:
            await ws.send(tensor_as_bytes)
        return True
    except CONNECTION_ERRORS:
        return False


async def send_str(s: str, uri: str) -> bool:
    try:
        async with websockets.connect(uri) as ws:
            await ws.send(s)
        return True
    except CONNECTION_ERRORS:
        return False
