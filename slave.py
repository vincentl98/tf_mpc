"""
A slave will retrieve the random tensor from the slave leader, do some calculation on it,
and send the result to the master.
"""

import asyncio

from slave_common import send_encrypted_tensor, get_random_tensor

# secret variables here
secret = 200


async def main():
    ok, tensor = await get_random_tensor()
    while not ok:
        ok, tensor = await get_random_tensor()

    print(f"received random tensor from slave leader: {tensor}")

    encrypted_secret = secret - tensor

    ok = await send_encrypted_tensor(encrypted_secret)
    while not ok:
        ok = await send_encrypted_tensor(encrypted_secret)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
