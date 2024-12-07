Proyecto de Basico basado en youtube Snowflake/dbt/airflow.

Hecho por Jose Junior, Cristopher y frania 

vamos a lo mas basico para que valla viendo como es que se a explicar los indicio de este proyecto. 
•	Extracción y carga de datos en Snowflake utilizando nuestro entorno local en contenedores.
•	Transformación de datos probada, controlada por versiones y documentada utilizando la conexión dbt a Snowflake.
•	Orquestación de todo el pipeline mediante flujo de aire.

 ejecutar los siguientes comandos:
•	ejecución dbt
•	prueba dbt

Recursosque se deben utilizar :
•	Obtenga más información sobre dbt en los documentos
•	Consulta Discourse para ver las preguntas y respuestas más frecuentes
•	Únase a la comunidad dbt para aprender de otros ingenieros analíticos
•	Encuentra eventos de dbt cerca de ti
•	Consulte el blog para conocer las últimas noticias sobre el desarrollo y las mejores prácticas de dbt.

Detalles de este proyecto:
•	Descargue el conjunto de datos de Kaggle: https://www.kaggle.com/datasets/joebeachcapital/startups

•	Configuración de copo de nieve:
o	Base de datos 'RAW' con el esquema 'STARTUPS' que contiene el formato de archivo y estado para cargar los datos preparados.
o	Base de datos 'STARTUPS' que se utiliza para los datos transformados.

o	DBT_ROLE se utiliza para el proyecto dbt: esto requerirá permisos relevantes para leer los datos sin procesar.
o	AIRFLOW_ROLE se utiliza para conexiones de flujo de aire: esto requerirá permisos relevantes para el esquema de inicio en la base de datos sin procesar, para cargar archivos en el escenario y copiar datos del escenario en tablas.

•	Configuración de DBT:
o	Cree una cuenta con conexión a Snowflake. Utilice la base de datos STARTUPS y configure un esquema (por ejemplo, dbt_schema) (aquí es donde dbt escribirá los datos transformados). Utilice el rol DBT_ROLE.

o	En dbt, preparamos nuestros datos con pequeñas transformaciones, probamos los datos preparados y luego los transformamos en un modelo intermedio normalizado con restricciones y relaciones clave probadas. A partir de ahí, podríamos agregar más transformaciones para convertir los datos en modelos dimensionales y datamarts, etc. Puede encontrar más información sobre la estructura de archivos aquí: https://docs.getdbt.com/guides/best-practices/how-we-structure/1-guide-overview
o	Vea este curso: https://courses.getdbt.com/courses/fundamentals
o	Además, estos documentos sobre paquetes: https://docs.getdbt.com/docs/build/packages (usamos los paquetes db-utils una vez para probar la unicidad en múltiples columnas)

•	Configuración del flujo de aire:
o	Consulte este repositorio para obtener información más detallada sobre cómo configurar el flujo de aire.
o	Aquí solo usamos la imagen base de flujo de aire en nuestro docker-compose, con las configuraciones adicionales de contenedor y volumen para el programador y la base de datos.
o	Nuestro DAG contiene todas las tareas necesarias para:
	Descargar archivos (Aquí estamos descargando los datos de Kaggle, necesitará tener instalada la API de Kaggle)
	Cargue los archivos en nuestro escenario en Snowflake (usando un PythonOperator que contiene un objeto Snowflake Connection obtenido usando la función SnowflakeHook)
	Copiar los datos de la etapa a la tabla utilizando el formato de archivo almacenado en Snowflake. Para ello, se utiliza SnowflakeOperator y el script SQL almacenado localmente.
