from django.shortcuts import render
import requests
import re
import json
from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp
from fake_useragent import UserAgent

data_kina = []
countFilm = 11
startNext = 1
ganreShow = []
# list_top = []
def index(request):


    global ganre
    
    data_to_htlm = {"data": data_kina,
                    "ganreShow": ganreShow
                    
    }
    if request.POST.get("next"):
        global startNext
        startNext = startNext + 11
        global countFilm
        countFilm = countFilm + 11
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(gather_data())

    if request.POST.get("start"):
        data_kina.clear()
        ganreShow.clear()
        answer = list(request.POST.items())
        ganr = answer[1:]
        print(ganr)
        ganre = []
        for i in ganr:
            ganre.append(i[0])
        ganre = str(ganre).translate({ord(i): None for i in "][ ''"})[6:]

        ganreShow.append(ganre)
        
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(gather_data())
        
        


    return render(request,'kino/index.html', context=data_to_htlm)

async def gather_data():
    tasks = []
    for i in range(startNext, countFilm, 1):
        url = f'https://www.imdb.com/search/title/?genres={ganre}&sort=num_votes,desc&explore=title_type&start={i}'

        task = asyncio.create_task(get_page_data(url))
        # await asyncio.sleep(randint(0,1))
        tasks.append(task)
        
        
    await asyncio.gather(*tasks)

async def get_page_data(url):
    ua = UserAgent()
    headers = {'User-Agent':str(ua.random)}
    async with aiohttp.ClientSession(trust_env=True) as session:
        # await asyncio.sleep(randint(0,1))
        q = await session.get(url, headers = headers)
        soup = BeautifulSoup(await q.text(), "lxml")
        
        try:
            nazFilm = soup.find(class_="lister-item-header").find('a').text
            href = 'https://www.imdb.com' + soup.find(class_="lister-item-header").find('a')['href']
            imdb = soup.find(class_="ratings-bar").find('strong').text
            pic = soup.find(class_="loadlate")
            pic_href_small = pic['loadlate']
            pic_href =(pic_href_small.split("."))
            pic_href = pic_href[:3]
            pic_href_add = "._V1_QL75_UX190_CR0,2,190,281_.jpg"
            pic_href = (" ".join(pic_href).replace(" ", "."))+pic_href_add
            all_ganre = soup.find(class_="genre").text
            all_ganre = re.sub(r"[ \n]", "", all_ganre)
            all_ganre = all_ganre.split(",")
            all_ganre = str(all_ganre).translate({ord(i): None for i in "][ ''"})
        except:
            nazFilm = "чтото пошло не так"

        try:
            data = {
            'href': href,
            'nazFilm': nazFilm,
            'pic_href': pic_href,
            'imdb': imdb,
            # 'prosmotr': prosmotr,
            # 'year': year,
            'ganre': all_ganre,

            }
            
            
        except:
            data = {
            'href': "",
            'nazFilm': '',
            
            'imdb': 'Нет',
            # 'prosmotr': prosmotr,
            # 'year': year,
            'ganre': 'Нет',
            }
        data_kina.append(data)        
        
        # lenD.append(len(data_kina))
        # print(lenD)




        

    

