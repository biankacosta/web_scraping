import requests
import re
from bs4 import BeautifulSoup

url = 'https://smd.ufc.br/pt/sobre-o-curso/matrizcurriculardiurno/'

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table')
    tables_n_titles = soup.find_all(["table", "h4"])

    elements = []
    current_h4_text = None
    subjects = []
    last_subject = None

    for t in tables_n_titles:
        if t.name == 'h4':
            text = t.get_text(strip=True)
            if re.search(r'\d', text):
                current_h4_text = re.findall(r'\d+', text)
            else:
                current_h4_text = "-"

        if t.name == 'table':
            rows = t.find_all('tr')[1:]

            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]

                if len(cols) == 6:
                    if not any(word in cols[1] for word in ["ELETIVA", "COMPLEMENTARES", "CONCLUSÃO"]):
                        subject = {
                            'Código': cols[0],
                            'Disciplina': cols[1],
                            'Carga Horária': cols[2],
                            'Créditos': cols[3],
                            'Tipo de Disciplina': cols[4],
                            'Pré-requisito': cols[5],
                            'Semestre': current_h4_text[0]
                        }
                        subjects.append(subject)
                        last_subject = subject

                elif len(cols) == 1 and last_subject:
                    last_subject['Pré-requisito'] += f", {cols[0]}"

    for s in subjects:
        print(s)

else:
    print("Erro")
