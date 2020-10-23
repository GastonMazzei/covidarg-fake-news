#!/usr/bin/env python

import os
from uuid import uuid4
import pandas as pd 
from numpy import nan

from numpy import linspace
from random import choice
from matplotlib import pyplot as plt
from scipy.stats import beta as b
from textwrap import wrap
import time
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
  if len(vals)<2: 
    print('vals are ',vals)
    raise Exception  
  A = choice(vals)
  B = updater(A,vals)
  local_info['key1'] = (
                  [A],
                  *fair_diagnostic(d[d[cat]==A]),
                                                 )
  local_info['key2'] = (
                  [B],
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
  if len(vals)<2: raise Exception
  A = choice(vals)
  B = updater(A,vals)
  local_info['key1'] = (
                  [Z,A],
                  *fair_diagnostic(d[d[cat2]==A]),
                                                 )
  local_info['key2'] = (
                  [Z,B],
                  *fair_diagnostic(d[d[cat2]==B]),
                                                 )  
  return  local_info

def third_type(d,cat1,cat2,cat3):
  local_info = {}
  Z_1 = choice(d[cat1].unique().tolist())
  Z_2 = choice(d[cat2].unique().tolist())
  vals = d[((d[cat1]==Z_1) & (d[cat2]==Z_2))][cat3].unique().tolist()
  if len(vals)<2: 
    print('vals are ',vals)
    raise Exception  
  A = choice(vals)
  B = updater(A,vals)
  local_info['key1'] = (
                  [Z_1,Z_2,A],
                  *fair_diagnostic(d[d[cat2]==A]),
                                                 )
  local_info['key2'] = (
                  [Z_1,Z_2,B],
                  *fair_diagnostic(d[d[cat2]==B]),
                                                 )  
  return local_info

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
    'residencia_pais_nombre',   # este es nuevito lo sacamos jeje
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
         'clasificacion',            #CONSIDERAR VOLVER A PONERLO! 
         'clasificacion_resumen',
          'residencia_provincia_id',
           'fecha_diagnostico',
           'residencia_departamento_id',
            'ultima_actualizacion']
  answ = choice(d.columns.tolist())
  if answ not in FORBIDDEN: return answ
  else: return colchus(d)

def edad_to_name(s):
  try:
    s=int(float(s))
  except: pass
  return str(s)+' años'

def comuna_to_name(s):
  if s in [f"COMUNA {x:02d}" for x in range(1,16)]:
    return 'la '+s.lower()+' de CABA'
  return s

def date_to_name(s):
  months={'01':'Enero' ,
           '02':'Febrero' ,
           '03':'Marzo' ,
           '04':'Abril' ,
           '05':'Mayo' ,
           '06':'Junio' ,
           '07':'Julio' ,
           '08':'Agosto' ,
           '09':'Septiembre' ,
           '10':'Octubre' ,
           '11':'Noviembre' ,
           '12':'Diciembre' ,
          }
  y,m,d = s.split('-')
  m = months[m]
  return f'{int(d)} de {m}'

def fancy_version(category, value):
  category_mapping = {
  'carga_provincia_nombre':'la provincia en la que que se hizo el test es', #"hizo el test" reemplaza "cargó"
  'fecha_inicio_sintomas':'la fecha en la que comenzaron los síntomas es el',
  'fecha_internacion':'la fecha en la que la persona ha sido internada es el',
  'residencia_departamento_nombre':'el departamento de residencia es',
  'residencia_provincia_nombre':'la provincia de residencia es',
  'origen_financiamiento':'el tipo de lugar en donde se hizo el test es',
  'sexo':'el sexo biológico es',
  'fallecido':'la persona',
  'edad':'la persona tiene',
               }
  fancy_category = category_mapping.get(category,category)

  value_mapping = {
  'carga_provincia_nombre':{  
    'CABA':'Capital Federal',
                            },
  'fecha_inicio_sintomas': date_to_name,
  'fecha_internacion': date_to_name,
  'residencia_departamento_nombre':comuna_to_name,
  'origen_financiamiento':{
    'Privado':'una institución privada',
    'Público':'una institución pública',
         },
  'sexo':{
    'F':'femenino',
    'M':'masculino',
         },
  'fallecido':{
    'SI':'ha fallecido',
    'NO':'no ha fallecido',
         },
  'edad':edad_to_name,
  '':{
    '':'',
    '':'',
         },
                 }
  try:
    print('trying to tidy up the value ',value, 'for category ',category)
    fancy_value = value_mapping[category][value]
  except:
    try: 
      print('trying one')
      fancy_value=value_mapping[category](value)
    except Exception as ins:
      print(ins.args) 
      print('surrendering')
      fancy_value=value

  return fancy_category, fancy_value

