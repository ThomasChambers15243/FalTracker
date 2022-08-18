from asyncio.windows_events import NULL
import discord
from discord import message
from discord.client import Client
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
# Implement a spam logger
# https://stackoverflow.com/questions/64865728/how-to-keep-track-of-messages-sent-in-discord-py


# Data for getting html data
falmouthServiceURL = data.newData["webInfo"]["falmouthServiceURL"]
tableCol = data.newData["webInfo"]["tableCol"]
# ShortHand sogetting service information is more maintainable
sName = data.data["sName"]
sIndex = data.data["sIndex"]

# Takes the hour's from the service string and returns a human
# readable string
def parseOpenHoursFormatting(hours):
    # TODO LEARN REGEX
    hours = re.sub("\u2013", "-", hours)
    # hours = re.sub("[\n]", "..", hours)
    # hours = re.sub("[\n\n\n]", "\n", hours)
    return hours

# Gets the table with tableID from a html string
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

# Take a file called "serviceInfo" and cleans it,
# removing useless data and writing the clean day
# to a file
def writeRelevantServiceDataIntoFile():
    start = 97
    end = 122
    lines = []
    with open("serviceInfo.txt") as f:
        for line in f:
            for i in range(0,7):
                if ord(line[i].lower()) >= start and ord(line[i].lower()) <= end:
                    lines.append(line)
                    break
    with open("smallerServiceFile.txt","w") as f:
        for i in lines:
            f.write(i)

# returns a dictionary called "services" of all the falmouth services
# Currently writes to a json file for development purposes, 
# I dont see a need to keep the json files in the final build
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
    print(cleanData)
    # Loads cleanData into services
    for i in cleanData:
        if i[0] == "Shop":
            services["Shop"].append({
            "Name": i[1],
            "OpenState": i[2],
            "Hours": parseOpenHoursFormatting(i[3])
            })
        elif i[0] == "Service":
            services["Service"].append({
            "Name": i[1],
            "OpenState": i[2],
            "Hours": parseOpenHoursFormatting(i[3])
            })
        elif i[0] == "Library":
            services["Library"].append({
            "Name": i[1],
            "OpenState": i[2],
            "Hours": parseOpenHoursFormatting(i[3])
            })
        elif i[0] == "Catering":
            if len(i) > 3:
                services["Catering"].append({
                "Name": i[1],
                "OpenState": i[2],
                "Hours": parseOpenHoursFormatting(i[3])
                })
            else:
                services["Catering"].append({
                "Name": i[1],
                "OpenState": i[2],
                "Hours": None
                })
    with open('result.json', 'w') as fp:
        json.dump(services, fp, indent=4)

    return services
'''
# Commented out as on python doesn't like the match-case for somereason :(
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
        '''
'''
    with open('result.json', 'w') as fp:
        json.dump(services, fp, indent=4)

    return services     
'''

# Passes through services[category][name] and returns whether the open state is true or false
def isOpen(services):
    if services["OpenState"] == "We're currently open.":
        return True
    else:
        return False

# Return the hours for a service
def getHours(services, name):
    hours = str(services[sName[name]][sIndex[name]]["Hours"])

    if hours != None:
        hoursString = "Opening Hours:\n" + str(services[sName[name]][sIndex[name]]["Hours"])
    else:
        hoursString = "Opening Hours Unkown"

    return hoursString

# procedure to print whether or not "name" is open or closed
async def printIsOpenOrClosed(msg,name):
            html = await getHtml()
            services = getService(html, tableCol)

            if isOpen(services[sName[name]][sIndex[name]]):
                await msg.send(name +  " is open at the moment!!!")
            else:
                print("Name is: " + name)
                await msg.send(name +  " is closed at the moment :(")

# Scrapes and parses html data from falmouth uni's websites
# and prints whether or not a request service (name) is open
async def getHtml(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            html = await response.text()
            #with open("testfile.txt", "w") as f:  # TEST
            #    f.write(html)
            return html

def isOpenTxt(html):
    if "currently open" in html:
        return True
    return False

async def returnOpen(url):
    html = await getHtml(url)
    return isOpenTxt(html)





#########################################################################################
#####################################     EVENTS     ####################################
#########################################################################################

# roof of concept for listening to commands as another way for working with user msg's

# @client.event
# async def onMessage(msg):
#     if message.author == client.user:
#         return
#     elif message.content.startswith("?"):
#         cmd = message.content.split()[0].replace("_","")
#         if len(message.content.split()) > 1:
#             parameters = message.content.split()[1:]        

#########################################################################################
##################################### COMMAND CALLS #####################################
#########################################################################################
@client.command()
async def koofi(msg):
    url = data.newData["FoodAndDrink"]["Koofi"]
    if await returnOpen(url):
        await msg.send("Koofi" +  " is open at the moment :)")
    else:
        await msg.send("Koofi" + " is closed at the moment :(")

@client.command()
async def koofiOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Koofi")
    await msg.send(message)

# Test on how to call commands from other functions
@client.command()
async def test(ctx):
    command = client.get_command("koofi")
    await ctx.invoke(command)

##########                 ##########
##########     CATERING    ##########
##########                 ##########

# Sends channel msg when procedure the name is called as a command
@client.command()
async def amata(msg):
    print("amata was called")
    await printIsOpenOrClosed(msg,"AMATA Cafe")


@client.command()
async def amataOt(msg):
    print("AmataOt was called")
    html = await getHtml()
    message = getHours(getService(html,tableCol),"AMATA Cafe")
    await msg.send(message)


@client.command()
async def esi(msg):
    await printIsOpenOrClosed(msg,"ESI Cafe")

@client.command()
async def ESIOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"ESI Cafe")
    await msg.send(message)




