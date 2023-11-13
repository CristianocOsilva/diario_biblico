import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
from datetime import datetime

class DiarioApp:
    def __init__(self):
        self.conn = self.setup_database()

    def setup_database(self):
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

    def insert_entry(self, data, texto):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO entradas_diario (data, texto) VALUES (?, ?)", (data, texto))
        self.conn.commit()

    def clear_entries(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM entradas_diario")
        self.conn.commit()

    def get_entries(self, num_entries=5):
        cursor = self.conn.cursor()
        cursor.execute("SELECT data, texto FROM entradas_diario ORDER BY data DESC LIMIT ?", (num_entries,))
        entries = cursor.fetchall()
        return entries

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

def main():
    st.set_page_config(page_title="Bíblia: Conexões e Reflexões", page_icon=":book:")

    st.title("Bíblia: Conexões e reflexões")

    # Adicionando calendário e relógio no topo
    col1, col2, col3 = st.columns(3)
    col1.subheader("Calendário")
    selected_date = col1.date_input("Data Atual", value=datetime.now(), format="DD/MM/YYYY")
    
    col2.subheader("Relógio")
    col2.write(datetime.now().strftime("%H:%M:%S"))

    col3.subheader("Contador de Acessos")
    access_count = update_counter()
    col3.write(f"Esta página foi acessada {access_count} vezes.")

    diario_app = DiarioApp()

    # Definir a imagem de fundo
    background_image = Image.open("biblia.jpg")
    st.image(background_image, use_column_width=True, caption="")

    # Lado esquerdo da tela para inserção de texto
    st.sidebar.title("Inserir Texto")

    data = st.sidebar.date_input("Data:", help="Selecione a data da entrada.", value=datetime.now(), format="DD/MM/YYYY")
    texto = st.sidebar.text_area("Texto:", help="Digite sua entrada de diário")

    if st.sidebar.button("Entrada de Texto"):
        if data and texto:
            diario_app.insert_entry(data, texto)
            st.sidebar.success("Entrada de texto adicionada com sucesso!")

    if st.sidebar.button("Limpar Tela"):
        diario_app.clear_entries()
        st.sidebar.success("Banco de dados limpo com sucesso!")

    # Recuperar entradas e exibir no Streamlit
    entries = diario_app.get_entries(num_entries=5)
    df_entries = pd.DataFrame(entries, columns=["Data", "Texto"])
    st.table(df_entries)

if __name__ == "__main__":
    main()
