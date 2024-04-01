import requests

def obter_cidades_ordenadas_por_nome():
    """
    Obtém uma lista de cidades ordenadas por nome e as imprime.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    response = requests.get(url)
    
    if response.status_code == 200:
        cidades = sorted(response.json(), key=lambda cidade: cidade['nome'])
        print("Lista de cidades ordenadas por nome:")
        for cidade in cidades:
            print(cidade['nome'])
    else:
        print("Erro ao acessar a API")

def agrupar_cidades_por_estado():
    """
    Agrupa as cidades por estado, ordena-as por nome e imprime o resultado.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    response = requests.get(url)
    
    if response.status_code == 200:
        estados = response.json()
        print("Agrupamento de cidades por estado:")
        for estado in estados:
            print(f"Estado: {estado['sigla']}")
            url_estado = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado['id']}/municipios"
            response_estado = requests.get(url_estado)
            
            if response_estado.status_code == 200:
                cidades_estado = sorted(response_estado.json(), key=lambda cidade: cidade['nome'])
                for cidade in cidades_estado:
                    print(f"- {cidade['nome']}")
            else:
                print("Erro ao acessar a API")
            print()
    else:
        print("Erro ao acessar a API")

def gerar_relatorio():
    """
    Gera um relatório em texto sobre as cidades ordenadas por nome e agrupadas por estado.
    """
    with open("relatorio.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write("Relatório sobre cidades brasileiras:\n\n")
        arquivo.write("1. Lista de cidades ordenadas por nome:\n")
        url_cidades = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        response_cidades = requests.get(url_cidades)
        if response_cidades.status_code == 200:
            cidades = sorted(response_cidades.json(), key=lambda cidade: cidade['nome'])
            for cidade in cidades:
                arquivo.write(f"- {cidade['nome']}\n")
        else:
            arquivo.write("Erro ao acessar a lista de cidades.\n")
        
        arquivo.write("\n2. Agrupamento de cidades por estado:\n")
        url_estados = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        response_estados = requests.get(url_estados)
        if response_estados.status_code == 200:
            estados = response_estados.json()
            for estado in estados:
                arquivo.write(f"Estado: {estado['sigla']}\n")
                url_estado = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado['id']}/municipios"
                response_estado = requests.get(url_estado)
                if response_estado.status_code == 200:
                    cidades_estado = sorted(response_estado.json(), key=lambda cidade: cidade['nome'])
                    for cidade in cidades_estado:
                        arquivo.write(f"  - {cidade['nome']}\n")
                else:
                    arquivo.write("  Erro ao acessar a lista de cidades deste estado.\n")
                arquivo.write("\n")
        else:
            arquivo.write("Erro ao acessar a lista de estados.\n")

if __name__ == "__main__":
    obter_cidades_ordenadas_por_nome()
    print("\n")
    agrupar_cidades_por_estado()
    gerar_relatorio()
    print("Relatório gerado com sucesso!")
