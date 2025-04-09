import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="VENDASPY - Consulta em Tempo Real", layout="wide")
st.title("VENDASPY - Consulta ao Vivo no Mercado Livre")

def buscar_via_api(termo, limite=50):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit={limite}"
    res = requests.get(url)
    data = res.json()

    resultados = []
    for item in data.get("results", []):
        resultados.append({
            "Título": item.get("title"),
            "Preço": f"R${item.get('price'):.2f}",
            "Link": item.get("permalink")
        })

    return pd.DataFrame(resultados)

palavra = st.text_input("Digite o produto que deseja pesquisar:", value="kit relação cg 150")

if palavra:
    st.info(f"Buscando resultados para: **{palavra}**")
    df = buscar_via_api(palavra)

    if not df.empty:
        st.dataframe(df)

        st.markdown("### Top 10 produtos com maior preço")
        df["Preço_Num"] = df["Preço"].str.replace('R\\$', '', regex=True).str.replace(',', '.').astype(float)
        st.dataframe(df.sort_values(by="Preço_Num", ascending=False).head(10).drop(columns=["Preço_Num"]))
    else:
        st.warning("Nenhum resultado encontrado.")