def filter_version(category, value):
  print('checking filter for ',category,value)
  filterer = {
  'residencia_provincia_nombre':{  
    'SIN ESPECIFICAR':False,
                            },
  'sexo':{
    'NR':False,
         },
  'edad':{
    nan:False,
    **{f'{x_}.0':False for x_ in range(90,110)},
         },
  'origen_financiamiento':{
    '*sin dato*':False,
         },
  'fecha_internacion': {nan:False
         },
  'fecha_internacion': {nan:False
         },
                 }
  if category in filterer:
    veredict = filterer[category].get(value,True)
  else: veredict=True
  return veredict

# protected while
def updater(C,D,flag=False):
  protector = 0
  if isinstance(C,int):
    new=C
    C = (C,)
  else:
    new=C[0]
  while new in C:
    if flag: new = colchus(D)
    else: new = choice(D)
    protector ++ 1
    if protector>8: 
      print('ERROR: EXITED LOOP')
      sys.exit(1)
  print('new its different from C: ',new,C)
  return new

# definimos el inicializador
# del .CSV con la data
# Rdo: si no esta en el directorio
# lo podes bajar con 
#os.system(
# 'wget https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv');
def initialize(opt=False):
  try: 
    op = pd.read_csv('data/smaller.csv') 
  except FileNotFoundError:
    if not opt:
      print('Apparently this is the first run...')
      print('creating "smaller.csv" database...')
    try: 
      op.to_csv('data/smaller.csv',index=False)
      op = pd.read_csv('data/Covid19Casos.csv', 
          sep=',',encoding='utf-8').sample(frac=1).iloc[:50000,:]   
    except FileNotFoundError:
      print('No tenes la database en el directorio!'\
            '\nla vamos a descargar...')
      os.system('wget https://sisa.msal.gov.ar/datos/descargas'\
                            '/covid-19/files/Covid19Casos.csv')
      initialize(True)
    print('DONE!')
  return op

def yellow_calculator(k,infor):
  ONE = (k['key1'][-2]+1)/(k['key1'][-2]
                        +k['key1'][-1]+2)
  TWO = (k['key2'][-2]+1)/(k['key2'][-2]
                        +k['key2'][-1]+2)                        
  if ONE>TWO: 
    ind=1
    extra = round(abs(ONE-TWO)/TWO*100,1)
  else: 
    ind=2
    extra = round(abs(ONE-TWO)/ONE*100,1)
  # ONLY INTEGER PROBA!
  extra = int(extra)
  q=''
  if len(k['key1'][0])==2:
    if extra!=0:
      msg = f"Cuando {infor[0]} {k['key1'][0][0]}, {q}"\
      f"si {infor[1]} {k[f'key{ind}'][0][1]} {q}la probabilidad "\
        f"de tener coronavirus es {extra}% mayor que si "\
          f"{infor[1]} {k[f'key{ind%2+1}'][0][1]}"
    else:
      msg = f"Cuando {infor[0]} {k['key1'][0][0]}, {q}"\
      f"si {infor[1]} {k[f'key{ind}'][0][1]} {q}la probabilidad de tener "\
        f"coronavirus es igual que si {infor[1]} {k[f'key{ind%2+1}'][0][1]}"

  elif len(k['key1'][0])==1:
    if extra!=0:
      msg =  f"Si {infor[0]} {k[f'key{ind}'][0][0]}, {q}la "\
            f"probabilidad de tener coronavirus es {extra}% mayor que si "\
              f"{infor[0]} {k[f'key{ind%2+1}'][0][0]}"
    else:
      msg =  f"Si {infor[0]} {k[f'key{ind}'][0][0]}, la "\
            f"probabilidad de tener coronavirus es igual que si "\
              f"{infor[0]} {k[f'key{ind%2+1}'][0][0]}"

  elif len(k['key1'][0])==3:
    if extra!=0:
      msg = f"Cuando {infor[0]} {k['key1'][0][0]}, {q}"\
      f"si {infor[1]} {k[f'key{ind}'][0][1]} {q}la probabilidad "\
        f"de tener coronavirus es {extra}% mayor que si "\
          f"{infor[1]} {k[f'key{ind%2+1}'][0][1]}"
    else:
      msg = f"Cuando {infor[0]} {k['key1'][0][0]} y {infor[1]} {k['key1'][0][1]},{q}"\
      f"si {infor[2]} {k[f'key{ind}'][0][2]} {q}la probabilidad de tener "\
        f"coronavirus es igual que si {infor[2]} {k[f'key{ind%2+1}'][0][2]}"

  return msg,ind

