# Import libs
import os
import sys
import argparse
from pathlib import Path
import json
# [MUDANÇA 1]: Alterado 'from datetime import datetime as dt' para importar 
# a classe 'datetime' sem alias, ou o módulo e a classe separadamente.
from datetime import datetime 

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
    
    # A lógica de criação de diretórios e arquivos de log é mantida aqui.
    if not Path.exists(src):
        Path.mkdir(src, parents=True)
        # O DB será criado em taskwiz.__init__ se não existir.
        
        with open(logf, 'w') as f:
            # [MUDANÇA 2, 3, 4]: Corrigido o uso de datetime.now(), aspas e '/n' para '\n'.
            dh = datetime.now()
            f.write(f'\n[{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create log file')
    else:
        if not Path.exists(logd):
            Path.mkdir(logd, parents=True)
            with open(logf, 'w') as f:
                dh = datetime.now()
                f.write(f'[{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create log file')
            with open(errors, 'w') as f:
                dh = datetime.now()
                f.write(f'[{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create errors log file')
        else:
            if not Path.exists(logf):
                with open(logf, 'w') as f:
                    dh = datetime.now()
                    f.write(f'[{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create log file')
            elif not Path.exists(errors):
                with open(errors, 'w') as f:
                    dh = datetime.now()
                    f.write(f'[{dh.strftime("%d/%m/%Y") } - {dh.strftime("%H:%M:%S")}] - Create errors log file')
            # Não é mais necessário verificar o DB aqui, pois fazemos isso em taskwiz.__init__
            else:
                pass

# Main Functions
class taskwiz:
    def __init__(self):
        # [MUDANÇA A]: Garantir que o DB exista antes de TENTAR abri-lo.
        if not file.db.exists():
            with open(file.db, 'w') as f:
                json.dump(file.js_init, f, indent=4)
            # O log é opcional, mas útil para rastrear a primeira execução.
            self.log("Database file created/re-created during startup.")

        # [MUDANÇA 5]: Removidas as leituras dos logs desnecessárias.
        with open(file.db, 'r') as f:
            self.db = json.load(f)
        self.profile = self.db["profile"]

    def log(self, msg:str):
        # [MUDANÇA 6]: Corrigido o uso de datetime.now().
        dh = datetime.now()
        time = dh.strftime("%H-%M-%S")
        data = dh.strftime("%d-%m-%Y")
        with open(file.logf, 'a') as f:
            # [MUDANÇA 7]: Removido f.write(self.log_file) e adicionado '\n'.
            f.write(f"\n[{data}: {time}] - {msg}")

    def error_log(self, error_type):
        # [MUDANÇA 6]: Corrigido o uso de datetime.now().
        dh = datetime.now()
        time = dh.strftime("%H-%M-%S")
        data = dh.strftime("%d-%m-%Y")
        with open(file.errors, 'a') as f:
            # [MUDANÇA 7]: Removido f.write(self.error_f) e adicionado '\n'.
            f.write(f"\n[{data} | {time}]: {error_type}")
        print(f"An error has occurred: {error_type}")

    def add(self, taskname:str):
        try:
            id = len(self.db["tasks"])
            if id < 10:
                id = "00" + str(id)
            elif id > 10 and id < 100:
                id = "0" + str(id)
            else:
                id = len(self.db["tasks"])

            self.db["tasks"][str(id)] = taskname
            with open(file.db, 'w') as f:
                json.dump(self.db, f, indent=4)
            self.log(f"Task added. ID:{id}")
            print(f"Task added sucessfully! ID: {id} Task Name: {taskname} ✔")
        except Exception as e:
            self.error_log(e)

    def list(self):
        try:
            print("ID     Task")
            print("-----------")
            for i in self.db["tasks"]:
                print(f"{i}      {self.db["tasks"][i]}")
        except Exception as e:
            print(f"ERROR: {e} ❌")

    def remove(self, ID:int):
        try:
            del self.db["tasks"][str(ID)] # [MUDANÇA 8]: Convertido ID para str.
            with open(file.db, 'w') as f:
                json.dump(self.db, f, indent=4)
            print("Removed Task Sucessfully ✅")
            self.log(f'Removed task: {ID}')
        except Exception as e:
            print(f"ERROR: {e} ❌")
            self.error_log(e)

    def done(self, ID:int):
        try:
            del self.db["tasks"][str(ID)] # [MUDANÇA 8]: Convertido ID para str.
            self.profile["xp"] += 10
            if self.profile["xp"] >= self.profile["to_up"]:
                self.profile["level"] += 1
                self.profile["to_up"] = int(self.profile["to_up"] * 1.5)
                print("Congratulations! You done a task ✅")
                print("You get 10 XP!")
                print(f"YOU LEVED UP!!! From level {self.profile["level"] - 1} to {self.profile["level"]}")
                print(f"Now you need {self.profile["to_up"]} to upgrade to {self.profile["level"] + 1}")
            else:
                print("Congratulations! You done a task ✅")
                print("You get 10 XP!")
            with open(file.db, 'w') as f:
                json.dump(self.db, f, indent=4)
        except Exception as e:
            self.error_log(e)

    def clear(self):
        while True:
            confirmation = input("Are you sure you want to remove all your tasks? [Y/N]: ")
            match confirmation.lower():
                case "y":
                    self.db["tasks"] = {}
                    with open(file.db, 'w') as f:
                        json.dump(self.db, f)
                    print("All tasks are removed")
                    break
                case "n":
                    print("Operation canceled")
                    break
                case _:
                    print(f"What is {confirmation}?")
                    print("You can only write Y or N! Try again")
    
    def GetTaskByID(self, ID):
        print(self.db["tasks"][ID]) # [MUDANÇA 8]: Convertido ID para str.

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
        print(f"LV (Level): {self.profile["level"]}")
        print(f"XP: {self.profile["xp"]}")
        print(f"To next upgrade: {self.profile["xp"]}/{self.profile["to_up"]}")

    def get(self, task_id=None, task_name=None):
        if task_id is not None:
            self.GetTaskByID(task_id)
        elif task_name is not None:
            self.GetTaskByName(task_name)

