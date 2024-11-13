import cx_Oracle
import pandas as pd
import os

'''Operações referente a produtos'''
# Função para criar um novo produto
def criar_produto(conexao):
    try:
        os.system('clear')
        cursor = conexao.cursor()
        print('-------------CADASTRAR PRODUTO------------------\n')
        nome = input('Digite o nome do produto......: ')
        tipo = input(' Digite o tipo: pesticida ou fungicida:   ')
        tipo = tipo.upper()
        dosagem_min = float(input(' Digite a dosagem minima em (L/ha):   '))
        dosagem_max = float(input(' Digite a dosagem maxima em (L/ha):   '))

        cadastro = f""" 
            INSERT INTO produtos (id_produto,nome, tipo, dosagem_min, dosagem_max) 
            VALUES (seq_produtos.NEXTVAL,'{nome}', '{tipo}', {dosagem_min},{dosagem_max})
            
            """
        cursor.execute(cadastro)
        conexao.commit()
        cursor.close()
        print('\n Produto cadastrado com suscesso')
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao criar produto: {e}")
    input(' Pressione enter para continuar')



# Função para ler produtos
def listar_produtos(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados 
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos")
        #Captura os registros e armazena no obj produtos
        produtos = cursor.fetchall()
        for produto in produtos:
            lista_dados.append(produto)
        lista_dados = sorted(lista_dados)
        # Gera um Dataframe com os dados da lista usando o Pandas
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id','Nome','Tipo','Dosagem Min','Dosagem Max'], 
                                             index ='Id')
        if dados_df.empty:
            print(f'Não há produtos cadastrados!!')
        else:
            print(dados_df)
        print('\nLISTADOS!')
        cursor.close()

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao ler produtos: {e}")
    input(' Pressione enter para continuar')



# Função para atualizar um produto
def alterar_produto(conexao):
    try:
        os.system('clear')
        print('------------Alterar dados do produto')
        lista_dados = [] #lista para captura de dados 
        id_produto = int(input('Informe o id do Produto a ser alterado....:   '))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM produtos WHERE id_produto = {id_produto}"""
        cursor.execute(consulta)
        data = cursor.fetchall()

        for dt in data:
            lista_dados.append(dt)
        
        if len(lista_dados)==0:
            print(f'Não há um produto cadastrado com o ID = {id_produto}')
        else:
            # Captura os novos dados
            novo_nome = input('Digite o nome do produto......: ')
            novo_tipo = input(' Digite o novo tipo:   ')
            nova_dosagem_min = float(input(' Digite a dosagem minima em (L/ha):   '))
            nova_dosagem_max = float(input(' Digite a dosagem maxima em (L/ha):   '))

            alteracao = f""" UPDATE produtos SET nome='{novo_nome}', tipo='{novo_tipo}', 
                                dosagem_min={nova_dosagem_min}, dosagem_max={nova_dosagem_max}
                        """
        
            cursor.execute(alteracao)
            conexao.commit()
            cursor.close()
            print(f"Produto {id_produto} atualizado com sucesso.")
   
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao atualizar produto: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione enter para continuar')



# Função para deletar um produto
def deletar_produto(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados
        id_produto = int(input('Informe o id do produto a ser deletado:   '))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM produtos WHERE id_produto = {id_produto}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
     
        if len(lista_dados)==0:
            print(f'Não há um produto cadastrado com o ID = {id_produto}')
        else:
            exclusao = f"""DELETE FROM produtos WHERE id_produto = {id_produto} """
            cursor.execute(exclusao)
            conexao.commit()
            cursor.close()
            print(f"Produto {id_produto} deletado com sucesso.")
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao deletar produto: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione enter para continuar')



# Função para criar um Menu para produtos
def menu_produto(conexao,conectado):
    os.system('clear')
    while conectado:
        print('-----------Operacoes Produtos-----------------')
        print("""
        1 - Cadastrar Produto
        2 - Listar Produto
        3 - Alterar Produto
        4 - Excluir Produto
        5 - Menu inicial
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
                criar_produto(conexao)
            case 2:
                listar_produtos(conexao)
            case 3:
                alterar_produto(conexao)
            case 4:
                deletar_produto(conexao)
            case 5:
                conectado = False
            case _:
                input('Digite um numero entre 1 e 5.')
