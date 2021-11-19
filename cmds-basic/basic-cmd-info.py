import disnake
from disnake.ext import commands

import asyncio, random, time, datetime, json


class GetInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid Arguments. Git gud.")

    @info.command(name="user", alias="userinfo")
    async def _user(self, ctx, *, user: disnake.Member = None):
        author = ctx.message.author

        if not user:
            user = author

        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - user.joined_at).days
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        user_joined = user.joined_at.strftime("%d %b %Y %H:%M")

        created_on = f"{user_created}\n({since_created} days ago)"
        joined_at = f"{user_joined}\n({since_joined} days ago)"

        activity = f"Currently in {user.status} status"
        roles = list(reversed([x.name for x in user.roles if x.name != "@everyone"]))

        if user.activity is None:
            pass
        else:
            if str(user.activity).startswith("<disnake.activity.Activity"):
                pass
            else:
                activity = f"Playing {user.activity}"

        if roles:
            roles = "\n".join(roles)
        else:
            roles = "None"

        embed = disnake.Embed(description=activity, colour=0x36393E)
        embed.add_field(name="Joined Discord on:", value=created_on, inline=False)
        embed.add_field(name="Joined Server at: ", value=joined_at, inline=False)
        embed.add_field(name="Roles:", value=roles, inline=False)
        embed.set_footer(text=f"User ID: {user.id}")

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.bot:
            embed.set_author(name=f"{name} [Bot]", url=user.avatar)
        elif user.id == self.client.owner_id:
            embed.set_author(name=f"{name} [My Creator]", url=user.avatar)
        elif user.id == self.client.user.id:
            embed.set_author(name=f"{name} [You can also do !botinfo]", url=user.avatar)
        else:
            embed.set_author(name=name, url=user.avatar)

        if user.avatar:
            embed.set_thumbnail(url=user.avatar)

        await ctx.send(embed=embed)

    @info.command(name="server", aliases=["serverinfo"], no_pm=True)
    async def _server(self, ctx):
        guild = ctx.message.guild
        online = len(
            [
                m.status
                for m in guild.members
                if m.status == disnake.Status.online or m.status == disnake.Status.idle
            ]
        )
        total_users = len(guild.members)
        total_bots = len([member for member in guild.members if member.bot == True])
        total_humans = total_users - total_bots
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = "Since {}. Over {} days ago." "".format(
            guild.created_at.strftime("%d %b %Y %H:%M"), passed
        )

        embed = disnake.Embed(
            description=created_at, colour=disnake.Colour(value=0x36393E)
        )
        embed.add_field(name="Region", value=str(guild.region))
        embed.add_field(name="Users", value="{}/{}".format(online, total_users))
        embed.add_field(name="Humans", value=total_humans)
        embed.add_field(name="Bots", value=total_bots)
        embed.add_field(name="Text Channels", value=text_channels)
        embed.add_field(name="Voice Channels", value=voice_channels)
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Owner", value=str(guild.owner))
        embed.set_footer(text=f"Guild ID:{str(guild.id)}")

        if guild.icon:
            embed.set_author(name=guild.name, url=guild.icon)
            embed.set_thumbnail(url=guild.icon)
        else:
            embed.set_author(name=guild.name)

        await ctx.send(content=" ", embed=embed)

    @info.command(name="bot", alias="botinfo")
    async def _bot(self, ctx):
        """Show's Spectrum's current information"""
        servers = str(len(self.client.guilds))
        users = 0
        for guild in self.client.guilds:
            users += len(guild.members)
        channels = str(len(set(self.client.get_all_channels())))
        em = disnake.Embed(
            description="Some current stats for Spectrum",
            colour=disnake.Colour(value=0x36393E),
        )
        em.add_field(name="Server count:", value=servers, inline=False)
        em.add_field(name="Users bot can see:", value=str(users), inline=False)
        em.add_field(name="Channels bot can see:", value=channels, inline=False)
        em.set_author(name="Bot Information", icon_url=config["styling"]["normalLogo"])
        em.set_thumbnail(url=config["styling"]["gifLogo"])
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(GetInfo(client))
