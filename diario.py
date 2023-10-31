import streamlit as st
import sqlite3

# Configurando a conexão com o banco de dados SQLite
def setup_database():
    conn = sqlite3.connect("diario.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entradas_diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE,
            texto TEXT
        )
    """)
    conn.commit()
    return conn

def main():
    st.title("Bíblia: Conexões e reflexões")

    conn = setup_database()

    # Lado esquerdo da tela para inserção de texto
    st.sidebar.title("Inserir Texto")
    data = st.sidebar.date_input("Data:", help="Selecione a data da entrada.", format="DD/MM/YYYY")
    texto = st.sidebar.text_area("Texto:", help="Digite sua entrada de diário.")
    
    if st.sidebar.button("Adicionar Entrada de Texto"):
        if data and texto:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO entradas_diario (data, texto) VALUES (?, ?)", (data, texto))
            conn.commit()
            st.sidebar.success("Entrada de texto adicionada com sucesso!")

    if st.sidebar.button(""):
        data = None
        texto = ""

    # Lado direito da tela para exibição das entradas
    st.title("")
    st.sidebar.title("")
    # Adicione um botão para limpar o banco de dados
    #if st.sidebar.button("Limpar Banco de Dados"):
    #    cursor = conn.cursor()
    #    cursor.execute("DELETE FROM entradas_diario")
    #    conn.commit()
    #    st.sidebar.success("Banco de dados limpo com sucesso!")

    cursor = conn.cursor()
    cursor.execute("SELECT data, texto FROM entradas_diario")
    entries = cursor.fetchall()

    for entry in entries:
        # Use uma formatação personalizada para criar uma chave única
        st.write(f"**Data:** {entry[0]}", key=f"data_{entry[0]}")
        st.write(f"**Texto:** {entry[1]}", key=f"texto_{entry[0]}")

if __name__ == "__main__":
    main()
