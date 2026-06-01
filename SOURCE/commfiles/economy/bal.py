from bottype import Context
import botlib

def main(ctx: Context):
    srch = ctx.args[0] if len(ctx.args) > 0 else ctx.user
    botlib.followup(ctx.user, f"{srch} has {botlib.balances[srch]} balance.")