def main(**kwargs):

  # Inicializar
  data = initialize()

  # Elegir "nivel de nesteo"
  # 
  # (pend expandir: systematic que
  #  funcione para N niveles)

  TIPO = choice([1]*2+[2]*8)
  limit =10
  lap = 0 
  if TIPO==1:
    c = colchus(data)
    print('chose column ',c)
    # main TYPE1
    veredict = 0
    while veredict != 2:
      result = first_type(data,c)
      veredict = (int(filter_version(c,result['key1'][0][0])) +
                 int(filter_version(c,result['key2'][0][0])) )
      if veredict!=2:
        print(f'rejected: it was category {c} and cases '\
             f"{result['key1'][0]} and {result['key2'][0]}")       
      lap += 1
      if lap>limit: raise Exception
    forward = (c,)
    fancy_cat, fancy_val1_0 = fancy_version(c, result['key1'][0][0])
    result['key1'] = ([fancy_val1_0,],
                       result['key1'][-2],result['key1'][-1],)
    fancy_cat, fancy_val2_0 = fancy_version(c, result['key2'][0][0])
    result['key2'] = ([fancy_val2_0,],
                       result['key2'][-2],result['key2'][-1],)
    forward = (fancy_cat,)

  elif TIPO==2:
    c1 = colchus(data)
    c2 = c1
    c2 = updater(c1,data,True)
    # SE TILDO CON residencia_pais_nombre  and  clasificacion
    # SE TILDO CON carga_provincia_nombre  and  fallecido
    # SE TILDO CON residencia_departamento_nombre  and  fallecido
    print('chose columns ',c1,' and ',c2)
    # main TYPE2
    veredict = 0
    limit =10
    lap = 0 
    while veredict != 4:
      result = second_type(data,c1,c2)
      veredict = (int(filter_version(c1,result['key1'][0][0])) +
                 int(filter_version(c1,result['key2'][0][0])) +
                 int(filter_version(c2,result['key1'][0][1])) +
                 int(filter_version(c2,result['key2'][0][1])))
      if veredict!=4:
        print(f'rejected: they were categories {c1} and {c2} cases '\
             f"\nfor the first:{result['key1'][0]} and {result['key2'][0]}"\
             f"\nfor the second:{result['key1'][1]} and {result['key2'][1]}")  
      # FILTER: c1&c2 cant be "residencia_departamento_nombre" and "residencia_provincia_nombre"
      if c1 in ["residencia_departamento_nombre", "residencia_provincia_nombre"]:
        if c2 in ["residencia_departamento_nombre", "residencia_provincia_nombre"]:
          veredict=0
      lap += 1
      if lap>limit: raise Exception
    forward = (c1,c2)
    print('ENTERED WITH SHAPE,LEN', len(result['key2']))
    
    fancy_cat_1, fancy_val1_0 = fancy_version(c1, result['key1'][0][0])
    fancy_cat_2, fancy_val1_1 = fancy_version(c2, result['key1'][0][1])
    result['key1'] = ([fancy_val1_0, fancy_val1_1],
                       result['key1'][-2],result['key1'][-1],)
    fancy_cat_1, fancy_val2_0 = fancy_version(c1, result['key2'][0][0])
    fancy_cat_2, fancy_val2_1 = fancy_version(c2, result['key2'][0][1])
    result['key2'] = ([fancy_val2_0, fancy_val2_1],
                       result['key2'][-2],result['key2'][-1],)

    forward = (fancy_cat_1, fancy_cat_2)
    print('EXITTED WITH SHAPE,LEN', len(result['key2']))
    #fancy_version(category, value): return fancy_category, fancy_value

  elif TIPO==3:
    c1 = colchus(data)
    c2 = c1
    c2 = updater(c1,data,True)
    c3 = updater((c1,c2),data,True) 
    print('chose columns ',c1,', ',c2,' and ',c3)
    # main TYPE2
    veredict = 0
    limit =10
    lap = 0 
    while veredict != 6:
      result = third_type(data,c1,c2,c3)
      veredict = (int(filter_version(c1,result['key1'][0][0])) +
                 int(filter_version(c1,result['key2'][0][0])) +
                 int(filter_version(c2,result['key1'][0][1])) +
                 int(filter_version(c1,result['key2'][0][1])) +
                 int(filter_version(c2,result['key1'][0][2])) +
                 int(filter_version(c2,result['key2'][0][2])))
      if veredict!=6:
        print(f'rejected: they were categories {c1} and {c2} cases '\
             f"\nfor the first:{result['key1'][0]} and {result['key2'][0]}"\
             f"\nfor the second:{result['key1'][1]} and {result['key2'][1]}"\
             f"\nfor the third:{result['key1'][2]} and {result['key2'][2]}")  
      if c1 in ["residencia_departamento_nombre", "residencia_provincia_nombre"]:
        if c2 in ["residencia_departamento_nombre", "residencia_provincia_nombre"]:
          veredict=0
        elif c3 in ["residencia_departamento_nombre", "residencia_provincia_nombre"]:
          veredict=0
      elif c2 in ["residencia_departamento_nombre", "residencia_provincia_nombre"]:
        if c3 in ["residencia_departamento_nombre", "residencia_provincia_nombre"]:
          veredict=0   
      lap += 1
      if lap>limit: raise Exception
    forward = (c1,c2,c3)
    print('ENTERED WITH SHAPE,LEN', len(result['key2']))
    
    fancy_cat_1, fancy_val1_0 = fancy_version(c1, result['key1'][0][0])
    fancy_cat_2, fancy_val1_1 = fancy_version(c2, result['key1'][0][1])
    fancy_cat_3, fancy_val1_2 = fancy_version(c3, result['key1'][0][2])
    result['key1'] = ([fancy_val1_0, fancy_val1_1, fancy_val1_2],
                       result['key1'][-2],result['key1'][-1],)
    fancy_cat_1, fancy_val2_0 = fancy_version(c1, result['key2'][0][0])
    fancy_cat_2, fancy_val2_1 = fancy_version(c2, result['key2'][0][1])
    fancy_cat_3, fancy_val2_2 = fancy_version(c3, result['key2'][0][2])
    result['key2'] = ([fancy_val2_0, fancy_val2_1, fancy_val2_2],
                       result['key2'][-2],result['key2'][-1],)

    forward = (fancy_cat_1, fancy_cat_2, fancy_cat_3)
    print('EXITTED WITH SHAPE,LEN', len(result['key2']))
    #fancy_version(category, value): return fancy_category, fancy_value


  f,ax = plt.subplots(1,
                    #dpi=200,
                    figsize=(21,7))
  amarillista,bigger_ind = yellow_calculator(result,forward)
  title=plot_from_keys(ax,result,forward,bigger_ind)


  new_name = str(uuid4())
  if kwargs.get('clean',True):
    for x in os.listdir('static'):
      if x[-4:]=='.png' and x!=new_name+'.png': 
        if x!='cuidados.png' and x!='cuidadosB.png': 
          os.remove('static/'+x)
  
  if kwargs.get('view',False):
    #add figtext 
    plt.figtext(0.5, 0.02, amarillista, 
               ha="center", fontsize=12, 
              bbox={"facecolor":"orange",
                    "alpha":0.5, "pad":5})
    plt.title(title,fontsize=8)

  # Mostrar!
  #plt.tight_layout()
  #plt.show()
  print('current dir isSS', os.getcwd())
  with open('static/message.txt','w') as f:
    f.write(amarillista)
                                                   #f5f5f5 <-- light  #363636<--dark
  plt.savefig(f'static/{new_name}.png', facecolor='#f5f5f5', transparent=True,bbox_inches='tight')
  with open('static/image.txt','w') as f:
    f.write(new_name)

  # Fin
  return print('ENDED!')

