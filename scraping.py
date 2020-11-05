from selenium import webdriver
from selenium.webdriver.common.by import By


import pandas as pd
import time
import requests
from datetime import date, timedelta

class SeleniumTwitter:
    def __init__(self):
        self.driver  = webdriver.Chrome()
        self.url = "https://twitter.com/search?lang=pt&q=open.spotify.com%20(%23NowPlaying)%20until%3A{}%20since%3A{}&src=typed_query"

    def save_txt(self, urls):
        print("=========== SPOTIFY URL ===============")
        name = 'data/data.txt'
        f=open(name,'w')
        s1='\n'.join(urls)
        f.write(s1)
        f.close()

    def create_csv(self, since, until, i, urls):
        csv_list = []
        cont = 1

        for url in urls:
            print(cont, "- PROCESSANDO URLS")

            try:

                spotify_url = requests.get(url).url

            except:
                continue

            print(spotify_url)
            csv_list.append({"SINCE_DATE": since, "UNITIL_DATE": until, "SPOTIFY_URL": spotify_url})
            cont+=1
            
        df = pd.DataFrame(csv_list)
        df.to_csv("data/data_" + str(i+1) + ".csv", index=False)


    def get_spotify_urls(self):

        scroll_time = 0.5

        i = 6
        urls = []
        for j in range(1, 31):
            since_search = date(2020, i, j)
            until_search = since_search + timedelta(days=1)

            since_str = since_search.isoformat()
            until_str = until_search.isoformat()
            
            query_url = self.url.format(until_str, since_str)
            self.driver.get(query_url)
            time.sleep(6)

            while(True):
                
                elements = self.driver.find_elements(By.XPATH,"//span[text()='Algo deu errado.']")
                if elements:
                    break
                
                try:
                    elements = self.driver.find_elements(By.XPATH,"//div[@class='css-1dbjc4n r-1omma8c']")
                    if elements:
                        break
                except:
                    continue

                elements = self.driver.find_elements(By.XPATH,"//div[@class='css-1dbjc4n r-156q2ks']/div/div/a")

                for option in elements:

                    print("Extraindo dados de {}".format(since_str))
                    url = option.get_attribute("href")

                    if not url in urls:
                        urls.append(url)
                    
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print("SCROLLL")
                time.sleep(scroll_time)
            
            self.save_txt(urls)
            # self.create_csv(since_str, until_str, i, urls)
                
if __name__ == "__main__":
    selenium_twitter = SeleniumTwitter()
    selenium_twitter.get_spotify_urls()
