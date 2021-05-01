
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



