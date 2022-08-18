import discord
from discord.ext import commands
import aiohttp
import data

# command prefix which us used for every bot command
client = commands.Bot(command_prefix = '?')

# TODO
# Implement a spam logger
# https://stackoverflow.com/questions/64865728/how-to-keep-track-of-messages-sent-in-discord-py



class ServiceData:
    def __init__(self, name, url):
        self.url = url
        self.name = name
        self.openingTimes = [] #await findOpeningTimes()
        self.isServiceOpen = False # await isOpen()
    async def SetData(self):
        self.openingTimes = await self.findOpeningTimes()
        self.openingTimesFormatted = await self.showOpeningTimes()
        self.isServiceOpen = await self.isOpen()
    '''
    Gets raw HTML data in string format from given html
    
    Args:
        String url for website to scrape
        
    Returns:
        String html 
        None if error occoured 
    '''
    async def getHtml(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    html = await response.text()
                    return html
        except Exception:
            return None

    async def findOpeningTimes(self):
        html = await self.getHtml()
        # Stores times and days
        openingTimesList = []
        with open("htmlDetail.txt","w") as f:
            for line in html:
                f.writelines(line)
        with open("htmlDetail.txt", "r") as f:
            # Get line up to the start of opening times
            for line in f:
                if "openingHoursSpecification" in line:
                    break
            # Load opeing times into list
            for line in f:
                # If at the end of the opening section, shown by ']', then break, else append
                if line.strip() == "]":
                    break
                # Filter out not needed lines
                if not ( "@" in line.strip() or '}' in line.strip() or '{' in line.strip()):
                    openingTimesList.append(line.strip())

        # Cleans List
        openingTimesList = self.cleanOpeningsList(openingTimesList)
        openingTimesList = self.reorderOpeningsList(openingTimesList)
        print(openingTimesList)
        return openingTimesList

    # Remove " and extra text from days
    def cleanOpeningsList(self, list):
        for i in range(0, len(list)):
            # Clean day
            if "dayOfWeek" in list[i]:
                list[i] = list[i][32:-1]
            else:
                # Remove " from times and add a space before :
                list[i] = list[i].replace('"', '')
                list[i] = list[i].replace(":", " : ")
                list[i] = list[i].title()
        return list
    # Reorders the list so that days are shown before times
    def reorderOpeningsList(self,list):
        for i in range(0, len(list)):
            # Only start swaps on days, not times
            if not ':' in list[i]:
                # swap date and open time
                temp = list[i-2]
                list[i-2] = list[i]
                list[i] = temp
                # swamp open and close time
                temp = list[i-1]
                list[i-1] = list[i]
                list[i] = temp
        return list
    async def showOpeningTimes(self):
        msg = self.name + " Opening Times are:\n"
        for i in range(0, len(self.openingTimes)):
            if ':' in self.openingTimes[i]:
                msg = msg + "    "
            msg = msg + self.openingTimes[i]
            msg = msg + "\n"
        return msg


    '''
    Checks if service is open or closed
    
    Args:
        String url for website service
        
    Returns:
        True if open
        False if closed
        None if error occoured 
    '''
    async def isOpen(self):
        html = await self.getHtml()

        if html == None:
            return None

        if data.data["Util"]["TargetOpen"] in html:
            return True

        return False

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

    koofiData = ServiceData("Koofi", data.data["FoodAndDrink"]["Koofi"])
    await koofiData.SetData()

    if koofiData.isServiceOpen:
        await msg.send("Koofi" + " is open at the moment :)")
    else:
        await msg.send("Koofi" + " is closed at the moment :(")
    '''
    if await isOpen(url):
        await msg.send("Koofi" +  " is open at the moment :)")
    else:
        await msg.send("Koofi" + " is closed at the moment :(")
    await findOpeningTimes(url)
    '''

@client.command()
async def koofiOt(msg):
    url = data.data["FoodAndDrink"]["Koofi"]
    koofiData = ServiceData("Koofi", data.data["FoodAndDrink"]["Koofi"])
    await koofiData.SetData()
    mes = await koofiData.showOpeningTimes()
    print(mes)
    await msg.send(mes)



# Test on how to call commands from other functions
@client.command()
async def test(ctx):
    command = client.get_command("koofi")
    await ctx.invoke(command)

##########                 ##########
##########     CATERING    ##########
##########                 ##########
'''
# Sends channel msg when procedure the name is called as a command
@client.command()
async def amata(msg):


@client.command()
async def amataOt(msg):
    html = await getHtml()


@client.command()
async def esi(msg):

@client.command()
async def ESIOt(msg):
    html = await getHtml()




@client.command()
async def stannaryB(msg):

@client.command()
async def stannaryBOt(msg):
    html = await getHtml()

@client.command()
async def fox(msg):

@client.command()
async def foxOt(msg):
    html = await getHtml()


@client.command()
async def lStannary(msg):

@client.command()
async def lStannaryOt(msg):
    html = await getHtml()


@client.command()
async def stannaryDeli(msg):

@client.command()
async def stannaryDeliOt(msg):
    html = await getHtml()


@client.command()
async def susCafe(msg):
@client.command()
async def susCafeOt(msg):
    html = await getHtml()


##########                 ##########
##########     SERVICE     ##########
##########                 ##########

@client.command()
async def pshop(msg):

@client.command()
async def pshopOt(msg):
    html = await getHtml()


@client.command()
async def fshop(msg):

@client.command()
async def fshopOt(msg):
    html = await getHtml()


@client.command()
async def gym(msg):
    
@client.command()
async def gymOt(msg):
    html = await getHtml()


@client.command()
async def gamesArea(msg):

@client.command()
async def gamesAreaOt(msg):
    html = await getHtml()


@client.command()
async def sportsCentre(msg):

@client.command()
async def sportsCentreOt(msg):
    html = await getHtml()

@client.command()
async def av(msg):

@client.command()
async def avOt(msg):
    html = await getHtml()

@client.command()
async def lilWonders(msg):

@client.command()
async def lilWondersOt(msg):
    html = await getHtml()

@client.command()
async def compass(msg):

@client.command()
async def compassOt(msg):
    html = await getHtml()

##########                 ##########
##########     LIBRARY     ##########
##########                 ##########

@client.command()
async def fLibrary(msg):

@client.command()
async def fLibraryOt(msg):
    html = await getHtml()

@client.command()
async def fHelpdesk(msg):

@client.command()
async def fHelpdeskOt(msg):
    html = await getHtml()


@client.command()
async def pLibrary(msg):

@client.command()
async def plibraryOt(msg):
    html = await getHtml()

@client.command()
async def pHelpdesk(msg):

@client.command()
async def pHelpdeskOt(msg):
    html = await getHtml()

@client.command()
async def vHelpdesk(msg):

@client.command()
async def vHelpdeskOt(msg):
    html = await getHtml()



'''
# Lets you know if the bot is up and running
@client.event
async def on_ready():
    print("bot is ready!")  
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Dreamy Night"))


# Token
client.run(data.data["keys"]["token"])