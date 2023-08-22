# Importando as bibliotecas necessárias
import pandas as pd
from tabulate import tabulate

"""
#Definindo os caminhos para os arquivos CSV

Caminho utilizado para chegar no arquivo CSV e conseguir acessalo para começar o tratamento dos dados.

"""
caminho_perfil_eleitorado = r'coloque o caminho para o arquivo .csv eleitorado'
caminho_sp_turno = r'coloque o caminho para o arquivo SP_turno_1.csv'

"""
#Colunas desnecessárias para serem removidas

são usadas para armazenar os nomes das colunas que devem ser removidas dos DataFrames.
Essas listas são usadas posteriormente para filtrar as colunas que não são necessárias para a análise,
visando melhorar a eficiência do código e reduzir a quantidade de dados carregados e processados.

"""
colunas_nao_necessarias_perfil = [
    'DS_ESTADO_CIVIL', 'CD_FAIXA_ETARIA', 'QT_ELEITORES_INC_NM_SOCIAL']
colunas_nao_necessarias_sp = [
    'NR_JUNTA_APURADORA', 'NR_TURMA_APURADORA', 'DS_AGREGADAS']


"""
#Função para tratar caracteres especiais
Em resumo, essa função tenta corrigir problemas de codificação que podem ocorrer ao lidar com texto em diferentes formatos de arquivo.
Ela é aplicada aos valores de cada célula em um DataFrame para garantir que os caracteres especiais sejam tratados corretamente e que o texto seja coerente e legível.
"""
def treat_special_chars(x):
    if isinstance(x, str):
        return x.encode('latin1').decode('utf-8', 'ignore')
    return x



"""
#Lendo e tratando os arquivos CSV do perfil do eleitorado.
Resumindo, essa parte do código serve para garantir que os dados sejam lidos corretamente, tenham os tipos de dados adequados, estejam livres de valores nulos e sejam tratados de forma apropriada para análises posteriores.
Isso contribui para um processamento mais eficiente e confiável dos dados.
"""
dtype_perfil = {
    'NR_TITULO_ELEITOR': str,
    #Primeiro é criado um dicionário chamado dtype_perfil onde você especifica os tipos de dados que deseja atribuir às colunas do DataFrame após a leitura do arquivo CSV.
    #Definir explicitamente os tipos de dados pode economizar memória e melhorar a eficiência nas operações subsequentes.
}
"""
Aqui está lendo o arquivo CSV do perfil do eleitorado usando a função pd.read_csv() do pandas.
No entanto, usando a opção dtype=dtype_perfil vamos aplicar os tipos de dados especificados no dicionário dtype_perfil às colunas relevantes.
Isso ajuda a evitar que o pandas faça inferências incorretas e economiza tempo na conversão de tipos de dados posteriormente.
"""
df_perfil_eleitorado = pd.read_csv(caminho_perfil_eleitorado, sep=';', encoding='latin1',
                                   usecols=lambda col: col not in colunas_nao_necessarias_perfil, dtype=dtype_perfil)
df_perfil_eleitorado.dropna(inplace=True) #Após a leitura do CSV, remove as linhas que contêm valores nulos no DataFrame df_perfil_eleitorado. Isso é importante para garantir que os dados sejam limpos e não contenham entradas vazias que possam prejudicar análises posteriores.
df_perfil_eleitorado = df_perfil_eleitorado.applymap(treat_special_chars) # Essa função é responsável por tratar caracteres especiais em strings, convertendo a codificação do texto de 'latin1' para 'utf-8'. Isso é necessário para garantir que os caracteres especiais sejam lidos e manipulados corretamente em todo o processo.

"""
#Lendo e tratando os arquivos CSV dos resultados do turno.
Resumindo, essa parte do código serve para garantir que os dados sejam lidos corretamente, tenham os tipos de dados adequados, estejam livres de valores nulos e sejam tratados de forma apropriada para análises posteriores.
Isso contribui para um processamento mais eficiente e confiável dos dados.
"""
dtype_sp = {
    'NR_TITULO_ELEITOR': str,

}
df_sp_turno = pd.read_csv(caminho_sp_turno, sep=';', encoding='latin1',
                          usecols=lambda col: col not in colunas_nao_necessarias_sp, dtype=dtype_sp)
df_sp_turno.dropna(inplace=True)
df_sp_turno = df_sp_turno.applymap(treat_special_chars)
"""
#Escolha o candidato (substitua pelo nome do candidato desejado)

Esta parte do código basicamente vai aplicar um filtro pesquisando o resultado do candidato onde mais recebeu votos e imprimir no terminal.
"""
candidato_X = "Coloque o Nome do Candidato"

# Filtrar os resultados para o candidato X
resultados_candidato_X = df_sp_turno[df_sp_turno['NM_VOTAVEL'] == candidato_X] #filtra os resultados do candidato que você escolher e depois será mostrado qual o município que mais votarão no candidato

# Encontrar o município onde o candidato X obteve mais votos
municipio_mais_votado = resultados_candidato_X.loc[resultados_candidato_X['QT_VOTOS'].idxmax(
), 'NM_MUNICIPIO']
print(
    f"O candidato {candidato_X} foi mais votado no município de {municipio_mais_votado}.") #mostra o candidato mais votado nos municípios

# Encontrar o candidato mais votado em cada município
candidatos_mais_votados_por_municipio = df_sp_turno.loc[df_sp_turno.groupby( #faz um groupby utilizando os municípios e candidatos, mostra quais os candidatos mais votados em order alfabética.
    'NM_MUNICIPIO')['QT_VOTOS'].idxmax(), ['NM_MUNICIPIO', 'NM_VOTAVEL']]
print("\nCandidato mais votado em cada município:")
print(tabulate(candidatos_mais_votados_por_municipio, #printa no terminal os candidatos mais votados e os municípios.
      headers='keys', tablefmt='pretty'))

# Realizar um merge entre os DataFrames para análise do perfil do eleitorado
df_merged = pd.merge(df_perfil_eleitorado, df_sp_turno,
                     on='NR_TITULO_ELEITOR', how='inner')

# Agregação para análise do perfil do eleitorado que mais votou em cada candidato
perfil_votos_por_candidato = df_merged.groupby(['NM_VOTAVEL', 'DS_GENERO', 'DS_GRAU_ESCOLARIDADE', 'DS_FAIXA_ETARIA', 'SG_UF', 'NM_MUNICIPIO',
                                               'QT_ELEITORES_PERFIL', 'QT_ELEITORES_BIOMETRIA', 'QT_ELEITORES_DEFICIENCIA', 'NR_ZONA']).size().reset_index(name='NUM_VOTOS')
print("\nPerfil do eleitorado que mais votou em cada candidato:")
print(tabulate(perfil_votos_por_candidato, headers='keys', tablefmt='pretty'))
