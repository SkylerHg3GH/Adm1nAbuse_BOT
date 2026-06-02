from system.lib import minescript as ms
import json
import yaml

cmds = json.load(open(r'C:\Users\skyler\AppData\Roaming\.minefabricnew\minescript\system\exec\Bot\commands.json'))
queue_path = r'C:\Users\skyler\AppData\Roaming\.minefabricnew\minescript\system\exec\Bot\queue.txt'
commands: dict = cmds["commands"]
cmdnames: list[str] = list(commands.keys())
cfg = yaml.safe_load(open(r'C:\Users\skyler\AppData\Roaming\.minefabricnew\minescript\system\exec\Bot\config.yml', 'r+'))
bal_path = r'C:\Users\skyler\AppData\Roaming\.minefabricnew\minescript\system\exec\Bot\bal.json'
balances = json.load(open(bal_path))

def followup(user, msg):
    with open(queue_path, 'a') as queue:
        queue.write(f"/msg {user} {msg}\n")
        queue.flush()

def setbal(user: str, amount: int | float):
    """Sets a user's balance, saves it to bal.json, and sends a confirmation message."""
    balances[user] = amount

    with open(bal_path, 'w') as f:
        json.dump(balances, f, indent=4)