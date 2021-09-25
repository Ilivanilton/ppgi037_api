# -*- coding: utf-8 -*-

import re
from unidecode import unidecode
from bulario import bulario

def lower(objAtratar):
  tratado = []
  for linha in range(len(objAtratar)):
    k = []
    for coluna in range(len(objAtratar[linha])):
      k.append(unidecode(objAtratar[linha][coluna].lower()))    # Diminui maiúsculas e retira acentos, til, cedilha. 
    tratado.append(k)                                           # Salva a linha (k) em pacienteTratado.
  return tratado

bularioTratado = lower(bulario)

"""#### Para a geração da lista branca"""

bulas = bularioTratado

# A seguir, são iniciadas três variáveis vazias: dois dicionários {}; e uma lista [].
diagnostico = {}
sintomas = {}
lista_negra = []

vida_1 = 0


# A seguir, são definidas algumas funções, chamadas umas pelas outras. Quem chama a primeira função da cadeia é a última linha deste código: Referencias(paciente).
def Lista(anamnese, coluna_bulario, coluna_paciente):
  GeraLista(Split_Texto(anamnese), coluna_bulario, coluna_paciente)


# A  função a seguir separa a string, quando encontrar vírgula ou "e". A barra | funciona como OU.
def Split_Texto(celula):
  termos = re.split( ', | e ', celula)    
  return termos


# A função recebe como parâmetros, respectivamente: os termos da célula, tratados pelo Split_Texto e Trata_texto; a coluna correspondente no dataset Bulário; e a coluna correspondente no dataset Pacientes.
def GeraLista(termos_tratados_separados, colunaB, colunaP):

  dicionario_termos = {}
  lista_termos_ausentes = []
  
  for i in range (len(termos_tratados_separados)):                         # Para cada termo i que foi tratado.
    lista_remedios = []
    for j in range(len(bulas[:])):                                         # Para cada linha de bulas (ou seja, para cada remédio do bulário).
        if bulas[j][colunaB].find(termos_tratados_separados[i]) >= 0:      # Verifica se o termo tratado aparece na linha j, colunaB, do bulário. Se sim, executam-se os comandos seguintes.
          lista_remedios.append(bulario[j][0])                             # O remédio (indicado em bulario[j][0], ou seja, com letras maiúsculas e acentos) é acrescentado à lista de remédios.
          dicionario_termos[termos_tratados_separados[i]] = lista_remedios # Atualiza o dicionário, com a nova lista de remédios.
          
          if contador == 0:                                                # O contador indica uma chave do dicionário colunas_Pacientes_Bulario. O contador = 0 é o "diagnóstico".
            diagnostico.update(dicionario_termos)                          # Atualiza-se diagnostico com o novo dicionario_termos.
          elif contador == 1:                                              # O contador = 1 é a "reclamação_do_paciente" (sintomas), no dicionário colunas_Pacientes_Bulario.
            sintomas.update(dicionario_termos)                             # Atualiza-se sintomas com o novo dicionario_termos.
          else:                                                            # Os demais valores de contador são as demais chaves de colunas_Pacientes_Bulario.
            lista_negra.extend(lista_remedios)                             # Atualiza-se a lista_negra com a nova lista_remedios.
            
    if termos_tratados_separados[i] not in dicionario_termos:              # Aqui, é verificado se um termo (termos_tratados_separados[i]) está em "dicionario_termos".
          lista_termos_ausentes.append(termos_tratados_separados[i])       # Acrescenta o termo ausente à lista_termos_ausentes.

  print("Remédios:", dicionario_termos)
  print("Sem opções de remédio:", lista_termos_ausentes)



# A seguir, são definidos dois dicionários. 
# O primeiro, gravidez, indica o que significam os números do dataset Pacientes, na coluna "gravidez". 
# O segundo dicionário, colunas_Pacientes_Bulario, indica, para cada chave (como "diagnóstico", "alergia_remedio" etc.), a coluna correspondente nos datasets Pacientes e Bulário, para pesquisa.

# Nos comentários a seguir, consta o que cada coluna contém, nos datasets Bulário e Pacientes (conforme arquivo "Datasets reunidos", no Drive).

