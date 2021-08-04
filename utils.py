# in python 3.9 we can just 'da | db'
def merge(da : dict, db : dict) -> dict:
    z = da.copy()
    z.update(db)
    return z