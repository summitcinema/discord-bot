import discord
from discord.ext import commands

from datetime import datetime

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        description="Deletes messages. All messages posted after <message-ID> will be deleted unless [user-ID] or [message-filter] is provided.",
        usage="<message-ID> [message-limit] [user-ID] [message-filter]",
        aliases=["deletemsg", "deletemessage", "deletemessages"],
        hidden = True
    )
    @commands.cooldown(1, 1, commands.BucketType.channel)
    @commands.has_permissions(manage_messages=True)
    async def delmsg(self, ctx, message_id: int, msg_limit: int = 500, author = None, filter_str = None):
        msg_snowflake = await ctx.fetch_message(message_id)

        self.client.LOGGER.info(f"User {ctx.author.display_name} ({ctx.author.id}) requested message deletion.")

        await ctx.send(f"Attempting message deletion with a limit of {msg_limit}...")

        def check_delete_msg(message):
            if author and str(message.author.id) != author:
                return False
            if filter_str and filter_str not in message.content:
                return False
            return True

        deleted = await ctx.channel.purge(check=check_delete_msg, after=msg_snowflake, limit=msg_limit)

        await ctx.send(f"Message deletion done. Deleted {len(deleted)} messages.")

    @commands.command(
        description="Changes the slowmode of a channel. Maximum cooldown is 6 hours (21,600 seconds).",
        usage="<channel> [seconds]",
        aliases=["changeslowmode"],
        hidden = True
    )
    @commands.cooldown(1, 1, commands.BucketType.channel)
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, channel: discord.TextChannel, seconds: int = 1):
        #21,600 seconds (6 hours) is the maximum value for slowmode
        seconds = min(21600, seconds)

        self.client.LOGGER.info(f"User {ctx.author.display_name} ({ctx.author.id}) adjusted slowmode for #{channel.name} ({seconds:,d} seconds).")

        try:
            await channel.edit(slowmode_delay = seconds)
            await ctx.send(f"Changed slowmode for channel {channel} to {seconds} seconds.")
        except:
            await ctx.send(f"Unable to adjust slowmode for channel {channel}.")

    @commands.command(
        description="Permanently bans a user via their Discord user ID.",
        usage="<id>",
        hidden=True
    )
    @commands.cooldown(1, 1, commands.BucketType.channel)
    @commands.has_permissions(administrator=True)
    async def pban(self, ctx, userId: str):
        user = await self.client.fetch_user(int(userId))

        self.client.LOGGER.info(f"User {ctx.author.display_name} ({ctx.author.id}) requested ban for user ID {userId}.")

        if user:
            await ctx.guild.ban(user)

            await ctx.send(f"Successfully banned user ID {userId}.")
        else:
            await ctx.send(f"Could not find user by user ID {userId}.")

    @commands.command(
        description="Gives moderator-related info on a user.",
        usage="<user>",
        hidden = True
    )
    @commands.cooldown(1, 1, commands.BucketType.channel)
    @commands.has_permissions(manage_messages=True)
    async def grabinfo(self, ctx, user: discord.Member):
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("The provided user isn't valid.")
            return

        embed = discord.Embed(colour=0x2E89F9, title=f"User info for {user.display_name} ({user.name} - {user.id})")
        embed.add_field(name="Account created", value=user.created_at.strftime("%B %m, %Y"))
        embed.add_field(name="Joined this server", value=user.joined_at.strftime("%B %m, %Y"))
        embed.add_field(name="Is pending verification?", value=("Yes" if user.pending else "No"))
        embed.add_field(name="Desktop status", value=user.desktop_status.value.title())
        embed.add_field(name="Web status", value=user.web_status.value.title())
        embed.add_field(name="Mobile status", value=user.mobile_status.value.title())
        embed.add_field(name="Overall status", value=user.status.value.title())
        embed.add_field(name="Is active on mobile?", value=("Yes" if user.is_on_mobile() else "No"))

        user_public_flags = ", ".join([name.replace("_", " ").title() for (name, value) in user.public_flags if value != 0])
        if user_public_flags == "":
            user_public_flags = "None"
        embed.add_field(name="Public flags", value=user_public_flags)

        user_member_flags = ", ".join([name.replace("_", " ").title() for (name, value) in user.flags if value != 0])
        if user_member_flags == "":
            user_member_flags = "None"
        embed.add_field(name="Member flags", value=user_member_flags)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
