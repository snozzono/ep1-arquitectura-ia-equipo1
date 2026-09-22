Arquitectura para sistemas IA 2 

## 1. Análisis Empresarial 

### 1.2 Contexto del caso y Problemática 

La empresa Shop Fast está sufriendo de un problema recomendando productos a sus usuarios, específicamente a estado sufriendo de un estancamiento de las ventas los últimos 6 meses, esto debido que los usuarios tienen dificultad encontrando productos interesantes, generando que el sitio tenga una tasa de conversión del 2.3% y el valor promedio de compra de 85$ USD. 

### 1.3 Objetivo del proyecto 

Se busca como solución un sistema de recomendación de productos que invente la tasa de conversión a 4% y el ticket promedio a 120 USD mediante sugerencias personalizadas. 

## 1.4 Requerimientos 

1.4.1 Requerimientos funcionales 

R.F 1 : El sistema debe permitir al usuario buscar y filtrar productos del catálogo a partir de distintos atributos como nombre, categoría y rango de precios. 

R.F 2 : El sistema debe permitir al usuario visualizar la información detallada de un producto seleccionado, incluyendo su imagen, nombre, descripción, especificaciones y precio. 

R.F 3 : El sistema debe mostrar en la página de inicio (Homepage) una sección personalizada denominada "Recomendado para ti" con un listado de hasta 10 productos sugeridos según el perfil e historial del usuario. 

R.F 4 : El sistema debe mostrar en la página de detalle de cada producto una sección denominada "También te puede interesar" con un listado de hasta 5 productos complementarios o alternativos. 

R.F 5 : El sistema debe generar recomendaciones personalizadas para cada usuario activo a partir del análisis de su comportamiento y similitud de patrones con otros usuarios. 

R.F 6 : El sistema debe registrar en tiempo real las interacciones de los usuarios, tales como clics en productos, visualizaciones de páginas, adiciones al carrito y compras realizadas. 

R.F 7 : El sistema debe permitir registrar la valoración de los usuarios respecto a los productos, ya sea de forma explícita o deducida a partir de su historial de compras e interacciones. 

R.F 8 : El sistema debe retornar un listado de los productos más vendidos como alternativa por defecto (fallback) cuando el usuario sea nuevo, no cuente con historial previo o el servicio de recomendaciones presente demoras o fallos. 

R.F 9 : El sistema debe permitir a las aplicaciones cliente solicitar sugerencias personalizadas mediante un identificador de usuario y recibir una lista de productos ordenados por un puntaje de relevancia. 

R.F 10 : El sistema debe permitir la interacción directa con las tarjetas de productos recomendados para ver su detalle o añadirlos al carrito, contabilizando la acción para la medición del porcentaje de clics (CTR). 

R.F 11 : El sistema debe exponer un mecanismo para consultar y verificar el estado de salud y disponibilidad operativa del servicio de recomendaciones. 

### .1.4.2 Requerimientos no funcionales 

R.N.F 1 : El sistema debe responder a las solicitudes de recomendaciones con un tiempo de latencia menor a 500 milisegundos en peticiones cálidas ( _warm requests_ ). 

R.N.F 2 : El servicio de recomendaciones debe mantener una disponibilidad operativa mínima del 99% durante el horario comercial. 

R.N.F 3 : El sistema debe soportar una capacidad de procesamiento concurrente de al menos 500 usuarios simultáneos y un tráfico pico de 2.100 peticiones por hora sin degradación del servicio. 

R.N.F 4 : La infraestructura computacional en la nube (AWS) debe operar bajo un esquema de costos optimizado que no supere los $200 USD mensuales. 

R.N.F 5 : La arquitectura debe ser serverless y desacoplada mediante AWS Lambda y API Gateway, permitiendo un autoescalado elástico de 0 a 1.000 instancias según la demanda. 

