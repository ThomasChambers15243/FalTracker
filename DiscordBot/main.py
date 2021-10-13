import discord
from discord.ext import commands
import aiohttp
import asyncio
import bs4
import data
from unitl import writeRelevantServiceDataIntoFile

#how to dump dict to json file
import json
# with open('result.json', 'w') as fp:
#     json.dump(data, fp)


#command prefix which us used for every bot command
client = commands.Bot(command_prefix = '?')

##TODO
##not in use atm, would like to put webcalls in a function but not 
# sure how since its async and not just a standard response

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
    # Im going to keep these os if service status every break, i have these to come back too, 
    # maybe I could add in checks to make sure it works, and if not use these, but hold shit 
    # that sounds like so much fucking effor
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

sName = {
    "Falmouth Campus Shop" : "Shop",
    "Penryn Campus Shop" : "Shop",
    "AV" : "Service",
    "Little Wonders Nurseries" : "Service",
    "Multi Use Games Area" : "Service",
    "Penryn Campus Gym" : "Service",
    "Penryn Sports Centre" : "Service",
    "The Compass" : "Service",
    "Falmouth Campus Library" : "Library",
    "Falmouth Campus Library Helpdesk" : "Library",
    "Penryn Campus Library" : "Library",
    "Penryn Campus Library Helpdesk" : "Library",
    "Virtual Helpdes" : "Library",
    "AMATA Cafe" : "Catering",
    "ESI Cafe" : "Catering",
    "Fox Cafe" : "Catering",
    "Lower Stannary" : "Catering",
    "Stannary Deli Bar" : "Catering",
    "Koofi" : "Catering",
    "The Stannary Bar" : "Catering",
    "The Sustainability Cafe" : "Catering"
}

