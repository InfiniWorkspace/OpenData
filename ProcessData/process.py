### descarregar excels any per any O tot junt --> bool
### penjarlos a streamlit?

from pathlib import Path
import os
import pandas as pd
from functions import *

######################################################## TOOL CONFIG #######################################################
# Specify the directory path
directory = Path('ProcessData/input_files/')

all_years_one_document = False

group_by_method = "MEAN"

indicador_column = "Indicador"

year_column = "Any"

name_district_column = "Nom_Districte"

total_column = "Total"

# If we need to group for more things than any and nom districte
added_group_by = []

# 
indicador_prefijo = "Evolución parque vehiculos"
indicador_columnas = ["Codi_Districte","Codi_Districte"]

####################################################### CODE ##############################################################

dataframes_names,dict_of_dataframes = get_dfs(directory)

common_columns = get_common_columns_along_dfs(dict_of_dataframes,dataframes_names)

combined_df = combine_dfs(dict_of_dataframes,dataframes_names,common_columns)
print(combined_df)

columns_remaining = [indicador_column,name_district_column,total_column,year_column]

combined_df = set_indicador_column_and_delete_columns(combined_df,indicador_prefijo,indicador_columnas,columns_remaining)

resulting_df = get_grouped_df(combined_df,columns_remaining,group_by_method)

resulting_df.to_csv("ProcessData/output_files/output.csv",index=False)

print(resulting_df)

### Selecciones columnes: 
    # Nom_Districte/ID
    # Total
    # Identificadors: si son 1 es agrupar per aquella columna, si es mes de una, concatenar i agrupar per aquelles

### Seleccioonar operand:
    ### Mitja, suma

### Descarregar el excel resultant que tindrà: Indicador, Districte, Valor, Any