R.N.F 6 : La persistencia de datos relacionales debe gestionarse a través de Amazon RDS con motor MySQL, complementada con Amazon S3 para almacenamiento duradero de modelos y datos históricos. 

R.N.F 7 : El motor de recomendación debe implementarse mediante técnicas de filtrado colaborativo con Factorización de Matrices (SVD), logrando un error cuadrático medio (RMSE) igual o menor a 0.85 y una precisión@10 de al menos 0.72. 

R.N.F 8 : Todas las comunicaciones y transferencias de datos entre el cliente web y las APIs deben estar cifradas mediante el protocolo seguro HTTPS. 

R.N.F 9 : El acceso a los endpoints de la API debe estar autenticado mediante API Keys gestionadas de forma segura en AWS Systems Manager Parameter Store y con políticas de acceso IAM basadas en el principio de mínimo privilegio. 

R.N.F 10 : La API debe implementar un control de tasa de consumo ( _rate limiting_ ) configurado a un máximo de 100 solicitudes por minuto por cliente. 

R.N.F 11 : Los registros y trazas del sistema no deben contener información de identificación personal (PII) y deben incluir un identificador único por petición ( _request_id_ ) para asegurar la observabilidad en Amazon CloudWatch. 

R.N.F 12 : El sistema debe contar con un mecanismo de resiliencia que active un reintento automático y un tiempo límite de espera (timeout) de 2 segundos, disparando el fallback de productos en menos de 500 milisegundos ante fallos de backend. 

R.N.F 13 : El proceso de integración y despliegue continuo (CI/CD) debe ejecutar despliegues de producción progresivos tipo Canary (10% por minuto) con reversión automática ( _rollback_ ) si la tasa de errores supera el 3%. 

R.N.F 14 : La arquitectura debe ser flexible y desacoplada, permitiendo la sustitución o actualización del algoritmo del modelo de aprendizaje automático sin interrumpir la operación continua del servicio. 

## 1.5 Identificación de elementos principales 

### 1.5.1 Descripción de las etapas del ciclo de vida de los datos 

A continuación se describe como los datos viajaran desde que llegan al modelo de aprendizaje continúa hasta su acoplamiento 

#### 1.5.2 Ingesta de los datos 

El modelo recibirá se alimentará de dos fuentes, los datos que se encuentren en la base de datos AWS de motor MySQL y los archivos históricos que se tengan guardado en S3 con 12 meses de antelación. Estos datos serán procesados por un pipeline, esto para asegurar que los datos lleguen limpios. 

#### 1.5.3 Entidades y atributos claves 

Como atributos o variables “Features” se encuentran **user_id, product_id, interaction_type, rating, timestamp, categoría, precio.** Si desglosamos estos atributos debido a su importancia podemos concluir con lo siguiente : 

- **user_id :** Atributo clave que sirve para identificar a un usuario de manera directa, es el uno de los atributos claves que ayudarán al modelo para ir asociando los 

productos , al final ayuda a identificar para quién va dirigido los productos recomendados. 

- **product_id :** Atributo clave que al igual que el atributo “user_id” sirve para identificar el producto a ser recomendado. 

- **Interaction_type :** Atributo que guarda el tipo de interacción, aca el modelo podría empezar a discriminar que atributo no recomendar o no, esto a base de la interacción que tuvo el usuario, por ejemplo si un usuario compró un producto en específico, el modelo de aprendizaje recomendará productos con características similares 

- **rating :** Atributo que ayudaría al modelo a discriminar productos a base de su calificación por parte de los usuarios. 

- **timestamp :** Atributo que guarda la fecha y hora , sirve para hacer auditoria 

- **categoria :** entidad y atributo el cual ayuda a poder discriminar los productos, sirve para que el modelo pueda identificar y separar los productos en clases , las clases en este caso vendrían siendo las categorías. 

- **precio :** atributo que que guarda el precio de un producto, servirá para que el usuario pueda filtrar a base de lo que dentro de su presupuesto 

