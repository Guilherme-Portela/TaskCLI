# Import libs
import os
import sys
import argparse as parse
from pathlib import Path
import json
import uuid
import datetime as dt

# Init Variables and Configs
class file:
    cwd = Path.cwd()
    src = cwd / "src"
    logd = src / "logs"

    db = src / "tasks.json"
    logf = logd / "log.txt"
    errors = logd / "error_log.txt"
    if not Path.exists(src):
        Path.mkdir(src, parents=True)
        with open(db, 'w') as f:
                pass
    else:
        if not Path.exists(logd):
            Path.mkdir(logd, parents=True)
            with open(logf, 'w') as f:
                pass
            with open(errors, 'w') as f:
                pass
        else:
            if not Path.exists(logf):
                with open(logf, 'w') as f:
                    pass
            elif not Path.exists(errors):
                with open(errors, 'w') as f:
                    pass
            elif not Path.exists(db):
                with open(db, 'w') as f:
                    pass
            else:
                pass
class configs:
    parser = parse.ArgumentParser(prog="taskwiz")

# Main Functions
class taskwiz:
    def __init__(self):
        self.db = file.db
        self.log_file = file.logf
        self.error_f = file.errors
    
    def add(taskname):
        pass
    
    def list():
        pass

    def remove():
        pass
    
    def done():
        pass

    def clear():
        pass

    def GetTaskByID():
        pass

    def GetTaskByName():
        pass