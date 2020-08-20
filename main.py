#!/usr/bin/env python

import os

import pandas as pd 

from numpy import linspace
from random import choice
from matplotlib import pyplot as plt
from scipy.stats import beta as b
beta = b.pdf

# Miremos cuantos casos tiene cada categoria, 
# calculado sobre un subset del 5% de SISA
#
#   COLUMNA: nombre        CANTIDAD DE CASOS: numero
#
# COL:  sexo OPTIONS:  3
# COL:  edad OPTIONS:  105
# COL:  edad_años_meses OPTIONS:  2
# COL:  residencia_pais_nombre OPTIONS:  4
# COL:  residencia_provincia_nombre OPTIONS:  25
# COL:  residencia_departamento_nombre OPTIONS:  345
# COL:  carga_provincia_nombre OPTIONS:  24
# COL:  fecha_inicio_sintomas OPTIONS:  131
# COL:  fecha_apertura OPTIONS:  5
# COL:  sepi_apertura OPTIONS:  1
# COL:  fecha_internacion OPTIONS:  80
# COL:  cuidado_intensivo OPTIONS:  2
# COL:  fecha_cui_intensivo OPTIONS:  45
# COL:  fallecido OPTIONS:  2
# COL:  fecha_fallecimiento OPTIONS:  61
# COL:  asistencia_respiratoria_mecanica OPTIONS:  2
# COL:  carga_provincia_id OPTIONS:  24
# COL:  origen_financiamiento OPTIONS:  2
# COL:  clasificacion OPTIONS:  11
# COL:  clasificacion_resumen OPTIONS:  3
# COL:  residencia_provincia_id OPTIONS:  25
# COL:  fecha_diagnostico OPTIONS:  105
# COL:  residencia_departamento_id OPTIONS:  141


# Definimos las comparaciones tipo uno 
# como las hechas intra-categoria
# e.g. 'proba en venado tuerto' VS
# 'proba en CABA' (LUGAR vs LUGAR)
#
def first_type(d,cat):
  local_info = {}
  vals = d[cat].unique().tolist()
  A = choice(vals)
  B = updater(A,vals)
  local_info['key1'] = (
                  [A],
                  *hard_diagnostic(d[d[cat]==A]),
                  *soft_diagnostic(d[d[cat]==A]),
                  *fair_diagnostic(d[d[cat]==A]),
                                                 )
  local_info['key2'] = (
                  [B],
                  *hard_diagnostic(d[d[cat]==B]),
                  *soft_diagnostic(d[d[cat]==B]),
                  *fair_diagnostic(d[d[cat]==B]),
                                                 )  
  return local_info

# Definimos las comparaciones de segundo tipo 
# como las hechas internamente en una categoria
# condicionados a pertenecer a una segunda 
# e.g. proba de CABA vs Mendoza para >20
#
def second_type(d,cat1,cat2):
  local_info = {}
  Z = choice(d[cat1].unique().tolist())
  vals = d[d[cat1]==Z][cat2].unique().tolist()
  A = choice(vals)
  B = updater(A,vals)
  local_info['key1'] = (
                  [Z,A],
                  *hard_diagnostic(d[d[cat2]==A]),
                  *soft_diagnostic(d[d[cat2]==A]),
                  *fair_diagnostic(d[d[cat2]==A]),
                                                 )
  local_info['key2'] = (
                  [Z,B],
                  *hard_diagnostic(d[d[cat2]==B]),
                  *soft_diagnostic(d[d[cat2]==B]),
                  *fair_diagnostic(d[d[cat2]==B]),
                                                 )  
  return  local_info

# Definimos un `diagnostico duro`
# como ignorar sospechosos
def hard_diagnostic(d):
  L = d.size
  aux_2 = len(d[d['clasificacion_resumen'] == 'Descartado']) 
  return (L-aux_2, aux_2)

# Definimos un `diagnostico blando`
# como confirmar sospechosos
def soft_diagnostic(d):
  L = d.size
  aux_1 = len(d[d['clasificacion_resumen'] == 'Confirmado'])
  return (aux_1, L-aux_1)

# Definimos un `diagonistoc justo`
# como confirmado o descartado
def fair_diagnostic(d):
  aux_2 = len(d[d['clasificacion_resumen'] == 'Descartado']) 
  aux_1 = len(d[d['clasificacion_resumen'] == 'Confirmado'])
  return (aux_1, aux_2)

# Definimos un selector de columnas
# capaz de ignorar las que no esten 
# comentadas      
def colchus(d):
  FORBIDDEN = [
    'id_evento_caso', 
    #'sexo', 
    #'edad',
   'edad_años_meses',
    #'residencia_pais_nombre',
    #'residencia_provincia_nombre', 
    #'residencia_departamento_nombre',
    #'carga_provincia_nombre', 
     #'fecha_inicio_sintomas', 
     'fecha_apertura', 
     'sepi_apertura',
      #'fecha_internacion',
       'cuidado_intensivo',
       'fecha_cui_intensivo',
        #'fallecido',
        'fecha_fallecimiento',
         'asistencia_respiratoria_mecanica',
         'carga_provincia_id',
          #'origen_financiamiento', 
         #'clasificacion', 
         'clasificacion_resumen',
          'residencia_provincia_id',
           'fecha_diagnostico',
           'residencia_departamento_id',
            'ultima_actualizacion']
  answ = choice(d.columns.tolist())
  if answ not in FORBIDDEN: return answ
  else: return colchus(d)