def plot_from_keys(axy,k,cate, bigger_ind):
  # utils
  xs = linspace(0,1,500)

  TYPE = len(k['key1'][0])
  
  
  # title is forked 1 vs 2
  if TYPE==1: 
    title = f'Funcion de Densidad de Probabilidad para la "probabilidad de contagio":\n'\
         f"SI ''{cate[0]} {k['key1'][0][0]}'' \nVS\n SI ''{cate[0]} {k['key2'][0][0]}''"\
  
  elif TYPE==2:
    title = f'Funcion de Densidad de Probabilidad para la "probabilidad de contagio":\n '\
         f"SI ''{cate[0]} {k['key1'][0][0]}'' para los casos especificos\n"\
         f"SI ''{cate[1]} {k['key1'][0][1]}'' \nVS\n SI ''{cate[1]} {k['key2'][0][1]}''"\
         f"SI ''{cate[1]} {k['key1'][0][1]}'' \nVS\n SI ''{cate[1]} {k['key2'][0][1]}''"
  elif TYPE==3:
    title = f'Funcion de Densidad de Probabilidad para la "probabilidad de contagio":\n '\
         f"SI ''{cate[0]} {k['key1'][0][0]}'' y también \n"\
         f"SI ''{cate[1]} {k['key1'][0][1]}'' para los casos especificos\n"\
         f"SI ''{cate[2]} {k['key1'][0][2]}'' \nVS\n SI ''{cate[1]} {k['key2'][0][2]}''"\
         f"SI ''{cate[2]} {k['key1'][0][2]}'' \nVS\n SI ''{cate[1]} {k['key2'][0][2]}''"
         
  # Effective plotting
  import matplotlib.patheffects as path_effects
  colorer={f'key{bigger_ind%2+1}':'#d0581c' ,f'key{bigger_ind}':'#98a3a5'}
  for x in k.keys():   
    axy.plot(
      xs,
      beta(
          xs,
          a=k[x][-2]+1,
          b=k[x][-1]+1 ),
      #label=' '.join([str(y) for y in k[x][0]]),
      label=k[x][0][-1],
          lw=6,ls='-',c=colorer[x],
          path_effects=[path_effects.SimpleLineShadow(),
          path_effects.Normal()])

  #f5f5f5 <-- light  #363636<--dark
  #axy.grid(color='#f5f5f5', linestyle='-', linewidth=5)
  with open('static/title.txt','w') as f:
    f.write(title)
  axy.get_yaxis().set_visible(False)
  from matplotlib.spines import Spine
  for child in axy.get_children():
    if isinstance(child, Spine):
      child.set_color('#363636')
      child.set_linewidth(10)
  axy.tick_params(axis='x', colors='#363636', width=10)
  #axy.set_title(title,fontsize=8)

  # Visual specs
  if TYPE==1:                      #34
    axy.legend(loc=1,title='\n'.join(wrap(cate[0],33)).capitalize(),
                  title_fontsize=18,fontsize=17,prop={'size': 17})#background_color='#f5f5f5'
  elif TYPE==2:
    axy.legend(loc=1,title='\n'.join(wrap(cate[0]+' '+k['key1'][0][0]+' y '+cate[1],33)).capitalize(),fontsize=17,
                  title_fontsize=17,prop={'size': 17,})#background_color='#f5f5f5'
  elif TYPE==3:
    axy.legend(loc=1,
           title='\n'.join(wrap(cate[0]+' '+k['key1'][0][0]+
                                ', '+cate[1]+' '+k['key1'][0][1]+
                                 ' y '+cate[2],33)).capitalize(),
                                     fontsize=17,
                  title_fontsize=17,prop={'size': 17,})#background_color='#f5f5f5'
  axy.set_xticks([0,0.25,0.5,0.75,1])
  axy.set_xticklabels(['0','25%','50%','75%','100%'],fontsize=30)
  #axy.set_xlim(0,1)

  return title


if __name__=='__main__':
  counter = 0
  import sys
  if len(sys.argv)==2:
    main()
    print('done!')
    sys.exit(1)
  while True:
    print(f'VUELTA NRO {counter}\nsi tarda mas de 2 segs'\
      ' se ha colgado\ndale reset...\n')
    main(clean=True, view=False)
    plt.show()
    time.sleep(3)
    counter += 1
