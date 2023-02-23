import os
import discord
import aiohttp
import data
import logging.handlers
from os import system
# from pretty_help import PrettyHelp
from discord.ext import commands
from keepAlive import keep_alive
from discord.ext.commands import CommandNotFound

# Global Colour constants
GREEN = 0x2ecc71
RED = 0xe74c3c

# Sets intents so that messages can be sent
intents = discord.Intents.all()

# Gets token from replit secrets
my_secret = os.environ['token']

# Note at the bottom of the help menu
endingNote = "Type ? then the name of a service to find out if its open or not\n Add Ot at the end for opening times.\nYou can also type ?help command for more info on that command\nContact "+ data.botData["botInfo"]["AuthorsDiscord"] +" for bugs and suggestions\nHelp is a bit messy right now but I'll make one my self soon"

# Sets up bot client
client = commands.Bot(intents=intents,command_prefix = '?')
# PrettyHelp(index_title="Commands",active_time=120, delete_after_timeout=True,ending_note=endingNote,sort_commands=True)


# Sets up logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='logs/discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

'''
    Holds all data and methods for services. Obj should be instantiated everytime a command is called.
'''
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
        with open("rawWebData/htmlDetail.txt","w") as f:
            for line in html:
                f.writelines(line)

        # Goes through .txt file as loads opening data into a list
        with open("rawWebData/htmlDetail.txt", "r") as f:
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
    Formats a embed to be sent showing opeing times
    Args:
        None
    Returns:
        Formatted embed message containing opening days and times 
    '''
    async def ShowOpeningTimes(self):
        embed = discord.Embed(title=self.name + " Opening Times Are:", colour=GREEN)     
        for i in range(0, len(self.openingTimes)):
            if not (':' in self.openingTimes[i]):
                embed.add_field(name=self.openingTimes[i],value=(self.openingTimes[i+1] + "\n" + self.openingTimes[i+2]),inline=False)                
        return embed

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
    Formats a sendable embed saying whether the service is open or not
    Args:
        None
    Returns:
        Formatted embed message indicating the service is open or closed
    '''
    def FormatOpenMsg(self):
        if self.isServiceOpen:            
            return discord.Embed(title=self.name, description=self.name + " is open\n:)",colour=GREEN)
        else:
            return discord.Embed(title=self.name, description=self.name + " is closed\n:(",colour=RED)


#########################################################################################
#####################################     EVENTS     ####################################
#########################################################################################

# roof of concept for listening to commands as another way for working with user msg's

@client.event
async def onMessage(msg):
    if msg.author == client.user:
        return
    elif msg.content == "?99":
        await msg.channel.send("Hi")

#########################################################################################
##################################### COMMAND CALLS #####################################
#########################################################################################
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@client.command(
    description = "Shows the service's opening times. For example, \nEnter\"ot koofi\" to get koofi's opening times",
    brief="Shows opening times of service. \"ot serviceName\""
)
async def ot(ctx, arg):
    
    arg = arg.lower()
    # Checks whether the arg value is equal to a service name and then invokes the correct command
    # I can't seem to upgrade replit's python version to 3.10...
    # so im stuck with this, no match-case :(
    if arg == "koofi":
        await ctx.invoke(client.get_command("koofiOt"))
    elif arg == "amata":
        await ctx.invoke(client.get_command("amataOt"))
    elif arg == "esi":
        await ctx.invoke(client.get_command("esiOt"))
    elif arg == "stannarybar":
        await ctx.invoke(client.get_command("stannaryBarOt"))        
    elif arg == "stannarykitchen":
        await ctx.invoke(client.get_command("stannarykitchenOt"))           
    elif arg == "fox":
        await ctx.invoke(client.get_command("foxOt"))       
    elif arg == "suscafe" or arg == "sustainabilitycafe":
        await ctx.invoke(client.get_command("susCafeOt"))     
    elif arg == "penryn" or arg == "penrynshop" or arg == "penryncampusshop":
        await ctx.invoke(client.get_command("penrynShopOt"))       
    elif arg == "falmouth" or arg == "falmouthshop" or arg == "falmouthcampusshop" or arg == "falmouthartshop" or arg == "falmouthcampusartshop":
        await ctx.invoke(client.get_command("falmouthShopOt"))
    else:
        embed = discord.Embed(title="Unknown argument", description="Only send one place as one word\nSuch as: \nstannarybar\nFalmouthArtShop", colour=RED)        
        await ctx.channel.send(embed=embed)

    
##########                  ##########
##########   FoodAndDrink   ##########
##########                  ##########


@client.command(
    name="koofi",
    aliases=["Koofi", "KOOFI"],
    description="Shows whether Koofi is open or not",
    brief="Shows whether Koofi is open or not")
async def koofi(msg):
    koofi = ServiceData("Koofi", data.data["FoodAndDrink"]["Koofi"])
    await koofi.SetOpenData()
    await msg.channel.send(embed=koofi.FormatOpenMsg())

