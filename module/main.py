import discord
from discord.ext import commands
import aiohttp
import asyncio
import bs4
import data
import json
import re




# command prefix which us used for every bot command
client = commands.Bot(command_prefix = '?')

# TODO
# not in use atm, would like to put webcalls in a function but not 
# sure how since its async and not just a standard response


# Url's for use in getting html data from the falmouth web pages
falmouthServiceURL = "https://fxplus.ac.uk/service-status/"

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
    "Virtual Helpdesk" : "Library",
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
    "Virtual Helpdesk" : 4,
    "AMATA Cafe" : 0,
    "ESI Cafe" : 1,
    "Fox Cafe" : 2,
    "Lower Stannary" : 3,
    "Stannary Deli Bar" : 4,
    "Koofi" : 5,
    "The Stannary Bar" : 6,
    "The Sustainability Cafe" : 7
}

# Takes the hourse from the service string and returns a human
# readable string
def parseOpenHoursFormatting(hours):
    # LEARN REGEX
    hours = re.sub("\u2013", "-", hours)
    # hours = re.sub("[\n]", "..", hours)
    # hours = re.sub("[\n\n\n]", "\n", hours)
    return hours

# Gets the table which tells you wether its open from a html string
# Returns the table as a list called data
def parseTable(html,tableID):
    data = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find(name="table", attrs={'id':tableID})
    tableBody = table.find('tbody')
    rows = tableBody.find_all('tr')
    #Write html data into readable array
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return data

# Take a file all service info and cleans it
def writeRelevantServiceDataIntoFile():
    start = 97
    end = 122
    lines = []
    with open("serviceInfo.txt") as f:
        for line in f:
            for i in range(0,7):
                #print("i is: " + line[i].lower())
                if ord(line[i].lower()) >= start and ord(line[i].lower()) <= end:
                    lines.append(line)
                    break
    with open("smallerServiceFile.txt","w") as f:
        for i in lines:
            f.write(i)

# returns a dictionary of all the falmouth services
def getService(html, tableID):
    # Write array into even more readable txt file
    data = parseTable(html, tableID)
    with open("serviceInfo.txt","w") as f:
        for i in range(0,len(data)):
            f.write(str(i) + ": ")
            f.write(str(data[i]))
            f.write("\n")
    writeRelevantServiceDataIntoFile()
    # List to hold new, indexable service data
    cleanData = []
    # appends service data to cleanData
    with open("smallerServiceFile.txt", "r") as f:
        lineData = []
        for line in f:
            lineData.append(line)
        for i in range(0,len(data)):
            for j in range(0,len(lineData)):
                if str(data[i]) in lineData[j]:
                    cleanData.append(data[i])
                    break
    # Dictionary that holds service data
    services = {
        "Shop": [],
        "Service" : [],
        "Library" : [],
        "Catering" : [],
        "Student Services" : [],
    }
    # Loads cleanData into services
    for i in cleanData:
        match i[0]:
            case "Shop":
                services["Shop"].append({
                    "Name" : i[1],
                    "OpenState" : i[2],
                    "Hours" : parseOpenHoursFormatting(i[3])
                })
            case "Service":
                services["Service"].append({
                    "Name" : i[1],
                    "OpenState" : i[2],
                    "Hours" : parseOpenHoursFormatting(i[3])
                })
            case "Library":
                services["Library"].append({
                    "Name" : i[1],
                    "OpenState" : i[2],
                    "Hours" : parseOpenHoursFormatting(i[3])
                })
            case "Catering":
                if len(i) > 3:
                    services["Catering"].append({
                        "Name" : i[1],
                        "OpenState" : i[2],
                        "Hours" : parseOpenHoursFormatting(i[3])
                    })
                else:
                    services["Catering"].append({
                        "Name" : i[1],
                        "OpenState" : i[2],
                        "Hours" : None                  
                    })                    
            case _:
                # Thise leaves the exceptions
                print("This was an exception")
                print(i[0])
                pass

    with open('result.json', 'w') as fp:
        json.dump(services, fp, indent=4)
    return services

def isOpen(services):
    if services["OpenState"] == "We're currently open.":
        return True
    else:
        return False

# Scrapes and parses html data from falmouth uni's websites
# and prints wether or not a request service (name) is open
async def printIsOpenOrClosed(msg,name):
    
    url = falmouthServiceURL

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            html = await response.text()
            services = getService(html, data.data["webInfo"]["tableCol"])

            if isOpen(services[sName[name]][sIndex[name]]):
                await msg.send(name +  " is open at the moment!!!")
            else:
                print("Name is: " + name)
                await msg.send(name +  " is closed at the moment :(")

#########################################################################################
##################################### COMMAND CALLS #####################################
#########################################################################################


##########                 ##########
##########     CATERING    ##########
##########                 ##########

# Sends channel msg when procedure the name is called as a command
@client.command()
async def amata(msg):
    print("amata was called")
    await printIsOpenOrClosed(msg,"AMATA Cafe")

@client.command()
async def esi(msg):
    await printIsOpenOrClosed(msg,"ESI Cafe")

@client.command()
async def koofi(msg):
    await printIsOpenOrClosed(msg,"Koofi")

@client.command()
async def stannaryB(msg):
    await printIsOpenOrClosed(msg,"The Stannary Bar")

@client.command()
async def fox(msg):
    await printIsOpenOrClosed(msg,"Fox Cafe")

@client.command()
async def lStannary(msg):
    await printIsOpenOrClosed(msg,"Lower Stannary")

@client.command()
async def stannaryDeli(msg):
    await printIsOpenOrClosed(msg,"Stannary Deli Bar")    

@client.command()
async def susCafe(msg):
    await printIsOpenOrClosed(msg,"The Sustainability Cafe")

##########                 ##########
##########     SERVICE     ##########
##########                 ##########

@client.command()
async def pshop(msg):
    await printIsOpenOrClosed(msg, "Penryn Campus Shop")

@client.command()
async def fshop(msg):
    await printIsOpenOrClosed(msg, "Falmouth Campus Shop")

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

##########                 ##########
##########     LIBRARY     ##########
##########                 ##########

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




# Lets you know if the bot is up and running
@client.event
async def on_ready():
    print("bot is ready!")  

# Token
client.run(data.data["keys"]["token"])    