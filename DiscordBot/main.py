import discord
from discord.ext import commands
import aiohttp
import asyncio
import bs4
import data

#command prefix which us used for every bot command
client = commands.Bot(command_prefix = '?')
##not in use atm
# async def getWebReqIsOpen(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:                    
#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])

#             html = await response.text()

#             if "We're currently open." in html:
#                 print("Is open")
#                 return True
#             else:
#                 print("Is Closed")
#                 return False


falmouthURLs = {    
    "sports_facilities" : "https://fxplus.ac.uk/facilities-shops/sports-facilities/",
    "TheStannary" : {
        "StannaryBar" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/the-stannary-bar/",
        "StannaryKitchen" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/the-lower-stannary-restaurant/"
    },
    "cafe" : {
        "AMATA" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/amata-cafe/",
        "ESI" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/esi-cafe/",
        "Koofi" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/koofi/",
        "Sustainability" : "https://fxplus.ac.uk/facilities-shops/catering/penryn/the-sustainability-cafe/",               
        "Fox" : "https://fxplus.ac.uk/facilities-shops/food-drink/falmouth/fox-cafe/"
    }

}


#Gets the table from a html string
def getTable(html):
    data = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find(name="table", attrs={'id':'tablepress-2'})
    tableBody = table.find('tbody')
    rows = tableBody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return data

#Returns dict of boolean vals for whether the area is open or not
def parseStannaryBarTable(table):
    stannaryBar = {
        "StannaryBar" : True if "open" in table[0][2] else False
    }
    return stannaryBar

##Returns dict of boolean vals for Koofi Cafe
def parseKoofiCafeTable(table):
    koofi = {
        "Koofi Cafe" : True if "open" in table[0][2] else False
    }
    return koofi

#Returns dict of boolean vals for whether the area is open or not 
def parseSportCentreTable(table):
    falcilities = {
        "Mult Use Games Area" : True if "open" in table[0][2] else False,
        "Penryn Campus Gym" : True if "open" in table[2][2] else False,
        "Penryn Sports Centre" : True if "open" in table[5][2] else False
    }
    return falcilities

###Sends channel msg when procedure name 'koofi' is called as a command
@client.command()
async def koofi(msg):
    url = falmouthURLs["cafe"]["Koofi"]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            table = getTable(html)
            koofi = parseKoofiCafeTable(table)
            if koofi["Koofi Cafe"]:
                print("is open")
                await msg.send("Koofi Cafe is open at the moment!!!")
            else:
                print("is closed")
                await msg.send("Koofi Cafe is closed at the moment :(")


###Sends channel msg when procedure name 'stannary' is called as a command
@client.command()
async def stannary(msg):
    url = falmouthURLs["TheStannary"]["StannaryBar"]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:                    
            html = await response.text()
            table = getTable(html)
            bar = parseStannaryBarTable(table)
            if bar["StannaryBar"]:
                print("Is open")
                await msg.send("The Stannary Bar is open at the moment!!!")
            else:
                print("Is Closed")
                await msg.send("The Stannary Bar is closed at the moment :(")

###Sends channel msg when procedure name 'gym' is called as a command
@client.command()
async def gym(msg):
    url = falmouthURLs["sports_facilities"]
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                    
                html = await response.text()
                table = getTable(html)
                falcilities = parseSportCentreTable(table)
            
                if falcilities["Penryn Campus Gym"]:
                    print("Is open")
                    await msg.send("The Penryn Campus Gym is open at the moment!!!")
                else:
                    print("Is Closed")
                    await msg.send("The Penryn Campus Gym is closed at the moment :(")

###Sends channel msg when procedure name 'GamesArea' is called as a command
@client.command()
async def GamesArea(msg):
    url = falmouthURLs["sports_facilities"]
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                    
                html = await response.text()
                table = getTable(html)
                falcilities = parseSportCentreTable(table)
            
                if falcilities["Mult Use Games Area"]:
                    print("Is open")
                    await msg.send("The Penryn Campus Games Area is open at the moment!!!")
                else:
                    print("Is Closed")
                    await msg.send("The Penryn Campus Games Area is closed at the moment :(")

###Sends channel msg when procedure name 'SportCentre' is called as a command
@client.command()
async def SportsCentre(msg):
    url = falmouthURLs["sports_facilities"]
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                    
                html = await response.text()
                table = getTable(html)
                falcilities = parseSportCentreTable(table)
            
                if falcilities["Penryn Sports Centre"]:
                    print("Is open")
                    await msg.send("The Penryn Campus Sports Centre is open at the moment!!!")
                else:
                    print("Is Closed")
                    await msg.send("The Penryn Campus Sports Centre is closed at the moment :(")


@client.event
async def on_ready():
    print("bot is ready!")    

#Token
client.run(data.data["keys"]["token"])    