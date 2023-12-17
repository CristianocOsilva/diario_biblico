# Importação de bibliotecas
import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
from datetime import datetime
import pybible  

# Classe principal do aplicativo
class DiarioApp:
    def __init__(self):
        # Configuração do banco de dados do diário
        self.conn_diario = self.setup_diario_database()
        # Configuração do banco de dados de usuários
        self.conn_users = self.setup_users_database()
        
                

    # Método para configurar o banco de dados do diário
    def setup_diario_database(self):
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

    # Método para configurar o banco de dados de usuários
    def setup_users_database(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                senha TEXT
            )
        """)
        conn.commit()
        return conn

    # Método para inserir uma entrada no diário
    def insert_entry(self, data, texto):
        cursor = self.conn_diario.cursor()
        cursor.execute("INSERT INTO entradas_diario (data, texto) VALUES (?, ?)", (data, texto))
        self.conn_diario.commit()

    # Método para limpar as entradas do diário
    def clear_entries(self):
        cursor = self.conn_diario.cursor()
        cursor.execute("DELETE FROM entradas_diario")
        self.conn_diario.commit()

    # Método para obter as últimas entradas do diário
    def get_entries(self, num_entries=5):
        cursor = self.conn_diario.cursor()
        cursor.execute("SELECT data, texto FROM entradas_diario ORDER BY data DESC LIMIT ?", (num_entries,))
        entries = cursor.fetchall()
        return entries

    # Método para registrar um novo usuário
    def register_user(self, email, senha):
        cursor = self.conn_users.cursor()
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha))
        self.conn_users.commit()

    # Método para obter um versículo da Bíblia
    def get_bible_verse(self, book, chapter, verse):
        try:
            verse_text = pybible.get_verse(book=book, chapter=chapter, verse=verse)
            return verse_text
        except Exception as e:
            return f"Erro ao obter o versículo: {e}"

# Função para atualizar o contador de acessos
def update_counter():
    conn = sqlite3.connect("counter.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS counter (count INTEGER)")
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

# Função principal do aplicativo
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

    # Carousel de Fotos
    st.subheader("Carousel de Fotos")
    photos = ["biblia.jpg", "biblia.jpg", "biblia.jpg"]  # Substitua pelos seus nomes de arquivo reais
    selected_photo = st.selectbox("Escolha uma foto:", photos)
    st.image(selected_photo, use_column_width=True, caption="")

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

    # Texto rolante usando HTML personalizado
    st.subheader("Texto Rolante")
    st.markdown(f'<marquee direction="left" style="font-size: 18px;">{texto}</marquee>', unsafe_allow_html=True)

    st.subheader("Consulta à Bíblia")
    book = st.selectbox("Livro:", ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"])  # Adicione mais conforme necessário
    chapter = st.number_input("Capítulo:", min_value=1, max_value=150, value=1)
    verse = st.number_input("Versículo:", min_value=1, value=1)

    if st.button("Consultar Versículo"):
        verse_text = diario_app.get_bible_verse(book, chapter, verse)
        st.write(f"Versículo {book} {chapter}:{verse} - {verse_text}")


    # Menu de Cadastro de Email e Senha
    st.sidebar.title("Cadastro de Usuário")
    email = st.sidebar.text_input("Email:", help="Digite seu email")
    senha = st.sidebar.text_input("Senha:", type="password", help="Digite sua senha")

    if st.sidebar.button("Cadastrar"):
        if email and senha:
            diario_app.register_user(email, senha)
            st.sidebar.success("Cadastro realizado com sucesso!")

# Verifica se o código está sendo executado diretamente
if __name__ == "__main__":
    main()
