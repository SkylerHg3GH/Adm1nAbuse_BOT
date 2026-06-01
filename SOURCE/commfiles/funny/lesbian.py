from bottype import Context
import botlib
import random

def main(ctx: Context):
    srch = ctx.args[0] if ctx.args.__len__() > 0 else ctx.user

    random.seed(srch)
    g = random.randint(0, 10000) / 100
    lesbian = 100 - g

    botlib.followup(ctx.user, f"{srch} is {lesbian:.2f}% lesbian (based off of seeded random number generator)")
