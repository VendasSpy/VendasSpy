import streamlit as st
import requests

st.set_page_config(page_title="VENDASPY – Análise de Concorrência")
st.title("VENDASPY - Consulta ao Vivo no Mercado Livre")

def buscar_produtos(termo):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}"
    response = requests.get(url)
    data = response.json()
    return data.get("results", [])

def calcular_lucro(preco):
    if preco >= 79:
        frete = 34.00
    else:
        frete = 6.50
    custo_estimado = preco * 0.60  # estimativa de custo (ajustável)
    lucro_liquido = preco - frete - custo_estimado
    margem = (lucro_liquido / preco) * 100 if preco != 0 else 0
    return round(lucro_liquido, 2), round(margem, 1)

termo = st.text_input("Digite o produto que deseja pesquisar:")

if termo:
    st.info(f"Buscando resultados para: **{termo}**")
    produtos = buscar_produtos(termo)

    if not produtos:
        st.warning("Nenhum resultado encontrado.")
    else:
        for produto in produtos[:10]:  # Limita a 10 resultados
            nome = produto.get("title", "Sem título")
            preco = produto.get("price", 0.0)
            link = produto.get("permalink", "#")
            imagem = produto.get("thumbnail", "")

            lucro, margem = calcular_lucro(preco)

            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(imagem, width=100)
            with col2:
                st.markdown(f"**[{nome}]({link})**")
                st.markdown(f"Preço: R$ {preco:.2f}")
                st.markdown(f"Lucro estimado: R$ {lucro:.2f}")
                st.markdown(f"Margem líquida: {margem}%")
            st.markdown("---")
