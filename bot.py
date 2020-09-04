### DISCORD DEL
import discord
from datetime import datetime
from discord.ext import commands

# tukaj se lahko spremeni predpona, za katero bot posluša
# here the prefix used to command the bot can be changed
client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Povabi me: !povabi"))
    # za lažji nadzor nad botom, ker ob zagonu potrebuje nekaj časa, da dobi ponudbo vseh ponudnikov
    # here for easier overview over the bot, as the initialization takes some time at the beginning
    print("[general] Bot is ready")


# pošlje embed z informacijami o botu ter ukazi, za katere posluša
# sends an embed with informations about the bot and its commands
@client.command(name="pomoc")
async def pomoc(ctx):
    embed = discord.Embed(
        title="Pomoč",
        description="Neuraden bot za informacije o študentski prehrani.",
        color=discord.Color.from_rgb(70, 193, 238)
    )
    ukazi = """
    `!hrana` izpiše ponudbo izbrane restavracije. Ta bot ima izbrano restavracijo {}.
    `!ponudba <iskalni_niz>` izpiše ponudbo iskane restavracije.
    `!informacije <iskalni_niz>` izpiše informacije o iskani restavraciji.
    `!povabi` izpiše povezavo za povabilo bota na drug discord strežnik.
    """.format(default_name)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="Ukazi", value=ukazi, inline=False)
    embed.add_field(name="Dodaj bota na svoj strežnik", value="https://bit.ly/2XaFvFn\nBot je trenutno v {} strežnikih".format(len(client.guilds)), inline=False)
    embed.add_field(name="Pomoč", value="Za več informacij o botu in izvorni kodi dodaj CaptainYEET#9943")
    await ctx.send(embed=embed)

# odstranjevanje privzetega ukaza za pomoč in preusmeritev na zgornji ukaz
# deletion of the default help command and rerouting !help to the version above
client.remove_command("help")
@client.command(name="help")
async def help(ctx):
    await pomoc(ctx)


# ob prejetju ukaza hrana ("!hrana") izpiše vso ponudbo restavracije, ki je določena v programu
# when command hrana ("!hrana") is called, entire menu of the chosen restaurant is sent
@client.command(name="hrana")
async def hrana(ctx):
    await ctx.send("**"+restaurant+"**")
    await ctx.send(get_menu_message(default))
    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    # izpis v konzolo za boljši nadzor
    # output to the console for better control
    print("[general] Request for "+restaurant+" menu complete: ", current_time)


# ob prejetju ukaza ponudba ("!ponudba <poizvedba>") izpiše ponudbo iskane restavracije, če se s poivedbo ujema
#   več ponudnikov, uporabnik izbere iskanega
# when command ("!ponudba <query>") menu of the searched restaurant is sent, if query matches multiple providers,
#   user chooses the one he is looking for
@client.command(name="ponudba")
async def ponudba(ctx, *, query):
    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    found = False
    options = []
    for key in providers:
        if query.lower() in key.lower():
            options.append(key)
    if len(options) == 1:
        await ctx.send("**"+options[0]+"**")
        await ctx.send(get_menu_message(providers[options[0]]))
        found = True
        print("[general] Request for", options[0], "menu complete: ", current_time)
    elif len(options) > 1:
        list = "```"
        for index, option in enumerate(options):
            list += ('{:<4}'.format(str(index+1))+"  "+option+"\n")
        list += "```"
        if len(list) <= 2000:
            await ctx.send("**Več ponudnikov vsebuje iskan niz.**\nOdgovorite z številko, ki je na seznamu pred ponudnikom, katerega ponudbo želite."+list)
        else:
            await ctx.send("**Iskani niz je preveč splošen, poskusite ponovno.**")
            print("[general] Search to broad for query", query+": "+current_time)
            return

        def check(m):
            return m.author.id == ctx.author.id and ctx.channel.id == m.channel.id and 1 <= int(m.content) <= len(options)

        msg = await client.wait_for('message', check=check, timeout=60)
        await ctx.send("**"+options[int("{.content}".format(msg))-1]+"**")
        await ctx.send(get_menu_message(providers[options[int("{.content}".format(msg))-1]]))
        found = True
        print("[general] Request for", options[int("{.content}".format(msg))-1], "menu complete: ", current_time)
    if not found:
        await ctx.send("**Med ponudniki ni zadetka, poskusite ponovno.**")
        print("[general] Provider", query, "not found: "+current_time)


# ob prejetju ukaza ponudba ("!informacije <poizvedba>") izpiše informacije o iskani restavraciji, če se s poivedbo ujema
#   več ponudnikov, uporabnik izbere iskanega
# when command ("!informacije <query>") informations about the searched restaurant are sent, if query matches multiple providers,
#   user chooses the one he is looking for
@client.command(name="informacije")
async def informacije(ctx, *, query):
    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    found = False
    options = []
    for key in providers:
        if query.lower() in key.lower():
            options.append(key)
    if len(options) == 1:
        naziv = options[0]
        info = get_info_message(providers[options[0]])
        info.title = naziv
        await ctx.send(embed=info)
        found = True
        print("[general] Request for", options[0], "informations complete: ", current_time)
    elif len(options) > 1:
        list = "```"
        for index, option in enumerate(options):
            list += ('{:<4}'.format(str(index+1))+"  "+option+"\n")
        list += "```"
        if len(list) <= 2000:
            await ctx.send("**Več ponudnikov vsebuje iskan niz.**\nOdgovorite z številko, ki je na seznamu pred ponudnikom, katerega informacije želite."+list)
        else:
            await ctx.send("**Iskani niz je preveč splošen, poskusite ponovno.**")
            print("[general] Search to broad for query", query+": "+current_time)
            return

        def check(m):
            return m.author.id == ctx.author.id and ctx.channel.id == m.channel.id and 1 <= int(m.content) <= len(options)

        msg = await client.wait_for('message', check=check, timeout=60)
        naziv = options[int("{.content}".format(msg))-1]
        info = get_info_message(providers[options[int("{.content}".format(msg))-1]])
        info.title = naziv
        await ctx.send(embed=info)
        found = True
        print("[general] Request for", options[int("{.content}".format(msg))-1], "informations: ", current_time)
    if not found:
        await ctx.send("**Med ponudniki ni zadetka, poskusite ponovno.**")
        print("[general] Provider", query, "not found: "+current_time)


