import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="VENDASPY - Concorrência e Lucro", layout="wide")
st.title("VENDASPY - Análise de Concorrência com Lucro Estimado")

def buscar_produtos_publicos_com_lucro(termo, limite=50):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit={limite}"
    response = requests.get(url)
    data = response.json()

    produtos = []

    for item in data.get("results", []):
        preco = float(item.get("price", 0))
        titulo = item.get("title")
        link = item.get("permalink")
        imagem = item.get("thumbnail")

        # Cálculo de comissão e custos
        comissao = preco * 0.17
        desconto_fixo = 34.00 if preco >= 79 else 6.50

        valor_liquido = preco - comissao - desconto_fixo
        margem = (valor_liquido / preco) * 100 if preco > 0 else 0

        produtos.append({
            "Imagem": imagem,
            "Título": titulo,
            "Preço (R$)": f"{preco:.2f}",
            "Link": link,
            "Lucro Estimado (R$)": f"{valor_liquido:.2f}",
            "Margem Estimada (%)": f"{margem:.1f}%"
        })

    return pd.DataFrame(produtos)

# Entrada do usuário
termo = st.text_input("Digite o nome do produto para analisar:", value="kit relação cg 150")

if termo:
    st.info(f"Buscando produtos para: **{termo}**")
    resultados = buscar_produtos_publicos_com_lucro(termo)

    if not resultados.empty:
        for _, row in resultados.iterrows():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(row["Imagem"], width=100)
            with col2:
                st.markdown(f"**{row['Título']}**")
                st.markdown(f"Preço: R$ {row['Preço (R$)']}")
                st.markdown(f"Lucro Estimado: R$ {row['Lucro Estimado (R$)']} | Margem: {row['Margem Estimada (%)']}")
                st.markdown(f"[Ver Anúncio]({row['Link']})")
                st.markdown("---")
    else:
        st.warning("Nenhum produto encontrado.")
