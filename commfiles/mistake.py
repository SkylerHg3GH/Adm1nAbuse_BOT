from bottype import Context
import botlib

def main(ctx: Context):
    cmdname = ctx.rargs[0]
    botlib.followup(ctx.user, "Oops! The command you used is a command that seems to exist but doesn't! See !cmds for real commands.")
    
