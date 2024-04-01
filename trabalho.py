from flask import Flask

import requests

app = Flask(__name__)

def ordenar_por_nome(cidade):
    """
    Função auxiliar para ordenar as cidades por nome.
    """
    return cidade['nome']

def obter_cidades_ordenadas_por_nome():
    """
    Obtém uma lista de cidades ordenadas por nome.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    response = requests.get(url)
    
    if response.status_code == 200:
        return sorted(response.json(), key=ordenar_por_nome)
    else:
        return None

def obter_cidades_por_estado():
    """
    Obtém as cidades agrupadas por estado.
    """
    url_estados = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    response_estados = requests.get(url_estados)
    
    if response_estados.status_code == 200:
        cidades_por_estado = {}
        estados = response_estados.json()
        for estado in estados:
            estado_sigla = estado['sigla']
            url_estado = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado['id']}/municipios"
            response_estado = requests.get(url_estado)
            if response_estado.status_code == 200:
                cidades_estado = sorted(response_estado.json(), key=ordenar_por_nome)
                cidades_por_estado[estado_sigla] = cidades_estado
            else:
                return None
        return cidades_por_estado
    else:
        return None

@app.route('/')
def index():
    cidades_ordenadas = obter_cidades_ordenadas_por_nome()
    cidades_por_estado = obter_cidades_por_estado()
    return f"Cidades Ordenadas: {cidades_ordenadas}\nCidades por Estado: {cidades_por_estado}"

if __name__ == "__main__":
    app.run(debug=True)
