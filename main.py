import discord
from discord.ext import commands
import aiohttp
import data
import logging.handlers

# command prefix which us used for every bot command
client = commands.Bot(command_prefix = '?')

# TODO
# Implement a spam logger
# https://stackoverflow.com/questions/64865728/how-to-keep-track-of-messages-sent-in-discord-py


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ServiceData:
    def __init__(self, name, url):
        self.url = url
        self.name = name
        self.openingTimes = []
        self.isServiceOpen = False

    '''
    Inits isServiceOpen
    Args:
        None
    Returns:
        None
    '''
    async def SetOpenData(self):
        self.isServiceOpen = await self.IsOpen()
    '''
    Innits openingtimes and openingtimesformatted
    Args:
        None
    Returns:
        None
    '''
    async def SetOpeningTimeData(self):
        self.openingTimes = await self.FindOpeningTimes()
        self.openingTimesFormatted = await self.ShowOpeningTimes()


    '''
    Gets raw HTML data in string format from given html
    Args:
        String url for website to scrape
    Returns:
        String html 
        None if error occoured 
    '''
    async def GetHtml(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    html = await response.text()
                    return html
        except Exception:
            return None
    '''
    Checks if service is open or closed
    Args:
        String url for website service
    Returns:
        True if open
        False if closed
        None if error occoured 
    '''
    async def IsOpen(self):
        html = await self.GetHtml()
        if html == None:
            return None
        # If the target string is found, then the service must be open, else closed
        if data.data["Util"]["TargetOpen"] in html:
            return True
        return False

    '''
    Finds opening times of the objects services
    Args: 
        None
    Returns:
        List containing string data of opening days and times for the service 
    '''
    async def FindOpeningTimes(self):
        html = await self.GetHtml()

        # Stores times and days
        openingTimesList = []
        # Write html data to a .txt file so its easier to read
        with open("htmlDetail.txt","w") as f:
            for line in html:
                f.writelines(line)

        # Goes through .txt file as loads opening data into a list
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
        openingTimesList = self.CleanOpeningsList(openingTimesList)
        openingTimesList = self.ReorderOpeningsList(openingTimesList)

        return openingTimesList

    '''
    Formats a message to be sent showing opeing times
    Args:
        None
    Returns:
        Formatted string message containing opening days and times 
    '''
    async def ShowOpeningTimes(self):
        msg = self.name + " Opening Times are:\n"
        for i in range(0, len(self.openingTimes)):
            if ':' in self.openingTimes[i]:
                msg = msg + "    "
            msg = msg + self.openingTimes[i]
            msg = msg + "\n"
        return msg

    '''
    Takes a list with expected data and formats the elemeants
    Args:
        List containing strings of days and opening times
    Returns:
        List containing strings of days and opening times
    '''
    def CleanOpeningsList(self, list):
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
    '''
    Puts days above opening times in a expected list
    Args:
        List containing strings of days and opening times
    Returns:
        List containing strings of days and opening times
    '''
    def ReorderOpeningsList(self,list):
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

    '''
    Formats a sendable message saying whether the service is open or not
    Args:
        None
    Returns:
        Formatted string message indicating the service is open or closed
    '''
    def FormatOpenMsg(self):
        if self.isServiceOpen:
            return self.name + " is open at the moment :)"
        else:
            return self.name + " is closed at the moment :("


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


# Test on how to call commands from other functions
@client.command()
async def test(ctx):
    command = client.get_command("koofi")
    await ctx.invoke(command)

##########                  ##########
##########   FoodAndDrink   ##########
##########                  ##########


@client.command(case_insensitive=False)
async def koofi(msg):
    koofi = ServiceData("Koofi", data.data["FoodAndDrink"]["Koofi"])
    await koofi.SetOpenData()
    await msg.channel.send(koofi.FormatOpenMsg())

@client.command()
async def koofiOt(msg):
    koofi = ServiceData("Koofi", data.data["FoodAndDrink"]["Koofi"])
    await koofi.SetOpeningTimeData()
    await msg.channel.send(koofi.openingTimesFormatted)

# Sends channel msg when procedure the name is called as a command
@client.command()
async def amata(msg):
    amata = ServiceData("Amata", data.data["FoodAndDrink"]["Amata"])
    await amata.SetOpenData()
    await msg.channel.send(amata.FormatOpenMsg())

@client.command()
async def amataOt(msg):
    amata = ServiceData("Amata", data.data["FoodAndDrink"]["Amata"])
    await amata.SetopeningTimeData()
    await msg.channel.send(amata.openingTimesFormatted)


@client.command()
async def esi(msg):
    esi = ServiceData("ESI Cafe", data.data["FoodAndDrink"]["ESI"])
    await esi.SetOpenData()
    await msg.channel.send(esi.FormatOpenMsg())

@client.command()
async def esiOt(msg):
    esi = ServiceData("ESI", data.data["FoodAndDrink"]["ESI"])
    await esi.SetOpeningTimeData()
    await msg.channel.send(esi.openingTimesFormatted)


@client.command()
async def stannaryBar(msg):
    stanBar = ServiceData("Stannary Bar", data.data["FoodAndDrink"]["Stannary Bar"])
    await stanBar.SetOpenData()
    await msg.channel.send(stanBar.FormatOpenMsg())

@client.command()
async def stannaryBarOt(msg):
    stanBar = ServiceData("Stannary Bar", data.data["FoodAndDrink"]["Stannary Bar"])
    await stanBar.SetOpeningTimeData()
    await msg.channel.send(stanBar.openingTimesFormatted)

@client.command()
async def stannaryKitchen(msg):
    stannaryKitchen = ServiceData("Stannary Kitchen", data.data["FoodAndDrink"]["Stannary Kitchen"])
    await stannaryKitchen.SetOpenData()
    await msg.channel.send(stannaryKitchen.FormatOpenMsg())

@client.command()
async def stannaryKitchenOt(msg):
    stannaryKitchen = ServiceData("Stannary Kitchen", data.data["FoodAndDrink"]["Stannary Kitchen"])
    await stannaryKitchen.SetOpeningTimeData()
    await msg.channel.send(stannaryKitchen.openingTimesFormatted)

@client.command()
async def fox(msg):
    fox = ServiceData("Fox Cafe", data.data["FoodAndDrink"]["Fox"])
    await fox.SetOpenData()
    await msg.channel.send(fox.FormatOpenMsg())
@client.command()
async def foxOt(msg):
    fox = ServiceData("Fox Cafe", data.data["FoodAndDrink"]["Fox"])
    await fox.SetOpeningTimeData()
    await msg.channel.send(fox.openingTimesFormatted)


@client.command()
async def susCafe(msg):
    susGuy = ServiceData("The Sustainability Cafe", data.data["FoodAndDrink"]["Sus cafe"])
    await susGuy.SetOpenData()
    await msg.channel.send(susGuy.FormatOpenMsg())

@client.command()
async def susCafeOt(msg):
    susGuy = ServiceData("The Sustainability Cafe", data.data["FoodAndDrink"]["Sus cafe"])
    await susGuy.SetOpeningTimeData()
    await msg.channel.send(susGuy.openingTimesFormatted)



@client.command()
async def penrynShop(msg):
    penrynShop = ServiceData("Penryn Campus Shop", data.data["FoodAndDrink"]["Penryn Shop"])
    await penrynShop.SetOpenData()
    await msg.channel.send(penrynShop.FormatOpenMsg())

@client.command()
async def penrynShopOt(msg):
    penrynShop = ServiceData("Penryn Campus Shop", data.data["FoodAndDrink"]["Penryn Shop"])
    await penrynShop.SetOpeningTimeData()
    await msg.channel.send(penrynShop.openingTimesFormatted)

##########                                 ##########
##########     Facilities and Services     ##########
##########                                 ##########

@client.command()
async def falmouthShop(msg):
    falmouthShop = ServiceData("Falmouth Campus Art Shop", data.data["Facilities and Services"]["Falmouth Art Shop"])
    await falmouthShop.SetOpenData()
    await msg.channel.send(falmouthShop.FormatOpenMsg())

@client.command()
async def falmouthShopOt(msg):
    falmouthShop = ServiceData("Falmouth Campus Art Shop", data.data["Facilities and Services"]["Falmouth Art Shop"])
    await falmouthShop.SetOpeningTimeData()
    await msg.channel.send(falmouthShop.openingTimesFormatted)

# Lets you know if the bot is up and running
@client.event
async def on_ready():
    print("bot is ready!")  
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Dreamy Night"))


# Token
client.run(data.botData["keys"]["token"])