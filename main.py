import asyncio
from game_manager import GameManager

async def main():
    game = GameManager()
    await game.start_game()

if __name__ == "__main__":
    asyncio.run(main())