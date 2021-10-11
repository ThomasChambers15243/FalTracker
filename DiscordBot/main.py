import discord
from discord.ext import commands
import aiohttp
import asyncio

client = commands.Bot(command_prefix = '?')

async def getWebReqIsOpen(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:                    
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()

            if "We're currently open." in html:
                print("Is open")
                return True
            else:
                print("Is Closed")
                return False
            #if html[i:i+] 

            


# async def isOpenMsg(msg, name):
#     await msg.send("The " + name + " is open at the moment!!!")

# async def isClosedMsg(msg, name):
#     await msg.send("The " + name + " is closed at the moment")


@client.command()
async def stannary(msg):
    url = "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/the-stannary-bar/"
    isOpen = getWebReqIsOpen(url)
    if isOpen:
        await msg.send('The Stannary Bar is open at the moment!!')
        #isOpenMsg(msg, "Stannary")
    else:
        await msg.send("The Stannary Bar is closed at the moment")
        #isClosedMsg(msg, "Stannary")



##this is how you get a command, the fucntion name
##is what needs to come after the command_prefix
@client.command()
async def gym(msg):
    url = "https://fxplus.ac.uk/facilities-shops/sports-facilities/"
    isOpen = getWebReqIsOpen(url)
    if isOpen == True:
        await msg.send('The sports facilities are open at the moment!!')
        #await isOpenMsg(msg,"gym")
    else:
        #await isClosedMsg(msg,"gym")
        await msg.send("The sports facilities are closed at the moment :(")



@client.event
async def on_ready():
    print("bot is ready!")    


#loop = asyncio.get_event_loop()
#loop.run_until_complete(getWebReq())





client.run('ODk3MTk4MDg3NDE0NjIwMTcy.YWSK1Q.1JUA2_tjXY2-bPp7yGT0bsK29sg')    





# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as', self.user)

#     async def on_message(self, message):
#         # don't respond to ourselves
#         if message.author == self.user:
#             return

#         if message.content == 'ping':
#             await message.channel.send('pong')

# client = MyClient()
# client.run('ODk3MTk4MDg3NDE0NjIwMTcy.YWSK1Q.1JUA2_tjXY2-bPp7yGT0bsK29sg')
