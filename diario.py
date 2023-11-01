import streamlit as st
import sqlite3
from PIL import Image

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

# Função para ler e atualizar o contador a partir do banco de dados
def update_counter():
    conn = sqlite3.connect("counter.db")
    cursor = conn.cursor()

    # Verifica se a tabela de contador já existe
    cursor.execute("CREATE TABLE IF NOT EXISTS counter (count INTEGER)")

    # Obtém o contador atual
    cursor.execute("SELECT count FROM counter")
    result = cursor.fetchone()

    if result:
        count = result[0]
        count += 1
        cursor.execute("UPDATE counter SET count = ?", (count,))
    else:
        cursor.execute("INSERT INTO counter (count) VALUES (1)")
        count = 1

    conn.commit()
    conn.close()
    return count

# Obtém o contador atual
access_count = update_counter()

# Página Streamlit
st.title("Contador de Acessos")
st.write(f"Esta página foi acessada {access_count} vezes.")

def main():
    st.title("Bíblia: Conexões e reflexões")

    # Definir a imagem de fundo
    background_image = Image.open("biblia.jpg")
    st.image(background_image, use_column_width=True, caption="")

    conn = setup_database()

    # Lado esquerdo da tela para inserção de texto
    st.sidebar.title("Inserir Texto")
    data = st.sidebar.date_input("Data:", help="Selecione a data da entrada.", format="DD/MM/YYYY")
    texto = st.sidebar.text_area("Texto:", help="Digite sua entrada de diário")
    
    if st.sidebar.button("Entrada de Texto"):
        if data and texto:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO entradas_diario (data, texto) VALUES (?, ?)", (data, texto))
            conn.commit()
            st.sidebar.success("Entrada de texto adicionada com sucesso!")

    if st.sidebar.button("Limpar Tela"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entradas_diario")
        conn.commit()
        st.sidebar.success("Banco de dados limpo com sucesso!")

    cursor = conn.cursor()
    cursor.execute("SELECT data, texto FROM entradas_diario ORDER BY data DESC")  # Ordenar por data decrescente
    entries = cursor.fetchall()

    # Dividir a tela em duas colunas
    col1, col2 = st.columns(2)

    for i, entry in enumerate(entries):
        # Use uma formatação personalizada para criar uma chave única
        if i % 2 == 0:
            with col1:
                st.write(f"**Data:** {entry[0]}", key=f"data_{entry[0]}")
                st.write(f"**Texto:** {entry[1]}", key=f"texto_{entry[0]}")
        else:
            with col2:
                st.write(f"**Data:** {entry[0]}", key=f"data_{entry[0]}")
                st.write(f"**Texto:** {entry[1]}", key=f"texto_{entry[0]}")

if __name__ == "__main__":
    main()
