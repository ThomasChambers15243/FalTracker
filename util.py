import aiohttp
'''
Gets raw HTML data in string format from given html
Args:
    String url for website to scrape
Returns:
    String html 
    None if error occoured 
'''
async def GetHtml(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                return html
    except Exception:
        return None