# protected while
def updater(C,D,flag=False):
  protector = 0
  new = C
  while new==C:
    if flag: new = colchus(D)
    else: new = choice(D)
    protector ++ 1
    if protector>8: 
      print('ERROR: EXITED LOOP')
      sys.exit(1)
  return new

# definimos el inicializador
# del .CSV con la data
# Rdo: si no esta en el directorio
# lo podes bajar con 
#os.system(
# 'wget https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv');
def initialize(opt=False):
  try: 
    op = pd.read_csv('smaller.csv') 
  except FileNotFoundError:
    if not opt:
      print('Apparently this is the first run...')
      print('creating "smaller.csv" database...')
    try: 
      op = pd.read_csv('Covid19Casos.csv', 
          sep=',',encoding='utf-8').sample(frac=1).iloc[:50000,:]   
      op.to_csv('smaller.csv',index=False)
    except FileNotFoundError:
      print('No tenes la database en el directorio!'\
            '\nla vamos a descargar...')
      os.system('wget https://sisa.msal.gov.ar/datos/descargas'\
                            '/covid-19/files/Covid19Casos.csv')
      initialize(True)
    print('DONE!')
  return op

def yellow_calculator(k,infor):
  ONE = (k['key1'][5]+1)/(k['key1'][5]
                        +k['key1'][6]+2)
  TWO = (k['key2'][5]+1)/(k['key2'][5]
                        +k['key2'][6]+2)                        
  if ONE>TWO: 
    ind=1
    extra = round(abs(ONE-TWO)/TWO*100,1)
  else: 
    ind=2
    extra = round(abs(ONE-TWO)/ONE*100,1)
  if len(k['key1'][0])==2:
    msg = f"bajo la condicion ''{infor[0]}=={k['key1'][0][0]}'', "\
      f"el caso ''{infor[1]}=={k[f'key{ind}'][0][1]}'' \ntiene una "\
        f"proba {extra}0% mayor de dar positivo que el caso "\
          f"''{infor[1]}=={k[f'key{ind%2+1}'][0][1]}''"
  else:
    msg =  f"el caso ''{infor[0]}=={k[f'key{ind}'][0][0]}'' tiene una "\
            f"proba \n{extra}0% mayor de dar positivo que el caso "\
              f"''{infor[0]}=={k[f'key{ind%2+1}'][0][0]}''"

  return msg


def main():

  # Inicializar
  data = initialize()

  # Elegir "nivel de nesteo"
  # 
  # (pend expandir: systematic que
  #  funcione para N niveles)
  TIPO = choice([1,2])
  if TIPO==1:
    c = colchus(data)
    print('chose column ',c)
    # main TYPE1
    result = first_type(data,c)
    forward = (c,)
  elif TIPO==2:
    c1 = colchus(data)
    c2 = c1
    c2 = updater(c1,data,True)
    print('chose columns ',c1,' and ',c2)
    # main TYPE2
    result = second_type(data,c1,c2)
    forward = (c1,c2)




  # Plot en fila:
  # IZQ la definicion estricta
  # (confirmado = 1)
  # DER la definicion laxa
  # (sospechoso OR confirmado = 1)
  f,ax = plt.subplots(1,3,
                    #dpi=200,
                    figsize=(24,22))
  axmap = {0:0,2:1,1:2}
  for  j in range(3):
    plot_from_keys(ax[axmap[j]],
                    result,j,forward)

  # Agregar "headline amarillista"
  amarillista = yellow_calculator(result,forward)
  plt.figtext(0.5, 0.02, 'TITULO AMARILLISTA: '+amarillista, 
               ha="center", fontsize=12, 
              bbox={"facecolor":"orange",
                    "alpha":0.5, "pad":5})

  # Mostrar!
  #plt.tight_layout()
  plt.show()

  # Fin
  return print('ENDED!')

def plot_from_keys(axy,k,n,cate):
  # utils
  xs = linspace(0,1,300)
  labeler = {0: 'definición-estricta',
             1: 'definición-laxa',
             2: 'definición-justa'}
  TYPE = len(k['key1'][0])

  # title is forked 1 vs 2
  if TYPE==1: 
    title = f'PDF de "proba de contagio"\n'\
         f"CASOS POR ''{cate[0]}'': \n''{k['key1'][0][0]}'' Y ''{k['key2'][0][0]}''"\
         f'\n\n   ({labeler[n]})'  
  elif TYPE==2:
    title = f'PDF de "proba de contagio"\n'\
         f"SOLO ''{cate[0]}'' IGUAL A ''{k['key1'][0][0]}''\n"\
         f"CASOS POR ''{cate[1]}'': \n''{k['key1'][0][1]}'' Y ''{k['key2'][0][1]}''"\
         f'\n\n   ({labeler[n]})'  
         
  # Effective plotting
  for x in k.keys():   
    axy.plot(
      xs,
      beta(
          xs,
          a=k[x][2*n+1]+1,
          b=k[x][2*n+2]+1 ),
      label=' '.join([str(y) for y in k[x][0]]))
  axy.set_title(title,fontsize=8)

  # Visual specs
  axy.legend(loc=1)
  axy.set_xlim(0,1)


  return

if __name__=='__main__':
  counter = 0
  while True:
    print(f'VUELTA NRO {counter}\nsi tarda mas de 2 segs'\
      ' se ha colgado\ndale reset...\n')
    main()
    #res = input('x para guardar, any key para continuar..')
    #if res.lower()=='x':
    #  plt.savefig(input('pllease input a figName')+'.png')
    counter += 1
