import csv
import json


def limpar_valor(valor):
    if not valor:
        #Se estiver vazio retorna nada.
        return None

    try:
        #Se tiver ponto ou vírgula, tentamos tratar como número decimal (float).
        if '.' in valor or ',' in valor:
            return float(valor.replace(',','.'))
        
        #Se não tem ponto/vírgula, tentamos converter para números inteiros
        return int(valor)
    
    except ValueError:
        #Se der erro na conversão (ex: é um texto como "ARAUCO").
        #Retornamos o valor original.
        return valor

def processar_arquivo(caminho_arquivo):
    print(f"Iniciando Leitura de: {caminho_arquivo}...")

    #Lista principal que vai guardar os módulos (Nível 01)
    lista_final = []
    # Ponteiros
    # Estas variáveis vão guardar a "referência" do último pai encontrado.
    # Em Python, dicionários são objetos mutáveis. Se eu guardo o dicionário
    # na variável 'nivel_atual_1' e adiciono algo nele, isso reflete na 'lista_final'
    nivel_atual_1 = None #Vai guardar o último Módulo
    nivel_atual_2 = None #Vai guardar a último Peça
    nivel_atual_3 = None #Vai guardar o último Material/Ferragem

    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8', errors='replace') as arquivo_csv:
            # O DictReader lê cada linha e já transforma num dicionário
            # onde a chave é o cabeçalho e o valor é o dado da linha.
            # delimiter='\t' avisa que é separado por TABULAÇÃO, não vírgula.
            leitor = csv.DictReader(arquivo_csv, delimiter='\t')
            # Limpa os nomes das colunas (tira espaços extras do cabeçalho)
            leitor.fieldnames = [nome.strip() for nome in leitor.fieldnames]
            for linha in leitor:
                # 1. Cria um dicionário limpo para a linha atual
                # (Usamos nossa função limpar_valor para arrumar números)
                item_limpo = {k: limpar_valor(v) for k, v in linha.items() if k}
                try:
                    nivel = int(item_limpo.get('NIVEL_WPS', 0))
                except:
                    continue #Se não tiver, nível pula a linha
                item_limpo['components'] = []
                if nivel == 1:
                    lista_final.append(item_limpo)
                    nivel_atual_1 = item_limpo
                    nivel_atual_2 = None
                    nivel_atual_3 = None
                elif nivel == 2:
                    if nivel_atual_1 is not None:
                        nivel_atual_1['components'].append(item_limpo)
                        nivel_atual_2 = item_limpo
                elif nivel == 3:
                    if nivel_atual_2 is not None:
                        nivel_atual_2['components'].append(item_limpo)
                        nivel_atual_3 = item_limpo
                elif nivel == 4:
                    if nivel_atual_3 is not None:
                        nivel_atual_3['components'].append(item_limpo)
    except FileNotFoundError:
        print('Erro: O arquivo não foi encontrado.')
        return []
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return []
    
    print('Conversão concluída com sucesso!')
    return lista_final


if __name__ == "__main__":
    nome_arquivo = 'ExportWPS_1.TXT'
    dados_json = processar_arquivo(nome_arquivo)

    with open('resultado_importacao.json', 'w', encoding='utf-8') as f:
        json.dump(dados_json, f, indent=4, ensure_ascii=False)
    print(f"Arquivo 'resultado_importacao.json' gerado com {len(dados_json)} módulos principais.")