@client.command(
    name="koofiOt", 
    aliases=["koofiot", "koofOT", "KOOFOT"],
    description="Shows the opening times for koofi",
    brief="Shows the opening times for koofi")                
async def koofiOt(msg):
    koofi = ServiceData("Koofi", data.data["FoodAndDrink"]["Koofi"])
    await koofi.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=koofi.openingTimesFormatted)

@client.command(
    name="amata", 
    aliases=["Amata", "AMATA", "academyofmusicandtheatrearts", "AcademyOfMusicAndTheatreArts"],
    description="Shows whether or not Amata Cafe is open",
    brief="Shows whether or not Amata Cafe is open")
async def amata(msg):
    amata = ServiceData("Amata Cafe", data.data["FoodAndDrink"]["Amata"])
    await amata.SetOpenData()
    await msg.channel.send(embed=amata.FormatOpenMsg())

@client.command(
    name="amataOt", 
    aliases=["amataot","amataOT","AMATAOT"],
    description="Shows the opening times for Amata Cafe",
    brief="Shows the opening times for Amata Cafe")
async def amataOt(msg):
    amata = ServiceData("Amata", data.data["FoodAndDrink"]["Amata"])
    await amata.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=amata.openingTimesFormatted)


@client.command(
    name="esi", 
    aliases=["ESI","esicafe","esiCafe","ESICAFE", "environment and sustainability institute"],
    description="Shows whether or not the esiCafe is open",
    brief="Shows whether or not esiCafe is open")    
async def esi(msg):
    esi = ServiceData("ESI Cafe", data.data["FoodAndDrink"]["ESI"])
    await esi.SetOpenData()
    await msg.channel.send(embed=esi.FormatOpenMsg())

@client.command(
    name="esiOt",
    aliases=["esiot","esiOT","ESIOT"],
    description="Shows the opening times for esiCafe",
    brief="Shows the opening times for esiCafe")
async def esiOt(msg):
    esi = ServiceData("ESI", data.data["FoodAndDrink"]["ESI"])
    await esi.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=esi.openingTimesFormatted)


@client.command(
    name="stannaryBar", 
    aliases=["stannarybar","stannaryBAR","STANNARYBAR","stanBar"],
    description="Shows whether or not the Stannary Bar is open",
    brief="Shows whether or not the Stannary Bar is open")    
async def stannaryBar(msg):
    stanBar = ServiceData("Stannary Bar", data.data["FoodAndDrink"]["Stannary Bar"])
    await stanBar.SetOpenData()
    await msg.channel.send(embed=stanBar.FormatOpenMsg())

@client.command(
    name="stannaryBarOt", 
    aliases=["stannarybarot","stannaryBarOT","stannaryBAROT","STANNARYBAROT","barOt","BAROT","barOT"],
    description="Shows the opening times for the Stannary Bar",
    brief="Shows the opening times for the Stannary Bar")    
async def stannaryBarOt(msg):
    stanBar = ServiceData("Stannary Bar", data.data["FoodAndDrink"]["Stannary Bar"])
    await stanBar.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=stanBar.openingTimesFormatted)

@client.command(
    name="stannaryKitchen", 
    aliases=["stannarykitchen","stannaryKITCHEN","STANNARYKITCHEN","stankitchen"],
    description="Shows whether or not the Stannary Kitchen is open",
    brief="Shows whether or not the Stannary Kitchen is open")    
async def stannaryKitchen(msg):
    stannaryKitchen = ServiceData("Stannary Kitchen", data.data["FoodAndDrink"]["Stannary Kitchen"])
    await stannaryKitchen.SetOpenData()
    await msg.channel.send(embed=stannaryKitchen.FormatOpenMsg())

@client.command(
    name="stannaryKitchenOt", 
    aliases=["stannarykitchenot","stannaryKitchenOT","stannaryKITCHENOT","STANNARYKITCHENOT","kitchenOt","kitchenOT"],
    description="Shows the opening times for the Stannary Kitchen",
    brief="Shows the opening times for the Stannary Kitchen")    
async def stannaryKitchenOt(msg):
    stannaryKitchen = ServiceData("Stannary Kitchen", data.data["FoodAndDrink"]["Stannary Kitchen"])
    await stannaryKitchen.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=stannaryKitchen.openingTimesFormatted)

@client.command(
    name="fox", 
    aliases=["foxCafe","foxCAFE","FOXCAFE"],
    description="Shows whether or not the Fox Cafe is open",
    brief="Shows whether or not Fox Cafe is open")    
async def fox(msg):
    fox = ServiceData("Fox Cafe", data.data["FoodAndDrink"]["Fox"])
    await fox.SetOpenData()
    await msg.channel.send(embed=fox.FormatOpenMsg())
    
@client.command(
    name="foxOt", 
    aliases=["foxot","foxOT","FOXOT", "foxCafeOT", "foxcafeot","FOXCAFEOT"],
    description="Shows the opening times for Fox Cafe",
    brief="Shows the opening times for the Fox Cafe")    