#### 1.5.4 Procesamiento y transformación de los datos 

Los datos serán transformados y procesados a través de un pipeline, usando librerías como **pandas** , librería que tiene herramientas que agiliza el análisis de datos. La idea es que los datos pasen por un “lavado de cara”, sea manejando valores nulos , atípicos o que esten fuera de norma (se rompen reglas de negocio), se respetaran principios como la integridad de los datos, sea generando copias o eliminando datos que pongan en riesgo la integridad de los usuarios (datos sensibles que el modelo no quiera), se espera que los datasets entregados esten en csv para mayor velocidad de procesamiento. 

#### 1.5.5 Almacenamiento de los datos 

Dónde reposa cada tipo de dato según su uso: Amazon RDS (MySQL) para las transacciones operativas diarias y Amazon S3 como _data lake_ para el histórico y los artefactos exportados del modelo Se usará un data lake porque la fuente de datos tiende a ver no procesada, además el modelo se irá “alimentando” de datos sin procesamiento desde la fuente, ademas son mas economicos. 

### 1.6 Identificación de elementos AWS y su función 

A continuación se desglosa elementos pertenecientes a los servicios que ofrece AWS y cómo se incorporan en el proyecto : 

- Amazon SageMaker: Orquestador de cómputo para entrenamiento. Ejecuta el job semanal de forma aislada en una instancia ml.t3.medium, entrena las 150K interacciones en 15 minutos y se apaga inmediatamente para reducir costos. 

- Amazon EventBridge: Programador de tareas (scheduler). Dispara automáticamente el reentrenamiento semanal cada domingo a las 2:00 AM conectándose con SageMaker. 

- Amazon S3 (Simple Storage Service): Repositorio central de datos crudos (Data Lake) y registro de artefactos (Model Registry). Guarda tanto el historial de 12 meses como el archivo binario del modelo SVD serializado. 

- AWS Lambda: Cómputo serverless para inferencia. Carga el modelo y resuelve las solicitudes /recommendations/{user_id} en milisegundos sin mantener servidores dedicados 24/7. 

- **Amazon API Gateway:** Punto de entrada y gestión de APIs ( _API Gateway_ ). Maneja el enrutamiento HTTP hacia Lambda, implementa cifrado HTTPS, autentica mediante API Key y aplica _rate limiting_ (100 req/min). 

- **Amazon RDS (MySQL):** Base de datos transaccional ( _OLTP_ ). Almacena las interacciones diarias en caliente (clics, compras, catálogo). 

- Amazon CloudWatch: Observabilidad y gobernanza. Recolecta logs estructurados con request_id, genera métricas de latencia (p50, p95, p99) y dispara alarmas automáticas si el error rate supera el umbral crítico. 

- AWS Systems Manager Parameter Store: Seguridad y configuración. Guarda credenciales y API Keys de manera segura y desacoplada del código fuente. 

# 2. Principios de diseño arquitectónico 

A continuación se explaya como el proyecto puede cumplir con los siguientes principios arquitectónicos : escalabilidad, flexibilidad, seguridad, observabilidad y confiabilidad. 

### 2.1 Escalabilidad 

La arquitectura implementa es principalmente de tipo escalabilidad horizontal automática y elástica en su capa de servicio al cliente mediante el uso de AWS Lambda y Amazon API Gateway, permitiendo escalar de forma transparente de 0 a 1.000 instancias concurrentes para absorber picos de tráfico (validados con 500 usuarios concurrentes sin errores). En la capa de Machine Learning se aplica un modelo de cómputo efímero bajo demanda a través de Amazon SageMaker y EventBridge, aprovisionando recursos únicamente durante los 15 minutos que toma el reentrenamiento semanal, garantizando alta eficiencia en costos ($0.20/mes en entrenamiento y $28/mes en inferencia). 

