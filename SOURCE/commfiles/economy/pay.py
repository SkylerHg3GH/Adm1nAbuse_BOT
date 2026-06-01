from bottype import Context
import botlib

def main(ctx: Context):
    if len(ctx.args) < 2:
        botlib.followup(ctx.user, "Usage: !pay <user> <amount>")
        return

    recipient = ctx.args[0]
    
    try:
        amount = int(ctx.args[1])
    except (ValueError, TypeError):
        botlib.followup(ctx.user, "Invalid integer.")
        return

    if amount <= 0:
        botlib.followup(ctx.user, "Amount must be greater than zero.")
        return

    if recipient == ctx.user:
        botlib.followup(ctx.user, "You can't give money to yourself.")
        return

    if botlib.balances[ctx.user] < amount:
        botlib.followup(ctx.user, "Not enough balance to complete the transaction.")
        return

    if recipient not in botlib.balances:
        botlib.followup(ctx.user, "That user doesn't exist.")
        return

    botlib.setbal(ctx.user, botlib.balances[ctx.user] - amount)
    botlib.setbal(recipient, botlib.balances[recipient] + amount)

    botlib.followup(ctx.user, f"You gave {amount} balance to {recipient}.")