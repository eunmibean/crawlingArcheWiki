import requests
from bs4 import BeautifulSoup

def getItems(link):
    header = {'User-agent' : 'Mozila/2.0'}
    response = requests.get(link, headers=header)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('#container-common > div > div > article > section > div.doc > ul:nth-child(3)')
    flag = False
    for item in items: 
        for ul in item.findAll('ul'):
            if '재료' in str(ul.text):    
                flag = True
                ings = ul
                break
    
    if flag == True:
        for ing in ings:  
            for i in ing: 
                # del 태그는 더이상 필요하지 않으니깐 패스
                if i.name == 'del':
                    continue
                
                # 재료라는 이름은 필요없으니깐 패스
                if '재료' in str(i.text):
                    continue

                # 아이템에 링크가 있다면 들어가서 최종 아이템인지 확인해야함  
                if i.name == 'a':
                    link = i.attrs['href']
                    getItems(link)
                
                print(i.text.replace(",",""))


keyword = "%EB%81%88%EC%A0%81%EC%9E%84%20%EC%97%86%EB%8A%94%20%EC%97%B0%EB%A7%88%EC%A0%9C" #끈적임없는 연마제
#keyword = "거친%20입자의%20연마제" 
url = f"https://archeage.xlgames.com/wikis/{keyword}"
getItems(url)

