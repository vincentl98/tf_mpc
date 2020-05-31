import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disable tf warnings
import tensorflow as tf

SLAVE_LEADER_PORT = 8765
SLAVE_LEADER_URI = "ws://localhost:" + str(SLAVE_LEADER_PORT)  # URI of slave leader
MASTER_PORT = 8766  # Master port (if executed locally, must be different from SLAVE_LEADER_PORT)
MASTER_URI = "ws://localhost:" + str(MASTER_PORT)  # URI of master (note "ws" means WebSocket)
CONNECTION_ERRORS = (OSError, ConnectionRefusedError, ConnectionAbortedError)  # All types of connection errors
DATA_TYPE = tf.int32  # Data type used for random tensor and calculation result. Can be modified.
