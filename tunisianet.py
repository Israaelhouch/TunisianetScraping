
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import pandas as pd
import json

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")


def json_file(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
def csv_file(data,filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index= False)

def scraping():
    names=[]
    references=[]
    prices =[]
    descriptions = []
    images = []
    disponibilities = []
    fiche_tech={"Système d'exploitation":[],"Processeur":[], "Réf processeur":[], "Mémoire":[], "Disque Dur":[],"Carte Graphique":[] ,"Réf Carte graphique":[],"Taille Ecran":[], "Type Ecran":[], "Ecran Tactile":[], "Lecteurs/Graveurs":[], "Réseau":[], "Caméra":[],"Garantie":[],"Taux de Rafraîchissement":[]}
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.tunisianet.com.tn/301-pc-portable-tunisie")

    categories = {"https://www.tunisianet.com.tn/301-pc-portable-tunisie":29,  "https://www.tunisianet.com.tn/681-pc-portable-gamer":8, "https://www.tunisianet.com.tn/703-pc-portable-pro":9}
    
    for key, value in categories.items():
        print("category: ", key)
        driver.get(key)
        i=1
        while i<=value:
            print(f"Page {i} is opened")
            j=1

            links = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-title")))
            print(f"Found {len(links)} product links!")

            product_urls = [link.find_element(By.TAG_NAME, "a").get_attribute("href") for link in links]

            for url in product_urls:
                driver.get(url)

                #time.sleep(1)
                
                name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "h1"))).text
                names.append(name[0: name.find("/")-1]) 
                print("j=",j)
                
                reference =  driver.find_element(By.CLASS_NAME, "product-reference").text   
                references.append(reference[reference.find(":")+2:]) 
                
                price = driver.find_element(By.CLASS_NAME, "product-prices").text
                prices.append(price[:price.find(" ") ])
                
                description = driver.find_element(By.CLASS_NAME, "prodes").text
                descriptions.append(description)
                
                image = driver.find_element(By.XPATH, "//*[@id='webizoom']/ul/li[1]/a/img").get_attribute("src")
                images.append(image)

                
                try:
                    dispo = driver.find_element(By.CLASS_NAME, "in-stock").text
                    disponibilities.append(dispo)
                except Exception as e:
                    disponibilities.append("Sur commande")

                            
                details_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "tab2")))
                details_button.send_keys(Keys.RETURN)

                name_elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "name")))
                value_elements =  WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "value")))

                name_list = [element.text for element in name_elements]
                value_list = [element.text for element in value_elements]

                for key in fiche_tech.keys():
                    
                    if key in name_list:
                        fiche_tech[key].append(value_list[name_list.index(key)])
                    else:
                        fiche_tech[key].append("")
            
                j+=1
                driver.back()
            i+=1

            if i == value+1:
                break
            next_button = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='next js-search-link']")))

            next_button.click()
            WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CSS_SELECTOR, ".product-title")))

            time.sleep(2)
    data={"names": names, 'references': references, 'prices': prices, 'descriptions':descriptions, 'disponibilities':disponibilities}
    data.update(fiche_tech)
    return(data)
    
    


if __name__ == '__main__':
    data = scraping()
    csv_file(data,'Tunisianet.csv')
    json_file(data, "Tunisianet.json")
    
    
    
    
