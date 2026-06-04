from system.lib import minescript as ms
import shlex
import json
import yaml
import re
import os
from dataclasses import dataclass
from rapidfuzz import process

# Minecraft username regex: 3-16 chars, alphanumeric and underscores only
MC_USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,16}$")

cfg = yaml.safe_load(open(os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'config.yml'), 'r+'))["bot"]
cmds = json.load(open(os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'commands.json')))
commands = cmds["commands"]
cmdnames = list(commands.keys())
queue_path = os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'queue.txt')
bans = yaml.safe_load(open(os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'bans.yml')))

def queue_write(msg):
    """Safely write to queue file"""
    with open(queue_path, 'a') as queue:
        queue.write(f"\n{msg}")
        queue.flush()

@dataclass
class Context:
    args: list[str]
    rargs: list[str]
    msg: str
    user: str
    prefix: str
    wins: str
    cmd: dict
        
ms.echo(f"§8[§bBot§8] §7Started")

ms.execute("\\bot\\qm")
with ms.EventQueue() as eq:
    eq.register_chat_listener()

    while True:
        e = eq.get()

        if e.type == ms.EventType.CHAT:
            try:
                parsing_error = None
                raw: str = e.message
                
                split_result = raw.split(":", 1)
                if len(split_result) < 2:
                    continue
                
                after = split_result[1]
                before = split_result[0]

                parts = before.split()
                
                if len(parts) < 2:
                    continue

                wins = parts[0]
                user = parts[-1]
                
                # Check if parsed user is a valid Minecraft username
                if not MC_USERNAME_REGEX.match(user):
                    continue
                
                # [Wins] RANK RANK Skyler: 11111
                if len(parts) >= 3:
                    prefix = " ".join(parts[1:-1] )
                else:
                    prefix = ""

                if prefix.startswith("["): continue

                msg = after.strip()
                try:
                    rargs = shlex.split(msg)
                except ValueError as error:
                    continue

                if not rargs:
                    continue
                
                args = rargs[1:]
                cmdname = rargs[0]

                try:
                    with open(os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'bal.json'), 'r+') as balances:
                        bals = json.load(balances)

                        bals[user] = bals.get(user, 0) + 1

                        balances.seek(0)
                        json.dump(bals, balances, indent=4)
                        balances.truncate()
                except Exception as e:
                    print(repr(e))
                
                try:
                    pdata_path = os.path.join(os.getcwd(), 'minescript', 'system', 'exec', 'Bot', 'pdata.json')

                    with open(pdata_path, 'r+', encoding='utf-8') as f:
                        pdata = json.load(f)

                        pdata[user] = {
                            "wins": wins,
                            "prefix": prefix
                        }

                        f.seek(0)
                        json.dump(pdata, f, indent=4)
                        f.truncate()

                except Exception as e:
                    print(f"Failed to update pdata.json: {e}")
                if cmdname.startswith("!"):
                    if cmdname in cmdnames:
                        
                        if user in bans["players"] and bans["players"][user]["banned"]:
                            queue_write(f"/msg {user} You are banned. Reason: {bans['players'][user]['reason']}")
                            continue
                        
                        cmdobj: dict = commands[cmdname]
                        module_name = f"commfiles.{cmdobj['from'].lstrip('.')}"

                        cmd = __import__(module_name, fromlist=[''])

                        try:
                            cmd.main(ctx=Context(args, rargs, msg, user, prefix, wins, cmdobj))

                        except Exception as e:
                            queue_write(f"/msg {user} Error while executing command: {e}")

                    else:
                        typo = process.extractOne(cmdname, cmdnames, score_cutoff=cfg["typoDetectionScoreCutoff"])
                        if not typo:
                            queue_write(f"/msg {user} Invalid command {cmdname}. Use !cmds for a list of available commands.")
                        else:
                            queue_write(f"/msg {user} Invalid command {cmdname}. Maybe you mean {typo[0]}?")

            except Exception as e:
                import traceback
                traceback.print_exc()
                continue