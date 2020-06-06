from typing import Any, Dict

import tensorflow as tf

RANDOM_PROVIDER = "random_provider"
MASTER = "master"
SLAVES = "slaves"
TENSOR_SHAPE = "tensor_shape"
DATA_TYPE = "data_type"

_config = {
    RANDOM_PROVIDER: ("localhost", 8765),
    MASTER: ("localhost", 8764),
    SLAVES: [
        ("localhost", 8763),
        ("localhost", 8762)
    ],
    TENSOR_SHAPE: (1,),
    DATA_TYPE: tf.int64
}


def get(attr: str) -> Any:
    return _config[attr]
