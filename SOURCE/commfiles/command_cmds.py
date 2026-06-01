from bottype import Context
import botlib

def main(ctx: Context):
    commands = botlib.commands.values()

    filtered = list(filter(lambda el: el["from"] != ".mistake", commands))

    names = ", ".join(str(cmd) for cmd in [k for k, v in botlib.commands.items() if v["from"] != ".mistake"])

    botlib.followup(ctx.user, f"Commands: {names}")