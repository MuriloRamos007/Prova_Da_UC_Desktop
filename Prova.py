import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import flet as ft
from functools import partial

url = 'https://g1.globo.com/'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

titulos = soup.find_all('a', class_='feed-post-link')

titulos_noticias = [titulo.get_text() for titulo in titulos]

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="noticias_db"
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS noticias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo TEXT,
    data_extração DATETIME
)
""")

for titulo in titulos_noticias:
    data_extração = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO noticias (titulo, data_extração) VALUES (%s, %s)"
    val = (titulo, data_extração)
    cursor.execute(sql, val)

db.commit()
cursor.close()
db.close()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="noticias_db"
)

cursor = db.cursor()

cursor.execute("SELECT id, titulo, data_extração FROM noticias ORDER BY data_extração DESC LIMIT 10")
noticias = cursor.fetchall()

cursor.close()
db.close()

def show_details(page, noticia_id, e=None):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="noticias_db"
    )
    
    cursor = db.cursor()
    cursor.execute("SELECT titulo, data_extração FROM noticias WHERE id = %s", (noticia_id,))
    noticia = cursor.fetchone()
    cursor.close()
    db.close()

    if noticia:
        page.clean()
        app_bar = ft.AppBar(
            title=ft.Text("Notícias Recentes", size=22, weight=ft.FontWeight.BOLD),
            center_title=True,
            leading=ft.IconButton(ft.Icons.HOUSE, on_click=lambda e: show_home(page))
        )
        
        page.add(
            app_bar,
            ft.Text(f"Detalhes da Notícia", size=32, weight=ft.FontWeight.BOLD),
            ft.Text(f"Título: {noticia[0]}", size=18),
            ft.Text(f"Data de extração: {noticia[1]}", size=16),
        )
        page.update()

def show_home(page):
    page.clean()

    app_bar = ft.AppBar(
        title=ft.Text("Notícias Recentes", size=22, weight=ft.FontWeight.BOLD),
        center_title=True,
        leading=ft.IconButton(ft.Icons.HOUSE, on_click=lambda e: show_home(page))
    )

    header = ft.Text("Notícias Recentes", size=24, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Escolha uma notícia para ver os detalhes.", size=16)

    componentes = []
    for i, n in enumerate(noticias):
        componentes.append(ft.Text(f"\n{i+1}. {n[1]}", size=18, weight=ft.FontWeight.BOLD))
        componentes.append(ft.Text(f"{n[2]}", size=12))
        componentes.append(
            ft.ElevatedButton(
                "Ver detalhes", 
                on_click=partial(show_details, page, n[0])
            )
        )

    page.add(app_bar, header, subtitle, *componentes)
    page.update()

def main(page):
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK
    show_home(page)

ft.app(target=main)