Este tipo de escalabilidad es favorable para el sitio, porque es de seguir funcionando pese a fallos y además automáticamente balancea las cargas para recortar gastos, por ejemplo si se llegara a caer una instancia o está cerca de su límite, las peticiones pueden enviarla hacia otra instancia (haciendo que el sistema no se rompa), en caso de suceder lo contrario automaticamente se recortará las instancias , favoreciendo la disminución de gastos. 

### 2.2 Flexibilidad 

La arquitectura cumple con el principio de flexibilidad mediante el desacoplamiento entre la lógica de servicio y los artefactos de Machine Learning. Al almacenar el modelo como un archivo binario independiente en Amazon S3 y externalizar las variables y credenciales en AWS Systems Manager Parameter Store, el sistema permite sustituir o actualizar el motor de recomendación sin modificar el código base de la API ni alterar los contratos REST expuestos por AWS Lambda y API Gateway. Esta capacidad quedó técnicamente validada en el caso al lograr la migración del algoritmo de SVD a Alternating Least Squares (ALS) en un lapso de 2 horas sin interrumpir la operación del frontend ni requerir cambios estructurales en la infraestructura. 

### 2.3 Seguridad 

La arquitectura aplica una estrategia integral de defensa en profundidad y el principio de mínimo privilegio mediante AWS IAM, garantizando que cada componente computacional solo disponga de los permisos estrictamente necesarios para su operación. En el perímetro, Amazon API Gateway impone cifrado obligatorio vía HTTPS, autenticación basada en API Keys y control de saturación (rate limiting a 100 req/min). La gestión de credenciales se encuentra desacoplada y cifrada en AWS Systems Manager Parameter Store, evitando secretos embebidos en el código. Adicionalmente, se asegura la privacidad de los datos al utilizar datasets anonimizados y logs estructurados en Amazon CloudWatch libres de información de identificación personal (PII), logrando una validación técnica con cero vulnerabilidades críticas en pruebas de penetración (penetration testing). 

### 2.4 Observabilidad 

La arquitectura garantiza una observabilidad integral mediante el ecosistema de Amazon CloudWatch (Logs, Metrics, Dashboards y Alarms), estructurando la supervisión técnica y de negocio en tiempo real. Las trazas de ejecución en AWS Lambda se emiten en formato JSON estructurado con un identificador único (request_id) y sin datos personales (PII), permitiendo una trazabilidad granular. El monitoreo automatizado supervisa percentiles de latencia (p50 en 235ms, p95 en 420ms y p99 en 780ms), arranques en frío (4.2%) y tasas de error (0.8%), configurando alarmas proactivas segmentadas en niveles Warning (latencia >800ms) y Crítica (latencia >1.5s o errores >5%). Esta integración asegura la detección de incidentes en menos de 15 minutos y proporciona las métricas necesarias para gobernar los rollbacks automáticos en el pipeline de despliegue. 

### 2.5 Confiabilidad 

El sistema implementa mecanismos de tolerancia a fallos y degradación elegante (graceful degradation) para garantizar una disponibilidad continua del 99.4%[cite: 1]. A nivel de cliente y API, se establecen políticas de reintento automático ante errores 5xx y un tiempo límite de espera (timeout) de 2 segundos, complementado con un mecanismo de fallback que despliega productos más vendidos cacheados en menos de 500 ms ante cualquier contingencia del motor de recomendaciones[cite: 1]. Asimismo, la confiabilidad en los despliegues se asegura mediante un pipeline de CI/CD (GitHub Actions y AWS SAM) con estrategia progresiva tipo Canary (10% de tráfico por minuto) y reversión automática (rollback) si la tasa de error supera el 3%[cite: 1]. Finalmente, el almacenamiento inmutable y versionado de modelos en Amazon S3 junto al endpoint GET /health garantizan la recuperabilidad del artefacto y la verificación proactiva del estado operativo del servicio. 

### 2.6 Decisiones arquitectónicas clave, basadas en principios de observabilidad y confiabilidad 