class Configs:
    parser = argparse.ArgumentParser(prog="Task Wizard CLI", description="A simples CLI task manager.", )
    # [MUDANÇA 9]: Adicionado 'required=True'.
    subparsers = parser.add_subparsers(dest='command', required=True)
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_done = subparsers.add_parser('done', help='Complete a task using your ID, your give 10 XP for each task done')
    parser_remove = subparsers.add_parser('remove', help='Remove a task by ID')
    parser_list = subparsers.add_parser('list', help='List all tasks')
    parser_clear = subparsers.add_parser('clear', help='Clean all tasks')
    parser_profile = subparsers.add_parser('profile', help='Show your profile; Show your Name, XP, XP to UP and Level')
    parser_get = subparsers.add_parser('get', help='Get a task by ID or name')

    # Argumentos para 'add'
    # [MUDANÇA 10]: Adicionado o argumento 'taskname'.
    parser_add.add_argument('taskname', type=str, help='Name of the task to add.') 

    # Argumentos para 'done' e 'remove'
    # [MUDANÇA 11]: Adicionado o argumento 'task_id'.
    parser_done.add_argument('task_id', type=int, help='ID of the task to complete.')
    parser_remove.add_argument('task_id', type=int, help='ID of the task to remove.')

    get_group = parser_get.add_mutually_exclusive_group(required=True)

    get_group.add_argument('-i', '--id', type=int, dest='task_id', help='Search task by ID')
    get_group.add_argument('-n', '--name', type=str, dest='task_name', help='Search task by name')

    parser_get.set_defaults(func=taskwiz.get)
    parser_add.set_defaults(func=taskwiz.add)
    parser_done.set_defaults(func=taskwiz.done)
    parser_remove.set_defaults(func=taskwiz.remove)
    parser_list.set_defaults(func=taskwiz.list)
    parser_clear.set_defaults(func=taskwiz.clear)
    parser_profile.set_defaults(func=taskwiz.profile)


if __name__ == "__main__":
    # [MUDANÇA B]: Inicializar 'manager' como None fora do try/except
    manager = None 
    try:
        # 1. Analisar os argumentos de linha de comando
        args = Configs.parser.parse_args()

        # 2. Inicializar a instância da classe taskwiz
        manager = taskwiz() # <-- Mover para dentro do bloco try

        # [MUDANÇA 12]: Implementação de roteamento universal.
        # Prepara os argumentos para a chamada da função
        args_dict = vars(args)
        func_to_call = args_dict.pop('func')
        args_dict.pop('command', None) # Remove 'command' que é apenas para roteamento
        
        # Chama a função roteada.
        func_to_call(manager, **args_dict)

    except KeyboardInterrupt:
        print("\n\n👋 Operação cancelada. Tchau!")
        # [MUDANÇA C]: Verifica se o manager foi instanciado antes de tentar logar
        if manager:
            manager.log("Keyboard Interrupt")
    except Exception as e:
        # Para capturar erros que ocorrem antes ou fora dos métodos logados.
        # [MUDANÇA D]: Verifica se o manager foi instanciado antes de tentar logar
        if manager:
            manager.error_log(e)