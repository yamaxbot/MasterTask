import random

symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

async def generation_code():
    code = ''
    for i in range(8):
        code += random.choice(symbols)
    return code