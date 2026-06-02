from bottype import Context
import botlib

def main(ctx: Context):
    botlib.followup(ctx.user, f"Quack!")
    