@client.command()
async def stannaryB(msg):
    await printIsOpenOrClosed(msg,"The Stannary Bar")

@client.command()
async def stannaryBOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"The Stannary Bar")
    await msg.send(message)


@client.command()
async def fox(msg):
    await printIsOpenOrClosed(msg,"Fox Cafe")

@client.command()
async def foxOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Fox Cafe")
    await msg.send(message)


@client.command()
async def lStannary(msg):
    await printIsOpenOrClosed(msg,"Lower Stannary")

@client.command()
async def lStannaryOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Lower Stannary")
    await msg.send(message)


@client.command()
async def stannaryDeli(msg):
    await printIsOpenOrClosed(msg,"Stannary Deli Bar")    

@client.command()
async def stannaryDeliOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Stannary Deli Bar")
    await msg.send(message)


@client.command()
async def susCafe(msg):
    await printIsOpenOrClosed(msg,"The Sustainability Cafe")

@client.command()
async def susCafeOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"The Sustainability Cafe")
    await msg.send(message)


##########                 ##########
##########     SERVICE     ##########
##########                 ##########

@client.command()
async def pshop(msg):
    await printIsOpenOrClosed(msg, "Penryn Campus Shop")

@client.command()
async def pshopOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Penryn Campus Shop")
    await msg.send(message)


@client.command()
async def fshop(msg):
    await printIsOpenOrClosed(msg, "Falmouth Campus Shop")

@client.command()
async def fshopOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Falmouth Campus Shop")
    await msg.send(message)


@client.command()
async def gym(msg):
    await printIsOpenOrClosed(msg,"Penryn Campus Gym")

@client.command()
async def gymOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Penryn Campus Gym")
    await msg.send(message)


@client.command()
async def gamesArea(msg):
    await printIsOpenOrClosed(msg,"Multi Use Games Area")

@client.command()
async def gamesAreaOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Multi Use Games Area")
    await msg.send(message)


@client.command()
async def sportsCentre(msg):
    await printIsOpenOrClosed(msg,"Penryn Sports Centre")

@client.command()
async def sportsCentreOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"penryn Sports Centre")
    await msg.send(message)


@client.command()
async def av(msg):
    await printIsOpenOrClosed(msg,"AV")

@client.command()
async def avOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"AV")
    await msg.send(message)


@client.command()
async def lilWonders(msg):
    await printIsOpenOrClosed(msg,"Little Wonders Nurseries")

@client.command()
async def lilWondersOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Little Wonders Nurseries")
    await msg.send(message)


@client.command()
async def compass(msg):
    await printIsOpenOrClosed(msg,"The Compass")

@client.command()
async def compassOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"The Compass")
    await msg.send(message)


##########                 ##########
##########     LIBRARY     ##########
##########                 ##########

@client.command()
async def fLibrary(msg):
    await printIsOpenOrClosed(msg,"Falmouth Campus Library")

@client.command()
async def fLibraryOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Falmouth Campus Library")
    await msg.send(message)


@client.command()
async def fHelpdesk(msg):
    await printIsOpenOrClosed(msg,"Falmouth Campus Library Helpdesk")

@client.command()
async def fHelpdeskOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Falmouth Campus Library Helpdesk")
    await msg.send(message)


@client.command()
async def pLibrary(msg):
    await printIsOpenOrClosed(msg,"Penryn Campus Library")

@client.command()
async def plibraryOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Penryn Campus Library")
    await msg.send(message)


@client.command()
async def pHelpdesk(msg):
    await printIsOpenOrClosed(msg,"Penryn Campus Library Helpdesk")

@client.command()
async def pHelpdeskOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Penryn Campus Library helpdesk")
    await msg.send(message)


@client.command()
async def vHelpdesk(msg):
    await printIsOpenOrClosed(msg,"Virtual Helpdesk")

@client.command()
async def vHelpdeskOt(msg):
    html = await getHtml()
    message = message = getHours(getService(html,tableCol),"Virtual Helpdesk")
    await msg.send(message)




# Lets you know if the bot is up and running
@client.event
async def on_ready():
    print("bot is ready!")  
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Dreamy Night"))


# Token
client.run(data.newData["keys"]["token"])