import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('livraria.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    titulo TEXT,
    preco TEXT,
    avaliacao TEXT,
    disponibilidade TEXT
)
''')


url = 'https://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

livros = soup.select('article.product_pod')[:10]

for livro in livros:
    titulo = livro.h3.a['title']
    preco = livro.select_one('.price_color').text.strip()
    disponibilidade = livro.select_one('.availability').text.strip()

    estrelas = livro.select_one('p.star-rating')['class'][1]  # Ex: 'Three'

    cursor.execute('''
        INSERT INTO livros (titulo, preco, avaliacao, disponibilidade)
        VALUES (?, ?, ?, ?)
    ''', (titulo, preco, estrelas, disponibilidade))

conn.commit()
conn.close()

print("✅ Informações dos livros salvas no banco 'livraria.db'.")
