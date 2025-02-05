import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import flet as ft

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

cursor.execute("SELECT titulo FROM noticias ORDER BY data_extração DESC LIMIT 10")
noticias = cursor.fetchall()

cursor.close()
db.close()

def main(page):
    page.add(ft.Column([ft.Text(n[0], size=18) for n in noticias]))

ft.app(target=main)
