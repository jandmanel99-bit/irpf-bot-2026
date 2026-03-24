import streamlit as st
import urllib.parse
import sys
import os
from streamlit.web import cli as stcli

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IRPF 2026 - Janderson", page_icon="🦁")

# --- 1. SAUDAÇÃO INICIAL ---
st.title("🦁 Assistente Virtual - IRPF 2026")
st.markdown("""
**Olá! Eu sou a assistente virtual de Janderson, tudo bem?** Estou aqui para ajudá-lo a reunir as informações necessárias para a **Declaração do IRPF 2026**.  
Também estarei organizando vocês para atendimento.
""")
st.divider()

if st.checkbox("✅ Podemos iniciar?"):
    
    # --- 2. DADOS PESSOAIS ---
    st.markdown("### 📝 Dados Pessoais")
    nome = st.text_input("Qual o seu nome completo?")
    cpf = st.text_input("Me informa seu CPF?")
    
    st.markdown("---")
    st.markdown("#### 🏠 Endereço")
    col1, col2 = st.columns(2)
    with col1:
        rua = st.text_input("Nome da Rua")
        numero = st.text_input("Número + Complemento")
    with col2:
        bairro = st.text_input("Bairro")
        cep = st.text_input("CEP")
    
    # --- 3. DADOS FAMILIARES ---
    st.markdown("---")
    st.markdown("#### 💍 Família")
    casado = st.radio("É casado(a)?", ["Não", "Sim"], horizontal=True)
    cpf_conjuge = ""
    if casado == "Sim":
        st.info("Precisaremos do CPF do seu/sua Cônjuge")
        cpf_conjuge = st.text_input("CPF do Cônjuge")

    filhos = st.radio("Tem filhos?", ["Não", "Sim"], horizontal=True)
    detalhes_filhos = ""
    if filhos == "Sim":
        st.info("Digite o CPF, Nome completo e Data de Nascimento dos filhos")
        detalhes_filhos = st.text_area("Ex: 123.456.789-10, João da Silva, 10/05/2015")

    # --- 4. FINANCEIRO ---
    st.markdown("---")
    st.markdown("#### 🚗 Veículos")
    
    tem_veiculo = st.radio("Possui Veículo?", ["Não", "Sim"], horizontal=True)
    
    tipo_veiculo = "" 
    detalhes_veiculo = ""
    
    if tem_veiculo == "Sim":
        tipo_veiculo = st.radio("Situação do Veículo:", ["Quitado", "Financiado"], horizontal=True)
        st.markdown(f"**Preencha os dados do Veículo ({tipo_veiculo}):**")
        
        if tipo_veiculo == "Quitado":
            # Cria colunas para organizar lado a lado
            c1, c2 = st.columns(2)
            with c1:
                v_modelo = st.text_input("Marca e Modelo")
                v_placa = st.text_input("Placa e Renavam")
                v_valor = st.text_input("Valor Pago (R$)")
            with c2:
                v_ano = st.text_input("Ano de Fabricação")
                v_data = st.text_input("Data da Compra")
                v_vendedor = st.text_input("Comprou de quem? (Nome/CPF, se tiver)")
            
            # Monta o texto final juntando tudo
            detalhes_veiculo = (f"Veículo: {v_modelo}\n"
                                f"   Ano: {v_ano} | Placa/Renavam: {v_placa}\n"
                                f"   Data Compra: {v_data} | Valor: R$ {v_valor}\n"
                                f"   Vendedor: {v_vendedor}")
            
        else: # Financiado
            c1, c2 = st.columns(2)
            with c1:
                f_modelo = st.text_input("Descrição (Marca/Modelo)")
                f_total = st.text_input("Valor Total Financiado (R$)")
                f_entrada = st.text_input("Valor Entrada + Parcelas Pagas")
            with c2:
                f_ano = st.text_input("Ano Fabricação")
                f_nf = st.text_input("Valor da Nota Fiscal (R$)")
                f_contrato = st.text_input("Número do Contrato")
            
            # Monta o texto final juntando tudo
            detalhes_veiculo = (f"Financiado: {f_modelo} ({f_ano})\n"
                                f"   Contrato: {f_contrato}\n"
                                f"   Valor NF: R$ {f_nf} | Financiado: R$ {f_total}\n"
                                f"   Pago em 2025: R$ {f_entrada}")

    st.markdown("---")
    st.markdown("#### 💰 Bens, Investimentos e Dívidas")

    # --- OUTROS BENS (CORRIGIDO: Sem barra azul, com placeholder) ---
    tem_bens = st.radio("Possui outros bens?", ["Não", "Sim"], horizontal=True)
    lista_bens = ""
    if tem_bens == "Sim":
        lista_bens = st.text_area("Descreva os bens:", placeholder="Ex: Casa, Terreno, Apartamento financiado...")
    
    # --- INVESTIMENTOS (CORRIGIDO: Sem barra azul) ---
    tem_invest = st.radio("Possui Investimentos?", ["Não", "Sim"], horizontal=True)
    detalhe_invest = ""
    if tem_invest == "Sim":
        detalhe_invest = st.text_area("Descrição dos Investimentos:", placeholder="Ex: Bolsa, Ações, Poupança, CDB, Tesouro Direto...")

    # --- EMPRÉSTIMOS ---
    tem_emprestimo = st.radio("Possui Empréstimos/Dívidas Bancárias?", ["Não", "Sim"], horizontal=True)
    detalhe_emprestimo = ""
    if tem_emprestimo == "Sim":
        detalhe_emprestimo = st.text_area("Descrição da Dívida:", placeholder="Ex: Banco do Brasil - Empréstimo Pessoal - Valor Total Devido - Valor Pago em 2025...")

    # --- 5. AVISO DE DOCUMENTOS ---
    st.markdown("---")
    st.warning("⚠️ **ATENÇÃO: DOCUMENTOS NECESSÁRIOS**")
    st.markdown("""
    Ao clicar no botão abaixo para abrir o WhatsApp, por favor, **anexe fotos ou PDFs** dos seguintes documentos:
    
    * 📄 **Declaração Entregue do Ano Anterior**
    * 🧾 **Recibo de Entrega**
    * 🏠 **Documentos de Imóveis** (Escrituras, Contratos)
    * 🚗 **Documentos do Veículo** (CRLV, Nota Fiscal ou Contrato de Financiamento)
    * 💰 **Informes de Rendimento** (Salários e Bancos/Investimentos)
    * 💸 **Informes de Dívidas e Ônus** (Se houver empréstimos)
    """)

    # --- 6. BOTÃO FINAL ---
    st.markdown("---")
    if st.button("Enviar Respostas para o WhatsApp 📲"):
        if nome and cpf:
            # O nome dentro dos colchetes deve ser exatamente o que você salvou no painel
            PHONE = st.secrets["PHONE"]
            
            # --- Preparando os textos auxiliares ---
            txt_conjuge = f"(CPF: {cpf_conjuge})" if casado == "Sim" else ""
            txt_filhos = f"\n--> {detalhes_filhos}" if filhos == "Sim" else ""
            
            # Texto do Veículo
            txt_veiculo = ""
            if tem_veiculo == "Sim":
                txt_veiculo = f"\n--> SITUAÇÃO: {tipo_veiculo}\n--> DETALHES:\n{detalhes_veiculo}"

            txt_bens = f"\n--> {lista_bens}" if tem_bens == "Sim" else ""
            txt_invest = f"\n--> {detalhe_invest}" if tem_invest == "Sim" else ""
            txt_emprestimo = f"\n--> {detalhe_emprestimo}" if tem_emprestimo == "Sim" else ""

            # --- EXTRAI O PRIMEIRO NOME PARA O TÍTULO ---
            primeiro_nome = nome.split()[0].title() if nome else "Cliente"

            # --- MENSAGEM FINAL ---
            msg = f"""*{primeiro_nome} - IRPF 2026*

👤 *Nome:* {nome}
🆔 *CPF:* {cpf}
🏠 *Endereço:* {rua}, {numero} - {bairro}
💍 *Casado:* {casado} {txt_conjuge}
👶 *Filhos:* {filhos} {txt_filhos}
🚗 *Veículo:* {tem_veiculo} {txt_veiculo}
🏡 *Outros Bens:* {tem_bens} {txt_bens}
📈 *Investimentos:* {tem_invest} {txt_invest}
💸 *Empréstimos:* {tem_emprestimo} {txt_emprestimo}

⚠️ *Estou enviando os documentos solicitados em seguida (Declaração anterior, Recibo, Bens, Informes e Dívidas).*"""
            
            # Cria o link
            link = f"https://wa.me/{PHONE}?text={urllib.parse.quote(msg)}"
            
            st.success(f"✅ Tudo pronto, {primeiro_nome}! Clique abaixo para enviar:")
            st.markdown(f"### [👉 CLIQUE AQUI - ENVIAR PARA JANDERSON]({link})")
        else:
            st.error("Por favor, preencha pelo menos Nome e CPF.")

# --- AUTO-START ---
if __name__ == '__main__':
    if st.runtime.exists():
        pass
    else:
        sys.argv = ["streamlit", "run", os.path.abspath(__file__)]
        sys.exit(stcli.main())
