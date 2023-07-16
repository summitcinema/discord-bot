# Main module
import discord
from discord import app_commands
from discord.ext import commands

# Our modules
import bot_constants, bot_checks

# Other modules
import os, re, asyncio
from datetime import datetime, timedelta

import logging
import logging.handlers

#
# Set up logger
#
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename = "summit_bot.log",
    encoding = "utf-8",

    # 32 MB max file size
    maxBytes = 32 * 1024 * 1024,

    # Keep up to 5 backups
    backupCount = 5
)

dt_fmt = "[%Y-%m-%d %H:%M:%S]"
formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", datefmt=dt_fmt, style="{")
handler.setFormatter(formatter)
logger.addHandler(handler)

# List of bot cogs
BOT_COGS = []

class SummitDiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.LOGGER = logger

        self.HTTP_HEADERS = {
            "User-Agent": "Dr. Isaac Kleiner Discord Bot/1.1.0 (Contact chevatsummit on Discord for inquiries)"
        }

        # 25 MB, used to notify when an uploaded file is too big
        self.MAX_IMAGE_FILESIZE = 25 * 1000 * 1000

        # Guild IDs for some Summit-related servers
        # Public server
        self.SUMMIT_GUILD_ID = "910640960122277898"
        # Discord bot testing server
        self.SUMMIT_DEV_GUILD_ID = "946593234119979028"

        self.CTREE_MANUAL_SYNC_GUILDS = (
            self.SUMMIT_GUILD_ID,
            self.SUMMIT_DEV_GUILD_ID
        )

        # Messages in these channels will be automatically deleted over time, to prevent clutter and keep moderation easier
        self.CHANNEL_AUTODELETE_WHITELIST = {
            # voice
            "994347853348618290": True,

            # bot
            "994347799145619466": True,
        }

    async def _sync_to_summit_guilds(self):
        for guild_id in self.CTREE_MANUAL_SYNC_GUILDS:
            print(f"Syncing CommandTree for Discord {guild_id}...")

            guild_obj = discord.Object(id=guild_id)

            # Copy global command list to guild command list.
            # Guild commands update instantly on Discord's end, while global commands
            # take up to an hour, so we use guild commands for immediate dev testing.
            self.tree.copy_global_to(guild=guild_obj)
        
            await self.tree.sync(guild=guild_obj)

    async def setup_hook(self):
        # Load cogs
        global BOT_COGS

        print("LOADING BOT COGS")
        print("-----------------------")
        for filename in os.listdir("./bot_cogs"):
            if filename.endswith(".py"):
                print(f"Loading cog: {filename}")
                await bot.load_extension(f"bot_cogs.{filename[:-3]}")
                BOT_COGS.append(filename[:-3])
        print("-----------------------")

        # Sync /slash commands immediately
        await self._sync_to_summit_guilds()

        # Set up background tasks
        print("Setting up background tasks..")
        self.auto_delete_timer = self.loop.create_task(self.auto_delete_channels())
        self.clear_color_roles_timer = self.loop.create_task(self.clear_color_roles())

        print("-----------------------")

    async def on_ready(self):
        print(f"Logged in as {self.user.name} ({self.user.id}) in {len(self.guilds)} guilds")

        # Bot plays Garry's Mod 24/7
        await self.change_presence(activity=discord.Game(name="Garry's Mod"))

    async def on_command_error(self, ctx, error):
        command_prefix = ctx.prefix

        # If the command is missing required arguments
        if isinstance(error, commands.MissingRequiredArgument):
            command = ctx.command
            await ctx.send(f"Missing required arguments.\nUsage: **{command_prefix}{command.name}** *{command.usage}*", delete_after=5.0)
        # When one or more checks do not go through
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        # If the command is not found (invalid)
        elif isinstance(error, commands.CommandNotFound):
            pass
        # If the action is forbidden (e.g. reacting to a user who is blocking the bot)
        elif isinstance(error, discord.errors.Forbidden):
            pass
        # When a command uses discord.Member, and the provided string could not be converted to a member
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Could not find member: " + str(error))
        # Every other error
        else:
            print(f"{ctx.author.display_name} caused an error: {type(error)} - {error}")
            try:
                #await ctx.send(f"An error occured while issuing this command: {type(error)} - {error}")
                await ctx.send("An error occured while issuing this command.")
            except: pass

    # On member join, log to #automod channel
    async def on_member_join(self, member):
        if str(member.guild.id) != self.SUMMIT_GUILD_ID:
            return

        channel = discord.utils.get(member.guild.channels, name="automod")
        if channel:
            await channel.send(f"Member {member.mention} ({member.name}#{member.discriminator}, {member.id}) has joined the server.")
        else:
            print("Could not find the proper channel for on_member_leave")

    # On member remove, log to #automod channel
    async def on_member_remove(self, member):
        if str(member.guild.id) != self.SUMMIT_GUILD_ID:
            return

        channel = discord.utils.get(member.guild.channels, name="automod")
        if channel:
            await channel.send(f"Member {member.mention} ({member.name}#{member.discriminator}, {member.id}) has left the server.")
        else:
            print("Could not find the proper channel for on_member_leave")

    async def on_message(self, message: discord.Message):
        # Prevent the bot from listening to other bots
        if message.author.bot:
            return

        lmsg = message.content.lower()

        # Delete potential scam links (like advertising "free Nitro")
        if re.search(r"https?:\/\/.+?\.[a-zA-Z]{1,6}", lmsg) and "nitro" in lmsg and ("free" in lmsg or "get" in lmsg):
            await message.delete()

            reportChannel = discord.utils.get(message.guild.channels, name="automod")
            
            if reportChannel:
                try:
                    await reportChannel.send(f"User {message.author.name}#{message.author.discriminator} attempted to send a Nitro scam link in {message.channel.mention}.")
                except: pass

            return

        # Run the old on_message function
        await self.process_commands(message)

    async def auto_delete_channels(self):
        await self.wait_until_ready()

        messageLimit = 50

        while not self.is_closed():
            self.LOGGER.info("Clearing old messages in text channels.")

            for channelIdStr in self.CHANNEL_AUTODELETE_WHITELIST:
                channelObj = self.get_channel(int(channelIdStr))

                # The channel must be a text channel
                if not isinstance(channelObj, discord.TextChannel):
                    continue

                dateNow = datetime.now()

                # Only messages 5 days or older get removed
                dateThen = dateNow - timedelta(days=5)

                deletedMessages = await channelObj.purge(limit=messageLimit, before=dateThen, oldest_first=True, bulk=True)
                self.LOGGER.info(f"#{channelObj.name}: deleted {len(deletedMessages):,d} messages.")

            # Run every 10 minutes
            await asyncio.sleep(10 * 60)

    async def clear_color_roles(self):
        await self.wait_until_ready()

        while not self.is_closed():
            summit_guild = discord.utils.get(self.guilds, id=int(self.SUMMIT_GUILD_ID))

            if summit_guild is not None:
                async for member in summit_guild.fetch_members(limit=500):
                    member_color_roles = []

                    for role in member.roles:
                        is_color_role = role.name.startswith("Color - ")
                        
                        if is_color_role:
                            member_color_roles.append(role)

                    # If the member has any color roles
                    if len(member_color_roles) > 0:
                        should_keep_color_roles = any([
                            member.premium_since is not None,
                            member == summit_guild.owner
                        ])

                        if not should_keep_color_roles:
                            await member.remove_roles(*member_color_roles)
                            
                            self.LOGGER.info(f"Removing color roles for member {member.display_name} ({member.id}) - Nitro boost expired.")

            # Run every 5 minutes
            await asyncio.sleep(5 * 60)

# Discord intents - discord.py 1.5.0
bot_intents = discord.Intents.default()
bot_intents.message_content = True
bot_intents.members = True
bot_intents.presences = True

bot = SummitDiscordBot(
    command_prefix = ["!", ".", "k!"],
    case_insensitive = True,
    #help_command = None,
    owner_id = 906681120320528414,
    description = "The official bot of the Summit Cinema Discord server.",
    intents = bot_intents,

    # Limit what mentions the bot can perform
    allowed_mentions = discord.AllowedMentions(everyone=False, users=True, roles=False)
)

# Reloads all cogs
# Limit this command to bot owners
@bot_checks.limit_bot_owner()
@bot.command(aliases=["rcs", "rcogs"], hidden=True)
async def reloadallcogs(ctx):
    await ctx.send(f"Attempting to reload {', '.join(BOT_COGS)}...")

    for k in BOT_COGS:
        await bot.unload_extension(f"bot_cogs.{k}")
        await bot.load_extension(f"bot_cogs.{k}")

    print(f"\'{', '.join(BOT_COGS)}\' were reloaded by {ctx.message.author.display_name}")

bot.run(bot_constants.DISCORD_API_TOKEN)
