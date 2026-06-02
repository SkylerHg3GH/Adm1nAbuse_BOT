import system.lib.minescript as ms
import time
import yaml

queue_path = r'C:\Users\skyler\AppData\Roaming\.minefabricnew\minescript\system\exec\Bot\queue.txt'
cfg = yaml.safe_load(open(r'C:\Users\skyler\AppData\Roaming\.minefabricnew\minescript\system\exec\Bot\config.yml', 'r+'))

ms.echo(f"§8[§cQueueManagers§8] §7Started")

while True:
    # Read queue file fresh each iteration
    try:
        with open(queue_path, 'r+') as queue:
            queue.seek(0)
            lines = queue.readlines()
            
            g = None
            remaining = []

            if len(lines) == cfg["qm"]["warning"]:
                ms.echo(f"§8[§cQueueManagers§8] §eQueue is approaching long sizes")
                
            for i, line in enumerate(lines):
                if line.strip():
                    g = line
                    remaining = lines[i+1:]
                    break
            
            if g is None:
                time.sleep(cfg["qm"]["msgQueueInterval"])
                continue
            
            queue.seek(0)
            queue.write("".join(remaining))
            queue.truncate()
            queue.flush()
    except Exception as e:
        ms.echo(f"§8[§cQueueManagers§8] §cQueue read error: {e}")
        time.sleep(cfg["qm"]["msgQueueInterval"])
        continue
    
    time.sleep(0.3)
    
    cmd = g.strip()

    if cmd.lower().startswith("/msg skylerhg3 "):
        msg_part = cmd[len("/msg SkylerHg3 "):]
        ms.echo(f"§6[§eSkylerHg3 §6-> §eSkylerHg3§6] {msg_part}")
        continue
    else:
        ms.execute(cmd)