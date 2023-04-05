from pony.orm import *

db = Database()


class Loteria(db.Entity):
    id = PrimaryKey(int, auto=True)
    start_time = Required(float, min=0)
    end_time = Required(float, min=lambda obj: obj.start_time)
    _status = Required(str, max_len=10)
    wallet = Required(str, min_len=34)
    winner = Optional(str)


print(__file__)
