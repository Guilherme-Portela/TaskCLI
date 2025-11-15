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
                dh = dt.now()
                f.write(f"[{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create log file")
            with open(errors, 'w') as f:
                dh = dt.now()
                f.write(f"[{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create errors log file")
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
        with open(file.db, 'r') as f:
            self.db = json.load(f)
        with open(file.logf, 'r') as f:
            self.log_file = f.read()
        with open(file.errors, 'r') as f:
            self.error_f = f.read()

    def log(self:None, msg:str):
        dh = dt.datetime.now()
        time = dh.strftime("%H-%M-%S")
        data = dh.strftime("%d-%m-%Y")
        with open(file.logf) as f:
            f.write(f"[{data}: {time}] - {msg}")

    def error_log(self:None, msg:str, error_type:str):
        dh = dt.datetime.now()
        time = dh.strftime("%H-%M-%S")
        data = dh.strftime("%d-%m-%Y")
        with open(file.errors) as f:
            f.write(f"[{data} | {time}]: {error_type} - {msg}")
    

    def add(self, taskname:str):
        try:
            id = len(self.db["tasks"])
            self.db["tasks"][str(id)] = taskname
            with open(file.db, 'w') as f:
                json.dump(self.db, f, indent=4)
            taskwiz.log(taskwiz, f"Task added. ID:{id}")
            print(f"Task added sucessfully! ID: {id} Task Name: {taskname}")
        except Exception as e:
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

inst = taskwiz()

inst.add("Watch Star Wars VII")