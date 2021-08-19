from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PureWindowsPath
from os.path import abspath
from icecream import ic
from push2postgresql import PSQL_INSERT
import json

# Parent class for all SQL Row Formats
class SQL_Row():

    # Class that adds DataClass functionality to any inherited class
    class dataMeta(type):
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
    class Event(metaclass=dataMeta):
        dateTouch: str


    class newNote(Event):
        dateStore: str
        dateWrite: str
        noteType: str
        filePath: str
        rawText: str


def get_timestamp():
    return datetime.now().strftime("%Y%m%d %I:%M:%S %p")

def get_note_cols():
    return list(SQL_Row.newNote.__dict__.items())[4][1].keys()

DATABASE = 'rbwolfff."NOTES"'

add_row = ''.join(["INSERT ", "INTO ", DATABASE, ' ("',
                      '","'.join(list(get_note_cols())), '") ',
                      "VALUES ", "(", ",".join(['%s' for val in list(get_note_cols())]), ")"])

ic(add_row)

### EXAMPLE INPUT TO THE DATABASE ####
filename = str(Path(PureWindowsPath(abspath(__file__))))
filename = filename.replace("\\", '/')
data = [get_timestamp(), get_timestamp(), get_timestamp(), 'txt', str(filename), '{"test" : "lots of textual"}']

PSQL_INSERT(add_row, data)