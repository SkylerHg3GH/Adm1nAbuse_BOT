from system.lib import minescript as ms
import json
import yaml
import os

class Balances(dict):
    def __missing__(self, key):
        return None

cmds = json.load(open(os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'commands.json')))
queue_path = os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'queue.txt')
commands: dict = cmds["commands"]
cmdnames: list[str] = list(commands.keys())
cfg = yaml.safe_load(open(os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'config.yml'), 'r+'))
bal_path = os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'bal.json')
balances = Balances(json.load(open(bal_path)))
    
def followup(user, msg):
    with open(queue_path, 'a') as queue:
        queue.write(f"/msg {user} {msg}\n")
        queue.flush()

def setbal(user: str, amount: int | float):
    """Sets a user's balance, saves it to bal.json, and sends a confirmation message."""
    balances[user] = amount

    with open(bal_path, 'w') as f:
        json.dump(balances, f, indent=4)