#BULÁRIO
#0: nome do remédio, 1: composição e dosagem, 2: excipientes, 3: dosagem_ex, 
#4: indicação, 5: contraindicação, 6: efeitos colaterais, 7: posologia, 8: advertências e precauções

#PACIENTES
#0: PatientId, 1: AppointmentID, 2: Gender, 3: AppointmentRegistration, 4: AppointmentData, 
#5: Age, 6: Neighbourhood, 7: Scholarship, 8: Hypertension, 9: Diabetes, 10: Alcoholism, 
#11: Handicap, 12: Pregnancy period, 13: Disease diagnosis, 14: Drug allergy, 15: Food allergy, 
#16: patient complaint, 17: Diagnosis after consultation and examination


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
    "fígado":                 [8, 5, "figado"],        # 8 coluna paciente; 5 coluna bulario; "" pesquisa string da 8 na 5
    "hepático":               [8, 5, "hepatico"],      # 8 coluna paciente; 5 coluna bulario; "" pesquisa string da 8 na 5
    "hepática":               [8, 5, "hepatica"],      # 8 coluna paciente; 5 coluna bulario; "" pesquisa string da 8 na 5
    "rim":                    [9, 5, "rim"],           # 9 coluna paciente; 5 coluna bulario; "" pesquisa string da 9 na 5
    "rins":                   [9, 5, "rins"],          # 9 coluna paciente; 5 coluna bulario; "" pesquisa string da 9 na 5
    "renal":                  [9, 5, "renal"],         # 9 coluna paciente; 5 coluna bulario; "" pesquisa string da 9 na 5
    "renais":                 [9, 5, "renais"],        # 9 coluna paciente; 5 coluna bulario; "" pesquisa string da 9 na 5
    "gravidez":               [10, 5, "gravidez"],     # 10 coluna paciente; 5 coluna bulario; "" pesquisa string da 10 na 5
    "grávida":                [10, 5, "gravida"],      # 10 coluna paciente; 5 coluna bulario; "" pesquisa string da 10 na 5
    "grávidas":               [10, 5, "gravidas"],}    # 10 coluna paciente; 5 coluna bulario; "" pesquisa string da 10 na 5

#OBS.: Não incluídos em colunas_Pacientes_Bulario as chaves: gênero, idade, deficiência (e outras, não relevantes).



def Converte_referencias(numero_paciente, termo,pacienteTratado):              # O "termo", string, é uma das chaves (como "diagnóstico" ou "sintomas") do dicionário imediatamente acima, "colunas_Pacientes_Bulario".

  termo_Pacientes = colunas_Pacientes_Bulario[termo][0]        # Nas três primeiras linhas, pega-se o valor da chave (termo) do dicionário.
  termo_Bulario = colunas_Pacientes_Bulario[termo][1]
  termo_pesquisa = colunas_Pacientes_Bulario[termo][2]
    
  #conteudo = paciente.cell(numero_paciente + 1, termo_Pacientes + 1).value  #UTILIZAR SOMENTE NO COLAB # Pega-se o valor da célula no dataset Pacientes, na linha do paciente, e na coluna correspondente ao termo.
  conteudo = pacienteTratado[numero_paciente][termo_Pacientes]        # Pega-se o valor da célula no dataset Pacientes, na linha do paciente, e na coluna correspondente ao termo.
  conteudoNaoTratado = pacienteTratado[numero_paciente][termo_Pacientes]     # Apenas para print.

  if termo_pesquisa == "":
    print("")
    print(termo, ":", conteudoNaoTratado)
    Lista(conteudo, termo_Bulario, termo_Pacientes)            # Será pesquisado o conteúdo (conteudo) na coluna do dataset Bulário (termo_Bulario) e na coluna 
  else:                                                        # Nesses casos, termo_pesquisa será um número, não uma string.
    y = conteudo
    y = int(y)
    if y > 0:
      if termo == "gravidez" or termo == "grávida" or termo == "grávidas":
        global vida_1 
        vida_1 = 1
        print("")
        print(termo, ":", gravidez[y])                         # "gravidez" é um dicionário definido acima. No caso, o número y é convertido na string correpondente, no dicionário.
      else:
        print("")
        print(termo)
      
      conteudo = termo_pesquisa                                # No dataset há acentos e maiúsculas. Portanto, não se reconhecem alguns casos.
      Lista(conteudo, termo_Bulario, termo_Pacientes)          # Como parâmetro, são passados, respectivamente, o conteúdo (string), a coluna no dataset Bulário (número) e a coluna correspondente no dataset Pacientes (número).     



