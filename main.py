import discord, os, sys, json
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import requests


if not os.path.isfile("config.json"):
    sys.exit("Could not find 'config.json', please make sure you have it in the root directory and try again.")
else:
    with open("config.json") as file:
        print("Found 'config.json'")
        config = json.load(file)


bot = Bot(command_prefix=config["BOT"]["PREFIX"])

bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")



# help command
@bot.command()
async def help(message):
    helpembed=discord.Embed(title="Here is the list of commands.")
    helpembed.add_field(name=config["BOT"]["PREFIX"] + "help", value="Display the help menu", inline=False)
    helpembed.add_field(name=config["BOT"]["PREFIX"] + "send", value="Send an SMS message\n```(Suggestion: " + config["BOT"]["PREFIX"] + "send +1093842222 [MESSAGE])```", inline=False)
    await message.channel.send(embed=helpembed)


# send command
@bot.command()
async def send(message, tonumber, *, messagebody=""):
    headers = {
    'Content-Type': 'application/json',
    'Authorization': config["API"]["TELNYX_API_KEY"]

    }

    data = json.dumps({
        "from" : config["API"]["FROM_NUMBER"],
        "to" : str(tonumber),
        "text" : str(messagebody)
    })

    response = requests.post('https://api.telnyx.com/v2/messages', headers=headers, data=data)
    
    await message.channel.send("Sending message")
    
    try:
        print("From: " + config["API"]["FROM_NUMBER"])
        print("To: " + str(tonumber))
        print("Message: " + str(messagebody))
        print(response.text)
        await message.channel.send("Your message ``" + str(messagebody) + "`` has been sent to ``" + str(tonumber) + "`` from this number ``" + config["API"]["FROM_NUMBER"] + "`` :thumbsup:")
    except:
        await message.channel.send("Could not send SMS message")
    



bot.run(config["BOT"]["DISCORD_TOKEN"])

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return




