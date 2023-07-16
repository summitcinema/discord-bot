import discord
from discord import app_commands
from discord.ext import commands

from enum import Enum

class RoleColor(Enum):
    red = 0
    orange = 1
    yellow = 2
    lime = 3
    green = 4
    skyblue = 5
    blue = 6
    purple = 7
    pink = 8
    black = 9
    brown = 10

class ColorRoles(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Refer to RoleColor enum for the indexing of this list
        # This is used to convert user input, e.g. "skyblue" to the role's actual name, "Color - Sky Blue"
        self.role_color_names = (
            "Red",
            "Orange",
            "Yellow",
            "Lime",
            "Green",
            "Sky Blue",
            "Blue",
            "Purple",
            "Pink",
            "Black",
            "Brown"
        )

    @commands.hybrid_command(
        description="Sets your role color. You must be Nitro-boosting the server to use this!",
        aliases=["setcolorrole", "setrolecolor"],
        usage="[color]"
    )
    @discord.app_commands.describe(
        role_color_int="The name of the color to apply."
    )
    @discord.app_commands.rename(
        role_color_int = "color_to_set"
    )
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def rolecolor(self, ctx, role_color_int: RoleColor):
        target_user = ctx.author

        # If the user is not Nitro boosting, and is not the guild owner
        if ctx.author.premium_since is None and ctx.author != ctx.guild.owner:
            await ctx.send("You need to Nitro boost this server to use color roles!")
            return

        # Get role name from enum value
        role_color_name = self.role_color_names[role_color_int.value]
        
        # Get the guild's role from the name, if any
        role_object = discord.utils.get(ctx.guild.roles, name=f"Color - {role_color_name}")

        if role_object is not None:
            #
            # Remove user's other colored roles
            #
            color_roles_to_remove = []

            for role in target_user.roles:
                if role.name.replace("Color - ", "") in self.role_color_names:
                    color_roles_to_remove.append(role)

            if len(color_roles_to_remove) > 0:
                await target_user.remove_roles(*color_roles_to_remove, reason="Existing color role detected, removing for incoming color role.")

            #
            # Now add the new role to the user
            #
            await target_user.add_roles(role_object)

            await ctx.send(f"Your role color is now **{role_color_name}**.")

            self.client.LOGGER.info(f"Assigning color role {role_color_name} to member {target_user.display_name} ({target_user.id}).")

async def setup(bot):
    await bot.add_cog(ColorRoles(bot))
