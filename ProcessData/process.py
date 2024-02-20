### descarregar excels any per any O tot junt --> bool
### penjarlos a streamlit?

from pathlib import Path
import os
import pandas as pd


######################################################## TOOL CONFIG #######################################################
# Specify the directory path
directory = Path('ProcessData/input_files/')

all_years_one_document = False

group_by_method = "MEAN"

year_column = "Any"

name_disctrict_column = "Nom_Districte"

####################################################### CODE ##############################################################

# Get all files in the directory
files = directory.glob('*')


dict_of_dataframes = {}
dataframes_names = []

# Print the list of files
for file_path in files:
    # Read the file into a DataFrame
    df = pd.read_csv(file_path)  
    # Get the df name
    df_name = str(file_path).split("\\")[-1]
    dataframes_names.append(df_name)
    # Store the DataFrame in the dictionary with the file name as key
    dict_of_dataframes[df_name] = df


common_columns = set(dict_of_dataframes[dataframes_names[0]].columns)

print(common_columns)

# Iterate over the rest of the DataFrames and find the intersection of columns
for df in dict_of_dataframes.values():
    common_columns = common_columns.intersection(df.columns)

# Make the instesection a list
common_columns = list(common_columns)

for df_name in dataframes_names:
    # get the dataframe with the subset of columns and store them back in the dictionary
    dict_of_dataframes[df_name] = dict_of_dataframes[df_name][list(common_columns)].copy()


combined_df = pd.concat(list(dict_of_dataframes.values()), ignore_index=True)
combined_df.reset_index(drop=True, inplace=True)

if group_by_method == "MEAN":
    grouped_df = combined_df.groupby(['Any', 'Nom_Districte']).sum().reset_index()

grouped_df = grouped_df[[]]
print(grouped_df)
### Selecciones columnes: 
    # Nom_Districte/ID
    # Total
    # Identificadors: si son 1 es agrupar per aquella columna, si es mes de una, concatenar i agrupar per aquelles

### Seleccioonar operand:
    ### Mitja, suma

### Descarregar el excel resultant que tindrà: Indicador, Districte, Valor, Any