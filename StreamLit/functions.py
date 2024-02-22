from pathlib import Path
import os
import pandas as pd


def get_dfs(directory):
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

    return dataframes_names,dict_of_dataframes



def get_common_columns_along_dfs(dict_of_dataframes,dataframes_names):
    common_columns = set(dict_of_dataframes[dataframes_names[0]].columns)

    # Iterate over the rest of the DataFrames and find the intersection of columns
    for df in dict_of_dataframes.values():
        common_columns = common_columns.intersection(df.columns)

    # Make the instesection a list
    common_columns = list(common_columns)

    return common_columns

def combine_dfs(dict_of_dataframes,dataframes_names,common_columns):
    for df_name in dataframes_names:
        # get the dataframe with the subset of columns and store them back in the dictionary
        dict_of_dataframes[df_name] = dict_of_dataframes[df_name][list(common_columns)].copy()

    # create the concatenated dataframe with all the previous columns
    combined_df = pd.concat(list(dict_of_dataframes.values()), ignore_index=True)
    combined_df.reset_index(drop=True, inplace=True)

    return combined_df

def set_indicador_column_and_delete_columns(combined_df,indicador_prefijo,indicador_columnas,columns_remaining):
    #  create column indicador with the prefix. If no indicador columns there, will be quiet
    combined_df["Indicador"] = indicador_prefijo

    if indicador_columnas:
        for ind in indicador_columnas:
            combined_df["Indicador"]  = combined_df["Indicador"] +"-"+ combined_df[ind]

    # get the minimum columns required
    # get stay 
    combined_df = combined_df[columns_remaining]

    return combined_df

def get_grouped_df(combined_df,columns_remaining,group_by_method,name_district_column,year_column):
    # Group by indicador, any and nom districte
    
    if group_by_method == "MEAN":
        grouped_df = combined_df.groupby(['Indicador',year_column, name_district_column]).mean().reset_index()

    elif group_by_method == "SUM":
        grouped_df = combined_df.groupby(['Indicador',year_column, name_district_column]).sum().reset_index()

    elif group_by_method == "COUNT":
        grouped_df = combined_df.groupby(['Indicador',year_column, name_district_column]).count().reset_index()

    # reorder columns
    grouped_df = grouped_df[columns_remaining]

    return grouped_df
