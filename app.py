# Import libs
import os
import sys
import argparse
from pathlib import Path
import json
import datetime as dt

# Init Variables and Configs
class file:
    js_init = {
        "tasks": {
        },
        "profile": {
            "to_up": 100,
            "xp": 0,
            "level": 1
        }
    }

    cwd = Path.cwd()
    src = cwd / "src"
    logd = src / "logs"

    db = src / "tasks.json"
    logf = logd / "log.txt"
    errors = logd / "error_log.txt"
    if not Path.exists(src):
        Path.mkdir(src, parents=True)
        with open(db, 'w') as f:
            json.dump(js_init, f)
        with open(logf, 'w') as f:
            log = f.read()
            dh = dt.now()
            f.write(log)
            f.write(f"/n [{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create log file")
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
                    json.dump(js_init, f)
                with open(logf, 'w') as f:
                    log = f.read()
                    dh = dt.now()
                    f.write(log)
                    f.write(f"/n [{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create log file")
            else:
                pass

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

    def log(self, msg:str):
        dh = dt.datetime.now()
        time = dh.strftime("%H-%M-%S")
        data = dh.strftime("%d-%m-%Y")
        with open(file.logf) as f:
            f.write(f"[{data}: {time}] - {msg}")
            f.close()

    def error_log(self, error_type):
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
            taskwiz.log(f"Task added. ID:{id}")
            print(f"Task added sucessfully! ID: {id} Task Name: {taskname} ✔")
        except Exception as e:
            taskwiz.error_log(e)

    def list(self):
        try:
            print("ID     Task")
            for i in self.db["tasks"]:
                print(f"{i}      {self.db["tasks"][i]}")
        except Exception as e:
            print(f"ERROR: {e} ❌")

    def remove(self, ID:int):
        try:
            del self.db["tasks"][ID]
            with open(file.db, 'w') as f:
                json.dump(self.db, f, indent=4)
                f.close()
            print("Removed Task Sucessfully ✅")
        except Exception as e:
            print(f"ERROR: {e} ❌")

    def done(self, ID:int):
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

    def clear(sel):
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
    
    def GetTaskByID(sel, ID:int):
        print(self.db["tasks"][ID])

    def GetTaskByName(self, name:str):
        length = len(self.db["tasks"])
        count = 0
        if length > 0:
            for i in self.db["tasks"]:
                if self.db["tasks"][i] == name:
                    print(f"ID: {i}")
                    print(f"Task: {self.db["tasks"][i]}")
                    return
                else:
                    count += 1
                    if count <= length:
                        pass
                    else:
                        break
        else:
            print("No tasks for search, add tasks using command \033[1m add")
    
    def profile(self):
        print(f"Name: {os.getlogin()}")
        print(f"LV (Level): {self.profile["level"]}")
        print(f"XP: {self.profile["xp"]}")
        print(f"To next upgrade: {self.profile["xp"]}/{self.profile["to_up"]}")

    def get(self, args):
        if args.task_id is not None:
            self.GetTaskByID(args.task_id)
        elif args.task_name is not None:
            self.GetTaskByName(args.task_name)

class configs:
    parser = argparse.ArgumentParser(prog="Task Wizard CLI", description="A simples CLI task manager.", )
    subparsers = parser.add_subparsers(dest='command', required=True)
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_done = subparsers.add_parser('done', help='Complete a task using your ID, your give 10 XP for each task done')
    parser_remove = subparsers.add_parser('remove', help='Remove a task by ID')
    parser_list = subparsers.add_parser('list', help='List all tasks')
    parser_clear = subparsers.add_parser('clear', help='Clean all tasks')
    parser_profile = subparsers.add_parser('profile', help='Show your profile; Show your Name, XP, XP to UP and Level')
    parser_get = subparsers.add_parser('get', help='Get a task by ID or name')

    get_group = parser_get.add_mutually_exclusive_group(required=True)

    get_group.add_argument('-i', '--id', type=int, dest='task_id', help='Search task by ID')
    get_group.add_argument('-n', '--name', type=str, dest='task_name', help='Seacrh task by name')

    parser_get.set_defaults(func=taskwiz.get)
    parser_add.set_defaults(func=taskwiz.add)
    parser_done.set_defaults(func=taskwiz.done)
    parser_remove.set_defaults(func=taskwiz.remove)
    parser_list.set_defaults(func=taskwiz.list)
    parser_clear.set_defaults(func=taskwiz.clear)
    parser_profile.set_defaults(func=taskwiz.profile)