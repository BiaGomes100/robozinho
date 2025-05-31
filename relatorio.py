from openpyxl import Workbook
from datetime import datetime
import sqlite3


wb = Workbook()

conn1 = sqlite3.connect('paises.db')
cursor1 = conn1.cursor()
cursor1.execute('SELECT * FROM paises')
paises = cursor1.fetchall()
headers_paises = [desc[0] for desc in cursor1.description]

ws1 = wb.active
ws1.title = "Países"
ws1.append(["Relatório - Países", "", "", "", f"Aluno: Bianca Gomes", f"Data: {datetime.today().strftime('%d/%m/%Y')}"])
ws1.append([]) 
ws1.append(headers_paises)
for pais in paises:
    ws1.append(pais)
conn1.close()

conn2 = sqlite3.connect('livraria.db')
cursor2 = conn2.cursor()
cursor2.execute('SELECT * FROM livros')
livros = cursor2.fetchall()
headers_livros = [desc[0] for desc in cursor2.description]

ws2 = wb.create_sheet(title="Livros")
ws2.append(["Relatório - Livros", "", "", "", f"Aluno: Seu Nome", f"Data: {datetime.today().strftime('%d/%m/%Y')}"])
ws2.append([])
ws2.append(headers_livros)
for livro in livros:
    ws2.append(livro)
conn2.close()

wb.save("relatorio_final.xlsx")
print("✅ Relatório gerado como 'relatorio_final.xlsx'.")