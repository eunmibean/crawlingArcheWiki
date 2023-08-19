from dbconnect_mysql import dbConnect

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

db = dbConnect()
# db.createTable()
dict = {}
recipe = {}

chrome_driver_path = "/opt/homebrew/bin/chromedriver"
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)


def retrieve_recipe(keyword):
    url = f"https://archeage.xlgames.com/wikis/{keyword}"
    recipe = {}
    # db에 데이터가 있는지 먼저 확인
    code = db.get_item_code(keyword)
    if code is None : # db에 없으면
        recipe = search(url, recipe)
        if recipe is None or len(recipe) == 0 : # 없는 데이터이면 
            return None
        else : 
            insert_new_recipe_to_db(keyword,recipe)        
    else : 
        recipe = db.get_recipe(code[0])

    
    return recipe

def insert_new_recipe_to_db(keyword="", recipe={}):
    db.insert_item_name(keyword) 
    code = db.get_item_code(keyword)
    for key, value in recipe.items():        
        db.insert_recipe(code[0], key, value)

## Selenium
def search(url, recipe={}):
    driver.get(url)
    time.sleep(1)

    prefix = "mat-inner"
    div_elements = len(driver.find_elements(By.XPATH,f"//div[starts-with(@class, '{prefix}')]"))
    if not div_elements:
        return None
    else : 
        for index in range(div_elements):

            element = driver.find_elements(By.XPATH,f"//div[starts-with(@class, '{prefix}')]")[index]
            item = element.text.split('x'); 
            a_tag = element.find_element(By.TAG_NAME, 'a')
            href_value = a_tag.get_attribute("href")
            # 하위 아이템이 더 있는지 확인             
            result = search(href_value, recipe)
            
            if result is None: 
                food = item[0]
                cnt = item[1]
                if recipe.get(food) is None: 
                    recipe[food] = int(cnt)
                else :
                    recipe[food] = recipe[food] + int(cnt)
            driver.back()
            time.sleep(1)
    return recipe