async def foxOt(msg):
    fox = ServiceData("Fox Cafe", data.data["FoodAndDrink"]["Fox"])
    await fox.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=fox.openingTimesFormatted)


@client.command(
    name="susCafe",
    aliases=["suscafe","susCAFE","SUSCAFE","sus","susGuy","jerma985"],
    description="Shows whd(her or not the Sustainability Cafe is open",
    brief="Shows whether or not the Sustainability Cafe is open")    
async def susCafe(msg):
    susGuy = ServiceData("The Sustainability Cafe", data.data["FoodAndDrink"]["Sus cafe"])
    await susGuy.SetOpenData()
    await msg.channel.send(embed=susGuy.FormatOpenMsg())

@client.command(
    name="susCafeOt", 
    aliases=["suscafeot","susCafeOT","susCAFEOT","SUSCAFEOT","susOt","susOT","SUSOT"],
    description="Shows the opening times for the Sustainability Cafe",
    brief="Shows the opening times for the Sustainability Cafe")    
async def susCafeOt(msg):
    susGuy = ServiceData("The Sustainability Cafe", data.data["FoodAndDrink"]["Sus cafe"])
    await susGuy.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=susGuy.openingTimesFormatted)

@client.command(
    name="penrynShop",
    aliases=["penrynshop","penrynSHOP","PENRYNSHOP","shop","SHOP"],
    description="Shows whether or not Penryn Campus Shop is open",
    brief="Shows whether or not Penryn Campus Shop is open")    
async def penrynShop(msg):
    penrynShop = ServiceData("Penryn Campus Shop", data.data["FoodAndDrink"]["Penryn Shop"])
    await penrynShop.SetOpenData()
    await msg.channel.send(embed=penrynShop.FormatOpenMsg())

@client.command(
    name="penrynShopOt",
    aliases=["penrynshopOT","penrynSHOPOT","PENRYNSHOPOT","shopOt","shopot","shopOT","SHOPOT"],
    description="Shows the opening times for Penryn Campus Shop",
    brief="Shows the opening times for Penryn Campus Shop")    
async def penrynShopOt(msg):
    penrynShop = ServiceData("Penryn Campus Shop", data.data["FoodAndDrink"]["Penryn Shop"])
    await penrynShop.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=penrynShop.openingTimesFormatted)

##########                                 ##########
##########     Facilities and Services     ##########
##########                                 ##########

@client.command(
    name="falmouthShop",
    aliases=["falmouthshop","falmouthSHOP","FALMOUTHSHOP","fal","FAL"],
    description="Shows whether or not Falmouth Campus Art Shop is open",
    brief="Shows whether or not Falmouth Campus Art Shop is open")    
async def falmouthShop(msg):
    falmouthShop = ServiceData("Falmouth Campus Art Shop", data.data["Facilities and Services"]["Falmouth Art Shop"])
    await falmouthShop.SetOpenData()
    await msg.channel.send(embed=falmouthShop.FormatOpenMsg())

@client.command(
    name="falmouthShopOt",
    aliases=["falmouthshopot","falmouthshopOt","falmouthshopOT","falmouthSHOPOT","FALMOUTHSHOPOT","falot","falOt","FALOT"],
    description="Shows the opening times for Falmouth Campus Art Shop",
    brief="Falmouth Campus Art Shop")    
async def falmouthShopOt(msg):
    falmouthShop = ServiceData("Falmouth Campus Art Shop", data.data["Facilities and Services"]["Falmouth Art Shop"])
    await falmouthShop.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=falmouthShop.openingTimesFormatted)

@client.command(
    name="gym",
    aliases=["GYM","Gym"],
    description="Shows whether or not Penryn Campus Gym is open or not",
    brief="Shows whether or not Penryn Campus Gym is open or not")
async def flexsiSportsCentre(msg):
    gym = ServiceData("Flexsi Gym", data.data["Facilities and Services"]["Flexsi Sports Centre"])
    await gym.SetOpenData()
    await msg.channel.send(embed=gym.FormatOpenMsg())

@client.command(
    name="gymOt",
    aliases=["gymot","GYMOT","GymOt","gymOT","GYMot"],
    description="Shows the opening times for Penryn Campus Gym",
    brief="Shows the opening times for Penryn Campus Gym")
async def flexsiSportsCentreOt(msg):
    gym = ServiceData("Flexsi Gym", data.data["Facilities and Services"]["Flexsi Sports Centre"])
    await gym.SetOpeningTimeData()
    await msg.channel.send(content=None, embed=gym.openingTimesFormatted)

# Lets you know if the bot is up and running
@client.event
async def on_ready():
    print("bot is ready!")  
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Dreamy Night"))


keep_alive()
# Token
#client.run(my_secret)
try:
    client.run(my_secret)
# if the error is too many requests, kill the bot and run it form another ip
except discord.errors.HTTPException as e:
    print()
    system("kill 1")
    client.run(my_secret)