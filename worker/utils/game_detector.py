async def detect_real_game_running(client) -> bool:
    try:
        games = await client.fetch_current_games()
        return any(game.get("is_real", False) for game in games)
    except:
        return False
