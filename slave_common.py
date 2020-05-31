import os
import websockets

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

from constants import CONNECTION_ERRORS, MASTER_URI, DATA_TYPE, SLAVE_LEADER_URI


async def send_encrypted_tensor(encrypted_tensor: tf.Tensor) -> bool:
    """
    Sends an encrypted tensor to the master
    :param encrypted_tensor: encrypted tensor
    :return: if the sending was successful or not
    """
    encrypted_tensor_as_bytes = tf.io.serialize_tensor(encrypted_tensor).numpy()

    try:
        async with websockets.connect(MASTER_URI) as websocket:
            await websocket.send(encrypted_tensor_as_bytes)
        return True
    except CONNECTION_ERRORS:
        return False


async def get_random_tensor() -> (bool, tf.Tensor):
    """
    Retrieves the random tensor from the slave leader
    :return: if the random tensor was successfully retrieved or not, and if yes, the random tensor
    """
    try:
        async with websockets.connect(SLAVE_LEADER_URI) as websocket:
            serialized_tensor = await websocket.recv()
        return True, tf.io.parse_tensor(serialized_tensor, DATA_TYPE)
    except CONNECTION_ERRORS:
        return False, None
