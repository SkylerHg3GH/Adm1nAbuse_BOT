from bottype import Context
import botlib

def main(ctx: Context):
    if len(ctx.args) < 1:
        botlib.followup(ctx.user, "No command provided")
        return
    if ctx.args[0] not in botlib.cmdnames: 
        botlib.followup(ctx.user, "Command not found.")
        return
    obj = botlib.commands[ctx.args[0]]
    match ctx.args[1] if len(ctx.args) > 1 else "":
        case "":
            o = "That command is from: Bot.commfiles" + obj.get("from", "[Not defined]")
        case "dest":
            o = "That command is from: Bot.commfiles" + obj.get("from", "[Not defined]")
        case "usage":
            o = "That command's usage is: " + obj.get("usage", "[Not defined]")
        case "description":
            o = "That command's description is: " + obj.get("description", "[Not defined]")
        case _:
            o = "Options: dest, usage, description"
    botlib.followup(ctx.user, o)
    
