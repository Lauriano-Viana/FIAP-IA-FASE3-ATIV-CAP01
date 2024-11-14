import cx_Oracle
import pandas as pd
import os


def calculo_irrigacao(vl_leitura, dosagem_min, dosagem_max):
    # Exemplo de regra de aplicação: a quantidade é proporcional à leitura
    quantidade = dosagem_min + (vl_leitura / 100) * (dosagem_max - dosagem_min)
    return quantidade


# Função para listar irrigacoes
def listar_irrigacao(conexao):
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
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id','Id_leitura','Id_cultura','tempo','data'], 
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
def aplicar_irrigacao(conexao, id_cultura,id_leitura, id_sensor, valor_leitura):
    cursor = conexao.cursor()
    cursor.execute(f"SELECT tipo FROM sensores WHERE id_sensor = '{id_sensor}'")
    tipo = cursor.fetchone()[0]
    cursor.execute(f"SELECT nivel_p, nivel_k, nivel_ph, umidade FROM culturas WHERE id_cultura = '{id_cultura}'")
    cultura = cursor.fetchone()
    
    if cultura:
        id_cultura, nivel_p, nivel_k, nivel_ph = cultura
        quantidade_aplicacao = calc_intensidade_irrigacao(valor_leitura, nivel_p, nivel_k, nivel_ph)
        # Inserir aplicação de cultura
        cursor.execute("""
            INSERT INTO aplicacao_culturas 
            (id_aplicacao, id_sensor, id_leitura, id_cultura, vl_leitura, quantidade_aplicacao, data_aplicacao) 
            VALUES (seq_aplicacao_culturas.NEXTVAL, :1, :2, :3, :4, :5, SYSDATE)
        """, (id_sensor, id_leitura, id_cultura, valor_leitura, quantidade_aplicacao))
        conexao.commit()
    cursor.close()

def criar_aplicacao(conexao):
    
        cursor = conexao.cursor()
        consulta = f"""SELECT id_leitura, id_sensor, valor FROM leituras """
        cursor.execute(consulta)
        #Captura os registros e armazena no obj leituras
        leituras = cursor.fetchall()
       
        for leitura in leituras:
            id_leitura, id_sensor, valor = leitura            
            aplicar_cultura(conexao, id_leitura, id_sensor, valor)
        
        listar_aplicacoes(conexao)
        cursor.close()