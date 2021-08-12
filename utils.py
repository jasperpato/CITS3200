from functools import reduce

# in python 3.9 we can just 'da | db'
def merge(da : dict, db : dict) -> dict:
    z = da.copy()
    z.update(db)
    return z

def pipe(*args):
    return lambda x: reduce(lambda y,z: z(y), args, x)