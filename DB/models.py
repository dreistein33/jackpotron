from peewee import *
import pathlib
import sys
from typing import Union

# Enable importing from parent directory
PARENT_DIR = pathlib.Path(__file__).parent.parent
sys.path.append(str(PARENT_DIR))
# Import config 
from config import DATABASE as DB

db = PostgresqlDatabase(
    database=DB["db_name"],
    user=DB["username"],
    password=DB["password"],
    host = DB["host"],
    port=DB["port"]
)


def format_table_name(model_class):
    model_name = model_class.__name__
    return model_name.lower()


class BaseModel(Model):
    
    class Meta:
        database = db
        schema = "pot"
        table_function = format_table_name


class Loteria(BaseModel):
    start_time = FloatField(
        null=False,
        unique=True,
        constraints=[Check('start_time > 0')]      
    )
    end_time = FloatField(
        null=False,
        unique=True,
        constraints=[Check('end_time > start_time')]
    )
    status = CharField(10, null=False)
    wallet = CharField(40, null=False)
    winner = CharField(40, null=True)
    prize = FloatField(default=0, null=False)


class Ticket(BaseModel):
    sender = CharField(40, null=False)
    amount = FloatField(
        null=False,
        constraints=[Check('amount > 0')]
    )
    timestamp = FloatField(
        null=False,
        constraints=[Check('timestamp > 0')]
    )
    memo = CharField(128)
    lottery = ForeignKeyField(Loteria)


if len(sys.argv) > 1:
    if sys.argv[1] == "build":
        with db:
            db.create_tables([Loteria, Ticket]) 


def define_model(table_name:str) -> Union[Loteria, Ticket]:
    name = table_name.lower()
    if name == "loteria":
        return Loteria
    elif name == "ticket":
        return Ticket
    else:
        raise ValueError("No such table exists!")       


def insert(table_name: str, **kwargs) -> Union[Loteria, Ticket]:
    _model = define_model(table_name)

    with db:
        try:
            new = _model.create(**kwargs)
            return new
        except Exception as e:
            print("Error: " + e)


def edit(table_name: str, id: int, column: str, new_val: Union[str, float]):
    _model = define_model(table_name)

    with db:
        try:
            target = _model.get(_model.id == id)
            target.__dict__["__data__"][column] = new_val
            print(target.__dict__)
            target.save()
        except Exception as e:
            print(e)


def get(table_name: str, limit: int=1) -> list[Union[Loteria, Ticket]]:
    _model = define_model(table_name)
    with db:
        try:
            table = _model.select()
            table_list = list(table)
            table_sorted = sorted(table_list, key=lambda obj: obj.id, reverse=True)
            return table_sorted[:limit]
        except Exception as e:
            print(e)

x = get("loteria", limit=2)
print(x)