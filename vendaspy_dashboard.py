import streamlit as st
import requests

st.set_page_config(page_title="VENDASPY – Consulta ao Vivo no Mercado Livre")
st.title("VENDASPY - Consulta ao Vivo no Mercado Livre")

def buscar_produtos_publicos_com_lucro(termo):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit=10"
    response = requests.get(url)
    data = response.json()

    produtos = []

    for item in data.get("results", []):
        titulo = item.get("title", "")
        preco = item.get("price", 0.0)
        link = item.get("permalink", "")
        thumbnail = item.get("thumbnail", "")

        # Estimativas conforme regras definidas
        if preco >= 79:
            frete = 34.00
        else:
            frete = 6.50

        estimativa_custo = preco * 0.65  # Assume custo como 65% do preço
        lucro_liquido = preco - estimativa_custo - frete
        margem = (lucro_liquido / preco) * 100 if preco > 0 else 0

        produtos.append({
            "titulo": titulo,
            "preco": preco,
            "link": link,
            "imagem": thumbnail,
            "lucro_liquido": round(lucro_liquido, 2),
            "margem": round(margem, 2)
        })

    return produtos

termo_busca = st.text_input("Digite o produto que deseja pesquisar:")

if termo_busca:
    st.info(f"Buscando resultados para: **{termo_busca}**")
    produtos = buscar_produtos_publicos_com_lucro(termo_busca)

    if produtos:
        for produto in produtos:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(produto["imagem"], width=100)
            with col2:
                st.markdown(f"**[{produto['titulo']}]({produto['link']})**")
                st.markdown(f"Preço: R$ {produto['preco']:.2f}")
                st.markdown(f"Lucro líquido estimado: R$ {produto['lucro_liquido']:.2f}")
                st.markdown(f"Margem: {produto['margem']:.1f}%")
            st.markdown("---")
    else:
        st.warning("Nenhum resultado encontrado.")
        def buscar_produtos_publicos_com_lucro(termo):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    produtos = []

    for item in data.get("results", []):
        preco = item["price"]
        acima_79 = preco >= 79
        frete = 34 if acima_79 else 6.50
        custo_estimado = preco * 0.7  # estimativa do custo real
        lucro_liquido = preco - frete - custo_estimado
        margem = (lucro_liquido / preco) * 100 if preco else 0

        produtos.append({
            "titulo": item["title"],
            "preco": preco,
            "link": item["permalink"],
            "thumbnail": item["thumbnail"],
            "lucro_liquido": round(lucro_liquido, 2),
            "margem": round(margem, 1)
        })

    return produtos
