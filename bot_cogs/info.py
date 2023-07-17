from sqlite3 import Time
import discord
from discord.ext import commands

import a2s
from asyncio.exceptions import TimeoutError

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.GMOD_ADDRESS = ("gmod.summitcinema.net", 27015)
        self.CONNECT_ADDRESS = "[Click to Connect](https://summitcinema.net/connect.html)"
        self.MOVIE_NIGHT_ROLE_NAME = "Movie Night Announcements"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Prevent the bot from listening to other bots
        if message.author.bot: return

    @commands.hybrid_command(
        description="Fetches info for the Garry's Mod server.",
        aliases=["gmod", "gmodinfo", "query", "serverinfo", "ip", "serverip"]
    )
    @commands.cooldown(1, 1, commands.BucketType.channel)
    async def server(self, ctx):
        progress_msg = await ctx.send("Pinging server...")

        try:
            result = await a2s.ainfo(self.GMOD_ADDRESS, timeout = 1.5)

            if result:
                # Players online include bots, so remove them
                realPlayerCount = result.player_count - result.bot_count

                embed = discord.Embed(
                    title=result.server_name,
                    description=f"{realPlayerCount} of {result.max_players} players online\n{self.CONNECT_ADDRESS}",
                    color=0x76cde7
                )

                ip_address = f"{self.GMOD_ADDRESS[0]}:{self.GMOD_ADDRESS[1]}"
                embed.add_field(name="Server IP", value=ip_address, inline=False)
                
                embed.add_field(name="Map Name", value=result.map_name, inline=False)
                
                embed.add_field(name="Players", value=realPlayerCount, inline=True)
                embed.add_field(name="Bots", value=result.bot_count, inline=True)

                if progress_msg: await progress_msg.edit(embed=embed, content="Server info found:")
            else:
                if progress_msg: await progress_msg.edit(content="The server could not be reached due to an unknown error. It may be offline.")
        except TimeoutError:
            if progress_msg: await progress_msg.edit(content="The server could not be reached. It may be offline.")

    @commands.group(
        description="Main command for movie night-related commands.",
        usage="<sub-command-or-'help'>",
        aliases=["movienights", "movie", "mnight"]
    )
    async def movienight(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing/Invalid command (Try **!movienight help** to get all commands).", delete_after=15.0)

    @movienight.command(
        description="Shows all commands.",
        aliases=["h", "hlep"]
    )
    @commands.cooldown(1, 1, commands.BucketType.channel)
    async def help(self, ctx):
        cmds_string = [f"{self.qualified_name} commands:"] # Every command help line

        for command in self.get_commands():
            # Don't show the command if it is hidden
            # Only show the movienight command
            if command.hidden or command.name != "movienight":
                continue

            usage = f"*{command.usage}*" if command.usage is not None else ""
            cmd_aliases = "/".join([command.name] + command.aliases)
            cmds_string.append(f"**!{cmd_aliases}** {usage}")

            if isinstance(command, discord.ext.commands.Group): # If the command is a group
                for group_command in command.commands:
                    if group_command.hidden: # Don't show the command if it is hidden
                        continue

                    usage = f"*{group_command.usage}*" if group_command.usage is not None else ""
                    group_cmd_aliases = "/".join([group_command.name] + group_command.aliases)
                    cmds_string.append(f"┗ **!{command.name} {group_cmd_aliases}** {usage}")

        cmds_string_final = "\n".join(cmds_string)

        await ctx.send(cmds_string_final)

    @movienight.command(
        description="Adds the movie night role, if you don't already have it.",
        aliases=["giverole"]
    )
    @commands.cooldown(1, 1, commands.BucketType.channel)
    async def addrole(self, ctx):
        for role in ctx.author.roles:
            # If the user already has the role
            if role.name == self.MOVIE_NIGHT_ROLE_NAME:
                return

        for role in ctx.guild.roles:
            if role.name == self.MOVIE_NIGHT_ROLE_NAME:
                await ctx.author.add_roles(role, reason="Movie Night role")
                await ctx.send(f"You now have the {self.MOVIE_NIGHT_ROLE_NAME} role.")
                break

    @movienight.command(
        description="Removes the movie night role if you currently have it.",
        aliases=["deleterole", "delrole"]
    )
    @commands.cooldown(1, 1, commands.BucketType.channel)
    async def removerole(self, ctx):
        roleToRemove = None

        for role in ctx.author.roles:
            # If the user has the role
            if role.name == self.MOVIE_NIGHT_ROLE_NAME:
                roleToRemove = role
                break

        if roleToRemove:
            await ctx.author.remove_roles(roleToRemove)
            await ctx.send(f"You no longer have the {self.MOVIE_NIGHT_ROLE_NAME} role.")

async def setup(bot):
    await bot.add_cog(Info(bot))
