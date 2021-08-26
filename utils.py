from functools import reduce, lru_cache

# in python 3.9 we can just 'da | db'
def merge(da : dict, db : dict) -> dict:
    z = da.copy()
    z.update(db)
    return z

# apply a list of functions LEFT-TO-RIGHT
# e.g. pipe(double, double, increment)(10) = 41
def pipe(*args):
    return lambda x: reduce(lambda y,z: z(y), args, x)

# memoising a function
# it'd be great if we could get this to memoize in between program executions
def cached(f):

    @lru_cache(maxsize=None)
    def helper(*args):
        return f(*args)

    return helper