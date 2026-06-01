from bottype import Context
import botlib
import random

def main(ctx: Context):
    if ctx.user != "SkylerHg3":
        botlib.followup(ctx.user, f"Not enough permission")
        return
    botlib.setbal(ctx.args[0], int(ctx.args[1]))
    botlib.followup(ctx.user, f"Set {ctx.args[0]}'s balance to {ctx.args[1]}.")