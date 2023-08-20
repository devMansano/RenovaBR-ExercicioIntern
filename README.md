# RenovaBR-ExercicioIntern

Desafio Tecnico da RenovaBR 


#Este repositório contem um conjunto de Scripts em Python para realização de análise de dados eleitorais e resultados de #eleições.

Foram utilizadas as bibliotecas Pandas e Tabulate com o objetivo de fornecer um guia passo a passo para a limpeza, exploração e analise de dados, além de realizar consultas específicias para responder perguntas sobre resultados eleitorais.

#Pré-Requisitos
Python 3 instalado (recomendado: Python 3.6 ou superior)
Bibliotecas necessárias instaladas (Pandas, Tabulate)
utilize esta função no terminal para instalar as bibliotecas: pip install pandas tabulate

#Passos do Processo de Desenvolvimento

#1-Preparação do Ambiente
Instale o Python 3.6 ou superior, caso não esteja instalado.
Instale as bibliotecas Pandas e Tabulate através do gerenciador de pacotes pip.

#2-Obtenção dos Dados
Certifique-se de ter acesso aos arquivos CSV do perfil do eleitorado e dos resultados das eleições.
Defina os caminhos para esses arquivos nas variáveis caminho_perfil_eleitorado e caminho_sp_turno.

#3-Limpeza e Tratamento dos Dados
Remova registros nulos ou em branco dos DataFrames.
Remova colunas desnecessárias que não serão utilizadas nas análises.
Utilize a função treat_special_chars para tratar caracteres especiais nas colunas de texto.

#4-Análise dos Resultados Eleitorais
Escolha um candidato de interesse e utilize a variável candidato_X para definir o nome do candidato.
Filtrar os resultados eleitorais para o candidato específico.
Encontrar o município onde o candidato obteve mais votos.
Calcular o candidato mais votado em cada município.

#5-Análise do Perfil do Eleitorado
Realizar um merge entre os DataFrames do perfil do eleitorado e dos resultados eleitorais usando o número do título de eleitor como chave.
Agrupar os dados para análise do perfil do eleitorado que mais votou em cada candidato, considerando gênero, grau de escolaridade e faixa etária.

#6-Visualização dos Resultados
Utilize a função tabulate para imprimir os DataFrames de forma formatada no terminal.
