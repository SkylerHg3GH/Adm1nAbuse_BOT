from bottype import Context
import botlib
import random

def main(ctx: Context):
    if not ctx.args:
        botlib.followup(ctx.user, f"Please specify an amount.")
        return

    try:
        amount = int(ctx.args[0])
    except (ValueError, TypeError):
        botlib.followup(ctx.user, f"Invalid integer")
        return

    if amount <= 0:
        botlib.followup(ctx.user, f"Amount must be greater than zero.")
        return

    if botlib.balances[ctx.user] < amount:
        botlib.followup(ctx.user, f"Not enough balance to complete the transaction.")
        return

    gain = amount if random.random() < 0.6 else 0

    if gain > 0:
        botlib.setbal(ctx.user, botlib.balances[ctx.user] + amount)
        botlib.followup(ctx.user, f"You won! You gained {amount} balances.")
    else:
        botlib.setbal(ctx.user, botlib.balances[ctx.user] - amount)
        botlib.followup(ctx.user, f"good job; You lost {amount} balance.")