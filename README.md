(es):es:<br>
<b>Hola, bienvenidos al repositorio asociado a la página web ["covidarg-fake-news"](https://covidarg-fake-news.herokuapp.com/) </b><br>
<i>Cada vez que se recarga la página, se muestra al azar un patrón estadístico de la base de datos del gobierno</i><br>
<img width=750, height=415, src="readme-static.png">
<br>
<p>
<b>¿Cuál es la misión de la página?</b></p>

1) concientizar sobre las fake news
2) recordar los cuidados generales
3) difundir el analisis estadistico

<p>
<b>¿Cómo funciona?</b></p>
A partir de los Datos Públicos del Gobierno Argentino :v: :argentina: :gorilla: sobre Coronavirus se puede computar la probabilidad de tener la enfermedad para distintos grupos sociales usando un modelo matemático muy sencillo. Cada vez que se carga la página, se muestra un patrón matemático calculado sobre dos categorías al azar y se enuncia la conclusión "en un tono amarillista".  

<p>
<br>
<b>¿Cómo se fundamenta la misión?</b></p>

1) concientizar sobre las fake news
> Cuando los resultados son matemáticamente correctos, una alternativa a creer en la conclusión es cuestionar las hipótesis. Dada la (alta) velocidad con la que ocurren las interacciones virtuales hoy en día, es posible perder ésto de vista y construir razonamientos mal cimientados.   
2) recordar los cuidados generales
> Argentina actualmente (Fines de Octubre 2020) tiene un máximo histórico en la cantidad de casos. Si bien la larga cuarentena generó entre otras cosas cansancio y aburrimiento es el tiempo presente (en un promedio geográfico) el momento en donde las precauciones individuales deben extremarse o en todo caso no relajarse.  
3) difundir el analisis estadistico
> La expectativa general es que la "<i>transferencia tecnológica</i>" va a mejorar la calidad de vida de todos los ciudadanos; es en tal marco que se observa: la puesta en marcha de una base de datos pública es un excelente ejemplo de las acciones necesarias para llevar a la sociedad hacia ese "<i>futuro mejor</i>". 

<br>
<b>¿Cómo se calcula el patrón?</b><br>
Hipótesis: tener o no la enfermedad se puede modelar como un ensayo de Bernoulli
<img src="https://render.githubusercontent.com/render/math?math=Probabilidad(enfermo)=\mu">
<img src="https://render.githubusercontent.com/render/math?math=Probabilidad(sano)=1-\mu">
Suponiendo que dentro de cada grupo social las personas son independientes se puede modelar la base de datos estatal como generada por un proceso de Bernoulli. La conclusión es que la probabilidad de que una fracción de gente tenga coronavirus se modela con la función de probabilidad de Bernoulli, i.e.<br>
<img src="https://render.githubusercontent.com/render/math?math=PMF(N_{sanos},N_{enfermos})=\binom{N_{sanos}+N_{enfermos}}{N_{enfermos}}\mu^{N_{enfermos}}(1-\mu)^{N_{sanos}}">
Finalmente, usando el paradigma estadístico bayesiano y suponiendo que la probabilidad de tener coronavirus es completamente desconocida se obtiene una densidad de probabilidad para la probabilidad de tener coronavirus, cuya forma funcional es una Distribución Beta, i.e.<br>
<img src="https://render.githubusercontent.com/render/math?math=Beta(\mu)\approx\frac{\Gamma(N_{sanos}+N_{enfermos})}{\Gamma(N_{enfermos})\Gamma(N_{sanos})}\mu^{N_{enfermos}}(1-\mu)^{N_{sanos}}">
Lo que hace la página es, cada vez que es cargada, seleccionar al azar dos grupos sociales y comparar sus probabilidades de tener coronavirus usando el pico de la distribución.

<b><br>¿Qué hace que sean "Fake News"?</b>
* El modelo es demasiado simplista pues no tiene en cuenta otros efectos; e.g. ver [Ferguson](https://www.imperial.ac.uk/mrc-global-infectious-disease-analysis/covid-19/report-13-europe-npi-impact/). 
* La reciente polémica desatada por el comunicado de Oxford en donde se cuestiona la calidad de los datos de la base [1](https://www.infobae.com/tendencias/2020/10/22/el-sitio-estadistico-de-la-universidad-de-oxford-explico-los-motivos-por-los-que-saco-a-la-argentina-de-su-mapa-de-datos/) [2](https://www.cronista.com/economiapolitica/Por-que-razon-Argentina-fue-excluida-de-las-estadisticas-mundiales-sobre-coronavirus-20201021-0041.html) hace foco en algo evidente: los casos negativos no están siendo reportados. Eso hace que la tasa de positivos parezca más alta de lo que verdaderamente es y en particular la diferencia geográfica no permite ser correctamente contemplada. 

<br><br>
<i>Datos Públicos: https://sisa.msal.gov.ar</i><br>
