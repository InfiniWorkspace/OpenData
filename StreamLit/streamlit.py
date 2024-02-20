import streamlit as st
import pandas as pd
from functions import *

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False,encoding='utf8').encode('utf-8')





def main():
    st.title("Manage excels")
    
    # Define default variables
    all_years_one_document = False
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
    all_years_one_document = st.sidebar.checkbox("All Years in One Document", value=all_years_one_document)
    group_by_method = st.sidebar.selectbox("Group By Method", ["MEAN", "SUM"], index=1)
    indicador_column = st.sidebar.text_input("Indicador Column", value=indicador_column)
    year_column = st.sidebar.text_input("Year Column", value=year_column)
    name_district_column = st.sidebar.text_input("District Name Column", value=name_district_column)
    total_column = st.sidebar.text_input("Total Column", value=total_column)
    added_group_by = st.sidebar.text_input("Additional Group By Columns (comma-separated)", value=",".join(added_group_by))
    added_group_by = [col.strip() for col in added_group_by.split(",") if col.strip()]
    indicador_prefijo = st.sidebar.text_input("Indicator Prefix", value=indicador_prefijo)
    indicador_columnas = st.sidebar.text_input("Indicator Columns (comma-separated)", value=",".join(indicador_columnas))
    indicador_columnas = [col.strip() for col in indicador_columnas.split(",") if col.strip()]
    
    # File upload
    st.title("Upload Files")
    uploaded_files = st.file_uploader("Upload your CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)
    
    
    dict_of_dataframes = {}
    dataframes_names = []
    
    if uploaded_files:
        for file in uploaded_files:
            df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
            st.write(f"Preview of {file.name}:")
            st.write(df.head(3))

            dataframes_names.append(str(file.name))
            # Store the DataFrame in the dictionary with the file name as key
            dict_of_dataframes[str(file.name)] = df
            # Perform data analysis using defined variables and uploaded data

    if dict_of_dataframes:
        common_columns = get_common_columns_along_dfs(dict_of_dataframes,dataframes_names)

        combined_df = combine_dfs(dict_of_dataframes,dataframes_names,common_columns)

        columns_remaining = [indicador_column,name_district_column,total_column,year_column]

        combined_df = set_indicador_column_and_delete_columns(combined_df,indicador_prefijo,indicador_columnas,columns_remaining)

        resulting_df = get_grouped_df(combined_df,columns_remaining,group_by_method)

        #resulting_df.to_csv("ProcessData/output_files/output.csv",index=False)

        st.title("Resulting Df")
        csv = convert_df(resulting_df)

        st.download_button(
        "Download resulting csv",
        csv,
        "result.csv",
        "text/csv",
        key='download-csv'
        )
        st.write(resulting_df)
if __name__ == "__main__":
    main()
