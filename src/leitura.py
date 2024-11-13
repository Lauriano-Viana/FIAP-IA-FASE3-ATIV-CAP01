import cx_Oracle
import pandas as pd
import os
# import datetime

'''Operações referente as leituras'''
# Função para criar um novo 
def criar_leitura(conexao):
    try:
        os.system('clear')
        print('-------------CADASTRAR LEITURA------------------\n')
        id_sensor = int(input(' Digite o id do sensor que será associado a leitura:   '))
        lista_dados = [] #lista para captura de dados
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM sensores WHERE id_sensor = {id_sensor}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
        if len(lista_dados)==0:
            print(f'Não há um sensor cadastrado com o ID = {id_sensor}')
        else:
            valor = float(input('Digite o valor da leitura......:     '))
            #data_leitura = datetime.datetime.now()  # Obtém a data e hora atuais
            cadastro = f""" 
            INSERT INTO leituras (id_leitura,id_sensor, valor, data_leitura) 
            VALUES (seq_leituras.NEXTVAL,{id_sensor}, {valor}, SYSDATE)
            """
            cursor.execute(cadastro)
            conexao.commit()
            cursor.close()
            print('Leitura criada com sucesso!!')

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao criar leitura: {e}")
    except ValueError:
        print(' Digite um número no "Id_sensor e/ou no valor da leitura" ')
    except:
        print('Erro desconhecido')
    input(' Pressione enter para continuar')



# Função para ler sensores
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
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id','Id_Sensor','Valor','Data'], 
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



# Função para atualizar um sensor
def alterar_leitura(conexao):
    try:
        os.system('clear')
        print('------------Alterar valor do leitura')
        lista_dados = [] #lista para captura de dados 
        id_leitura = int(input('Informe o id da leitura a ser alterada.....:'   ))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM leituras WHERE id_leitura = {id_leitura}"""
        cursor.execute(consulta)
        data = cursor.fetchall()

        for dt in data:
            lista_dados.append(dt)
        
        if len(lista_dados)==0:
            print(f'Não há uma leitura cadastrada com o ID = {id_leitura}')
        else:
            # Captura os novos dados
            novo_tipo = input('Digite o tipo de sensor......: ')
            nova_descricao = input(' Digite uma breve descrição para o sensor: \n')
            nova_localizacao = input(' Digite a localizacao do sensor')

            alteracao = f""" UPDATE sensores SET tipo='{novo_tipo}', descricao='{nova_descricao}', 
                             localizacao='{nova_localizacao}' 
                            """
            cursor.execute(alteracao)
            conexao.commit()
        cursor.close()
        print(f"Leitura {id_leitura} atualizado com sucesso.")
   
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao atualizar leitura: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    else:
        input(' Pressione qualquer tecla para continuar')



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
            print(f'Não há um sensor cadastrado com o ID = {id_leitura}')
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
        3 - Alterar leitura
        4 - Excluir Leitura
        5 - Menu Inicial
        """)
        escolha = input('Escolha -> ')

        if escolha.isdigit():
            escolha = int(escolha)
        else:
            escolha = 5
            print('Digite um numero.\nReinicie a Aplicação!')
        os.system('clear')
        match escolha:
            case 1:
                criar_leitura(conexao)
            case 2:
                listar_leituras(conexao)
            case 3:
                alterar_leitura(conexao)
            case 4:
                deletar_leitura(conexao)
            case 5:
                conectado = False
            case _:
                input('Digite um numero entre 1 e 5.')