import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="VENDASPY - Dashboard", layout="wide")
st.title("VENDASPY - Consulta ao Vivo no Mercado Livre")

def buscar_produtos(palavra, paginas=1):
    base_url = "https://lista.mercadolivre.com.br/"
    headers = {"User-Agent": "Mozilla/5.0"}

    resultados = []
    for pagina in range(paginas):
        offset = pagina * 50
        url = f"{base_url}{palavra.replace(' ', '-')}_Desde_{offset}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        anuncios = soup.find_all("li", {"class": "ui-search-layout__item"})

        for anuncio in anuncios:
            titulo_tag = anuncio.find("h2", {"class": "ui-search-item__title"})
            preco_tag = anuncio.find("span", {"class": "andes-money-amount__fraction"})
            link_tag = anuncio.find("a", {"class": "ui-search-link"})

            if titulo_tag and preco_tag and link_tag:
                resultados.append({
                    "Título": titulo_tag.get_text(strip=True),
                    "Preço": f"R${preco_tag.get_text(strip=True)}",
                    "Link": link_tag["href"]
                })

    return pd.DataFrame(resultados)

palavra = st.text_input("Digite o produto que deseja pesquisar:", value="kit relação cg 150")

if palavra:
    st.info(f"Buscando resultados para: **{palavra}**")
    df = buscar_produtos(palavra, paginas=2)

    if not df.empty:
        st.dataframe(df)

        st.markdown("### Top 10 produtos com maior preço")
        df['Preço_Num'] = df['Preço'].str.replace('R\\$', '', regex=True).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
        st.dataframe(df.sort_values(by="Preço_Num", ascending=False).head(10).drop(columns=["Preço_Num"]))
    else:
        st.warning("Nenhum resultado encontrado.")
