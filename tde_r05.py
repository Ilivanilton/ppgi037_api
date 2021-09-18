# -*- coding: utf-8 -*-

import re
from unidecode import unidecode
from bulario import bulario
#from paciente import paciente

"""#### Para a geração da lista branca"""

bulas = bulario

# A seguir, são iniciadas três variáveis vazias: dois dicionários {}; e uma lista [].
diagnostico = {}
sintomas = {}
lista_negra = []
paciente = []
#lista_negra = set()

# A seguir, são definidas algumas funções, chamadas umas pelas outras. Quem chama a primeira função da cadeia é a última linha deste código, em: Referencias(paciente).
def Lista(anamnese, coluna_bulario, coluna_paciente):
  GeraLista(Split_Texto(Trata_Texto(anamnese)), coluna_bulario, coluna_paciente)

def Trata_Texto(texto):                   # Função trata a string (texto) que será consultada nos datasets.
  texto = re.sub('\.', '', texto)         # Substitui ponto-final (pelo símbolo '\.') por nada (''). Apenas este está funcionando.
  unidecode(texto)                        # Retiraria os acentos. Mas, por alguma razão, não está funcionando.
  texto.lower()                           # Tornaria minúsculos todos os caracteres. Mas, por alguma razão, não está funcionando.
  #texto.casefold()                       # Outra maneira de tornar minúsculos todos os caracteres. Também não está funcionando.
  #print(texto)
  return texto

def Split_Texto(celula):
  termos = re.split( ', | e ', celula)    # Separa a string, quando encontrar vírgula ou "e". No primeiro parâmetro de split(), a barra | funciona como um OU.
  return termos


# A função recebe como parâmetros, respectivamente: os termos da célula, tratados pelo Split_Texto e Trata_texto; a coluna correspondente no dataset Bulário; e a coluna correspondente no dataset Pacientes.
def GeraLista(termos_tratados_separados, colunaB, colunaP):
  dicionario_termos = {}
  lista_termos_ausentes = []
  for i in range (len(termos_tratados_separados)):                         # Para cada termo i que foi tratado.
    lista_remedios = []
    for j in range(len(bulas[:])):                                         # Para
        if bulas[j][colunaB].find(termos_tratados_separados[i]) > 0:
          lista_remedios.append(bulas[j][0])
          dicionario_termos[termos_tratados_separados[i]] = lista_remedios
          if contador == 0:
            diagnostico.update(dicionario_termos)
          elif contador == 1:
            sintomas.update(dicionario_termos)
          else:
            lista_negra.extend(lista_remedios)
            #lista_negra.add(lista_remedios)
            
    if termos_tratados_separados[i] not in dicionario_termos:
          lista_termos_ausentes.append(termos_tratados_separados[i])

  print("Remédios:", dicionario_termos)
  print("Sem opções de remédio:", lista_termos_ausentes)



#BULÁRIO
#0: nome do remédio, 1: composição e dosagem, 2: excipientes, 3: dosagem_ex, 
#4: indicação, 5: contraindicação, 6: efeitos colaterais, 7: posologia, 8: advertências e precauções

#PACIENTES
#0: PatientId, 1: AppointmentID, 2: Gender, 3: AppointmentRegistration, 4: AppointmentData, 
#5: Age, 6: Neighbourhood, 7: Scholarship, 8: Hypertension, 9: Diabetes, 10: Alcoholism, 
#11: Handicap, 12: Pregnancy period, 13: Disease diagnosis, 14: Drug allergy, 15: Food allergy, 
#16: patient complaint, 17: Diagnosis after consultation and examination

#Não incluídos abaixo: gênero, idade, deficiência (e outros, não relevantes).

