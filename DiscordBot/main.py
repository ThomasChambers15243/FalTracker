import discord
from discord.ext import commands
import aiohttp
import asyncio
import bs4
import data

#how to dump dict to json file
#import json
# with open('result.json', 'w') as fp:
#     json.dump(data, fp)


#command prefix which us used for every bot command
client = commands.Bot(command_prefix = '?')

##TODO
##not in use atm, would like to put webcalls in a function but not sure how since its async and not just a standard response

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


## Url's for use in getting html data from the falmouth web pages
falmouthURLs = {    
    "SportsFacilities" : {
        "SportsFacilities" : "https://fxplus.ac.uk/facilities-shops/sports-facilities/",
        "FitnessCentre" : "https://fitnesscentre.fxplus.ac.uk/"
    },
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
    },
    #Holy fucking shit why didnt i know this existed
    #now i need to refactor everything and just use this one link, fuck me
    "ServiceStatus" : "https://fxplus.ac.uk/service-status/"

}


#Gets the table which tells you wether its open from a html string
#Returns the table as a list called data
def getTable(html, tableID):
    data = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    #Table id for the main table in the page which shows relevant data
    #Praying this is the same for all pages, seems to be since
    #all these pages seem to use the same template, THANK GOD
    table = soup.find(name="table", attrs={'id':tableID})
    tableBody = table.find('tbody')
    rows = tableBody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    f = open("serviceInfo.txt","w")
    for i in range(0,len(data)):
        f.write(str(i) + ": ")
        f.write(str(data[i]))
        f.write("\n")
    f.close()

    cleanData = []
    start = 97
    end = 122
    lineData = []

    ##WHATS GOING ON
    #opens up smallerServiceFile.txt, that file comes from unitil, and has 28 lines
    #all the relivant lines that i need from the file serviceInfo.txt
    #ServiceInfo.txt is the data array, that was scarpped form falmouth service website,
    #written neatly so its readable, i even added line numbers - each line represents an elemeant.
    #here, i compare each element in data, to every element in lineData (a list where each ele is a line from smallerServiceFile.txt)
    #and if the ele from data is in (not equal), I add it to list cleanData.
    #You end up with some a cleanData array which has all the needed infomation, id indexable and cant be transfered to a json file (with effort)


    #TODO   Turn unitl into a reusable function
    #TODO   Turn cleanData into a dictionary/JSON file
    #TODO   Clean and optimise everything that happened here today mygod

    with open("smallerServiceFile.txt", "r") as f:
        for line in f:
            lineData.append(line)
        for i in range(0,len(data)):
            for j in range(0,len(lineData)):
                if str(data[i]) in lineData[j]:
                    print(data[i])
                    cleanData.append(data[i])
                    break
    print("\nclean data is: \n")
    print(len(cleanData))
    for i in cleanData:
        print(i)
        # if i[0] == "Catering" or i[0] == "Library" or i[0] == "Service":
        #     print(i[1])
        # else:
        #     print(i[0])
        print("   ")


    #print(lineData[25])
    #print("this is data data\n\n" + str(data[56]))

    # if str(data[56]) in str(lineData[25]):
    #     print("is equal")
    # else:
    #     print("fuck of")


    return data


##########                 ##########
##########  TABLE PARSING  ##########
##########                 ##########

##Returns a dict, even if theres just one value, for
# A. Consitancy
# B. Maintainabliltiy, if anymore are added it makes my life easier

#Returns dict of boolean vals for whether the Bar is open or not
def parseStannaryBarTable(table):
    stannaryBar = {
        "StannaryBar" : True if "open" in table[0][2] else False
    }
    return stannaryBar

#Returns dict of bloolean vals for AMATA Cafe
def parseAMATAcafeTable(table):
    AMATA = {
        "AMATA Cafe" : True if "open" in table[0][2] else False
    }
    return AMATA

##Returns dict of boolean vals for ESI Cafe
def parseESIcafeTable(table):
    ESI = {
        "ESI Cafe" : True if "open" in table[0][2] else False
    }
    return ESI

##Returns dict of boolean vals for Koofi Cafe
def parseKoofiCafeTable(table):
    koofi = {
        "Koofi Cafe" : True if "open" in table[56][2] else False#table[0][2] else False
    }
    return koofi

##Returns dict of boolean vals for Fox Cafe
def parseFoxCafeTable(table):
    fox = {
        "Fox Cafe" : True if "open" in table[0][2] else False
    }
    return fox

