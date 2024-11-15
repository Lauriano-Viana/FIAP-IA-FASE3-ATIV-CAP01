import cx_Oracle
import pandas as pd
import os
from irrigacao import aplicar_irrigacao

def check_cultura(conexao): # Verifica se a cultura está cadastrado
        id_cultura = int(input(f' Digite o id da cultura:   '))
        lista_dados = [] #lista para captura de dados
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM culturas WHERE id_cultura = {id_cultura}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
        if len(lista_dados)==0:
            msg = f'Não há uma cultura cadastrada com o ID = {id_cultura}'
            id_cultura = 0       
        return id_cultura,msg


def check_sensor(conexao): # Verifica se o sensor está cadastrado
        id_sensor = int(input(f' Digite o id do sensor da leitura:   '))
        lista_dados = [] #lista para captura de dados
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM sensores WHERE id_sensor = {id_sensor}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
        if len(lista_dados)==0:
            msg = f'Não há um sensor cadastrado com o ID = {id_sensor}' 
            id_sensor = 0     
        return id_sensor, msg
        
        


'''Operações referente as leituras'''
# Função para criar um nova Leitura
def criar_leitura(conexao):
    try:
        os.system('clear')
        print('-------------CADASTRAR LEITURA------------------\n')
        cursor = conexao.cursor()
        msg1 = ""
        id_cultura,msg = check_cultura(conexao)
        msg1 = msg
        id_sensor,msg = check_sensor(conexao)
        msg1 += '\n' + msg
        if  (id_sensor == 0) or (id_cultura == 0):
            print(msg1)
        else:
            valor_p = float(input(' Digite a valor de Fosforo (P):   '))
            valor_k = float(input(' Digite a valor de Potassio(K):   '))
            valor_ph = float(input(' Digite a valor de PH do solo:   '))
            valor_umidade = float(input(' Digite a valor de umidade:   '))
            cadastro = f"""
                INSERT INTO leituras (id_leitura,id_cultura,id_sensor, leit_p,leit_k,leit_ph,leit_umidade, data_leitura)
                VALUES (seq_leituras.NEXTVAL,{id_cultura},{id_sensor},{valor_p},{valor_k},{valor_ph},{valor_umidade} SYSDATE)
                
            """
            cursor.execute(cadastro)
            conexao.commit()
            cursor.close()
            print('Leitura criada com sucesso!!')
                  

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao criar leitura: {e}")
    except ValueError:
        print(' Digite somente numero(s) no(s) campo(s) solicitado(s) ')
    except:
        print('Erro desconhecido')
    input(' Pressione enter para continuar')

# Função para listar leituras
def listar_leituras(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados 
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM leituras")
        #Captura os registros e armazena no obj leituras
        leituras = cursor.fetchall()
        for leitura in leituras:
            lista_dados.append(leitura)
        lista_dados = sorted(lista_dados)
        # Gera um Dataframe com os dados da lista usando o Pandas
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id','id_cultura','id_sensor','valor_p','valor_k','valor_ph','valor_umidade','data_leitura'], 
                                             index ='Id')
        if dados_df.empty:
            print(f'Não há leituras cadastradas!!')
        else:
            print(dados_df)
        print('\nLISTADOS!')
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao ler leituras: {e}")
    input(' Pressione enter para continuar')


# Função para deletar um sensor
def deletar_leitura(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados
        id_leitura = int(input('Informe o id da leitura a ser deletada'))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM leituras WHERE id_leitura = {id_leitura}"""
        cursor.execute(consulta)
        data = cursor.fetchall()

        for dt in data:
            lista_dados.append(dt)
        
        if len(lista_dados)==0:
            print(f'Não há uma leitura cadastrada com o ID = {id_leitura}')
        else:
            exclusao = f"""DELETE FROM leituras WHERE id_leitura = {id_leitura} """
            cursor.execute(exclusao)
            conexao.commit()
            print(f"Leitura {id_leitura} deletado com sucesso.")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao deletar leitura: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione qualquer tecla para continuar')

# Função para criar um Menu para Leituras
def menu_leitura(conexao,conectado):
    while conectado:
        os.system('clear')
        print('-----------Operacoes Leitura-----------------')
        print("""
        1 - Cadastrar Leitura
        2 - Listar Leituras
        3 - Excluir Leitura
        4 - Menu Inicial
        """)
        escolha = input('Escolha -> ')

        if escolha.isdigit():
            escolha = int(escolha)
        else:
            escolha = 4
            print('Digite um numero.\nReinicie a Aplicação!')
        os.system('clear')
        match escolha:
            case 1:
                criar_leitura(conexao)
                aplicar_irrigacao(conexao)
            case 2:
                listar_leituras(conexao)
            case 3:
                deletar_leitura(conexao)
            case 4:
                conectado = False
            case _:
                input('Digite um numero entre 1 e 4.')