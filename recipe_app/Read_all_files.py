import os
import pandas as pd

path = "data"

def read_all_files(path):
    df_list = []
    for i in os.listdir(path):
        df = pd.read_csv(os.path.join(path, i))
        df_list.append(df)
        
    df_full = pd.concat(df_list).reset_index(drop=True)
    df_full.columns = ["Recipe_Name","Link","Ingredients","Instructions","Image"]
    df_full['ingredients_list'] = df_full.Ingredients.apply(lambda x: x[2:-2].replace("'","").replace(",",""))
    
    return df_full