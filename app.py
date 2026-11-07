
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Lanchonete", page_icon="🍔", layout="centered")

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "historico" not in st.session_state:
    st.session_state.historico = []

st.title("🍔 vt buger")
st.write("Sistema com cardápio ilustrado, tipo de pedido, carrinho, pagamentos e histórico.")

cardapio = {
    "X-Burger": {
        "preco": 15.00,
        "imagem": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd"
    },
    "X-Salada": {
        "preco": 18.00,
        "imagem": "https://images.unsplash.com/photo-1550547660-d9450f859349"
    },
    "X-Bacon": {
        "preco": 22.00,
        "imagem": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90"
    },
    
    "Batata Frita": {
        "preco": 12.00,
        "imagem": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877"
    },
    "Refrigerante": {
        "preco": 6.00,
        "imagem": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97"
    },
    "Água": {
        "preco": 4.00,
        "imagem": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d"
    }
}

st.markdown("---")
st.subheader("Fazer Pedido")

tipo_pedido = st.radio("Escolha a modalidade do pedido:", ["Retirar no Balcão", "Para Entregar (Delivery)"])

endereco_entrega = ""
if tipo_pedido == "Para Entregar (Delivery)":
    endereco_entrega = st.text_input("Informe o endereço de entrega:")

produto_selecionado = st.selectbox("Selecione o produto:", list(cardapio.keys()))

col_img, col_info = st.columns([1, 2])
with col_img:
    st.image(cardapio[produto_selecionado]["imagem"], width=150)
with col_info:
    preco_unitario = cardapio[produto_selecionado]["preco"]
    st.write(f"### {produto_selecionado}")
    st.write(f"Preço unitário: **R$ {preco_unitario:.2f}**")

quantidade = st.number_input(
    "Informe a quantidade:", 
    min_value=1, 
    step=1, 
    value=1, 
    format="%d"
)

if st.button("Adicionar ao Carrinho"):
    subtotal = preco_unitario * quantidade
    st.session_state.carrinho.append({
        "produto": produto_selecionado,
        "preco_unitario": preco_unitario,
        "quantidade": quantidade,
        "subtotal": subtotal
    })
    st.success(f"{quantidade}x **{produto_selecionado}** adicionado(s) ao carrinho!")

st.markdown("---")
st.subheader("🛒 Carrinho de Compras")

if len(st.session_state.carrinho) > 0:
    total_carrinho = 0
    for i, item in enumerate(st.session_state.carrinho):
        c1, c2, c3 = st.columns([3, 2, 1])
        with c1:
            st.write(f"**{item['quantidade']}x** {item['produto']}")
        with c2:
            st.write(f"R$ {item['subtotal']:.2f}")
        with c3:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.carrinho.pop(i)
                st.rerun()
        total_carrinho += item["subtotal"]
    
    st.markdown(f"### Total do Carrinho: R$ {total_carrinho:.2f}")
    
    st.markdown("---")
    st.subheader("💳 Forma de Pagamento")
    forma_pagamento = st.selectbox("Selecione a forma de pagamento:", ["Dinheiro", "Cartão de Crédito/Débito", "Pix"])
    
    if forma_pagamento == "Dinheiro":
        valor_recebido = st.number_input("Valor recebido do cliente (R$):", min_value=0.0, step=1.0, value=float(total_carrinho))
        if valor_recebido >= total_carrinho:
            troco = valor_recebido - total_carrinho
            st.info(f"Troco a devolver: **R$ {troco:.2f}**")
        else:
            st.warning("O valor recebido é menor que o total da compra!")
    
    if st.button("Finalizar Compra"):
        if tipo_pedido == "Para Entregar (Delivery)" and not endereco_entrega.strip():
            st.error("Por favor, preencha o endereço de entrega.")
        elif forma_pagamento == "Dinheiro" and valor_recebido < total_carrinho:
            st.error("Não é possível finalizar: valor recebido insuficiente.")
        else:
            pedido_final = {
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "tipo": tipo_pedido,
                "endereco": endereco_entrega if tipo_pedido == "Para Entregar (Delivery)" else "Retirada no local",
                "itens": list(st.session_state.carrinho),
                "total": total_carrinho,
                "pagamento": forma_pagamento
            }
            st.session_state.historico.append(pedido_final)
            st.session_state.carrinho = []
            st.success("Compra finalizada com sucesso e salva no histórico!")
            st.rerun()
else:
    st.info("O seu carrinho está vazio.")

st.markdown("---")
st.subheader("📋 Histórico de Pedidos")

if len(st.session_state.historico) > 0:
    for i, pedido in enumerate(st.session_state.historico):
        with st.expander(f"Pedido #{i+1} - {pedido['tipo']} - {pedido['data']} - R$ {pedido['total']:.2f}"):
            st.write(f"**Modo:** {pedido['tipo']}")
            if pedido['tipo'] == "Para Entregar (Delivery)":
                st.write(f"**Endereço:** {pedido['endereco']}")
            st.write(f"**Pagamento:** {pedido['pagamento']}")
            st.markdown("**Itens:**")
            for item in pedido["itens"]:
                st.write(f"- {item['quantidade']}x {item['produto']} (R$ {item['subtotal']:.2f})")
    
    if st.button("Limpar Histórico"):
        st.session_state.historico = []
        st.rerun()
else:
    st.info("Nenhum pedido finalizado ainda.")