### Cloud Computing
## Despliegue de un servicio Cloud Native
### Apache Airflow

---

Cloud Computing: Servicios y Aplicaciones  
Máster en Ingeniería Informática  
Universidad de Granada (UGR)							               

----

**Índice**  
* Introducción	
* Resolución de tareas	
    * Preparar el entorno	
    * Captura de datos	
    * Desempaquetado de los datos	
    * Captura de fuentes	
    * Levantar la base de datos	
    * Procesado y carga de los datos	
    * Test de los servicios	
    * Levantar servicios	
        * Servicio V1	
        * Servicio V2	
* Grafo de dependencias	


## Introducción
Esta práctica consiste en la creación de un servicio de cloud completo, desde la preparación del entorno y los datos hasta el despliegue, definiendo un flujo de trabajo con Apache Airflow. En esta práctica se ha llevado a cabo tareas de preparación del entorno, de descarga de los datos y los códigos, testeo de los servicios, carga de los datos y levantar los servicios en contenedores.  
Estos servicios son APIs de tipo HTTP RESTful que permiten servir la predicción del tiempo en 24/48/72 horas. En el primer servicio se ha usado Arima para hacer la predicción de los datos y en el segundo se ha obtenidos los datos que proporciona la AEMET.

## Resolución de tareas
Antes de explicar las tareas es importante comentar que para los servicios se ha usado docker compose en el que se declaran todos los servicios (db, v1, v2).  

## Preparar el entorno
Es la primera tarea, en ella creamos la carpeta donde se guardarán y se llevarán a cabo las operaciones. Esa carpeta es /tmp/workflow.

## Captura de datos
Para la captura de datos se han utilizado 2 comandos bash, curl y wget. De esta forma obtenemos los datos de temperatura y humedad, que son guardados en la carpeta anteriormente creada, /tmp/workflow.

## Desempaquetado de los datos
Como los datos vienen comprimidos, es necesario desempaquetarlos, así que se usa un bash operator con unzip sobre los archivos, y se almacenan en la carpeta de trabajo.

## Captura de fuentes
Para poner a disposición los fuentes de los servicios se ha creado un repositorio en GitHub (https://github.com/iMiguel10/airflow-CC), que tiene 3 ramas, service_V1, que tiene lo referente al servicio 1, service_V2, que tiene lo referente al servicio 2 y la rama máster que tiene lo referente a la práctica.  
Al tener los datos en GitHub, para descargarlos, solamente hemos hecho un git clone de las ramas correspondientes (service_V1 y service_V2).

## Levantar la base de datos
Es necesario levantar un servicio de base de datos para almacenarlos, así que utilizamos un contenedor de mariadb y que levantamos con docker-compose up -d db.

## Procesado y carga de los datos
Una vez que tenemos la base de datos levantada podemos procesar los datos, para quedarnos con la fecha, la temperatura y la humedad de la ciudad de San Francisco, y almacenarla en ella. Para esta tarea se ha hecho uso de una función en python usando pandas, con la que hemos construido un dataframe con los campos anteriores y usando SQLAlchemy hemos conectado con la base de datos y los hemos cargado.

## Test de los servicios
Para testear los servicios se han creado unas pruebas, en ambos servicios, en las que se testea que la ruta /servicio/Vx/status devuelve { “status”: “OK” }. Para comprobar que se hace correctamente usamos pytest.  
Con todo esto, para llevar a cabo la tarea primero es necesario declarar las variables de entorno necesarias, entrar en el directorio de test de cada uno de los servicios y ejecutar pytest.

## Levantar servicios
En esta parte por un lado tenemos los servicios y por otro como se han levantado.
En cuanto a los servicios, tenemos 2, V1 y V2, como anteriormente se comentó.

**Servicio V1**  
En este servicio lo que se hace es coger 1000 entradas de la base de datos, y hacer una predicción de la temperatura y humedad, con arima, de la ciudad de San Francisco, para las n horas especificadas por el usuarios en la ruta /servicio/v1/prediccion/\<n>horas.

**Servicio V2** 
En este caso se han obtenido los datos de predicción de la AEMET de la ciudad de Granada por horas. Por lo que en el servicio mostramos la predicción de 24/48/72 horas como la predicción de hoy/mañana/pasado en función de la ruta que el usuario especifique. /servicio/v2/prediccion/(24/48/72)horas.

Para levantar estos servicios, se ha usado un docker compose en el que se construyen las imágenes a partir de un Dockerfile de cada servicio. Y se levantan en los puestos 8001 (V1) y 8002 (V2) con la orden docker-compose up -d.

## Grafo de dependencias
Aquí vamos a poder ver como queda el grafo de dependencias entre las tareas definidas

![Grafo1](https://github.com/iMiguel10/airflow-CC/tree/master/img/Grafo.png)  
![Grafo2](https://github.com/iMiguel10/airflow-CC/tree/master/img/Grafo2.png)
---

**Autor:** *Miguel Jiménez Cazorla*