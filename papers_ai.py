import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class PapersAI:
    def __init__( self ):
        self.client = OpenAI( api_key = os.getenv("OPENAI_API_KEY") )
        self.system_message_base = { 
            "role": "system", 
            "content": (
              "Eres un asistente que ayuda extraer informacion de papers de investigacion en base a un input de texto."
              "En base al input ingresado, debes entregar SOLAMENTE la informacion del titulo, abstract, autores y keywords." 
              
              "Ejemplo de formato de {autores} en input de texto:"
              "Rodrigo Olivares, Ricardo Soto, Broderick Crawford, Víctor Ríos, Pablo Olivares, Camilo Ravelo, Sebastian Medina, Diego Nauduan"
              "Olivares, R., Soto, R., Crawford, B., Ríos, V., Olivares, P., Ravelo, C., Medina, S., Nauduan, D."
              "Martinez, F."
              "Omar Salinas"
              "Sílvia Móbille Awoyama, Henrique Cunha Carvalho, Túlia de Souza Botelho, Sandra Irene Sprogis Dos Santos, Debora Alicia Buendia Palacios, Sebastian San Martín Henríque" 
              
              "Ejemplo de formato de {keywords} en input de texto:"
              "economic losses, sea level rise, shoreline change, wave climate"
              "Keywords: HER2, machine learning, immunohistochemistry, breast cancer, explainable AI, fluorescence in situ hybridization."
              "Engineering controlled terms: Artificial intelligence, Engineering education, Learning systems, Teaching"
              "local dialects, Sociolinguistic perception, urban/rural context"

              "La respuesta debe tener el siguiente formato: {titulo};;{abstract};;{autores};;{keywords}"
              "No agregues nada de texto adicional, solo lo solicitado en el formato de la respuesta."
              "Si no encuentras la informacion sobre el {titulo}, {abstract}, {autores} o {keywords} basado en sus formatos, entrega un null en su lugar."
            )
        }

    def execute( self, paper_content ):
        response = self.__get_paper_information( paper_content ).choices[0].message.content

        return response.split(";;")
        
    def __get_paper_information( self, paper_content ):
        return self.client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                self.system_message_base,
                { "role": "user", "content": paper_content },
            ]
        )

if __name__ == "__main__":
    instance = PapersAI()
    paper_content = '''
    Your privacy, your choice
       We use essential cookies to make sure the site can function. We also use optional cookies for advertising, personalisation of content, usage analysis, and social media.
       By accepting optional cookies, you consent to the processing of your personal data - including transfers to third parties. Some third parties are outside of the European Economic Area, with varying standards of data protection.
       See our privacy policy for more information on the use of your personal data.
       Manage preferences for further information and to change your choices.
       Accept all cookies
       Skip to main content
       Advertisement
       Log in
       Find a journal
       Publish with us
       Track your research
       Search
       Cart
       Home Journal of Ambient Intelligence and Humanized Computing Article
       Affective autonomous agents for supporting investment decision processes using artificial somatic reactions
       Original Research
       Published: 30 May 2021
       Volume 14, pages 677–696, (2023)
       Cite this article
       Journal of Ambient Intelligence and Humanized Computing
       Aims and scope
       Submit manuscript
       Daniel Cabrera-Paniagua
       & Rolando Rubilar-Torrealba
         456 Accesses
       3 Citations
       Explore all metrics
       Abstract
       Sometimes, the conscious act of decision-making in humans is dramatically interrupted by situations that warrant an immediate response (e.g. when there is an imminent risk). The human body somatizes this interruption such that an action could be taken without a rational analysis. The above is known as a somatic marker. According to the somatic marker hypothesis, somatic markers could directly influence several ambits of decision-making. This research work presents the incorporation of artificial somatic reactions into affective autonomous agents who implement decision-making in the stock market. This implies the design of a general decision architecture for stock markets considering artificial somatic reactions and the definition of a set of decision-making algorithms for supporting investment decisions performed by affective autonomous agents (considering artificial somatic reactions). Test scenarios were defined using official data from Standard & Poor's 500 and Dow Jones. The experimental results are promising and indicated that affective autonomous agents are able to experience artificial somatic reactions and achieve effectiveness and efficiency in their decision-making.
       This is a preview of subscription content, log in via an institution to check access.

       Similar content being viewed by others
       Felix: A Model for Affective Multi-agent Simulations
       Chapter © 2021
       The Relationships Between Emotional States and Information Processing Strategies in IS Decision Support—A NeuroIS Approach
       Chapter © 2020
       Emotion-Integrated Cognitive Architectures: A Bio-Inspired Approach to Developing Emotionally Intelligent AI Agents
       Chapter © 2024
       Data availability
       The datasets used and analyzed during the current study correspond to S&P500 Index and Dow Jones Index, which are available in https://finance.yahoo.com/.
       Acknowledgements
       This work was funded by ANID Chile through FONDECYT INICIACION Project No. 11190370.
       Author information
       Authors and Affiliations
       Escuela de Ingeniería Informática, Universidad de Valparaíso, Valparaíso, Chile
       Daniel Cabrera-Paniagua
       Instituto de Estadística, Universidad de Valparaíso, Valparaíso, Chile
       Rolando Rubilar-Torrealba
       Corresponding author
       Correspondence to Daniel Cabrera-Paniagua.
       Additional information
       Publisher's Note
       Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.
       Rights and permissions
       Reprints and permissions
       About this article
       Cite this article
       Cabrera-Paniagua, D., Rubilar-Torrealba, R. Affective autonomous agents for supporting investment decision processes using artificial somatic reactions. J Ambient Intell Human Comput 14, 677–696 (2023). https://doi.org/10.1007/s12652-021-03319-1
       Download citation
       Received
       07 December 2020
       Accepted
       24 May 2021
       Published
       30 May 2021
       Issue Date
       January 2023
       DOI
       https://doi.org/10.1007/s12652-021-03319-1
       Keywords
       Somatic marker
       Artificial somatic reaction
       Affective autonomous agent
       Investment decision process
       Access this article
       Log in via an institution
       Buy article PDF USD 39.95
       Price includes VAT (Chile)
       Instant access to the full article PDF.
       Rent this article via DeepDyve
       Institutional subscriptions
       Sections
       Figures
       References
       Abstract
       Data availability
       References
       Acknowledgements
       Author information
       Additional information
       Rights and permissions
       About this article
       Advertisement
       Discover content
       Journals A-Z
       Books A-Z
       Publish with us
       Publish your research
       Open access publishing
       Products and services
       Our products
       Librarians
       Societies
       Partners and advertisers
       Our imprints
       Springer
       Nature Portfolio
       BMC
       Palgrave Macmillan
       Apress
       Your privacy choices/Manage cookies Your US state privacy rights Accessibility statement Terms and conditions Privacy policy Help and support Cancel contracts here
       181.72.201.135
       Not affiliated
       © 2024 Springer Nature
    '''
    instance.execute(paper_content)