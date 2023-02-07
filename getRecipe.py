import requests
from bs4 import BeautifulSoup
from dbconnect import dbConnect

import json

db = dbConnect()
dict = {}


def giveFinalRecipe(keyword):
    url = f"https://archeage.xlgames.com/wikis/{keyword}"
    # db.createTable()
    code = checkItem(url,keyword)

    finalRecipe = {}
    finalRecipe = getFinal(code)
    return finalRecipe



def getItems(link, code):
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
        recipe = {}
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
                    checkItem(link, i.text)
                
                food = i.text.replace(",","")
                if hasNumber(food):
                    count = food.replace("개","")
                    recipe[prevFood] = int(count)
                    #insertData
                    db.insertRecipe(code, prevFood, count)

                elif food.strip() == "" :
                    continue
                else :
                    prevFood = food
        return recipe
    return None
                
def hasNumber(inputString):
    return any(char.isdigit() for char in inputString)

# def checkItems(url, code):
#     if dict.get(code) == None:
#         dict[code] = getItems(url, code)

def checkItem(url, name):
    code = db.getItemCode(name)
    if code == None:
        db.insertItemName(name)
        code = db.getItemCode(name)
        dict[code] = getItems(url, code[0])
    #else : 
     #   code = code[0]
    
    return code[0]

def checkItemCode(name):
    code = db.getItemCode(name)
    if code != None:
        return code[0]
    return None

    
def getFinalRecipe(name, recipe = {}):
   # if name not in dict.keys():
    #    return None

    for key in dict[name].keys():
        if dict[key] == None: 
            count = dict[name][key]
            if recipe.get(key) != None:
                count = count + recipe.get(key)
            recipe[key] = count
        else :
            recipe = getFinalRecipe(key, recipe)
    
    return recipe

def getFinal(code, finalRecipe = {}):
    list = db.getRecipe(code)
    for i in list: 
        code = checkItemCode(i[0])
        recipe = db.getRecipe(code)
        if not recipe:
            if finalRecipe.get(i[0]) is None: 
                finalRecipe[i[0]] = i[1]
            else : 
                finalRecipe[i[0]] = finalRecipe.get(i[0]) + i[1]
        else : 
            finalRecipe = getFinal(code, finalRecipe)
    
    return finalRecipe
    

            
 

#keyword = "%EB%81%88%EC%A0%81%EC%9E%84%20%EC%97%86%EB%8A%94%20%EC%97%B0%EB%A7%88%EC%A0%9C" #끈적임없는 연마제
#keyword = "끈적임%20없는%20연마제"
#keyword = "거친%20입자의%20연마제" 
#keyword = "로즈마리"
# keyword = "불투명한%20연마제"
# url = f"https://archeage.xlgames.com/wikis/{keyword}"
# db.createTable()

# code = checkItem(url,keyword)

# finalRecipe = {}
# finalRecipe = getFinal(code)
# print(finalRecipe)

