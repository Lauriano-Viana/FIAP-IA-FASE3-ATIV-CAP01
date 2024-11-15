import cx_Oracle
import pandas as pd
import os

def get_leitura(conexao): # buscar os dados da ultima leitura executada
    cursor = conexao.cursor()
    cursor.execute("SELECT seq_leituras.CURRVAL FROM dual")
    id_leitura = cursor.fetchone()
    consulta = f""" SELECT id_leitura,id_cultura,leit_p,leit_k,leit_ph,leit_umidade FROM leituras WHERE id_leitura = {id_leitura}"""
    cursor.execute(consulta)
    leitura = cursor.fetchone()
    return leitura

def get_cultura(conexao,id_cultura): # buscar dados refentes a cultura da leitura
    cursor = conexao.cursor()
    cursor.execute(f"SELECT nome, nivel_p, nivel_k, nivel_ph, umidade FROM culturas WHERE id_cultura = '{id_cultura}'")
    cultura = cursor.fetchone()
    return cultura

def verificar_nutrientes(cultura,leitura):
    # dados referentes a leitura 
    valor_p = leitura[3]
    valor_k = leitura[4]
    valor_ph = leitura[5]
    valor_umidade = leitura[6]
   
    # dados referentes aos valores da cultura 
    cultura_p, cultura_k ,cultura_ph ,cultura_umidade = cultura

    tempo = 2000 # valor de tempo para irrigação niveis normais
    if any(valor < cultura for valor, cultura in 
       [(valor_p, cultura_p), (valor_k, cultura_k), (valor_ph, cultura_ph), (valor_umidade, cultura_umidade)]):
        tempo = 3000
    return tempo

def deletar_irrigacao(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados
        id_irrigacao = int(input('Informe o id da irrigacao a ser deletada'))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM irrigacoes WHERE id_irrigacao = {id_irrigacao}"""
        cursor.execute(consulta)
        data = cursor.fetchall()

        for dt in data:
            lista_dados.append(dt)
        
        if len(lista_dados)==0:
            print(f'Não há uma irrigacao cadastrada com o ID = {id_irrigacao}')
        else:
            exclusao = f"""DELETE FROM irrigacoes WHERE id_irrigacao = {id_irrigacao} """
            cursor.execute(exclusao)
            conexao.commit()
            print(f"Leitura {id_irrigacao} deletado com sucesso.")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao deletar leitura: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione qualquer tecla para continuar')

# Função para listar irrigacoes
def listar_irrigacoes(conexao):
    try:
        lista_dados = [] #lista para captura de dados 
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM irrigacoes ")
        #Captura os registros e armazena no obj aplicacoes
        aplicacoes = cursor.fetchall()
        for aplicacao in aplicacoes:
            lista_dados.append(aplicacao)
        lista_dados = sorted(lista_dados)
        # Gera um Dataframe com os dados da lista usando o Pandas
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id','Id_cultura','Id_leitura','tempo','data'], 
                                             index ='Id')
        if dados_df.empty:
            print(f'Não há irrigacoes cadastradas!!')
        else:
            print(dados_df)
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao listar irrigacao: {e}")
    except:
        print('Erro desconhecido')
        input('Digite enter para continuar')
    else:
        input('Digite enter para continuar')

# Procedimento para criar irrigação de cultura com base na leitura
def aplicar_irrigacao(conexao):
    cursor = conexao.cursor()
    leitura = get_leitura(conexao)
    id_leitura,id_cultura,leit_p,leit_k,leit_ph,leit_umidade = leitura
    cultura = get_cultura(conexao,id_cultura)
    tempo = verificar_nutrientes(leitura, cultura)
    if tempo > 2000:
        motivo = f'Nivel de nutrientes: BAIXO, tempo de irrigação mais longo {tempo/1000} segundos'
    else:
        motivo = f'Nivel de nutrientes: NORMAL, tempo de irrigação {tempo/1000} segundos'
    cursor.execute("""
        INSERT INTO irrigacoes 
        (id_irrigacao,id_cultura, id_leitura, tempo, motivo, data_aplicacao) 
        VALUES (seq_irrigacoes.NEXTVAL, :1, :2, :3, :4, :5, SYSDATE)
    """, (id_cultura, id_leitura, tempo, motivo))
    conexao.commit()
    cursor.close()

def menu_irrigacao(conexao,conectado):
    while conectado:
        os.system('clear')
        print('-----------Operacoes Irrigacao-----------------')
        print("""
        1 - Listar Irrigacoes
        2 - Excluir Irrigacao
        3 - Menu Inicial
        """)
        escolha = input('Escolha -> ')

        if escolha.isdigit():
            escolha = int(escolha)
        else:
            escolha = 3
            print('Digite um numero.\nReinicie a Aplicação!')
        os.system('clear')
        match escolha:
            case 1:
                listar_irrigacoes(conexao)
            case 2:
                deletar_irrigacao(conexao)
            case 3:
                conectado = False
            case _:
                input('Digite um numero entre 1 e 3.')