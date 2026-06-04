from bottype import Context
import botlib
import random

def main(ctx: Context):
    if len(ctx.args) < 1:
        botlib.followup(ctx.user, f"Usage: !random <items separated by ,>")
        return
    choices = " ".join(ctx.args).split(",")
    botlib.followup(ctx.user, f"Out of all of the options, you got: {random.choice(choices)}")