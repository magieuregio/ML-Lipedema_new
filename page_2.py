import streamlit as st
import pandas as pd


st.title("Dataset")

# Assign the Excel file
df1 = pd.read_excel("met_prot_results.xlsx", sheet_name=0)  # Use sheet_name='Sheet1' if you know the sheet name

# Display the DataFrame
st.subheader("Results of metabolomics and proteomics analysis")
st.markdown("""
<div style="text-align: justify;">
Targeted metabolomic and proteomic analyses were conducted on SAT to evaluate dysregulated molecules and proteins associated with lipedema. We analyzed 63 SAT biopsies from lipedema patients, consisting of 42 samples of lipedema tissue and 21 samples from healthy adipose tissue. We selected 10 metabolites (Histamine, Histidine, 1-Methylhistamine, Imidazole Acetaldehyde, Leukotrien E4, Leukotrien D4, Leukotrien B4, Octanoyl carnitine, Decatrienoyl carnitine, Stearoyl carnitine) and 13 proteins (FABP4, ACSL1, FAS, APOE, PLIN1, PPARg, PPARa, COX2, GIP, RETN, MSTN, CD36, LEP), all being already correlated to lipedema or adipose tissue-related disorders in literature. The statistical analysis showed that all selected metabolites and proteins were significantly elevated in lipedema tissues, except for one metabolite (Acetyl-Carnitine) which was significantly increased in control samples.
</div>
<br>
""", unsafe_allow_html=True)
st.dataframe(df1)  # Use st.table(df) if you prefer a static table


# Display the dataset
st.subheader("Normalized dataset")
st.write("In this page you can see the raw database (normalized data) used for the training: ")


# Assign the Excel file
df = pd.read_excel("raw_data.xlsx", sheet_name=0)  # Use sheet_name='Sheet1' if you know the sheet name

# Display the DataFrame
st.dataframe(df)  # Use st.table(df) if you prefer a static table

#Display images
image_path2 = "immagine_proteine.png"

st.subheader("Distribution of analyzed metabolites")
st.write("In this graph, we can see the distribution of all metabolites, all overexpressed in diseases tissues (orange) apart from Acetyl-Carnitine.")
st.image("boxplots_metaboliti.png", caption="Distribution of analyzed metabolites.", use_column_width=True)


st.subheader("Distribution of analyzed proteins")
st.write("In this graph, we can see the distribution of all proteins, all overexpressed in diseases tissues (orange).")
st.image("boxplots_proteine.png", caption="Distribution of analyzed proteins.", use_column_width=True)


