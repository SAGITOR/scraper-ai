import glob
import json

import pandas as pd

excels_data = glob.glob(f"./assets/*.xlsx")

dois = []
titles = []

for excel_data in excels_data:
    df =  pd.read_excel(excel_data)
    df.dropna(subset = ["URL"], inplace = True)
    for index, data in pd.read_excel(excel_data).iterrows():
        if ( data["TITULO"] not in titles ):
            if ( ( type(data["URL"]) != float ) and ( data["URL"] not in dois )  and ( "https" in data["URL"] ) ):
                dois.append(data["URL"].strip())
            elif ( ( type(data["DOI"]) != float ) and ( f"https://doi.org/{data["DOI"].strip()}" not in dois )):
                dois.append(f"https://doi.org/{data["DOI"].strip()}")
                
            titles.append(data["TITULO"])

with open( "./results/dois.json", "w", encoding = "utf-8" ) as output_file:
    json.dump( dois, output_file, ensure_ascii = False )