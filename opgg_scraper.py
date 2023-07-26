from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from lxml import etree
import numpy as np

class OpggScraper:
    def __init__(self) -> None:
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def get_overview(self,players):
        overview = {}
        for player in players:
            url = f'https://www.op.gg/summoners/euw/{player}/matches'
        
        #get win_lose, kda_ratio, kill_participation
            try:
                self.driver.get(url)
                rendered_content = self.driver.page_source
                dom = etree.HTML(rendered_content)
   
                win_lose = dom.xpath("//*[@id='content-container']/div[2]/div[2]/div[1]/div[1]/text()") #['20G 13W 7L']
                kda_ratio = dom.xpath("//*[@id='content-container']/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/text()")#['4.06:1']
                kill_participation = dom.xpath("//*[@id='content-container']/div[2]/div[2]/div[1]/div[2]/div[2]/div[3]/text()")#['P/Kill 62%']
                
                overview[player] = {"win_lose":win_lose[0],"kda_ratio":kda_ratio[0],"kill_participation":kill_participation[0].split()[1]}
        
            except Exception as e:
                print(f"Error: {e}")

        return overview

    
    def get_last_twenty_matches(self,players):
        last_twenty_matches = {}
        for player in players:
            url = f'https://www.op.gg/summoners/euw/{player}/matches'

 
            try:
                self.driver.get(url)
                rendered_content = self.driver.page_source
                dom = etree.HTML(rendered_content)
        
                # get kda array
                lst_kda = []
                for i in (1,2,3):
                    lst = dom.xpath(
                        '//*[@class="css-164r41r e1r5v5160"]'
                        '//*[contains(@class, "e1iiyghw3")]'
                         f'/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/span[{i}]/text()'
                    )
                    lst_kda.append(lst)
                kda = np.array(lst_kda).astype(int).transpose() # 3*20
                last_twenty_matches[player] = {"kda":kda}
            
            # get multi_kill array
            

            except Exception as e:
                print(f"Error: {e}")
    
        return last_twenty_matches
    
    def close(self):
        self.driver.close()


OpS = OpggScraper()
players = ['Magnoliar','ˆĘKKØˆ']
print(OpS.get_last_twenty_matches(players))
OpS.close()