# Importando as bibliotecas necessárias
import pandas as pd
from tabulate import tabulate

# Definindo os caminhos para os arquivos CSV
caminho_perfil_eleitorado = r'Coloque o Caminho do Banco de Dados Eleitorado'
caminho_sp_turno = r'Coloque o caminho do Banco de dados sp_turno'

# Colunas desnecessárias para serem removidas
colunas_nao_necessarias_perfil = [
    'DS_ESTADO_CIVIL', 'CD_FAIXA_ETARIA', 'QT_ELEITORES_INC_NM_SOCIAL']
colunas_nao_necessarias_sp = [
    'NR_JUNTA_APURADORA', 'NR_TURMA_APURADORA', 'DS_AGREGADAS']

# Função para tratar caracteres especiais


def treat_special_chars(x):
    if isinstance(x, str):
        return x.encode('latin1').decode('utf-8', 'ignore')
    return x


# Lendo e tratando os arquivos CSV do perfil do eleitorado
dtype_perfil = {
    'NR_TITULO_ELEITOR': str,  # Ajuste os tipos de dados conforme necessário
    # Inclua outras colunas necessárias e seus tipos de dados
}
df_perfil_eleitorado = pd.read_csv(caminho_perfil_eleitorado, sep=';', encoding='latin1',
                                   usecols=lambda col: col not in colunas_nao_necessarias_perfil, dtype=dtype_perfil)
df_perfil_eleitorado.dropna(inplace=True)
df_perfil_eleitorado = df_perfil_eleitorado.applymap(treat_special_chars)

# Lendo e tratando os arquivos CSV dos resultados do turno
dtype_sp = {
    'NR_TITULO_ELEITOR': str,  # Ajuste os tipos de dados conforme necessário
    # Inclua outras colunas necessárias e seus tipos de dados
}
df_sp_turno = pd.read_csv(caminho_sp_turno, sep=';', encoding='latin1',
                          usecols=lambda col: col not in colunas_nao_necessarias_sp, dtype=dtype_sp)
df_sp_turno.dropna(inplace=True)
df_sp_turno = df_sp_turno.applymap(treat_special_chars)

# Escolha o candidato (substitua pelo nome do candidato desejado)
candidato_X = "Nome do Candidato"

# Filtrar os resultados para o candidato X
resultados_candidato_X = df_sp_turno[df_sp_turno['NM_VOTAVEL'] == candidato_X]

# Encontrar o município onde o candidato X obteve mais votos
municipio_mais_votado = resultados_candidato_X.loc[resultados_candidato_X['QT_VOTOS'].idxmax(
), 'NM_MUNICIPIO']
print(
    f"O candidato {candidato_X} foi mais votado no município de {municipio_mais_votado}.")

# Encontrar o candidato mais votado em cada município
candidatos_mais_votados_por_municipio = df_sp_turno.loc[df_sp_turno.groupby(
    'NM_MUNICIPIO')['QT_VOTOS'].idxmax(), ['NM_MUNICIPIO', 'NM_VOTAVEL']]
print("\nCandidato mais votado em cada município:")
print(tabulate(candidatos_mais_votados_por_municipio,
      headers='keys', tablefmt='pretty'))

# Realizar um merge entre os DataFrames para análise do perfil do eleitorado
df_merged = pd.merge(df_perfil_eleitorado, df_sp_turno,
                     on='NR_TITULO_ELEITOR', how='inner')

# Agregação para análise do perfil do eleitorado que mais votou em cada candidato
perfil_votos_por_candidato = df_merged.groupby(['NM_VOTAVEL', 'DS_GENERO', 'DS_GRAU_ESCOLARIDADE', 'DS_FAIXA_ETARIA', 'SG_UF', 'NM_MUNICIPIO',
                                               'QT_ELEITORES_PERFIL', 'QT_ELEITORES_BIOMETRIA', 'QT_ELEITORES_DEFICIENCIA', 'NR_ZONA']).size().reset_index(name='NUM_VOTOS')
print("\nPerfil do eleitorado que mais votou em cada candidato:")
print(tabulate(perfil_votos_por_candidato, headers='keys', tablefmt='pretty'))
