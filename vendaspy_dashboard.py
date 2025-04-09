import streamlit as st
import pandas as pd

st.set_page_config(page_title="VENDASPY - Dashboard", layout="wide")

try:
    df = pd.read_csv("produtos_mercadolivre.csv")
    st.title("VENDASPY - Painel de Produtos Coletados")
    st.markdown("### Resultados da coleta no Mercado Livre")
    
    st.dataframe(df)

    st.markdown("### Top 10 Produtos com Maior Preço")
    df['Preço_Num'] = df['Preço'].str.replace('R\\$', '', regex=True).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    st.dataframe(df.sort_values(by="Preço_Num", ascending=False).head(10).drop(columns=["Preço_Num"]))

    st.markdown("### Filtrar por palavra no título")
    filtro = st.text_input("Digite uma palavra:")
    if filtro:
        filtrado = df[df["Título"].str.contains(filtro, case=False, na=False)]
        st.dataframe(filtrado)

except FileNotFoundError:
    st.warning("Arquivo 'produtos_mercadolivre.csv' não encontrado. Execute o scraper primeiro.")