# pošlje embed s skrajšanjio povezavo za povabilo bota na drug discord strežnik
# sends an embed with a shortened invite link for the bot
@client.command(name="povabi")
async def povabi(ctx):
    sporocilo = discord.Embed(
        title="Povabi me na svoj discord strežnik:",
        description="https://bit.ly/2XaFvFn",
        color=discord.Color.from_rgb(70, 193, 238)
    )
    await ctx.send(embed=sporocilo)


### WEB REQUESTS DEL
import requests
from bs4 import BeautifulSoup

# tu se lahko izbere katerakoli restavracija
# here any of the providers can be chosen
default = 2529
url = "https://www.studentska-prehrana.si/restaurant/Details/"+str(default)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

cards = [str(card) for card in soup.find_all(class_="text-bold color-blue")]
restaurant = [str(niz) for niz in soup.find_all(class_="no-margin bold")][0].replace('<h3 class="no-margin bold">', "").replace('</h3>', "").strip()

default_name = restaurant


# DOBIVANJE IMENIKA PONUDNIKOV
# retrieval of a list of providers
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
# retrieval of specified provider's menu
def get_menu_message(ID):
    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    if ID not in recent_providers:
        store_menu_message(ID, now)
        print("[storage] Added "+str(ID)+" to recent providers: "+current_time)
    else:
        if now.strftime("%D") != recent_providers[ID].strftime("%D"):
            store_menu_message(ID, now)
            print("[storage] Refreshed the menu for "+str(ID)+": "+current_time)
        else:
            print("[storage] Today's menu already stored for "+str(ID)+": "+current_time)

    return menu_messages[ID]


# shranjevanje ponudbe in časa pridobitve ponudbe
# storing the menu and the time of retrieval
def store_menu_message(ID, now):
    menu_messages[ID] = scrape_menu(ID)
    recent_providers[ID] = now


# "praskanje" ponudbe iz ustrezne spletne strani
# scraping the menu from the correct web page
def scrape_menu(ID):
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


# DOBIVANJE INFORMACIJ
def get_info_message(ID):
    url = "https://www.studentska-prehrana.si/restaurant/Details/" + str(ID)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    informacije = soup.find(class_="col-md-6")
    naslov = str(informacije.find("small")).replace("<small>", "").replace("</small>", "")
    if len(naslov) == 0:
        naslov = "Ponudnik nima vpisanega naslova"
    telefonska = naslov.split("(")[1].replace(")", "")
    if len(telefonska) == 0:
        telefonska = "Ponudnik nima vpisane telefonske številke"
    doplacilo = str(informacije.find(class_="color-light-grey")).replace('<span class="color-light-grey">', "").replace("</span>", "")
    if len(doplacilo) == 0:
        doplacilo = "Ponudnik nima vpisanega zneska doplačila"
    casi = str(soup.find_all(class_="col-md-12 text-bold"))
    med_tednom = casi.split("<br/>")[1].strip()
    sobota = casi.split("Sobota :")[1].strip()
    if sobota.startswith("Zaprto"):
        sobota = "Zaprto"
    else:
        sobota = casi.split("<br/>")[4].strip()
    nedelja = casi.split("Nedelja / Prazniki :")[1].replace("</div>]", "").replace("<br/> ", "").strip()
    odpiralni_casi = "\tMed tednom: "+med_tednom+"\n\tSobota: "+sobota+"\n\tNedelja in prazniki: "+nedelja
    embed = discord.Embed(
        color=discord.Color.from_rgb(70, 193, 238)
    )
    embed.add_field(name="Naslov", value=naslov.split("(")[0], inline=False)
    embed.add_field(name="Telefonska številka", value=telefonska, inline=False)
    embed.add_field(name="Doplačilo", value=doplacilo, inline=False)
    embed.add_field(name="Odpiralni časi", value=odpiralni_casi, inline=False)
    return embed


# ERROR HANDLING
# vem da to ni prav, ampak trenutno to ni prioriteta
# I know that this is not the right way, but it is not a priority at the moment
@client.event
async def on_command_error(ctx, error):
    print("[ error ] "+str(error))


### ZAGON BOTA
providers = get_providers()
recent_providers = dict()
menu_messages = dict()
# branje ključa za bot iz zasebne datoteke, ker se takšne stvari ne objavljajo na internetu
# reading the bot key from a private file because things like that shouldn't be posted on the internet
dat = open("key.txt", "r")
key = dat.read().strip()
client.run(key)
