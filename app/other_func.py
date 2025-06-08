import random

symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

async def generation_code():
    code = ''
    for i in range(8):
        code += random.choice(symbols)
    return code


async def random_num():
    return random.randint(1, 11)


async def random_battle_num():
    return random.randint(0, 2)