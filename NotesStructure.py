import os.path
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from os.path import abspath
from icecream import ic
from push2postgresql import PSQL_INSERT
import json

# Parent class for all SQL Row Formats
class SqlRow:

    # Class that adds DataClass functionality to any inherited class
    class DataMeta(type):
        def __new__(metacls, cls, bases, classdict):
            """__new__ is a classmethod, even without @classmethod decorator
            Parameters
            ----------
            cls : str
                Name of the class being defined (Event in this example)
            bases : tuple
                Base classes of the constructed class, empty tuple in this case
            attrs : dict
                Dict containing methods and fields defined in the class
            """
            new_cls = super().__new__(metacls, cls, bases, classdict)
            return dataclass(unsafe_hash=True, frozen=True)(new_cls)

    # New Row needs to be created
    # Process as new event with inherited DataClass decorator
    class Event(metaclass=DataMeta):
        modifiedOn: str


    class NewNote(Event):
        storedOn: str
        # createdOn: str
        noteType: str
        filePath: str


def get_timestamp():
    return datetime.now().strftime("%Y%m%d %I:%M:%S %p")

def get_extension(filepath):
    return str(Path(filepath).suffix)

def get_note_cols():
    return list(SqlRow.NewNote.__dict__.items())[4][1].keys()


def process_file(filepath):
    Table = '"CORE".noteimage'

    add_row = ''.join(["INSERT ", "INTO ", Table, ' ("',
                       '","'.join(list(get_note_cols())), '") ',
                       "VALUES ", "(", ",".join(['%s' for val in list(get_note_cols())]), ")"])

    filename = str(os.path.abspath(filepath))
    data = [get_timestamp(), get_timestamp(), get_extension(filename), str(Path(filename))]

    PSQL_INSERT(add_row, data)
