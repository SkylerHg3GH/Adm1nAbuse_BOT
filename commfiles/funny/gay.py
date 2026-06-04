from bottype import Context
import botlib
import random

def main(ctx: Context):
    srch = ctx.args[0] if len(ctx.args) > 0 else ctx.user
    random.seed(srch)
    g = random.randint(0, 10000) / 100
    if srch == "sembarn" or srch == "sembee":
        g = 999999
    botlib.followup(ctx.user, f"{srch} is {g}% gay (based off of seeded random number generator)")
    