En estos apartados sobresale herramientas como github actions, la cual hace un filtro de “calidad” de código procesado antes de pasar a producción (por ejemplo en lo que se genera en el pipeline), también el uso CloudWatch sirve para generar auditorías y generar alertas en caso de estar en riesgo el rendimiento ,también  sirve como un respaldo ante fallos. Al final el sistema contiene elementos que previenen la caída del sistema. 

## 3. Especificaciones de Infraestructura 

Los recursos computacionales determinados para este sistema se han podido calificar en dos apartados, **entrenamiento y inferencia en tiempo real.** 

###### **Fase de Entrenamiento (Amazon SageMaker):** 

- **Recursos asignados** : Instancia **ml.t3.medium** equipada con **2 vCPU y 4 GB** de RAM. 

- **Evaluación de GPU/TPU** : No se requiere el aprovisionamiento de aceleradores de hardware como GPU o TPU. El algoritmo de Factorización de Matrices (SVD) utilizado con la librería Surprise es CPU-intensivo y no aprovecha paralelismo masivo de tensores. Con este perfil de CPU, el volumen de 150.000 registros históricos entrena completamente en apenas 15 minutos, representando un costo mínimo de $0.20 USD/mes. 

###### **Fase de Inferencia en Tiempo Real (AWS Lambda):** 

- **Recursos asignados:** Funciones serverless configuradas con **1 GB de memoria RAM** . 

- **Evaluación de GPU/TPU:** La inferencia no requiere aceleración por hardware dedicado. La ejecución en CPU sobre arquitectura serverless permite procesar solicitudes en 300 ms ( _warm requests_ ) y escalar elásticamente de 0 a 1.000 instancias concurrentes según la demanda. 

### 3.1 Selección de frameworks de desarrollo de IA apropiados 

###### **Framework de IA seleccionado para hacer recomendaciones :** 

- **Python Surprise (versión 1.1.3):** Biblioteca especializada en sistemas de recomendación basados en filtrado colaborativo y factorización matricial explícita/implícita (SVD/ALS). Se selecciona porque está altamente optimizada para ejecutarse en CPU sin requerir dependencias complejas de tensores o aceleradores GPU, logrando entrenar las 150.000 interacciones en solo 15 minutos con métricas sobresalientes (RMSE 0.85 y Precisión@10 de 0.72). 

###### **Librerías complementarias del ciclo de datos:** 

- Pandas: Empleada en la capa de datos para la extracción, limpieza de interacciones y estructuración tabular de las variables (user_id, product_id, rating, timestamp, etc.) antes de alimentarlas al algoritmo. 

- **Flask / Werkzeug:** Microframework ligero que permite encapsular el artefacto serializado del modelo y servirlo como **API REST** dentro del contenedor serverless de AWS Lambda con una latencia p50 de 235 ms. 

###### **Cuestionamiento de Frameworks o librerías como TensorFlow / PyTorch:** 

- Aunque TensorFlow (mediante módulos como TensorFlow Recommenders) o PyTorch son estándares para arquitecturas neuronales profundas (redes TwoTower, Autoencoders), para el tamaño actual del catálogo (5.000 productos) y volumen de usuarios (50.000 clientes), **Surprise ofrece menor complejidad de** 

**despliegue, empaquetado mínimo para evitar penalizar el** **_cold start_ de Lambda y cumplimiento total del presupuesto mensual** ($0.20 USD en entrenamiento). Su adopción quedaría reservada como una evolución futura en caso de que el catálogo escale a millones de interacciones o requiera incrustaciones ( _embeddings_ ) multimodales de texto e imagen. 

### 3.2 Selección de servicios cloud (AWS, Azure, GCP) considerando almacenamiento, redes de comunicación y escalabilidad 

