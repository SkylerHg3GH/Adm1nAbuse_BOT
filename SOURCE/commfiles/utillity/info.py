from bottype import Context
import botlib

class Info:
    def __init__(self, thing, p):
        self.ctxobj = thing
    def main(self, ctx: Context):
        botlib.followup(ctx.user, self.p + self.ctxobj)

rank = Info("ctx.prefix", "Prefix: ")
prefix = Info("ctx.prefix", "Prefix: ")