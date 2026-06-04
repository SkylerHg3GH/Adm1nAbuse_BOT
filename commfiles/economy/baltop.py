from bottype import Context
import botlib

def main(ctx: Context):
    # Verify there are balances in the loaded dictionary
    if not botlib.balances:
        botlib.followup(ctx.user, "The leaderboard is currently empty.")
        return

    # Sort players by balance descending from the botlib dictionary
    sorted_bals = sorted(botlib.balances.items(), key=lambda item: item[1], reverse=True)

    # Take the top 5 players
    top_players = sorted_bals[:5]

    # Format into a clean line for Minecraft messaging
    leaderboard_lines = []
    for index, (player, bal) in enumerate(top_players, start=1):
        leaderboard_lines.append(f"#{index} {player}: {bal}")

    response = " | ".join(leaderboard_lines)
    botlib.followup(ctx.user, f"Top Balances: {response}")