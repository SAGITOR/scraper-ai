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
        self.driver = webdriver.Chrome()
        self.papers_ai_client = PapersAI()
        self.dois_file_path = "./results/dois.json"

    def execute( self ):
        print("\nCreating error.logs file\n")

        with open( './error_logs.txt', "w", encoding = 'utf-8' ) as error_logs:
            error_logs.write(f'Start at: {str(datetime.now())}\n')
            print("     error.logs file created")

        try:
            dois_file = open(self.dois_file_path)
            dois = json.load(dois_file)

            with alive_bar( len(dois), bar = "blocks", title = "Starting process..." ) as process_bar:
                for doi in dois:
                    paper_text_content = []

                    process_bar.title(f"Scraping Paper URL: {doi}")
                    self.driver.get(doi)
                    self.__humanizaitor(4.5, 5.3)

                    try:
                        html_main_component = self.driver.find_element(By.TAG_NAME, "html")

                        titles = list(html_main_component.find_elements(By.TAG_NAME, "h1")) + list(self.driver.find_elements(By.TAG_NAME, "h2")) + list(self.driver.find_elements(By.TAG_NAME, "h3"))
                        
                        for text_page in titles:
                            if ( len(text_page.text.split(" ")) >= 4 ):
                                paper_text_content.append(text_page.text.strip())

                        for text_page in html_main_component.find_elements(By.TAG_NAME, "p"):
                            if ( ( len(text_page.text.split(" ")) >= 100 ) and  ( len(text_page.text.split(" ")) <= 300 ) ):
                                paper_text_content.append(text_page.text.strip())

                        for text_page in html_main_component.find_elements(By.TAG_NAME, "span"):
                            if ( ( text_page.text.strip() not in paper_text_content ) and ( len(text_page.text.strip()) > 1 ) and ( len(text_page.text.split(" ")) <= 3 ) ):
                                paper_text_content.append(text_page.text.strip())

                        paper_text_content = "\n".join(paper_text_content)
                        if ( len(paper_text_content.split(" ")) <= 80 ):
                            print(f"Paper URL: {doi} enviado a to_fixed.json")
                            self.to_fixed.append(doi)
                            self.__save_json("to_fixed.json", self.to_fixed)
                            continue
                    
                        parse_paper_content = self.papers_ai_client.execute(paper_text_content)
        
                        self.output_json.append({
                            "titulo": parse_paper_content[0].strip(),
                            "abstract": parse_paper_content[1].strip(),
                            "autores": parse_paper_content[2].strip(),
                            "keywords": parse_paper_content[3].strip() if parse_paper_content[3] != "null" else None,
                            "url": doi
                        })

                        self.__save_json("papers_information.json", self.output_json)
                        
                    except Exception as error:
                        traceback.print_exc()
                        self.__error_handler(error, doi)
                        print(f"Paper URL with Error: {doi} enviado a to_fixed.json")
                        self.to_fixed.append(doi)
                        self.__save_json("to_fixed", self.to_fixed)

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