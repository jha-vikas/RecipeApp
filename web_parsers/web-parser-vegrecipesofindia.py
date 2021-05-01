import numpy as np
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import re
from typing import List
from collections import defaultdict



def details_parser(url: str) -> List:
    #url = "https://www.vegrecipesofindia.com/pav-bhaji-recipe-mumbai-pav-bhaji-a-fastfood-recipe-from-mumbai/"

    browser = Browser('firefox', headless=True)

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    recipe_ingredients_detail = soup.find_all('li', attrs={'class': 'wprm-recipe-ingredient'})
    ingredients_list = []

    #replacement_dict = defaultdict(str)

    for ingredients in recipe_ingredients_detail:
        ingredients1 = re.sub(r"[^a-zA-Z ]", "",ingredients.text).strip()
        ingredients_list.append(ingredients1)


    recipe_instructions_detail  = soup.find_all('li', attrs={'class': 'wprm-recipe-instruction'})
    instructions_list  = []

    #replacement_dict = defaultdict(str)

    for instruction  in recipe_instructions_detail:
        instruction1 = re.sub(r"[^a-zA-Z ]", "",instruction.text).strip()
        instructions_list.append(instruction1)

    # Extract Image
    try:
        image_url = soup.find("img", class_ = "aligncenter wp-post-image")['src']
    except:
        image_url = None
    #post_content = soup.find("div", attrs={"class": "aligncenter wp-post-image"}).find_all_next("img")
    """
    pic_links = []
    for link in soup.find_all('img'):  #Cycle through all 'img' tags
        imgSrc = link.get('src')   #Extract the 'src' from those tags
        pic_links.append(imgSrc)    #Append the source to 'links'

    pic_links = list(filter(None, pic_links))
    """
    header = soup.find("h1").text
    header = re.sub(r"[^a-zA-Z ]", "",header).strip()
    browser.quit()
    return ingredients_list, instructions_list, image_url, header



def website_links_parser(url: str = "https://www.vegrecipesofindia.com/recipes", main_web_level=0) -> List[str]:
    #url = "https://www.vegrecipesofindia.com/recipes"
    browser = Browser('firefox', headless=True)

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')



    links = []

    for i in soup.find_all('a'):
        links.append(i.get('href'))

    links = pd.Series(links)
    links.drop_duplicates(inplace=True)

    links = links[~links.isna()]
    links = links[~links.str.contains(r"privacy-policy|press-media|terms-and-conditions|install-website-app|glossary|accessibility")]

    

    if main_web_level == 0:
        my_dict = {}
        all_recipe_links = []
        links = links[links.str.contains(r"/recipes/.+")]
        links = links[links.str.contains(r".com/.+")]
        #return list(links)

        print("Parsing Links")
        for link in links:
            all_recipe_links.extend(website_links_parser(url=link, main_web_level=1))
    
        all_recipe_links = list(set(all_recipe_links))
        
        #return all_recipe_links

        print("Parsing Recipes")
        for link in all_recipe_links:
            print(link)
            try:
                ingredients, instructions, image, recipe_name = details_parser(link)
            except:
                continue
            my_dict[recipe_name] = []
            my_dict[recipe_name].append(link)
            my_dict[recipe_name].append(ingredients)
            my_dict[recipe_name].append(instructions)
        
            if image:
                my_dict[recipe_name].append(image)
            else:
                print("Image not found!")

            print(my_dict[recipe_name])
        browser.quit()
        return my_dict


    elif main_web_level == 1:
        print(f"Super Link {url}")
        links = links[~links.str.contains(r"/recipes/.+")]
        links = links[links.str.contains(r"-")]
        links = links[links.str.contains(r".com/.+")]
        browser.quit()
        return list(links)


ind_recipes = website_links_parser()
df = pd.DataFrame(ind_recipes.values(), index=ind_recipes.keys(), columns=['Link', 'Ingredients', 'Instructions', "Image"])

df.to_csv("ind_recipes.csv", index=True)

