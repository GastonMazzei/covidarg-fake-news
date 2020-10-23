<img width=80, height=80, src="readme-static.png">

(es):es:<br>
<b>Explicación</b><br>
Hola, bienvenid@s al repositorio asociado a la página ["covidarg-fake-news"](https://covidarg-fake-news.herokuapp.com/).<br>
La intención es triple:
* concientizar sobre las fake news
* recordar los cuidados generales
* difundir el analisis estadistico
<br>
<br><br>
<i>Más info</i><br>
A partir de los [Datos Públicos](https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv) del Gobierno Argentino :v: :argentina: :gorilla: sobre Coronavirus se puede computar la probabilidad de tener la enfermedad para distintos grupos sociales.  

<br>
* Concientizar sobre las "<i>Fake News</i>" (noticias falsas). Cuando los resultados son matemáticamente correctos, una alternativa a creer en la conclusión es cuestionar las hipótesis. Dada la (alta) velocidad con la que ocurren las interacciones virtuales es posible perder ésto de vista y construir razonamientos mal cimientados.   
* 
* Difundir el análisis estadístico en general y en particular agradecer a quien corresponda por la puesta en marcha de una base de datos pública. La expectativa general es que la "<i>transferencia tecnológica</i>" va a mejorar la calidad de vida de todos los ciudadanos; es en tal marco que se observa: la puesta en marcha de una base de datos pública es un excelente ejemplo de las acciones necesarias para llevar a la sociedad hacia ese "<i>futuro mejor</i>". 

_____________E_X_P_L_I_C_A_C_I_O_N___________________________________.
                                                                     |
__A PARTIR DE__                                                      |
                                                                     |
 1. La data del SISA.gov                                             |
    (https://sisa.msal.gov.ar/                                       |
     datos/descargas/covid-19/                                       |
     files/Covid19Casos.csv)                                         |
                                                                     |
 2. La lista de hipótesis:                                           |
    (2.A) - modelar positivo-negativo con Bernouilli                 |   
    (2.B) - modelar prior uniforme                                   |
    (2.C) - suponer que en la beta tenemos casos                     |
            "suficientemente simetricos" como para                   |
            decir Xmax=Xmean y usamos que:                           |
              Xmean = alpha / (alpha + beta)                         |
            (esto podria cambiarse en el codigo...)                  |
                                                                     |
__TENEMOS__                                                          |
                                                                     |
 1. Un codigo que usa una version reducida de la database            |
    para comparar la probabilidad de dos condiciones distintas       |
    y entregar, ademas de un plot con la forma de Beta, un           |
    "newspaper headline" amarillista del tipo                        |
     ``el caso A tiene p% mas de proba de dar positivo que B``       |
                                                                     |
      DETALLES:                                                      |
                .El código corre en un Loop: (1) te da un gráfico,   |
                 (2) lo cerrás, (3) te da otro, etc.                 |
                                                                     |
 2. Pendientes (ver en "Issues", o al final de este texto)           |
_____________________________________________________________________| 
DISCLAIMER Y FILOSOFIA: Es un 'juego' con forma de burla. O una burla|
con forma de juego. En ningún caso apunta a alentar la creación y/o  |
distribución de FAKE-NEWS en torno a algo grave como el Coronavirus. |
En Argentina, si creen que tienen síntomas deben llamar al 107.      |
Más info: https://www.argentina.gob.ar/salud/coronavirus-COVID-19    |
_____________________________________________________._______________|
                  DIRECTORY MAP                      |
                                                     |
                          Headlines                  |
. main.py ------------->  generating                 |
                          code                       |
                                                     |
. README &                                           |
  LICENSE                                            |
                            small covid              |
. smaller.zip ------------>  database: it's          |
                              lighter than the       |
                               "sisa.gov" version    |
                                                     |
                                                     |
__________________________.__________________________|
       TUTORIAL           |
                          |
1) unzip "smaller.zip"    |
                          |
 !!!                      |
   IF you don't do it,    |
   the script will:       |
  -download the "sisa"    |
   database               |
  -use it to build the    |
   "smaller.csv" file     |
                     !!!  |
                          |
2) run "main.py"          |
                          |
--------------------------/


PENDIENTES:

                .El código tiene un bug (ver "Issues") que consiste
                 en que "se queda colgado procesando" aprox. 1 en 10
                 veces. Repito la única advertencia de la consola:
                 si tarda más de 2 segundos en calcular un gráfico 
                 termínenlo y córranlo de vuelta


                .La main branch quiere ser una Dockerized-version de 
                 una página de internet
                   ALGUNAS CUESTIONES DE DISEÑO:
                     1) Boton que recalcula? puede ser muy cpu-intense
                        quizas tiene que actualizarse solo...
                     2) Sección repitiendo los consejos de seguridad 
                        del ministerio de salud
                     3) Incluir gráficos? o solo el headline?


                .Falta agregar comparaciones de varios tipos.
                 Actualmente tiene DOS: 

                     1) intra-categoría: e.g. Chaco vs Misiones

                     2) intra-categoría con una segunda catego-
                        ría fija: e.g. Chaco vs Misiones para 
                        Edad > 30                 