# Dicionário: y = 0 significa sem gravidez ou homem; y = 1 significa menor do que 4 semanas; y = 2 significa um mês de gravidez; e assim sucessivamente, até o número 10, que é igual a 9 meses.
gravidez = {0: "sem gravidez ou homem", 1: "até 4 semanas", 2: "um mês de gravidez", 3: "dois meses de gravidez",
            4: "três meses de gravidez", 5: "quatro meses de gravidez", 6: "cinco meses de gravidez",
            7: "seis meses de gravidez", 8: "sete meses de gravidez", 9: "oito meses de gravidez",
            10: "nove meses de gravidez"}  

colunas_Pacientes_Bulario = {
    "diagnóstico":            [13, 4, ""],             # 13 coluna paciente; 4 coluna bulario; "" pesquisa tudo da 13 na 4
    "reclamação_do_paciente": [12, 4, ""],             # 12 coluna paciente; 4 coluna bulario; "" pesquisa tudo da 12 na 4
    "alergia_remedio":        [11, 0, ""],             # 11 coluna paciente; 0 coluna bulario; "" pesquisa tudo da 11 na 0
    "alergia_composição":     [11, 1, ""],             # 11 coluna paciente; 1 coluna bulario; "" pesquisa tudo da 11 na 1 
    "alergia_excipientes":    [11, 2, ""],             # 11 coluna paciente; 2 coluna bulario; "" pesquisa tudo da 11 na 2
    "hipertensão":            [6, 5, "hipertens"],     # 6 coluna paciente; 5 coluna bulario; "" pesquisa string da 6 na 5
    "diabete":                [7, 5, "diabete"],       # 7 coluna paciente; 5 coluna bulario; "" pesquisa string da 7 na 5
    "diabetes":               [7, 5, "diabetes"],      # 7 coluna paciente; 5 coluna bulario; "" pesquisa string da 7 na 5
    "hepatite":               [8, 5, "hepatite"],      # 8 coluna paciente; 5 coluna bulario; "" pesquisa string da 8 na 5
    "fígado":                 [8, 5, "fígado"],        # 8 coluna paciente; 5 coluna bulario; "" pesquisa string da 8 na 5
    "hepático":               [8, 5, "hepático"],      # 8 coluna paciente; 5 coluna bulario; "" pesquisa string da 8 na 5
    "hepática":               [8, 5, "hepática"],      # 8 coluna paciente; 5 coluna bulario; "" pesquisa string da 8 na 5
    "rim":                    [9, 5, "rim"],           # 9 coluna paciente; 5 coluna bulario; "" pesquisa string da 9 na 5
    "rins":                   [9, 5, "rins"],          # 9 coluna paciente; 5 coluna bulario; "" pesquisa string da 9 na 5
    "renal":                  [9, 5, "renal"],         # 9 coluna paciente; 5 coluna bulario; "" pesquisa string da 9 na 5
    "renais":                 [9, 5, "renais"],        # 9 coluna paciente; 5 coluna bulario; "" pesquisa string da 9 na 5
    "gravidez":               [10, 5, "gravidez"],     # 10 coluna paciente; 5 coluna bulario; "" pesquisa string da 10 na 5
    "grávida":                [10, 5, "grávida"],      # 10 coluna paciente; 5 coluna bulario; "" pesquisa string da 10 na 5
    "grávidas":               [10, 5, "grávidas"],}    # 106 coluna paciente; 5 coluna bulario; "" pesquisa string da 10 na 5