La solución planteada para este caso se despliega sobre la nube de Amazon Web Services (AWS) bajo un patrón puramente _serverless_ y desacoplado, optimizando la relación entre rendimiento y costo operativo ($50 USD/mes frente al límite de $200 USD/mes) **:** 

- **Almacenamiento:** Combina persistencia relacional transaccional mediante Amazon RDS (MySQL) para la captura continua de interacciones y catálogo, con almacenamiento masivo y duradero en Amazon S3 para alojar 2 GB de datos históricos y versionar los artefactos binarios del modelo. 

- **Redes y Comunicación:** La gestión perimetral se resuelve con Amazon API Gateway, que centraliza el enrutamiento HTTP, asegura el cifrado HTTPS, impone cuotas de consumo ( _rate limiting_ a 100 req/min) y autentica clientes con API Keys resguardadas en AWS Systems Manager Parameter Store. La orquestación temporal de eventos se delega a Amazon EventBridge para la activación periódica de procesos. 

- **Cómputo y Escalabilidad** : Se divide en dos frentes complementarios: cómputo elástico horizontal con AWS Lambda (escala de 0 a 1.000 instancias para inferencias con latencia warm de 300 ms) y cómputo efímero vertical con Amazon SageMaker (instancia ml.t3.medium que entrena 150K registros en 15 minutos y se apaga automáticamente). 

- **Observabilidad:** Amazon CloudWatch gobierna la salud de la red y el cómputo mediante trazabilidad estructurada de logs, dashboards en tiempo real y alertas que protegen la estabilidad global del sistema. 

### 3.3 Dimensionamiento inicial de recursos con estimación de costos 

El proyecto tiene como tope de inversión de **200$ USD por mes,** desglosando los gastos y uso destinado se encuentra lo siguiente : 

