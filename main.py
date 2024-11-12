import requests
from bs4 import BeautifulSoup

url = 'https://smd.ufc.br/pt/sobre-o-curso/matrizcurriculardiurno/'

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table')

    subjects = []
    last_subject = None

    for table in tables:
        rows = table.find_all('tr')[1:]

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            if len(cols) == 6:
                if not any(word in cols[1] for word in ["ELETIVA", "COMPLEMENTARES", "CONCLUSÃO"]):
                    pre_requisitos = ", ".join(cols[5:])
                    subject = {
                        'Código': cols[0],
                        'Disciplina': cols[1],
                        'Carga Horária': cols[2],
                        'Créditos': cols[3],
                        'Tipo de Disciplina': cols[4],
                        'Pré-requisito': pre_requisitos
                    }
                    subjects.append(subject)
                    last_subject = subject

            elif len(cols) == 1 and last_subject:
                last_subject['Pré-requisito'] += f", {cols[0]}"

    for s in subjects:
        print(s)

else:
    print("Erro")
