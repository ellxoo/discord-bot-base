import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Set up intents
intents = discord.Intents.default()

# Create the bot instance
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        # Load all command cogs
        for filename in os.listdir('./commands'):
            if filename.endswith('.py') and filename != '__init__.py':
                await self.load_extension(f'commands.{filename[:-3]}')
                print(f'Loaded extension: {filename[:-3]}')

        # Sync slash commands globally
        await self.tree.sync()
        print("Synced slash commands globally (may take up to an hour to propagate to all servers)")

    async def on_ready(self):
        print("Login successful")
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

# Initialize and run the bot
bot = Bot()

# Run the bot with the token
async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN is not set. Copy .env.example to .env and add your token.")
        return

    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