|**Componente /**<br>**Servicio**|**Dimensionamiento**<br>**de Recursos**|**Frecuencia /**<br>**Volumen de Uso**|**Costo**<br>**Estimado**<br>**Mensual**|
|---|---|---|---|
|**Entrenamiento**<br>**(Amazon**<br>**SageMaker)**|Instancia ml.t3.medium<br>(2 vCPU, 4GB RAM)|Semanal<br>(domingos 2 AM),<br>15 minutos de<br>ejecución por<br>corrida|**$0.20**<br>**USD/mes**|
|**Inferencia (AWS**<br>**Lambda)**|Función Serverless<br>con 1GB de memoria<br>RAM|~60,000<br>invocaciones al<br>mes bajo demanda|**$28.00**<br>**USD/mes**|
|**Almacenamiento**<br>**en la Nube**<br>**(Amazon S3)**|Capacidad de 2GB de<br>datos históricos y<br>artefactos de modelos<br>serializados|Almacenamiento<br>continuo<br>persistente|**$0.05**<br>**USD/mes**|
|**Base de Datos**|Instancia MySQL|Instancia activa|**$16.00**|



|**Relacional**<br>**(Amazon RDS)**|db.t3.micro con 20GB<br>de almacenamiento|24/7 para<br>operaciones<br>transaccionales|**USD/mes**|
|---|---|---|---|
|**Costo Total de la**<br>**Solución**|**Infraestructura**<br>**Serverless + RDS**|—|**~$50.00**<br>**USD/mes**<br>(aprox.<br>$44.25 -<br>$50 USD)|



**Costo de arquitectura tradicional (Alternativa descartada):** Mantener instancias de cómputo dedicadas tipo Amazon EC2 encendidas 24/7 costaría **$180 USD/mes** el cual es caro considerando el presupuesto, mientras que la solución serverless (Lambda + SageMaker) factura exclusivamente por los milisegundos reales de cómputo consumidos durante las invocaciones y los 15 minutos del entrenamiento semanal. 

## 4. Estrategias de Integración y Despliegue 

La estrategia de despliegue se decide tomar la estrategia **CI/CD (Continuous Integration / Continuous Deployment)** en el cual para no arruinar la experiencia del usuario o disminuir aquella probabilidad lo más que se pueda es la más viable, eso debido a que con herramientas como **GitHub Actions** se puede controlar los fallos, generando un filtro de calidad antes de entrar a producción , la herramienta **AWS Sam** también ayuda en lo mismo. 

Como estrategia de despliegue en modelos de producción se decide ir por el **Canary Deployment** el cual minimiza el fallo del modelo con los usuario, esto debido a que si las métricas van siendo positivas se va desplegando progresivamente , de esta manera como se describió anteriormente se minimiza los fallos que arruinen la experiencia de los usuarios. 

### 4.1 Comparación de alternativas de integración evaluando eficiencia, rendimiento y confiabilidad 

Otras estrategias de despliegue son **Blue/Green Deployment ,Rolling (Progresivo) ,Big bang. Despliegue por fases y Despliegue Shadow** 

#### 4.1.1 Blue/Green Deployment 

Este método de despliegue consiste en mantener dos entornos de producción idénticos: uno activo recibiendo el 100% del tráfico ( **Blue** ) y otro inactivo donde se despliega la nueva versión ( **Green** ). Una vez validado Green, el enrutador cambia el 100% del tráfico de golpe de Blue a Green,a pesar de que esta metodología tenga la ventaja de reversiones inmediatas y no generar inactividad  el **principal problema con esta estrategia es el costo** , mantener dos entornos de producción duplica los costos, eso quiere decir de que com mínimo se debería duplicar el presupuesto inicial, haciendo financieramente no sea viable. 

#### 4.1.2 Rolling (Progresivo) 

Estrategia con despliegue gradual que sustituye las versiones antiguas por las nuevas instancia por instancia o servidor por servidor, de forma escalonada. A Pesar de que esta estrategia es eficaz para microservicios, se debe tener en cuenta alta compatibilidad entre los códigos y bases de datos , eso quiere decir que para funciones mas complejas como lo puede ser en este caso integración de pipelines y modelos de aprendizaje continuo puede costar tiempo y incluso mas dinero, porque no deja ver gradualmente como rinde el modelo en producción. 

#### 4.1.3 Big Bang 

Consiste en apagar el sistema antiguo y activar el nuevo de golpe para el 100% de los usuarios, realizando un reemplazo total en un solo evento. Es el método mas riesgoso, se descarta debido a que no deja poder calificar el rendimiento del modelo de manera gradual. 

#### 4.1.4 Despliegue por fases 

Implementa el software de manera paulatina segmentando por grupos de usuarios, regiones geográficas, áreas de la empresa o módulos específicos. Debido a que es un sistema de comercio electrónico, es clave que la mayor cantidad de usuarios puedan comprar y además recibir recomendaciones, además al hacer despliegue por regiones , significa mayor inversión, específicamente en el soporte. 

#### 4.1.5 Despliegue Shadow 

Este despliegue consiste en duplicar el tráfico entrante en tiempo real de la versión activa de producción y enviar una copia exacta a una nueva versión oculta (shadow). La versión activa procesa la solicitud y responde al usuario normalmente, mientras que la versión oculta procesa la copia de la solicitud en segundo plano. Las respuestas de esta nueva versión se registran para su análisis, pero se descartan y nunca llegan al usuario final. El problema con esta estrategia es que el proyecto busca aumentar la tasa de conversión al 4% y el ticket promedio a $120 USD. Para validar si el algoritmo logra esto, es obligatorio que los usuarios reales vean las recomendaciones y decidan si hacen clic en ellas o no. Lo cual esta estrategia no ofrece porque el modelo real nunca llega al usuario. 

## 5. Pipeline Propuesto de Integración Continua y Despliegue Continuo (CI/CD) 

El sistema de ShopFast implementa un flujo de CI/CD automatizado enfocado en minimizar errores en producción, asegurar pruebas de calidad y mitigar riesgos comerciales mediante liberaciones progresivas. 

##### 5.1. Herramientas Involucradas y su Función 

- **GitHub Actions** 

Función: Plataforma central de orquestación y automatización del pipeline. Escucha los eventos de código (como un push a la rama main) y ejecuta los flujos de trabajo (workflows) secuenciales de compilación, análisis y despliegue. 

- **pytest:** 

**Función** : Framework de ejecución de pruebas automatizadas en Python. Se encarga de correr las pruebas unitarias y las validaciones de integración tanto en la fase inicial de construcción como tras el despliegue en el entorno de pruebas ( _staging_ ). 

- **AWS SAM (Serverless Application Model):** 

**Función:** Herramienta de Infraestructura como Código (IaC) orientada a arquitecturas serverless. Se encarga de empaquetar la función AWS Lambda, definir los contratos de Amazon API Gateway y gestionar los despliegues progresivos controlando la ponderación del tráfico. 

- **Amazon CloudWatch:** 

**Función:** Sistema de monitoreo y telemetría en tiempo real. Supervisa la tasa de errores durante la fase de despliegue canary para activar el mecanismo de reversión automática si se degradan las métricas. 

##### 5.2 Flujo del Pipeline Paso a Paso 

###### **El proceso de entrega continua se ejecuta en 5 etapas secuenciales:** 

1. **Push a rama main y Construcción (Build** ): 

   - El desarrollador sube los cambios aprobados al repositorio. 

   - Se ejecutan automáticamente las pruebas unitarias con pytest, el análisis estático de código (linting) y los escaneos de seguridad en busca de vulnerabilidades. 

**2. Despliegue a Staging y Pruebas de Integración:** 

   - Si el paso anterior es exitoso, AWS SAM despliega los artefactos en un entorno de pruebas ( _staging_ ) idéntico a producción. 

   - Se ejecutan 5 validaciones automáticas de pruebas de integración para certificar la comunicación entre endpoints y bases de datos. 

**3. Aprobación Manual (** **_Gate_ de Control):** 

   - Se establece una pausa de control donde un responsable técnico o líder del proyecto valida los resultados de staging y aprueba explícitamente el paso a producción. 

###### **4. Despliegue Progresivo en Producción (Canary):** 

   - El despliegue a producción no se hace de golpe; AWS SAM enruta inicialmente solo el 10% del tráfico real a la nueva versión. 

   - De forma controlada, el tráfico se incrementa en un 10% adicional cada minuto hasta alcanzar el 100% de los usuarios si las condiciones operativas son estables. 

**5. Monitoreo y Reversión Automática (** **_Rollback_ ):** 

   - Durante el despliegue canary, se evalúan constantemente las métricas en CloudWatch. 

   - Si la tasa de errores del sistema supera el 3% (error rate > 3%), el pipeline interrumpe el despliegue y ejecuta un rollback automático instantáneo hacia 

la versión previa estable, evitando afectaciones masivas a las vent6. DIagrama del Pipeline 



<!-- Start of picture text -->
Push ala ramaNN s)<br>“main”<br>Builds calidag<br>Test unitarios con pytest<br> Scaneo de seguirdad<br>probado Fall,<br>Deploy and Staging<br>-Despliegue con AWS Sam Cancelacién de Pipeline<br>5 Test de integracion<br>Exito<br>‘Aprobacion<br>manual<br>eAprobado por el<br>equipo?<br>gates Rechazado<br>= Despliegue Rechazado<br>Deploy Canary<br>-Inerementa-Inicio con unun  10%10% cadade traficominuto<br>Monitoreo CloudWatch<br>LE mor Rate < 3%?<br>Rollback 4 100% del trfico en produccién<br>Retorno a laautomaticouitima version inmediest a toble Despliegue exitoso<br><!-- End of picture text -->

### Fuentes : 

<u>Estrategias de despliegue - The Codest Fase de Despliegue en SDLC: Estrategias y CI/CD</u> 

