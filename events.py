import bs4
import util
import data
import discord

class Events:
    GREEN = 0x2ecc71
    def __innit__(self):
        self.test = []        
    
    async def GetRawData(self):
        html = await util.GetHtml(data.data["SU"]["Events"])
        soup = bs4.BeautifulSoup(html, features="html5lib")
        div = soup.find("div", {"class": "msl_eventlist"})
        with open("eventsHTML", "w") as f:
            f.writelines(div.prettify())
    
    def CleanEventsHTML(self):
        with open("eventsHTML", "r") as f:            
            events = []
            event = {}            
            orgLine = None
            nameLine = None
            timeLine = None
            locationLine = None
            desLine = None            
            
            for i, line in enumerate(f):
                # Add Lines
                if orgLine != None:
                    event["org"] = line.strip()
                    orgLine = None
                if nameLine != None:
                    event["name"] = line.strip()
                    nameLine = None
                if timeLine != None:
                    event["time"] = line.strip()
                    timeLine = None
                if locationLine != None:
                    event["location"] = line.strip()
                    locationLine = None
                if desLine != None:
                    event["description"] = line.strip()
                    desLine = None
                    events.append(event)
                    event = {}
                    
                
                
                # Check if a line should be added
                if "msl_event_organisation" in line:
                    orgLine = i+1
                if "msl_event_name" in line:
                    nameLine = i+1
                if "msl_event_time" in line:
                    timeLine = i+1
                if "msl_event_location" in line:
                    locationLine = i+1
                if "msl_event_description" in line:
                    desLine = i+1            
        return events
                    
                    
                    
                    

    async def GetListOfEvents(self):
        await self.GetRawData()
        events = self.CleanEventsHTML()
        return events
    
    async def GetNumberOfEvents(self, numOfEvents):
        # Gets list of events with each element a dictionary
        events = await self.GetListOfEvents()
        
        if numOfEvents > len(events):
            eventMsg = f"Theres not that many planned events, so heres the next {len(events)} planned"
            numOfEvents = len(events)
        else:
            eventMsg = f"Here are the next {numOfEvents} events"        
        embed = discord.Embed(title=eventMsg, colour=self.GREEN)
        for i in range(0,numOfEvents):
            embed.add_field(
                name = "Event: " + events[i]["name"], 
                value="Organisation: " + events[i]["org"] + "\n" +
                "DateAndTime: " + events[i]["time"] + "\n" +
                "Location: " + events[i]["location"] + "\n" +
                "Description: " + events[i]["description"],
                inline = False)
        return embed
            

        
