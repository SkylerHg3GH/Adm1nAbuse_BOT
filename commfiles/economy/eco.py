from bottype import Context
import botlib
import botperm

LOCKED_USERS = botperm.list_with_perm("eco.setbal")

def main(ctx: Context):
    if len(ctx.args) < 2:
        botlib.followup(
            ctx.user,
            "Usage: !eco get <user> | !eco set <user> <amount> | !eco add <user> <amount>"
        )
        return

    action = ctx.args[0].lower()
    target = ctx.args[1]

    if action == "get":
        bal = botlib.balances.get(target, 0)
        botlib.followup(ctx.user, f"{target}'s balance: {bal}")
        return

    if ctx.user not in LOCKED_USERS:
        botlib.followup(ctx.user, "Not enough permission")
        return

    if action == "set":
        if len(ctx.args) < 3:
            botlib.followup(ctx.user, "Usage: !eco set <user> <amount>")
            return

        amount = int(ctx.args[2])
        botlib.balances[target] = amount

        botlib.followup(
            ctx.user,
            f"Set {target}'s balance to {amount}."
        )
        return

    if action == "add":
        if len(ctx.args) < 3:
            botlib.followup(ctx.user, "Usage: !eco add <user> <amount>")
            return

        amount = int(ctx.args[2])

        if target not in botlib.balances:
            botlib.balances[target] = 0

        botlib.balances[target] += amount

        botlib.followup(
            ctx.user,
            f"Added {amount} to {target}. New balance: {botlib.balances[target]}"
        )
        return

    botlib.followup(ctx.user, "Unknown subcommand")