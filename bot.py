### DISCORD DEL
import discord
from datetime import datetime
from discord.ext import commands

# tukaj se lahko spremeni predpona, za katero bot posluša
# here the prefix used to command the bot can be changed
client = commands.Bot(command_prefix="!")

# za lažji nadzor nad botom, ker ob zagonu potrebuje nekaj časa, da dobi ponudbo vseh ponudnikov
# here for easier overview over the bot, as the initialization takes some time at the beginning
@client.event
async def on_ready():
    print("Bot is ready")

# ob prejetju ukaza hrana ("!hrana") izpiše vso ponudbo restavracije, ki je določena v programu
# when command hrana ("!hrana") is called, entire menu of the chosen restaurant is sent
@client.command(name="hrana")
async def hrana(ctx):
    await ctx.send("**"+restaurant+"**")
    food_message = "```\n"
    food_message += "\n".join(food_list)
    food_message += "```"
    #for food in food_list: food_message += food
    await ctx.send(food_message)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # izpis v konzolo za boljši nadzor
    # output to the console for better control
    print("Request: ", current_time)

### WEB REQUESTS DEL
import requests
from bs4 import BeautifulSoup

# tu se lahko izbere katerakoli restavracija
# here any of the providers can be chosen
url = "https://www.studentska-prehrana.si/restaurant/Details/2529"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

cards = [str(card) for card in soup.find_all(class_="text-bold color-blue")]
restaurant = [str(niz) for niz in soup.find_all(class_="no-margin bold")][0].replace('<h3 class="no-margin bold">', "").replace('</h3>', "").strip()
food_list = [card.replace('<p class="text-bold color-blue"><h5><strong class="color-blue">', "").replace('</strong></h5></p>', "") for card in cards]


### ZAGON BOTA
# branje ključa za bot iz zasebne datoteke, ker se takšne stvari ne objavljajo na internetu
# reading the bot key from a private file because things like that shouldn't be posted on the internet
dat = open("key.txt", "r")
key = dat.read().strip()
client.run(key)