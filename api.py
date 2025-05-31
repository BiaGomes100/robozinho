import requests
import sqlite3

conn = sqlite3.connect('paises.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS paises (
    nome_comum TEXT,
    nome_oficial TEXT,
    capital TEXT,
    continente TEXT,
    regiao TEXT,
    sub_regiao TEXT,
    populacao INTEGER,
    area REAL,
    moeda_nome TEXT,
    moeda_simbolo TEXT,
    idioma_principal TEXT,
    fuso_horario TEXT,
    url_bandeira TEXT
)
''')


paises = []
for i in range(3):
    pais = input(f"Digite o nome do {i+1}º país: ").strip()
    paises.append(pais)


for pais in paises:
    try:
        response = requests.get(f'https://restcountries.com/v3.1/name/{pais}')
        data = response.json()[0]

        nome_comum = data['name']['common']
        nome_oficial = data['name']['official']
        capital = ', '.join(data.get('capital', ['Desconhecida']))
        continente = ', '.join(data.get('continents', ['Desconhecido']))
        regiao = data.get('region', 'Desconhecida')
        sub_regiao = data.get('subregion', 'Desconhecida')
        populacao = data.get('population', 0)
        area = data.get('area', 0.0)
        moeda_chave = list(data['currencies'].keys())[0]
        moeda_info = data['currencies'][moeda_chave]
        moeda_nome = moeda_info['name']
        moeda_simbolo = moeda_info.get('symbol', '')
        idioma_principal = list(data['languages'].values())[0]
        fuso_horario = ', '.join(data['timezones'])
        url_bandeira = data['flags']['png']

   
        cursor.execute('''
            INSERT INTO paises (
                nome_comum, nome_oficial, capital, continente, regiao, sub_regiao,
                populacao, area, moeda_nome, moeda_simbolo, idioma_principal,
                fuso_horario, url_bandeira
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome_comum, nome_oficial, capital, continente, regiao, sub_regiao,
              populacao, area, moeda_nome, moeda_simbolo, idioma_principal,
              fuso_horario, url_bandeira))

        print(f"✅ Dados do país '{nome_comum}' salvos com sucesso.")
    
    except Exception as e:
        print(f"❌ Erro ao processar o país '{pais}': {e}")

conn.commit()
conn.close()
