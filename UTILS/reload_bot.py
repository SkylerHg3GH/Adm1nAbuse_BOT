from system.lib import minescript as ms

bot_job = None

for job in ms.job_info():
    if job.command[0] == "bot\\bot":
        ms.execute(f"\\killjob {job.job_id}")
        bot_job = job
    elif job.command[0] == "bot\\qm":
        ms.execute(f"\\killjob {job.job_id}")

if bot_job:
    ms.execute(f"\\{' '.join(bot_job.command)}")

# THIS ASSMUMES THAT YOUR BOT DIRECTORY IS bot\