##Returns dict of boolean vals for the Sports Centre
def parseSportCentreTable(table):
    falcilities = {
        "Mult Use Games Area" : True if "open" in table[0][2] else False,
        "Penryn Campus Gym" : True if "open" in table[2][2] else False,
        "Penryn Sports Centre" : True if "open" in table[5][2] else False
    }
    return falcilities


#########################################################################################
##################################### COMMAND CALLS #####################################
#########################################################################################


##########                 ##########
########## PENRYN CATERING ##########
##########                 ##########

###Sends channel msg when procedure name 'amata' is called as a command
@client.command()
async def amata(msg):
    url = falmouthURLs["cafe"]["AMATA"]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            table = getTable(html, data.data["webInfo"]["tableCol"])
            amata = parseAMATAcafeTable(table)
            if amata["AMATA Cafe"]:
                await msg.send("AMATA Cafe is open at the moment!!!")
            else:
                await msg.send("AMATA Cafe is closed at the moment :(")

###Sends channel msg when procedure name 'esi' is called as a command
@client.command()
async def esi(msg):
    url = falmouthURLs["cafe"]["ESI"]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            table = getTable(html, data.data["webInfo"]["tableCol"])
            ESI = parseESIcafeTable(table)
            if ESI["ESI Cafe"]:
                await msg.send("ESI Cafe is open at the moment!!!")
            else:
                await msg.send("ESI Cafe is closed at the moment :(")


###Sends channel msg when procedure name 'koofi' is called as a command
@client.command()
async def koofi(msg):
    #url = falmouthURLs["cafe"]["Koofi"]
    #testing link
    url = falmouthURLs["ServiceStatus"]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            table = getTable(html, data.data["webInfo"]["tableCol"])
            koofi = parseKoofiCafeTable(table)
            if koofi["Koofi Cafe"]:
                await msg.send("Koofi Cafe is open at the moment!!!")
            else:
                await msg.send("Koofi Cafe is closed at the moment :(")


###Sends channel msg when procedure name 'stannaryB' is called as a command
@client.command()
async def stannaryB(msg):
    url = falmouthURLs["TheStannary"]["StannaryBar"]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:                    
            html = await response.text()
            table = getTable(html, data.data["webInfo"]["tableCol"])
            bar = parseStannaryBarTable(table)
            if bar["StannaryBar"]:
                await msg.send("The Stannary Bar is open at the moment!!!")
            else:
                await msg.send("The Stannary Bar is closed at the moment :(")

##########                   ##########
########## SPORTS FACILITIES ##########
##########                   ##########

###Sends channel msg when procedure name 'gym' is called as a command
@client.command()
async def gym(msg):
    url = falmouthURLs["SportsFacilities"]["SportsFacilities"]
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                    
                html = await response.text()
                table = getTable(html, data.data["webInfo"]["tableCol"])
                falcilities = parseSportCentreTable(table)
            
                if falcilities["Penryn Campus Gym"]:
                    await msg.send("The Penryn Campus Gym is open at the moment!!!")
                else:
                    await msg.send("The Penryn Campus Gym is closed at the moment :(")

###Sends channel msg when procedure name 'GamesArea' is called as a command
@client.command()
async def gamesArea(msg):
    url = falmouthURLs["SportsFacilities"]["SportsFacilities"]
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                    
                html = await response.text()
                table = getTable(html, data.data["webInfo"]["tableCol"])
                falcilities = parseSportCentreTable(table)
            
                if falcilities["Mult Use Games Area"]:
                    await msg.send("The Penryn Campus Games Area is open at the moment!!!")
                else:
                    await msg.send("The Penryn Campus Games Area is closed at the moment :(")

###Sends channel msg when procedure name 'SportCentre' is called as a command
@client.command()
async def sportsCentre(msg):
    url = falmouthURLs["SportsFacilities"]["SportsFacilities"]
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                    
                html = await response.text()
                table = getTable(html, data.data["webInfo"]["tableCol"])
                falcilities = parseSportCentreTable(table)
            
                if falcilities["Penryn Sports Centre"]:
                    await msg.send("The Penryn Campus Sports Centre is open at the moment!!!")
                else:
                    await msg.send("The Penryn Campus Sports Centre is closed at the moment :(")

#Lets you know if the bot is up and running
@client.event
async def on_ready():
    print("bot is ready!")    

#Token
client.run(data.data["keys"]["token"])    