def Referencias(numero_paciente,pacienteTratado):
  global contador 
  contador = 0
  for chave in colunas_Pacientes_Bulario:
    Converte_referencias(numero_paciente, chave,pacienteTratado)
    contador += 1


print ("RELATÓRIO")



"""#### Lista branca"""

lista_branca_diagnostico = set()  # O "set()" é um conjunto (matemático). Ou seja, os elementos não são ordenados, e não há repetições.
lista_branca_sintomas = set()


def gera_lista_branca(pacienter):
  global diagnostico
  global sintomas
  global lista_negra
  global lista_branca_diagnostico
  global lista_branca_sintomas
  diagnostico = {}
  sintomas = {}
  lista_negra = []
  vida_1 = 0
  lista_branca_diagnostico.clear()
  lista_branca_sintomas.clear()
  pacienteTratado = lower(pacienter)
  # Para consultar o paciente, informe a ID.
  pacientex = 1              # Corresponde a uma linha do dataset Pacientes.
  Referencias(pacientex,pacienteTratado)
  
  #print("LISTA BRANCA \n")  
  #print("Recomendado para a doença:")
  lb_diagnostico = retira_termos(diagnostico, lista_branca_diagnostico)  # Para o diangóstico, retiram-se os remédios da lista negra, sobrando a lista branca do diagnóstico.
  
  if vida_1 == 1:
    #print("Recomenda-se que o(a) médico(a) consulte a bula para as pacientes grávidas.")
    AdvertenciasPrecaucoes(lista_branca_diagnostico)       # Apresenta as informações de advertência e precauções para as medicações principais (do diagnóstico)

  #print()
  #print("Recomendado para os sintomas:")
  lb_sintomas = retira_termos(sintomas, lista_branca_sintomas)        # Para os sintomas, retiram-se os remédios da lista negra, sobrando a lista branca dos sintomas.

  return {"lb_diagnostico":lb_diagnostico,"lb_sintomas":lb_sintomas}


def retira_termos(termo, lb):       # O parâmetro "termo" recebe um dicionário contendo, para cada chave string (como "Dor de cabeça" e "Azia"), uma lista com os remédios que tratam o respectivo sintoma ou diagnóstico.
  for i in termo:                   # i é uma chave (como "Dor de cabeça" e "Azia") do dicionário.
    for j in termo[i]:              # j é um remédio da chave.
      if j not in set(lista_negra): 
        lb.add(j)                   # Ou seja, se o remédio não estiver na lista negra, então o remédio é adicionado à lista branca dos sintomas ou do diagnótico, conforme recebido por parâmetro.
  
  if len(lb) == 0:
    return "Não há recomendações de remédios no banco de dados."
  else:
    return lb   


def AdvertenciasPrecaucoes(lb):        # Imprime as advertências e precauções dos medicamentos da lista branca.
  print("LISTA DE ADVERTÊNCIAS E PRECAUÇÕES PARA AS MEDICAÇÕES")
  for j in lb:
    for i in range(len(bulario)):
      if bulario[i][0] == j:
        print(j, ":", bulario[i][8], "\n")

"""
paciente = [
  ['PatientId', 'num', 'sexo', 'data_consulta', 'idade', 'local', 'hipertencao', 'diabetes', 'figado', 'rins', 'gravidez', 'alergias', 'reclamação_do_paciente', 'apos_diagnostico'],
  ['204790', '122738', '0', '8/27/2021', '28', 'Hospital Universitário', '0', '0', '0', '0', '0', 'Tinidazol', 'Enjoo, gases (flatulência) e cólicas abdominais.', 'Giardíase']
]
print(gera_lista_branca(paciente))
"""

# diagnostico = {}                    # Zera as variáveis
# sintomas = {}                       # Zera as variáveis
# #lista_negra = []                    # Zera as variáveis - Observação: habilitando estas funções a lista negra não é gerada
# gravida_1 = 0

#print("TIPOS DE LISTAS:\n")

print("LISTA NEGRA")
print(lista_negra)

#print("LISTA BRANCA")
#print(lista_branca)

