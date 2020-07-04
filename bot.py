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
    if len(food_list)>0:
        food_message = "```\n"
        food_message += "\n".join(food_list)
        food_message += "```"
    else:
        food_message = "Ponudnik danes nima ponudbe."
    await ctx.send(food_message)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # izpis v konzolo za boljši nadzor
    # output to the console for better control
    print("Request for "+restaurant+"menu complete: ", current_time)

# ob prejetju ukaza ponudba ("!ponudba <poizvedba>") izpiše ponudbo iskane restavracije, če se s poivedbo ujema
#   več ponudnikov, uporabnik izbere iskanega
# when command ("!ponudba <query>") menu of the searched restaurant is sent, if query matches multiple providers,
#   user chooses the one he is looking for
@client.command(name="ponudba")
async def ponudba(ctx, *, query):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    found = False
    options = []
    for key in providers:
        if query.lower() in key.lower():
            options.append(key)
    if len(options) == 1:
        await ctx.send("**"+options[0]+"**")
        await ctx.send(get_menu_message(providers[options[0]]))
        found = True
        print("Request for", options[0], "menu complete: ", current_time)
    elif len(options) > 1:
        list="```"
        for index, option in enumerate(options):
            list+=('{:>4}'.format(str(index+1))+"  "+option+"\n")
        list+="```"
        if len(list)<=2000:
            await ctx.send("**Več ponudnikov vsebuje iskan niz.**\nOdgovorite z številko, ki je na seznamu pred ponudnikom, katerega ponudbo želite.")
            await ctx.send(list)
        else:
            await ctx.send("**Iskani niz je preveč splošen, poskusite ponovno.**")
            print("Search to broad for query", query, "", current_time)
            return

        def check(m):
            return int(m.content) >= 1 and int(m.content) <= len(options)

        msg = await client.wait_for('message', check=check)
        await ctx.send("**"+options[int("{.content}".format(msg))-1]+"**")
        await ctx.send(get_menu_message(providers[options[int("{.content}".format(msg))-1]]))
        found = True
        print("Request for", options[0], "menu complete: ", current_time)
    if not found:
        await ctx.send("**Med ponudniki ni zadetka, poskusite ponovno.**")
        print("Provider", query, "not found!", current_time)

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

# DOBIVANJE IMENIKA PONUDNIKOV
def get_providers():
    url = "https://www.studentska-prehrana.si/sl/restaurant"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    cards = [str(card).replace('<h2 class="no-margin color-blue">', "").replace('</a>\n</h2>', "").lstrip() for card in soup.find_all(class_="no-margin color-blue")]
    names = [((str(card).replace('<a href="/sl/restaurant/Details/', ""))[4:]).replace('">', "").strip() for card in cards]
    IDs = [int(str(card).replace('<a href="/sl/restaurant/Details/', "")[:4]) for card in cards]
    restaurants = {}
    for name, ID in zip(names, IDs):
        restaurants[name] = ID

    return restaurants

# DOBIVANJE JEDI
def get_menu_message(ID):
    url = "https://www.studentska-prehrana.si/restaurant/Details/" + str(ID)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    cards = [str(card) for card in soup.find_all(class_="text-bold color-blue")]
    food_list = [card.replace('<p class="text-bold color-blue"><h5><strong class="color-blue">', "").replace('</strong></h5></p>', "") for card in cards]
    if len(food_list) > 0:
        food_message = "```"
        food_message += "\n".join(food_list)
        food_message += "```"
    else:
        food_message = "Ponudnik danes nima ponudbe."
    if len(food_message) <= 2000:
        return food_message
    else:
        return food_message[:1966] + "\nPrikazan je samo delni meni```"

### ZAGON BOTA
providers = get_providers()
# branje ključa za bot iz zasebne datoteke, ker se takšne stvari ne objavljajo na internetu
# reading the bot key from a private file because things like that shouldn't be posted on the internet
dat = open("key.txt", "r")
key = dat.read().strip()
client.run(key)