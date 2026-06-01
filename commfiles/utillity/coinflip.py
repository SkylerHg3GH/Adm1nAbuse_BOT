from bottype import Context
import botlib
import random

def main(ctx: Context):
    if len(ctx.args) > 1:
        heads = ctx.args[0]
        tails = ctx.args[1]
    else:
        heads = "heads"
        tails = "tails"
    res = True if random.randint(1, 2) == 1 else False
    res = heads if res else tails
    botlib.followup(ctx.user, f"You landed: {res}!")