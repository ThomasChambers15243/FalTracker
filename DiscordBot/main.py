import discord
from discord.ext import commands
import aiohttp
import asyncio
import bs4

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
    "the_stannary" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/the-stannary-bar/",
    "sports_facilities" : "https://fxplus.ac.uk/facilities-shops/sports-facilities/",
    "Koofi" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/koofi/"
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
def parseStannaryBarOpen(table):
    stannaryBar = {
        "StannaryBar" : True if "open" in table[0][2] else False
    }
    return stannaryBar

#Returns dict of boolean vals for whether the area is open or not 
def parseSportCentreTable(table):
    falcilities = {
        "Mult Use Games Area" : True if "open" in table[0][2] else False,
        "Penryn Campus Gym" : True if "open" in table[2][2] else False,
        "Penryn Sports Centre" : True if "open" in table[5][2] else False
    }
    return falcilities

##Says if the Stannary Bar is open or closed
@client.command()
async def stannary(msg):
    url = falmouthURLs["the_stannary"]
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                    
                html = await response.text()
                table = getTable(html)
                bar = parseStannaryBarOpen(table)
                if bar["StannaryBar"]:
                    print("Is open")
                    await msg.send("The Stannary Bar is open at the moment!!!")
                else:
                    print("Is Closed")
                    await msg.send("The Stannary Bar is closed at the moment :(")

#Says is the gym is open or closed
@client.command()
async def gym(msg):
    url = falmouthURLs["sports_facilities"]
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(getWebReqIsOpen(url))

    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                    
                html = await response.text()
                table = getTable(html)
                falcilities = parseSportCentreTable(table)
            
                if falcilities["Penryn Campus Gym"]:
                    print("Is open")
                    await msg.send("The Sports facilities are open at the moment!!!")
                else:
                    print("Is Closed")
                    await msg.send("The sports facilities are closed at the moment :(")


@client.event
async def on_ready():
    print("bot is ready!")    


client.run('ODk3MTk4MDg3NDE0NjIwMTcy.YWSK1Q.1JUA2_tjXY2-bPp7yGT0bsK29sg')    