sIndex = {
    "Falmouth Campus Shop" : 0,
    "Penryn Campus Shop" : 1,
    "AV" : 0,
    "Little Wonders Nurseries" : 1,
    "Multi Use Games Area" : 2,
    "Penryn Campus Gym" : 3,
    "Penryn Sports Centre" : 4,
    "The Compass" : 5,
    "Falmouth Campus Library" : 0,
    "Falmouth Campus Library Helpdesk" : 1,
    "Penryn Campus Library" : 2,
    "Penryn Campus Library Helpdesk" : 3,
    "Virtual Helpdes" : 4,
    "AMATA Cafe" : 0,
    "ESI Cafe" : 1,
    "Fox Cafe" : 2,
    "Lower Stannary" : 3,
    "Stannary Deli Bar" : 4,
    "Koofi" : 5,
    "The Stannary Bar" : 6,
    "The Sustainability Cafe" : 7
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
    with open("htmlHorror.txt","w") as f:
        f.write(str(html))
    #Write html data into readable array
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    #Write array into even more readable txt file
    with open("serviceInfo.txt","w") as f:
        for i in range(0,len(data)):
            f.write(str(i) + ": ")
            f.write(str(data[i]))
            f.write("\n")
    writeRelevantServiceDataIntoFile()
    #List to hold new, indexable service data
    cleanData = []
    #appends service data to cleanData
    with open("smallerServiceFile.txt", "r") as f:
        lineData = []
        for line in f:
            lineData.append(line)
        for i in range(0,len(data)):
            for j in range(0,len(lineData)):
                if str(data[i]) in lineData[j]:
                    cleanData.append(data[i])
                    break
    
    #Dictionary that holds service data
    services = {
        "Shop": [],
        "Service" : [],
        "Library" : [],
        "Catering" : [],
        "Student Services" : [],
    }
    #Loads cleanData into services
    for i in cleanData:
        match i[0]:
            case "Shop":
                services["Shop"].append({
                    "Name" : i[1],
                    "OpenState" : i[2],
                    "Hours" : i[3]
                })
            case "Service":
                services["Service"].append({
                    "Name" : i[1],
                    "OpenState" : i[2],
                    "Hours" : i[3]
                })
            case "Library":
                services["Library"].append({
                    "Name" : i[1],
                    "OpenState" : i[2],
                    "Hours" : i[3]
                })
            case "Catering":
                if len(i) > 3:
                    services["Catering"].append({
                        "Name" : i[1],
                        "OpenState" : i[2],
                        "Hours" : i[3]                  
                    })
                else:
                    services["Catering"].append({
                        "Name" : i[1],
                        "OpenState" : i[2],
                        "Hours" : None                  
                    })                    
            case _:
                #Thise leaves the exceptions
                print("This was an exception")
                print(i[0])
                pass
    #print(services)
    with open('result.json', 'w') as fp:
        json.dump(services, fp, indent=4)
    
    # with open("result.json") as jf:
    #     jsonObj = json.load(jf)
    # print("DIC TESTS")
    # print(services["Shop"])#[0][0]["Name"])
    # print("\n")
    # print(services["Shop"][0]["Name"])
    # print(services["Shop"][1]["OpenState"])
        
    ##WHATS GOING ON
    #opens up smallerServiceFile.txt, that file comes from unitil, and has 28 lines
    #all the relivant lines that i need from the file serviceInfo.txt
    #ServiceInfo.txt is the data array, that was scarpped form falmouth service website,
    #written neatly so its readable, i even added line numbers - each line represents an elemeant.
    #here, i compare each element in data, to every element in lineData (a list where each ele is a line from smallerServiceFile.txt)
    #and if the ele from data is in (not equal), I add it to list cleanData.
    #You end up with some a cleanData array which has all the needed infomation, id indexable and cant be transfered to a json file (with effort)


    #TODO   Turn cleanData into a dictionary/JSON file
    #TODO   Clean and optimise everything that happened here today mygod
    #TODO   Create function to parse opening time (Regex???)
    return services

def isOpen(services):
    if services["OpenState"] == "We're currently open.":
        return True
    else:
        return False



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

async def printIsOpenOrClosed(msg,name):
    url = falmouthURLs["ServiceStatus"]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            services = getTable(html, data.data["webInfo"]["tableCol"])
            if isOpen(services[sName[name]][sIndex[name]]):#services["Catering"][5]):
                await msg.send(name +  " is open at the moment!!!")
            else:
                print("Name is: " + name)
                await msg.send(name +  " is closed at the moment :(")

##########                 ##########
########## PENRYN CATERING ##########
##########                 ##########

###Sends channel msg when procedure name 'amata' is called as a command
@client.command()
async def amata(msg):
    print("amata was called")
    await printIsOpenOrClosed(msg,"AMATA Cafe")
    # url = falmouthURLs["ServiceStatus"]
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:
    #         html = await response.text()
    #         services = getTable(html, data.data["webInfo"]["tableCol"])            
    #         if isOpen(services[sName["AMATA Cafe"]][sIndex["AMATA Cafe"]]):
    #             await msg.send("AMATA Cafe is open at the moment!!!")
    #         else:
    #             await msg.send("AMATA Cafe is closed at the moment :(")

###Sends channel msg when procedure name 'esi' is called as a command
@client.command()
async def esi(msg):
    await printIsOpenOrClosed(msg,"ESI Cafe")
    # url = falmouthURLs["ServiceStatus"]
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:
    #         html = await response.text()
    #         services = getTable(html, data.data["webInfo"]["tableCol"])
    #         if isOpen(services[sName["ESI Cafe"]][sIndex["ESI Cafe"]]):
    #             await msg.send("ESI Cafe is open at the moment!!!")
    #         else:
    #             await msg.send("ESI Cafe is closed at the moment :(")
    

###Sends channel msg when procedure name 'koofi' is called as a command

@client.command()
async def koofi(msg):
    await printIsOpenOrClosed(msg,"Koofi")
    # #url = falmouthURLs["cafe"]["Koofi"]
    # #testing link
    # url = falmouthURLs["ServiceStatus"]
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:
    #         html = await response.text()
    #         services = getTable(html, data.data["webInfo"]["tableCol"])
    #         if isOpen(services[sName["Koofi"]][sIndex["Koofi"]]):#services["Catering"][5]):
    #             await msg.send("Koofi Cafe is open at the moment!!!")
    #         else:
    #             await msg.send("Koofi Cafe is closed at the moment :(")

# TODO

###Sends channel msg when procedure name 'stannaryB' is called as a command
@client.command()
async def stannaryB(msg):
    await printIsOpenOrClosed(msg,"The Stannary Bar")
    # url = falmouthURLs["ServiceStatus"]
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:                    
    #         html = await response.text()
    #         services = getTable(html, data.data["webInfo"]["tableCol"])
    #         if isOpen(services[sName["The Stannary Bar"]][sIndex["The Stannary Bar"]]):
    #             await msg.send("The Stannary Bar is open at the moment!!!")
    #         else:
    #             await msg.send("The Stannary Bar is closed at the moment :(")



@client.command()
async def fox(msg):
    await printIsOpenOrClosed(msg,"Fox Cafe")
    # #url = falmouthURLs["cafe"]["Koofi"]
    # #testing link
    # url = falmouthURLs["ServiceStatus"]
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:
    #         html = await response.text()
    #         services = getTable(html, data.data["webInfo"]["tableCol"])
    #         if isOpen(services[sName[""]][sIndex[""]]):
    #             await msg.send(" is open at the moment!!!")
    #         else:
    #             await msg.send(" is closed at the moment :(")

##########                   ##########
########## SPORTS FACILITIES ##########
##########                   ##########

###Sends channel msg when procedure name 'gym' is called as a command

    # url = falmouthURLs["ServiceStatus"]
    # async with aiohttp.ClientSession() as session:
    #         async with session.get(url) as response:                    
    #             html = await response.text()
    #             services = getTable(html, data.data["webInfo"]["tableCol"])            
    #             if isOpen(services[sName["Penryn Campus Gym"]][sIndex["Penryn Campus Gym"]]):
    #                 await msg.send("The Penryn Campus Gym is open at the moment!!!")
    #             else:
    #                 await msg.send("The Penryn Campus Gym is closed at the moment :(")
#TODO
###Sends channel msg when procedure name 'GamesArea' is called as a command

    # url = falmouthURLs["ServiceStatus"]
    # async with aiohttp.ClientSession() as session:
    #         async with session.get(url) as response:                    
    #             html = await response.text()
    #             table = getTable(html, data.data["webInfo"]["tableCol"])
    #             falcilities = parseSportCentreTable(table)
            
    #             if falcilities["Multi Use Games Area"]:
    #                 await msg.send("The Penryn Campus Games Area is open at the moment!!!")
    #             else:
    #                 await msg.send("The Penryn Campus Games Area is closed at the moment :(")
#TODO
###Sends channel msg when procedure name 'SportCentre' is called as a command

    # url = falmouthURLs["ServiceStatus"]
    # async with aiohttp.ClientSession() as session:
    #         async with session.get(url) as response:                    
    #             html = await response.text()
    #             table = getTable(html, data.data["webInfo"]["tableCol"])
    #             falcilities = parseSportCentreTable(table)
            
    #             if falcilities["Penryn Sports Centre"]:
    #                 await msg.send("The Penryn Campus Sports Centre is open at the moment!!!")
    #             else:
    #                 await msg.send("The Penryn Campus Sports Centre is closed at the moment :(")

@client.command()
async def lStannary(msg):
    await printIsOpenOrClosed(msg,"Lower Stannary")

@client.command()
async def stannaryDeli(msg):
    await printIsOpenOrClosed(msg,"Stannary Deli Bar")    

@client.command()
async def susCafe(msg):
    await printIsOpenOrClosed(msg,"The Sustainability Cafe")

##Service

@client.command()
async def gym(msg):
    await printIsOpenOrClosed(msg,"Penryn Campus Gym")

@client.command()
async def gamesArea(msg):
    await printIsOpenOrClosed(msg,"Multi Use Games Area")

@client.command()
async def sportsCentre(msg):
    await printIsOpenOrClosed(msg,"Penryn Sports Centre")

@client.command()
async def av(msg):
    await printIsOpenOrClosed(msg,"AV")

@client.command()
async def lilWonders(msg):
    await printIsOpenOrClosed(msg,"Little Wonders Nurseries")

@client.command()
async def compass(msg):
    await printIsOpenOrClosed(msg,"The Compass")

## Library

@client.command()
async def fLibrary(msg):
    await printIsOpenOrClosed(msg,"Falmouth Campus Library")

@client.command()
async def fHelpdesk(msg):
    await printIsOpenOrClosed(msg,"Falmouth Campus Library Helpdesk")

@client.command()
async def pLibrary(msg):
    await printIsOpenOrClosed(msg,"Penryn Campus Library")

@client.command()
async def pHelpdesk(msg):
    await printIsOpenOrClosed(msg,"Penryn Campus Library Helpdesk")

@client.command()
async def vHelpdesk(msg):
    await printIsOpenOrClosed(msg,"Virtual Helpdesk")



# @client.command()
# async def (msg):
#     await printIsOpenOrClosed(msg,"")


#Lets you know if the bot is up and running
@client.event
async def on_ready():
    print("bot is ready!")    

#Token
client.run(data.data["keys"]["token"])    