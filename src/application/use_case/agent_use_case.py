import requests
import re

API_URL = "http://localhost:5000/automoveis/search"

def extrair_info(texto, palavra_chave):
    pattern = rf"{palavra_chave}\s+(\w+)"
    m = re.search(pattern, texto, re.IGNORECASE)
    if m:
        return m.group(1)
    return None

def agente_virtual():
    print("Olá! Eu sou seu assistente virtual de carros. Me conte o que você procura.")

    filtros = {}
    perguntas = {
        "marca": ["Qual marca você prefere?", "Quer algum fabricante específico?"],
        "modelo": ["E o modelo, sabe qual quer?", "Tem algum modelo em mente?"],
        "ano": ["Qual o ano do carro?", "Você quer um carro de qual ano?"],
        "combustivel": ["Qual tipo de combustível prefere?", "Gasolina, álcool, diesel...?"],
        "preco_min": ["Qual o valor mínimo que você pretende pagar?"],
        "preco_max": ["Qual o valor máximo?"]
    }

    while True:
        entrada = input("> ").strip()

        if "sair" in entrada.lower():
            print("Até logo! Boa sorte na busca.")
            break

                
        faltantes = [k for k in perguntas if k not in filtros]

        if faltantes:
            chave_atual = faltantes[0]

            if chave_atual in ["preco_min", "preco_max"]:
                m = re.search(r"(\d+)", entrada)
                if m:
                    filtros[chave_atual] = int(m.group(1))
            else:
                val = extrair_info(entrada, chave_atual)
                if not val:
                    val = entrada
                filtros[chave_atual] = val


       
        faltantes = [k for k in perguntas if k not in filtros]
        if faltantes:
            print(perguntas[faltantes[0]][0])
        else:
            
            print("Buscando veículos que correspondem ao que você quer...")
            print("Enviando filtros:", filtros)
            r = requests.post(API_URL, json=filtros)
            print("Status code:", r.status_code)
            print("Resposta:", r.text)

            if r.status_code == 200:
                carros = r.json()
                if not carros:
                    print("Desculpe, não encontrei carros com esses critérios.")
                else:
                    print(f"Encontrei {len(carros)} carro(s) para você:")
                    for c in carros:
                        print(f"- {c['marca']} {c['modelo']} {c['ano']}, {c['cor']}, {c['quilometragem']} km, R$ {c['preco']}")
            else:
                print("Erro ao buscar no servidor.")
            break

if __name__ == "__main__":
    agente_virtual()
