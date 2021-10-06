import disnake
from disnake.ext import commands
from discord_slash import cog_ext, SlashContext
## DATE AND TIME ##
from datetime import datetime, timedelta, timezone
import time
import asyncio

def validate_time(sesh_time):
    if len(sesh_time) != 5:
        return "Invalid time format."
    else:
        if int(sesh_time[0:2]) > 24:
            return "Invalid HOUR format."
        elif int(sesh_time[3:5]) > 59:
            return "Invalid MINUTE format."
        else:
            return "Ok."

test_guilds=[860414380444483584]

class Sessions(commands.Cog):

    def __init__(self, client):
        self.client = client

#### 1ST SESSION ####

    @cog_ext.cog_slash(
        name="sessions",
        description = "Set a reminder for a Vedantu/Unacademy session.",
        options = [
            {
                "name": "sesh_time",
                "description": "Enter time in 'HH:MM AM/PM' format.",
                "type": 3,
                "required": "true"
            },
            {
                "name": "sesh_name",
                "description": "Name of the session.",
                "type": 3,
                "required": "true"
            }
        ],
        guild_ids = test_guilds
    )
    async def sessions(self, ctx: SlashContext, sesh_time, sesh_name):
        
        validate = validate_time(sesh_time.lower())
            
        if validate != "Ok.":

            await ctx.send("You didn't enter the time correctly, dumbass.")

        else:

            await ctx.send(f"Oki, noted.\n\n**Session Name:** {sesh_name}\n**Session Time:** {sesh_time}")

            sesh_hour = sesh_time[0:2]
            sesh_min = sesh_time[3:]

            while True:
                
                now = datetime.now(tz=timezone(timedelta(hours=5.5)))
                
                current_hour = now.strftime("%H")
                current_min = now.strftime("%M")
                current_sec = now.strftime("%S")

                if current_hour == sesh_hour:
                    if current_min == sesh_min:
                        await ctx.send(f"Oi {ctx.author.mention}! It's **{current_hour}:{current_min}** right now, aka time for **{sesh_name}**.", tts=True, delete_after=120.0)
                        break
                await asyncio.sleep(40)
        
def setup(client):
    client.add_cog(Sessions(client))