# O "termo", string, é uma das chaves (como "diagnóstico" ou "sintomas") do dicionário imediatamente acima, "colunas_Pacientes_Bulario".
def Converte_referencias(numero_paciente, termo):
  termo_Pacientes = colunas_Pacientes_Bulario[termo][0]        # Nas três primeiras linhas, pega-se o valor da chave (termo) do dicionário.
  termo_Bulario = colunas_Pacientes_Bulario[termo][1]
  termo_pesquisa = colunas_Pacientes_Bulario[termo][2]
    
  #conteudo = paciente.cell(numero_paciente + 1, termo_Pacientes + 1).value  #UTILIZAR SOMENTE NO COLAB # Pega-se o valor da célula no dataset Pacientes, na linha do paciente, e na coluna correspondente ao termo.
  conteudo = paciente[numero_paciente][termo_Pacientes]        # Pega-se o valor da célula no dataset Pacientes, na linha do paciente, e na coluna correspondente ao termo.


  if termo_pesquisa == "":
    print("")
    print(termo, ":", conteudo)
    Lista(conteudo, termo_Bulario, termo_Pacientes)            # Será pesquisado o conteúdo (conteudo) na coluna do dataset Bulário (termo_Bulario) e na coluna 
  else:                                                        # Nesses casos, termo_pesquisa será um número, não uma string.
    y = conteudo
    y = int(y)
    if y > 0:
      if termo == "gravidez":
        print("")
        print(termo, ":", gravidez[y])                         # "gravidez" é um dicionário definido acima. No caso, o número y é convertido na string correpondente, no dicionário.
      else:
        print("")
        print(termo)
      
      conteudo = termo_pesquisa                                # No dataset há acentos e maiúsculas. Portanto, não se reconhecem alguns casos.
      Lista(conteudo, termo_Bulario, termo_Pacientes)          # Como parâmetro, são passados, respectivamente, o conteúdo (string), a coluna no dataset Bulário (número) e a coluna correspondente no dataset Pacientes (número). 
    

print ("RELATÓRIO")

def Referencias(numero_paciente):
  global contador 
  contador = 0
  for chave in colunas_Pacientes_Bulario:
    Converte_referencias(numero_paciente, chave)
    contador += 1

    
# Para consultar o paciente, informe a ID.
#pacientex = 1              # Corresponde a uma linha do dataset Pacientes.
#Referencias(pacientex)

"""#### Lista branca"""

#print(diagnostico)
#print(sintomas)
#print("TIPOS DE LISTAS:\n")

#print("LISTA NEGRA")
#print(lista_negra)

#lista_negra = list(dict.fromkeys(lista_negra))
#print(lista_negra)

lista_branca = set()             # O "set()" é um conjunto (matemático). Ou seja, os elementos não são ordenados, e não há repetições.


def gera_lista_branca(pacienter):
  global paciente
  global diagnostico
  global sintomas
  global lista_negra
  global lista_branca
  lista_branca.clear()
  paciente = pacienter

  pacientex = 1              # Corresponde a uma linha do dataset Pacientes.
  Referencias(pacientex)

  retira_termos(diagnostico)
  retira_termos(sintomas)

  print()
  print("LISTA BRANCA")
  print(lista_branca)
  result = lista_branca
  print(paciente)

  diagnostico = {}
  sintomas = {}
  lista_negra = []
  paciente = []
  

  return result

def retira_termos(termo):        # O parâmetro "termo" recebe um dicionário contendo, para cada chave string (como "Dor de cabeça" e "Azia"), uma lista com os remédios que tratam o respectivo sintoma ou diagnóstico.
  global lista_branca
  for i in termo:                # i é uma chave (como "Dor de cabeça" e "Azia") do dicionário.
    for j in termo[i]:           # j é um remédio da lista da chave.
      if j not in lista_negra: 
        lista_branca.add(j)      # Ou seja, se o remédio não estiver na lista negra, então o remédio é adicionado à lista branca.


#pacientess = [
#  ['PatientId', 'num', 'sexo', 'data_consulta', 'idade', 'local', 'hipertencao', 'diabetes', 'figado', 'rins', 'gravidez', 'alergias', 'reclamação_do_paciente', 'apos_diagnostico'],
#  [1, '121214', 2, 'dfdf', 29, 'Hospital Universitário', 0, 1, 0, 0, 2, 'Paracetamol', 'Azia e má digestão', 'Indigestão'],
#  ['102030', '121212', '1', '8/12/2021', '35', 'Hospital Universitário', '1', '0', '0', '0', '0', 'Dipirona e penicilina', 'Febre alta, calafrios, dor de garganta, dor de cabeça, coriza, fraqueza, dor muscular.', 'Febre Comum'],
#]
#gera_lista_branca(pacientess)





