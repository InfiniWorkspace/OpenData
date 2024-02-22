import streamlit as st
import pandas as pd
from functions import *

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False,encoding='utf8').encode('utf-8')

def main():
    st.title("Manage excels")

    # File upload
    st.subheader("Upload Files")
    uploaded_files = st.file_uploader("Upload your CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)
    
    
    dict_of_dataframes = {}
    dataframes_names = []
    
    if uploaded_files:
        for file in uploaded_files:
            df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
            st.write(f"Preview of {file.name} (shape {df.shape}):")
            st.write(df.head(3))

            dataframes_names.append(str(file.name))
            # Store the DataFrame in the dictionary with the file name as key
            dict_of_dataframes[str(file.name)] = df
    
    # Define default variables
    year_column_is_datetime = False
    group_by_method = "SUM"
    indicador_column = "Indicador"
    year_column = "Any"
    name_district_column = "Nom_Districte"
    total_column = "Total"
    added_group_by = []
    indicador_prefijo = "Evolución parque vehiculos"
    indicador_columnas = ["Codi_Districte", "Codi_Districte"]
    
    # User-defined variables
    st.sidebar.header("Define Variables")
    year_column_is_datetime = st.sidebar.checkbox("Year column is datetime", value=year_column_is_datetime)
    group_by_method = st.sidebar.selectbox("Group By Method", ["MEAN", "SUM","COUNT"], index=1)
    indicador_column = st.sidebar.text_input("Indicador Column", value=indicador_column)
    year_column = st.sidebar.text_input("Year Column", value=year_column)
    name_district_column = st.sidebar.text_input("District Name Column", value=name_district_column)
    total_column = st.sidebar.text_input("Total Column", value=total_column)
    indicador_prefijo = st.sidebar.text_input("Indicator Prefix", value=indicador_prefijo)
    indicador_columnas = st.sidebar.text_input("Indicator Columns (comma-separated). These are the columns that will be used to group by")
    indicador_columnas = [col.strip() for col in indicador_columnas.split(",") if col.strip()]
    
    

    if dict_of_dataframes:
        common_columns = get_common_columns_along_dfs(dict_of_dataframes,dataframes_names)

        combined_df = combine_dfs(dict_of_dataframes,dataframes_names,common_columns)

        columns_remaining = [indicador_column,name_district_column,total_column,year_column]

        combined_df = set_indicador_column_and_delete_columns(combined_df,indicador_prefijo,indicador_columnas,columns_remaining)

        if year_column_is_datetime:
            combined_df[year_column] = combined_df[year_column].astype(str).str[0:3]

        resulting_df = get_grouped_df(combined_df,columns_remaining,group_by_method,name_district_column,year_column)

        resulting_df = resulting_df.rename({name_district_column: 'Nom_Districte', year_column: 'Any',total_column:"Total"}, axis=1)

        st.subheader("Resulting Df")
        csv = convert_df(resulting_df)

        file_name = st.text_input("Downloaded file name (include .csv)", value="result.csv")

        st.download_button(
        "Download resulting csv",
        csv,
        file_name,
        "text/csv",
        key='download-csv'
        )
        st.write(resulting_df)
if __name__ == "__main__":
    main()
