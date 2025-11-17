# Import libs
import os
import sys
import argparse as parse
from pathlib import Path
import json
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
                f.close()
            with open(errors, 'w') as f:
                dh = dt.now()
                f.write(f"[{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create errors log file")
                f.close()
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
# class configs:

# Main Functions
class taskwiz:
    def __init__(self):
        with open(file.db, 'r') as f:
            self.db = json.load(f)
            f.close()
        with open(file.logf, 'r') as f:
            self.log_file = f.read()
            f.close()
        with open(file.errors, 'r') as f:
            self.error_f = f.read()
            f.close()
        self.profile = self.db["profile"]

    def log(self:None, msg:str):
        dh = dt.datetime.now()
        time = dh.strftime("%H-%M-%S")
        data = dh.strftime("%d-%m-%Y")
        with open(file.logf) as f:
            f.write(f"[{data}: {time}] - {msg}")
            f.close()

    def error_log(self:None, error_type):
        dh = dt.datetime.now()
        time = dh.strftime("%H-%M-%S")
        data = dh.strftime("%d-%m-%Y")
        with open(file.errors) as f:
            f.write(f"[{data} | {time}]: {error_type}")
            f.close()
        print(f"An error has occurred: {error_type}")
    

    def add(self, taskname:str):
        try:
            id = len(self.db["tasks"])
            if id < 100:
                id = "0" + str(id)
            else:
                id = len(self.db["tasks"])

            self.db["tasks"][str(id)] = taskname
            with open(file.db, 'w') as f:
                json.dump(self.db, f, indent=4)
                f.close()
            taskwiz.log(taskwiz, f"Task added. ID:{id}")
            print(f"Task added sucessfully! ID: {id} Task Name: {taskname} ✔")
        except Exception as e:
            taskwiz.error_log(e)

    def list(self:None):
        try:
            print("ID     Task")
            for i in self.db["tasks"]:
                print(f"{i}      {self.db["tasks"][i]}")
        except Exception as e:
            print(f"ERROR: {e} ❌")

    def remove(self:None, ID):
        try:
            del self.db["tasks"][ID]
            with open(file.db, 'w') as f:
                json.dump(self.db, f, indent=4)
                f.close()
            print("Removed Task Sucessfully ✅")
        except Exception as e:
            print(f"ERROR: {e} ❌")

    def done(self:None, ID):
        try:
            del self.db["tasks"][ID]
            self.profile["xp"] += 10
            if self.profile["xp"] >= self.profile["to_up"]:
                self.profile["level"] += 1
                self.profile["to_up"] *= 1
                print("Congratulations! You done a task ✅")
                print("You get 10 XP!")
                print(f"YOU LEVED UP!!! From level {self.profile["level"] - 1} to {self.profile["level"]}")
                print(f"Now you need {self.profile["to_up"]} to upgrade to {self.profile["level"] + 1}")
            else:
                print("Congratulations! You done a task ✅")
                print("You get 10 XP!")
            with open(file.db, 'w') as f:
                json.dump(self.db, f, indent=4)
                f.close()
        except Exception as e:
            taskwiz.error_log(e)

    def clear(self:None):
        while True:
            confirmation = input("Are you sure you want to remove all your tasks? [Y/N]: ")
            match confirmation.lower():
                case "y":
                    self.db["tasks"] = {}
                    with open(file.db, 'w') as f:
                        json.dump(self.db, f)
                        f.close()
                    print("All tasks are removed")
                    break
                case "n":
                    print("Operation canceled")
                    break
                case _:
                    print(f"What is {confirmation}?")
                    print("You can only write Y or N! Try again")
    
    def GetTaskByID(self:None, ID):
        print(self.db["tasks"][ID])

    def GetTaskByName(self:None, name):
        length = len(self.db["tasks"])
        count = 0
        if length > 0:
            while count < length:
                for i in self.db["tasks"]:
                    if self.db["tasks"][i] == name:
                        print(f"ID: {i}")
                        print(f"Task: {self.db["tasks"][i]}")
                        break
                    elif i != name:
                        count += 1
                        pass
        else:
            print("No tasks for search, add tasks using command \033[1m add")
    
    def profile(self:None):
        print(f"Name: {os.getlogin()}")
        print(f"LV (Level): {self.profile["level"]}")
        print(f"XP: {self.profile["xp"]}")
        print(f"To next upgrade: {self.profile["xp"]}/{self.profile["to_up"]}")
