import discord
from discord import app_commands
import responses
import log

logger = log.setup_logger(__name__)

config = responses.get_config()

isPrivate = False



class aclient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="список ваших грехов.")

async def send_message(message, user_message):
    await message.response.defer(ephemeral=isPrivate)
    try:
        response = '> **' + user_message + '** - <@' + \
            str(message.user.id) + '>\n\n'
        response = f"{response}{await responses.handle_response(user_message)}"
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
            if "```" in response:
                # Split the response if the code block exists
                parts = response.split("```")
                # Send the first message
                await message.followup.send(parts[0])
                # Send the code block in a seperate message
                code_block = parts[1].split("\n")
                formatted_code_block = ""
                for line in code_block:
                    while len(line) > 1900:
                        # Split the line at the 50th character
                        formatted_code_block += line[:1900] + "\n"
                        line = line[1900:]
                    formatted_code_block += line + "\n"  # Add the line and seperate with new line

                # Send the code block in a separate message
                if (len(formatted_code_block) > 2000):
                    code_block_chunks = [formatted_code_block[i:i+1900]
                                         for i in range(0, len(formatted_code_block), 1900)]
                    for chunk in code_block_chunks:
                        await message.followup.send("```" + chunk + "```")
                else:
                    await message.followup.send("```" + formatted_code_block + "```")

                # Send the remaining of the response in another message

                if len(parts) >= 3:
                    await message.followup.send(parts[2])
            else:
                response_chunks = [response[i:i+1900]
                                   for i in range(0, len(response), 1900)]
                for chunk in response_chunks:
                    await message.followup.send(chunk)
        else:
            await message.followup.send(response)
    except Exception as e:
        await message.followup.send("> **Ты не достоин моего ответа, смертный.**")
        logger.exception(f"Error while sending message: {e}")


def run_discord_bot():
    client = aclient()

    @client.event
    async def on_ready():
        await client.tree.sync()
        logger.info(f'{client.user} is now running!')

    @client.tree.command(name="chat", description="Обсудить с Габриелем ваши грехи.")
    async def chat(interaction: discord.Interaction, *, message: str):
        if interaction.user == client.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
        await send_message(interaction, user_message)




    TOKEN = config['Gabriel_token']
    client.run(TOKEN)

run_discord_bot()
