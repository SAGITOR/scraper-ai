import json
import traceback
from time import sleep
from random import uniform
from datetime import datetime
from selenium import webdriver
from papers_ai import PapersAI
from alive_progress import alive_bar
from selenium.webdriver.common.by import By

class Scraper:
    def __init__( self ):
        self.to_fixed = []
        self.output_json = []
        self.papers_ai_client = PapersAI()
        #self.dois_file_path = "./results/dois.json"
        self.dois_file_path = "./results/to_fixed_complete.json"

        options = webdriver.ChromeOptions()

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-extensions')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(options = options)

    def execute( self ):
        print("\nCreating error.logs file\n")

        with open( './error_logs.txt', "w", encoding = 'utf-8' ) as error_logs:
            error_logs.write(f'Start at: {str(datetime.now())}\n')
            print("     error.logs file created")

        try:
            not_found = []
            dois_file = open(self.dois_file_path)
            dois = json.load(dois_file)

            with alive_bar( len(dois), bar = "blocks", title = "Starting process..." ) as process_bar:
                for doi in dois:

                    process_bar.title(f"Scraping Paper URL: {doi}")
                    self.driver.get(doi)
                    self.__humanizaitor(4.5, 5.3)

                    try:
                        html_main_component = self.driver.find_element(By.TAG_NAME, "html").text[:8000]
                        
                        # for div in html_main_component.find_elements(By.TAG_NAME, "div"):
                        #     print(div.text)
         
                        if ( "Verifique que usted es un ser humano completando la acción a continuación." in html_main_component ):
                            self.__humanizaitor(30, 45)
                            html_main_component = self.driver.find_element(By.TAG_NAME, "html").text[:8000]
                        elif ( "DOI NOT FOUND" in html_main_component ):
                            print(f"Paper URL: {doi} enviado a not_found.json")
                            not_found.append(doi)
                            self.__save_json("not_found.json", not_found)
                            process_bar(1)
                            continue

                        if ( len(html_main_component.split(" ")) <= 80 ):
                            print(f"Paper URL: {doi} enviado a to_fixed.json")
                            self.to_fixed.append(doi)
                            self.__save_json("to_fixed.json", self.to_fixed)
                            process_bar(1)
                            continue
                    
                        parse_paper_content = self.papers_ai_client.execute(html_main_component)

                        print(parse_paper_content)

                        self.output_json.append({
                            "titulo": parse_paper_content[0].strip() if parse_paper_content[0] != "null" else None,
                            "abstract": parse_paper_content[1].strip() if parse_paper_content[1] != "null" else None,
                            "autores": parse_paper_content[2].strip() if parse_paper_content[2] != "null" else None,
                            "keywords": parse_paper_content[3].strip() if parse_paper_content[3] != "null" else None,
                            "url": doi
                        })

                        self.__save_json("papers_information.json", self.output_json)

                    except Exception as error:
                        traceback.print_exc()
                        self.__error_handler(error, doi)
                        print(f"Paper URL with Error: {doi} enviado a to_fixed.json")
                        self.to_fixed.append(doi)
                        self.__save_json("to_fixed.json", self.to_fixed)

                    process_bar(1)
        except:
            traceback.print_exc()
        finally:
            dois_file.close()
    
    def __humanizaitor( self, x: float = 1.5, y: float = 2.5 ):
        sleep(uniform(x, y))
    
    def __save_json( self, file_name, input_object ):
        with open( f"./results/{file_name}", "w", encoding = "utf-8" ) as output_file:
            json.dump( input_object, output_file, ensure_ascii = False )
            print(f"Guardando informacion en {file_name}")
    
    def __error_handler( self, error: str, paper_url: str ):
        with open( f"./error_logs.txt", "a", encoding = "utf-8" ) as error_logs_file:
            error_logs_file.write(f"Date: {str(datetime.now())} - Paper URL: {paper_url} - Error: {error}")

if __name__ == "__main__":

    instance = Scraper()
    instance.execute()