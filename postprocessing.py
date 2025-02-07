import json
import pandas as pd

df_to_fixed = pd.read_json("./base/to_fixed.json")
df_papers_information = pd.read_json("./base/papers_information.json")

json_output = []

for index, paper_information in df_papers_information[~df_papers_information["titulo"].isna()].iterrows():
    json_output.append({
            "titulo": paper_information["titulo"],
            "abstract": paper_information["abstract"],
            "autores": paper_information["autores"],
            "keywords": paper_information["keywords"],
            "url": paper_information["url"]
    })

with open("./results/papers_information_clean.json", "w", encoding = "utf-8") as output_file_paper:
    json.dump(json_output, output_file_paper, ensure_ascii = False)


with open("./results/to_fixed_complete.json", "w", encoding = "utf-8") as output_file_fixed:
    json.dump(list(pd.concat([df_to_fixed, pd.DataFrame({0: df_papers_information[df_papers_information["titulo"].isna()]["url"].values})], ignore_index = True)[0].values), output_file_fixed, ensure_ascii = False)