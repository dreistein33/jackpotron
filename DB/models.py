from pony.orm import *
import pathlib
import sys

# Enable importing from parent directory
PARENT_DIR = pathlib.Path(__file__).parent.parent
print(PARENT_DIR)
sys.path.append(str(PARENT_DIR))

from config import DATABASE


db = Database()

db.bind(
    provider=DATABASE["provider"],
    user=DATABASE["username"],
    password=DATABASE["password"],
    host=DATABASE["host"],
    database=DATABASE["db_name"]
)

db.schema = "pot"

class Loteria(db.Entity):
    id = PrimaryKey(int, auto=True)
    start_time = Required(float, min=0)
    end_time = Required(float, min=lambda obj: obj.start_time)
    _status = Required(str, max_len=10)
    wallet = Required(str, min_len=34)
    winner = Optional(str)



