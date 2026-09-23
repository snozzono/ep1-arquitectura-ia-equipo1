# Diseño y Documentación de Arquitectura de Sistemas IA

## Evaluación Parcial N°1 — Informe Técnico

### Sistema de Recomendación de Productos para E-commerce (ShopFast)

- **Asignatura:** Arquitectura de Sistemas de Inteligencia Artificial
- **Sigla:** ITY1102
- **Institución:** Duoc UC — Subdirección de Diseño Curricular e Instruccional 2025
- **Tipo de evaluación:** Parcial 1 — ponderación 30%
- **Plantilla:** arc42 simplificada
- **Caso empresarial:** Caso 1 — Sistema de Recomendación para E-commerce (ShopFast)

**Equipo N°:** ___

**Integrantes:** ___________________________________________

**Docente:** ______________________________________________

**Fecha de entrega:** Semana 7 — ____ / ____ / 2026

<div style="page-break-after: always;"></div>

## Índice

- **1.1 Análisis del caso empresarial**
  - 1.1.1 Contexto del caso y problemática
  - 1.1.2 Objetivo del proyecto
  - 1.1.3 Requerimientos funcionales
  - 1.1.4 Requerimientos no funcionales
  - 1.1.5 Componentes principales de la arquitectura
  - 1.1.6 Ciclo de vida y elementos de los datos
  - 1.1.7 Elementos AWS y su función
- **1.2 Principios de diseño arquitectónico**
  - 1.2.1 Escalabilidad
  - 1.2.2 Flexibilidad
  - 1.2.3 Seguridad
  - 1.2.4 Observabilidad
  - 1.2.5 Confiabilidad
  - 1.2.6 Decisiones arquitectónicas clave
- **1.3 Especificación de infraestructura**
  - 1.3.1 Recursos computacionales (CPU, GPU y TPU)
  - 1.3.2 Selección de frameworks de desarrollo de IA
  - 1.3.3 Selección de servicios cloud (AWS, Azure, GCP)
  - 1.3.4 Dimensionamiento inicial con estimación de costos
- **1.4 Estrategias de integración y despliegue**
  - 1.4.1 Uso de edge computing
  - 1.4.2 Comparación de alternativas de integración
  - 1.4.3 Pipeline de integración continua y despliegue continuo (CI/CD)
  - 1.4.4 Diagrama de flujo de despliegue
- **Referencias**
- **Declaración de uso de herramientas de IA generativa**

<div style="page-break-after: always;"></div>

## 1.1 Análisis del caso empresarial

### 1.1.1 Contexto del caso y problemática

La empresa ShopFast presenta un problema en la recomendación de productos a sus usuarios: específicamente, ha estado afectada por un estancamiento de las ventas en los últimos 6 meses, debido a que los usuarios tienen dificultad para encontrar productos interesantes, lo que genera una tasa de conversión del 2.3% y un valor promedio de compra de 85 USD.

### 1.1.2 Objetivo del proyecto

Se busca como solución un sistema de recomendación de productos que aumente la tasa de conversión a 4% y el ticket promedio a 120 USD mediante sugerencias personalizadas.

### 1.1.3 Requerimientos funcionales

R.F 1: El sistema debe permitir al usuario buscar y filtrar productos del catálogo a partir de distintos atributos como nombre, categoría y rango de precios.

R.F 2: El sistema debe permitir al usuario visualizar la información detallada de un producto seleccionado, incluyendo su imagen, nombre, descripción, especificaciones y precio.

R.F 3: El sistema debe mostrar en la página de inicio (Homepage) una sección personalizada denominada "Recomendado para ti" con un listado de hasta 10 productos sugeridos según el perfil e historial del usuario.

R.F 4: El sistema debe mostrar en la página de detalle de cada producto una sección denominada "También te puede interesar" con un listado de hasta 5 productos complementarios o alternativos.

R.F 5: El sistema debe generar recomendaciones personalizadas para cada usuario activo a partir del análisis de su comportamiento y similitud de patrones con otros usuarios.

R.F 6: El sistema debe registrar en tiempo real las interacciones de los usuarios, tales como clics en productos, visualizaciones de páginas, adiciones al carrito y compras realizadas.

R.F 7: El sistema debe permitir registrar la valoración de los usuarios respecto a los productos, ya sea de forma explícita o deducida a partir de su historial de compras e interacciones.

R.F 8: El sistema debe retornar un listado de los productos más vendidos como alternativa por defecto (fallback) cuando el usuario sea nuevo, no cuente con historial previo o el servicio de recomendaciones presente demoras o fallos.

R.F 9: El sistema debe permitir a las aplicaciones cliente solicitar sugerencias personalizadas mediante un identificador de usuario y recibir una lista de productos ordenados por un puntaje de relevancia.

R.F 10: El sistema debe permitir la interacción directa con las tarjetas de productos recomendados para ver su detalle o añadirlos al carrito, contabilizando la acción para la medición del porcentaje de clics (CTR).

R.F 11: El sistema debe exponer un mecanismo para consultar y verificar el estado de salud y disponibilidad operativa del servicio de recomendaciones.

### 1.1.4 Requerimientos no funcionales

R.N.F 1: El sistema debe responder a las solicitudes de recomendaciones con un tiempo de latencia menor a 500 milisegundos en peticiones cálidas ( _warm requests_ ).

R.N.F 2: El servicio de recomendaciones debe mantener una disponibilidad operativa mínima del 99% durante el horario comercial.

R.N.F 3: El sistema debe soportar una capacidad de procesamiento concurrente de al menos 500 usuarios simultáneos y un tráfico pico de 2.100 peticiones por hora sin degradación del servicio.

R.N.F 4: La infraestructura computacional en la nube (AWS) debe operar bajo un esquema de costos optimizado que no supere los $200 USD mensuales.

R.N.F 5: La arquitectura debe ser serverless y desacoplada mediante AWS Lambda y API Gateway, permitiendo un autoescalado elástico de 0 a 1.000 instancias según la demanda.

R.N.F 6: La persistencia de datos relacionales debe gestionarse a través de Amazon RDS con motor MySQL, complementada con Amazon S3 para almacenamiento duradero de modelos y datos históricos.

R.N.F 7: El motor de recomendación debe implementarse mediante técnicas de filtrado colaborativo con Factorización de Matrices (SVD), logrando un error cuadrático medio (RMSE) igual o menor a 0.85 y una precisión@10 de al menos 0.72.

R.N.F 8: Todas las comunicaciones y transferencias de datos entre el cliente web y las APIs deben estar cifradas mediante el protocolo seguro HTTPS.

R.N.F 9: El acceso a los endpoints de la API debe estar autenticado mediante API Keys gestionadas de forma segura en AWS Systems Manager Parameter Store y con políticas de acceso IAM basadas en el principio de mínimo privilegio.

R.N.F 10: La API debe implementar un control de tasa de consumo ( _rate limiting_ ) configurado a un máximo de 100 solicitudes por minuto por cliente.

R.N.F 11: Los registros y trazas del sistema no deben contener información de identificación personal (PII) y deben incluir un identificador único por petición ( _request_id_ ) para asegurar la observabilidad en Amazon CloudWatch.

R.N.F 12: El sistema debe contar con un mecanismo de resiliencia que active un reintento automático y un tiempo límite de espera (timeout) de 2 segundos, disparando el fallback de productos en menos de 500 milisegundos ante fallos de backend.

R.N.F 13: El proceso de integración y despliegue continuo (CI/CD) debe ejecutar despliegues de producción progresivos tipo Canary (10% por minuto) con reversión automática ( _rollback_ ) si la tasa de errores supera el 3%.

R.N.F 14: La arquitectura debe ser flexible y desacoplada, permitiendo la sustitución o actualización del algoritmo del modelo de aprendizaje automático sin interrumpir la operación continua del servicio.

### 1.1.5 Componentes principales de la arquitectura

Los cuatro componentes exigidos (datos, modelo, API e interfaz) se materializan en ShopFast de la siguiente manera:

| Componente | Función específica | Tecnología en el caso (ShopFast) | Requerimiento(s) que satisface |
|---|---|---|---|
| **Datos** | Ingesta, limpieza y persistencia del histórico de interacciones y del catálogo que alimentan al motor | Amazon RDS (MySQL) para transacciones en caliente; Amazon S3 como data lake (12 meses, 2 GB); pandas para transformación | R.F 6, R.F 7, R.N.F 6 |
| **Modelo** | Generar recomendaciones personalizadas: filtrado colaborativo con puntaje de relevancia y alternativa de *fallback* | Python Surprise 1.1.3 (SVD); entrenamiento en Amazon SageMaker (ml.t3.medium, semanal) y artefacto serializado versionado en S3 (Model Registry) | R.F 5, R.F 8, R.N.F 7, R.N.F 14 |
| **API** | Exponer el modelo como servicio REST seguro, disponible y con control de consumo | Flask sobre AWS Lambda + API Gateway: `GET /recommendations/{user_id}`, `POST /track-interaction`, `GET /health` | R.F 9, R.F 11, R.N.F 1, R.N.F 5, R.N.F 9, R.N.F 10, R.N.F 12 |
| **Interfaz** | Presentar las recomendaciones al usuario final y permitir su interacción | Frontend React: homepage "Recomendado para ti" (10 productos) y página de producto "También te puede interesar" (5 productos), con tarjetas de imagen, nombre, precio y botón | R.F 1, R.F 2, R.F 3, R.F 4, R.F 10 |

Relacionando cada componente con su función mediante modelos de referencia (apartado c de la pauta), los cuatro encadenan el ciclo de vida **MLOps**: *ingesta* (RDS MySQL + S3) → *entrenamiento* (SageMaker, disparado semanalmente por EventBridge) → *registro de modelo* (S3 como Model Registry del artefacto SVD) → *despliegue* (API Gateway + Lambda con inferencia serverless) → *monitoreo y retroalimentaje* (CloudWatch para métricas/alarms y `POST /track-interaction` para reincorporar interacciones al data lake). Este flujo es la manifestación práctica de la **arquitectura de referencia de AWS** para workloads de IA, en la que cada servicio cubre una etapa del ciclo sin acoplar el modelo al código de la aplicación, cumpliendo además la flexibilidad exigida en R.N.F 14.

### 1.1.6 Ciclo de vida y elementos de los datos

A continuación se describe el ciclo de vida de los datos: desde su ingesta, pasando por su procesamiento y almacenamiento, hasta su consumo por el modelo de aprendizaje.

#### Ingesta de los datos

El modelo se alimentará de dos fuentes: los datos que se encuentren en la base de datos de AWS de motor MySQL y los archivos históricos guardados en S3 con una antigüedad de hasta 12 meses. Estos datos serán procesados por un pipeline, con el fin de asegurar que lleguen limpios.

#### Entidades y atributos clave

Como atributos o variables ("_features_") se encuentran **user_id, product_id, interaction_type, rating, timestamp, categoría, precio**. Su rol en el modelo es el siguiente:

| Atributo ( _feature_ ) | Descripción y rol en el modelo |
|---|---|
| **user_id** | Identifica de forma única al usuario; permite asociar y personalizar los productos recomendados para cada cliente. |
| **product_id** | Identifica de forma único el producto a recomendar. |
| **interaction_type** | Registra el tipo de interacción (clic, vista, compra); permite al modelo ponderar los comportamientos (p. ej., recomendar productos similares a los comprados). |
| **rating** | Calificación del usuario; permite discriminar productos según su recepción por parte de los usuarios. |
| **timestamp** | Guarda la fecha y hora de la interacción; sirve para auditoría y análisis temporal. |
| **categoría** | Ayuda a separar los productos en clases (categorías), facilitando el filtrado y la organización del catálogo. |
| **precio** | Guarda el precio de un producto; permite filtrar recomendaciones según el presupuesto del usuario. |

#### Procesamiento y transformación de los datos

Los datos serán transformados y procesados a través de un pipeline, usando librerías como **pandas**, que agiliza el análisis de datos. La idea es que los datos pasen por una limpieza general: manejo de valores nulos, atípicos o fuera de norma (que rompen reglas de negocio). Se respetarán principios como la integridad de los datos, generando copias de respaldo o eliminando datos que pongan en riesgo la integridad de los usuarios (datos sensibles que el modelo no deba consumir). Se espera que los datasets entregados estén en formato CSV para mayor velocidad de procesamiento.

#### Almacenamiento de los datos

Cada tipo de dato reposa según su uso: Amazon RDS (MySQL) para las transacciones operativas diarias y Amazon S3 como _data lake_ para el histórico y los artefactos exportados del modelo. Se usará un data lake porque la fuente de datos tiende a permanecer sin procesar, el modelo se irá "alimentando" de datos crudos desde la fuente, además de ser más económico.

### 1.1.7 Elementos AWS y su función

A continuación se desglosan elementos pertenecientes a los servicios que ofrece AWS y cómo se incorporan en el proyecto:

- Amazon SageMaker: Orquestador de cómputo para entrenamiento. Ejecuta el job semanal de forma aislada en una instancia ml.t3.medium, entrena las 150K interacciones en 15 minutos y se apaga inmediatamente para reducir costos.

- Amazon EventBridge: Programador de tareas (scheduler). Dispara automáticamente el reentrenamiento semanal cada domingo a las 2:00 AM conectándose con SageMaker.

- Amazon S3 (Simple Storage Service): Repositorio central de datos crudos (Data Lake) y registro de artefactos (Model Registry). Guarda tanto el historial de 12 meses como el archivo binario del modelo SVD serializado.

- AWS Lambda: Cómputo serverless para inferencia. Carga el modelo y resuelve las solicitudes /recommendations/{user_id} en milisegundos sin mantener servidores dedicados 24/7.

- **Amazon API Gateway:** Punto de entrada y gestión de APIs ( _API Gateway_ ). Maneja el enrutamiento HTTP hacia Lambda, implementa cifrado HTTPS, autentica mediante API Key y aplica _rate limiting_ (100 req/min).

- **Amazon RDS (MySQL):** Base de datos transaccional ( _OLTP_ ). Almacena las interacciones diarias en caliente (clics, compras, catálogo).

- Amazon CloudWatch: Observabilidad y gobernanza. Recolecta logs estructurados con request_id, genera métricas de latencia (p50, p95, p99) y dispara alarmas automáticas si el error rate supera el umbral crítico.

- AWS Systems Manager Parameter Store: Seguridad y configuración. Guarda credenciales y API Keys de manera segura y desacoplada del código fuente.

## 1.2 Principios de diseño arquitectónico

A continuación se explican los principios arquitectónicos que el proyecto debe cumplir: escalabilidad, flexibilidad, seguridad, observabilidad y confiabilidad.

### 1.2.1 Escalabilidad

La arquitectura implementa es principalmente de tipo escalabilidad horizontal automática y elástica en su capa de servicio al cliente mediante el uso de AWS Lambda y Amazon API Gateway, permitiendo escalar de forma transparente de 0 a 1.000 instancias concurrentes para absorber picos de tráfico (validados con 500 usuarios concurrentes sin errores). En la capa de Machine Learning se aplica un modelo de cómputo efímero bajo demanda a través de Amazon SageMaker y EventBridge, aprovisionando recursos únicamente durante los 15 minutos que toma el reentrenamiento semanal, garantizando alta eficiencia en costos ($0.20/mes en entrenamiento y $28/mes en inferencia).

Este tipo de escalabilidad es favorable para el sitio porque permite seguir funcionando pese a fallos y, además, balancea las cargas automáticamente para recortar gastos: por ejemplo, si una instancia se cae o está cerca de su límite, las peticiones se redirigen hacia otra instancia (evitando que el sistema se rompa); en el caso contrario, se reducen automáticamente las instancias, favoreciendo la disminución de gastos.

### 1.2.2 Flexibilidad

La arquitectura cumple con el principio de flexibilidad mediante el desacoplamiento entre la lógica de servicio y los artefactos de Machine Learning. Al almacenar el modelo como un archivo binario independiente en Amazon S3 y externalizar las variables y credenciales en AWS Systems Manager Parameter Store, el sistema permite sustituir o actualizar el motor de recomendación sin modificar el código base de la API ni alterar los contratos REST expuestos por AWS Lambda y API Gateway. Esta capacidad quedó técnicamente validada en el caso al lograr la migración del algoritmo de SVD a Alternating Least Squares (ALS) en un lapso de 2 horas sin interrumpir la operación del frontend ni requerir cambios estructurales en la infraestructura.

### 1.2.3 Seguridad

La arquitectura aplica una estrategia integral de defensa en profundidad y el principio de mínimo privilegio mediante AWS IAM, garantizando que cada componente computacional solo disponga de los permisos estrictamente necesarios para su operación. En el perímetro, Amazon API Gateway impone cifrado obligatorio vía HTTPS, autenticación basada en API Keys y control de saturación (rate limiting a 100 req/min). La gestión de credenciales se encuentra desacoplada y cifrada en AWS Systems Manager Parameter Store, evitando secretos embebidos en el código. Adicionalmente, se asegura la privacidad de los datos al utilizar datasets anonimizados y logs estructurados en Amazon CloudWatch libres de información de identificación personal (PII), logrando una validación técnica con cero vulnerabilidades críticas en pruebas de penetración (penetration testing).

### 1.2.4 Observabilidad

La arquitectura garantiza una observabilidad integral mediante el ecosistema de Amazon CloudWatch (Logs, Metrics, Dashboards y Alarms), estructurando la supervisión técnica y de negocio en tiempo real. Las trazas de ejecución en AWS Lambda se emiten en formato JSON estructurado con un identificador único (request_id) y sin datos personales (PII), permitiendo una trazabilidad granular. El monitoreo automatizado supervisa percentiles de latencia (p50 en 235ms, p95 en 420ms y p99 en 780ms), arranques en frío (4.2%) y tasas de error (0.8%), configurando alarmas proactivas segmentadas en niveles Warning (latencia >800ms) y Crítica (latencia >1.5s o errores >5%). Esta integración asegura la detección de incidentes en menos de 15 minutos y proporciona las métricas necesarias para gobernar los rollbacks automáticos en el pipeline de despliegue.

### 1.2.5 Confiabilidad

El sistema implementa mecanismos de tolerancia a fallos y degradación elegante (graceful degradation) para garantizar una disponibilidad continua del 99.4%. A nivel de cliente y API, se establecen políticas de reintento automático ante errores 5xx y un tiempo límite de espera (timeout) de 2 segundos, complementado con un mecanismo de fallback que despliega productos más vendidos cacheados en menos de 500 ms ante cualquier contingencia del motor de recomendaciones. Asimismo, la confiabilidad en los despliegues se asegura mediante un pipeline de CI/CD (GitHub Actions y AWS SAM) con estrategia progresiva tipo Canary (10% de tráfico por minuto) y reversión automática (rollback) si la tasa de error supera el 3%. Finalmente, el almacenamiento inmutable y versionado de modelos en Amazon S3 junto al endpoint GET /health garantizan la recuperabilidad del artefacto y la verificación proactiva del estado operativo del servicio.

### 1.2.6 Decisiones arquitectónicas clave, basadas en principios de observabilidad y confiabilidad

**Decisión 1 — Despliegue Canary gobernado por alarmas de CloudWatch**
- **Decisión:** el pipeline de GitHub Actions + AWS SAM despliega incrementalmente 10% de tráfico por minuto y CloudWatch actúa como árbitro del proceso: si la tasa de error supera el 3%, se revierte automáticamente a la última versión estable.
- **Principio(s):** observabilidad y confiabilidad.
- **Alternativas descartadas:** despliegue directo o _big bang_ (expone el 100% del tráfico sin señal previa de regresión) y _blue/green_ completo (duplica infraestructura, tensionando el límite de costos del R.N.F 4).
- **Consecuencia/validación:** cumple el R.N.F 13 (Canary 10%/min con rollback ante error >3%) y sostiene el uptime de 99.4%, por sobre el 99% exigido en R.N.F 2.

**Decisión 2 — Resiliencia en inferencia: retry, timeout 2 s y fallback**
- **Decisión:** ante errores 5xx el cliente reintenta una vez con un timeout de 2 segundos y, si el motor falla, degrada a un listado de productos más vendidos cacheado.
- **Principio(s):** confiabilidad.
- **Alternativas descartadas:** propagar el error al usuario (rompe la continuidad del servicio) y esperas de retry superiores a 2 s (incompatible con la latencia p95 de 420 ms).
- **Consecuencia/validación:** cumple R.N.F 12 (fallback en <500 ms) y R.F 8, manteniendo p50 de 235 ms y tasa de error de 0.8%.

**Decisión 3 — Trazas `request_id` sin PII y alarmas segmentadas**
- **Decisión:** Lambda emite logs JSON estructurados con `request_id` y sin datos personales, y CloudWatch configura alarmas Warning (latencia >800 ms) y Crítica (latencia >1.5 s o errores >5%).
- **Principio(s):** observabilidad.
- **Alternativas descartadas:** logs en texto libre (impiden correlación por petición) y un único umbral de alarma (genera fatiga de alerta o detección tardía).
- **Consecuencia/validación:** cumple R.N.F 11; permite detectar incidentes en menos de 15 minutos monitoreando p50 235 ms, p95 420 ms, p99 780 ms, cold starts 4.2% y errores 0.8%.

**Decisión 4 — Modelo inmutable en S3 y health check `/health`**
- **Decisión:** cada modelo SVD se registra como artefacto versionado e inmutable en S3 y API Gateway expone `GET /health` para verificar el estado operativo antes y durante la operación.
- **Principio(s):** confiabilidad y observabilidad.
- **Alternativas descartadas:** sobrescribir el archivo del modelo (impide revertir a una versión conocida) y confiar únicamente en la ausencia de errores reportados (detección reactiva).
- **Consecuencia/validación:** garantiza la recuperabilidad del artefacto y la actualización sin interrupción del R.N.F 14, coherente con R.N.F 6 (S3 como repositorio duradero).

## 1.3 Especificación de infraestructura

Los recursos computacionales determinados para este sistema se han podido calificar en dos apartados, **entrenamiento y inferencia en tiempo real.**

### 1.3.1 Recursos computacionales (CPU, GPU y TPU)

**Fase de entrenamiento (Amazon SageMaker):**

- **Recursos asignados:** Instancia **ml.t3.medium** equipada con **2 vCPU y 4 GB** de RAM.

- **Evaluación de GPU/TPU:** No se requiere el aprovisionamiento de aceleradores de hardware como GPU o TPU. El algoritmo de Factorización de Matrices (SVD) utilizado con la librería Surprise es CPU-intensivo y no aprovecha paralelismo masivo de tensores. Con este perfil de CPU, el volumen de 150.000 registros históricos entrena completamente en apenas 15 minutos, representando un costo mínimo de $0.20 USD/mes.

**Fase de inferencia en tiempo real (AWS Lambda):**

- **Recursos asignados:** Funciones serverless configuradas con **1 GB de memoria RAM**.

- **Evaluación de GPU/TPU:** La inferencia no requiere aceleración por hardware dedicado. La ejecución en CPU sobre arquitectura serverless permite procesar solicitudes en 300 ms ( _warm requests_ ) y escalar elásticamente de 0 a 1.000 instancias concurrentes según la demanda.

### 1.3.2 Selección de frameworks de desarrollo de IA apropiados

**Framework de IA seleccionado para hacer recomendaciones:**

- **Python Surprise (versión 1.1.3):** Biblioteca especializada en sistemas de recomendación basados en filtrado colaborativo y factorización matricial explícita/implícita (SVD/ALS). Se selecciona porque está altamente optimizada para ejecutarse en CPU sin requerir dependencias complejas de tensores o aceleradores GPU, logrando entrenar las 150.000 interacciones en solo 15 minutos con métricas sobresalientes (RMSE 0.85 y Precisión@10 de 0.72).

**Librerías complementarias del ciclo de datos:**

- Pandas: Empleada en la capa de datos para la extracción, limpieza de interacciones y estructuración tabular de las variables (user_id, product_id, rating, timestamp, etc.) antes de alimentarlas al algoritmo.

- **Flask / Werkzeug:** Microframework ligero que permite encapsular el artefacto serializado del modelo y servirlo como **API REST** dentro del contenedor serverless de AWS Lambda con una latencia p50 de 235 ms.

**Cuestionamiento de frameworks o librerías como TensorFlow / PyTorch:**

- Aunque TensorFlow (mediante módulos como TensorFlow Recommenders) o PyTorch son estándares para arquitecturas neuronales profundas (redes TwoTower, autoencoders), para el tamaño actual del catálogo (5.000 productos) y volumen de usuarios (50.000 clientes), **Surprise ofrece menor complejidad de despliegue, empaquetado mínimo para evitar penalizar el** **_cold start_ de Lambda y cumplimiento total del presupuesto mensual** ($0.20 USD en entrenamiento). Su adopción quedaría reservada como una evolución futura en caso de que el catálogo escale a millones de interacciones o requiera incrustaciones ( _embeddings_ ) multimodales de texto e imagen.

### 1.3.3 Selección de servicios cloud (AWS, Azure, GCP) considerando almacenamiento, redes de comunicación y escalabilidad

La solución planteada para este caso se despliega sobre la nube de Amazon Web Services (AWS) bajo un patrón puramente _serverless_ y desacoplado, optimizando la relación entre rendimiento y costo operativo ($50 USD/mes frente al límite de $200 USD/mes) **:**

- **Almacenamiento:** Combina persistencia relacional transaccional mediante Amazon RDS (MySQL) para la captura continua de interacciones y catálogo, con almacenamiento masivo y duradero en Amazon S3 para alojar 2 GB de datos históricos y versionar los artefactos binarios del modelo.

- **Redes y Comunicación:** La gestión perimetral se resuelve con Amazon API Gateway, que centraliza el enrutamiento HTTP, asegura el cifrado HTTPS, impone cuotas de consumo ( _rate limiting_ a 100 req/min) y autentica clientes con API Keys resguardadas en AWS Systems Manager Parameter Store. La orquestación temporal de eventos se delega a Amazon EventBridge para la activación periódica de procesos.

- **Cómputo y Escalabilidad:** Se divide en dos frentes complementarios: cómputo elástico horizontal con AWS Lambda (escala de 0 a 1.000 instancias para inferencias con latencia warm de 300 ms) y cómputo efímero vertical con Amazon SageMaker (instancia ml.t3.medium que entrena 150K registros en 15 minutos y se apaga automáticamente).

- **Observabilidad:** Amazon CloudWatch gobierna la salud de la red y el cómputo mediante trazabilidad estructurada de logs, dashboards en tiempo real y alertas que protegen la estabilidad global del sistema.

### 1.3.4 Dimensionamiento inicial de recursos con estimación de costos

El proyecto tiene como tope de inversión de **200$ USD por mes;** desglosando los gastos y uso destinado, se encuentra lo siguiente:

| Componente / Servicio | Dimensionamiento de recursos | Frecuencia / Volumen de uso | Costo estimado mensual |
|---|---|---|---|
| **Entrenamiento (Amazon SageMaker)** | Instancia ml.t3.medium (2 vCPU, 4 GB RAM) | Semanal (domingos 2 AM), 15 minutos de ejecución por corrida | **$0.20 USD/mes** |
| **Inferencia (AWS Lambda)** | Función serverless con 1 GB de memoria RAM | ~60.000 invocaciones al mes bajo demanda | **$28.00 USD/mes** |
| **Almacenamiento en la nube (Amazon S3)** | 2 GB de datos históricos y artefactos de modelos serializados | Almacenamiento continuo persistente | **$0.05 USD/mes** |
| **Base de datos relacional (Amazon RDS)** | db.t3.micro con MySQL y 20 GB de almacenamiento | 24/7 para operaciones transaccionales | **$16.00 USD/mes** |
| **Costo total de la solución** | **Infraestructura serverless + RDS** | — | **~$50.00 USD/mes** (aprox. $44.25 – $50 USD) |

**Costo de arquitectura tradicional (alternativa descartada):** Mantener instancias de cómputo dedicadas tipo Amazon EC2 encendidas 24/7 costaría **$180 USD/mes**, el cual es caro considerando el presupuesto, mientras que la solución serverless (Lambda + SageMaker) factura exclusivamente por los milisegundos reales de cómputo consumidos durante las invocaciones y los 15 minutos del entrenamiento semanal.

## 1.4 Estrategias de integración y despliegue

Como estrategia de integración y entrega se seleccionó **CI/CD (Continuous Integration / Continuous Deployment)**: con herramientas como **GitHub Actions** se genera un filtro de calidad antes de entrar a producción, controlando los fallos y evitando afectar la experiencia del usuario; la herramienta **AWS SAM** complementa este control durante el despliegue.

Como estrategia de despliegue de modelos en producción se seleccionó **Canary Deployment**, la cual minimiza el riesgo frente a los usuarios: a medida que las métricas son positivas, el modelo se despliega progresivamente, reduciendo la probabilidad de fallos que arruinen la experiencia de los usuarios.

### 1.4.1 Uso de edge computing

Dentro de la selección de estrategias de despliegue también se evaluó el *edge computing*, es decir, ejecutar lógica y almacenar contenido en puntos de la red cercanos al usuario final. Para ShopFast se recomienda una **adopción parcial** coherente con su patrón *serverless*: servir el frontend React mediante **Amazon CloudFront** y usar **Lambda@Edge** para cachear cerca del usuario el *fallback* de productos más vendidos (R.F 8), de modo que la respuesta degradada se cumpla en menos de 500 ms incluso si el motor de recomendaciones falla (R.N.F 12), mejorando la latencia efectiva y la tolerancia a fallos sin duplicar infraestructura (uso actual ~$50 de un tope de $200/mes). Se descarta, en cambio, llevar la inferencia SVD al *edge*: el modelo se reentrena de forma centralizada y semanal (SageMaker), mantiene estado compartido en RDS y S3, y su serializado periódico en nodos distribuidos elevaría la complejidad y el costo sin beneficio medible frente a la latencia *warm* de 300 ms ya alcanzada. El cómputo *edge* queda, por tanto, limitado a entrega y caché, no a inferencia.

### 1.4.2 Comparación de alternativas de integración evaluando eficiencia, rendimiento y confiabilidad

Se evaluaron además las estrategias **Blue/Green Deployment, Rolling (Progresivo), Big Bang, Despliegue por fases y Despliegue Shadow**:

| Estrategia | Eficiencia | Rendimiento | Confiabilidad | Decisión en este caso |
|---|---|---|---|---|
| Blue/Green | Baja: duplica entornos y costos | Alto: conmutación instantánea de tráfico | Alta: reversión inmediata | Descartada: duplicaría el presupuesto de $200/mes |
| Rolling (Progresivo) | Alta: reutiliza una sola infraestructura | Medio: depende de compatibilidad entre versiones | Media: reversión más lenta | Descartada: poca visión del rendimiento del modelo en producción |
| Big Bang | Alta: un solo evento de despliegue | Riesgoso: pico único sin validación previa | Baja: sin reversión gradual | Descartada: máxima exposición de los 50.000 clientes a fallos |
| Por fases | Media: exige segmentar por grupos o regiones | Alto dentro de cada segmento | Media-alta: daño acotado por segmento | Descartada: mayor costo de soporte e inversión por regiones |
| Shadow | Media: duplica tráfico sin impacto en usuario | Alto para comparar versiones en paralelo | Alta para validación, nula para el usuario | Descartada: el usuario nunca ve el modelo, no mide la conversión |
| **Canary (elegida)** | **Alta: un solo entorno, despliegue gradual de 10% por minuto** | **Se valida con tráfico real desde el primer minuto** | **Alta: rollback automático si el error rate supera el 3%** | **Elegida: progresión hasta el 100% con reversión automática** |

Se elige Canary porque es la alternativa más **eficiente** al operar sobre un único entorno *serverless* sin duplicar costos, la de mejor **rendimiento** observable al medir el modelo SVD con tráfico real desde el 10% inicial, y la más **confiable** al acoplar CloudWatch a un rollback automático ante un error rate superior al 3%. Las alternativas evaluadas se detallan a continuación:

#### Blue/Green Deployment

Este método de despliegue consiste en mantener dos entornos de producción idénticos: uno activo recibiendo el 100% del tráfico ( **Blue** ) y otro inactivo donde se despliega la nueva versión ( **Green** ). Una vez validado Green, el enrutador cambia el 100% del tráfico de golpe de Blue a Green. A pesar de que esta metodología tenga la ventaja de reversiones inmediatas y no generar inactividad, el **principal problema con esta estrategia es el costo**: mantener dos entornos de producción duplica los costos, es decir, como mínimo se debería duplicar el presupuesto inicial, lo que lo hace financieramente inviable.

#### Rolling (Progresivo)

Estrategia con despliegue gradual que sustituye las versiones antiguas por las nuevas instancia por instancia o servidor por servidor, de forma escalonada. A pesar de que esta estrategia es eficaz para microservicios, se debe tener en cuenta la alta compatibilidad entre los códigos y bases de datos, lo que quiere decir que para funciones más complejas, como la integración de pipelines y modelos de aprendizaje continuo en este caso, puede costar tiempo e incluso más dinero, porque no permite ver de forma gradual cómo rinde el modelo en producción.

#### Big Bang

Consiste en apagar el sistema antiguo y activar el nuevo de golpe para el 100% de los usuarios, realizando un reemplazo total en un solo evento. Es el método más riesgoso, se descarta debido a que no permite calificar el rendimiento del modelo de manera gradual.

#### Despliegue por fases

Implementa el software de manera paulatina segmentando por grupos de usuarios, regiones geográficas, áreas de la empresa o módulos específicos. Debido a que es un sistema de comercio electrónico, es clave que la mayor cantidad de usuarios puedan comprar y además recibir recomendaciones; además, desplegar por regiones significa mayor inversión, específicamente en el soporte.

#### Despliegue Shadow

Este despliegue consiste en duplicar el tráfico entrante en tiempo real de la versión activa de producción y enviar una copia exacta a una nueva versión oculta (shadow). La versión activa procesa la solicitud y responde al usuario normalmente, mientras que la versión oculta procesa la copia de la solicitud en segundo plano. Las respuestas de esta nueva versión se registran para su análisis, pero se descartan y nunca llegan al usuario final. El problema con esta estrategia es que el proyecto busca aumentar la tasa de conversión al 4% y el ticket promedio a $120 USD. Para validar si el algoritmo logra esto, es obligatorio que los usuarios reales vean las recomendaciones y decidan si hacen clic en ellas o no, lo que esta estrategia no ofrece porque el modelo real nunca llega al usuario.

### 1.4.3 Pipeline de integración continua y despliegue continuo (CI/CD)

El sistema de ShopFast implementa un flujo de CI/CD automatizado enfocado en minimizar errores en producción, asegurar pruebas de calidad y mitigar riesgos comerciales mediante liberaciones progresivas.

#### Herramientas involucradas y su función

- **GitHub Actions:** plataforma central de orquestación y automatización del pipeline. Escucha los eventos de código (como un push a la rama main) y ejecuta los flujos de trabajo ( _workflows_ ) secuenciales de compilación, análisis y despliegue.

- **pytest:** framework de ejecución de pruebas automatizadas en Python. Corre las pruebas unitarias y las validaciones de integración tanto en la fase inicial de construcción como tras el despliegue en el entorno de pruebas ( _staging_ ).

- **AWS SAM (Serverless Application Model):** herramienta de Infraestructura como Código (IaC) orientada a arquitecturas serverless. Empaqueta la función AWS Lambda, define los contratos de Amazon API Gateway y gestiona los despliegues progresivos controlando la ponderación del tráfico.

- **Amazon CloudWatch:** sistema de monitoreo y telemetría en tiempo real. Supervisa la tasa de errores durante la fase de despliegue canary para activar el mecanismo de reversión automática si se degradan las métricas.

#### Flujo del pipeline paso a paso

El proceso de entrega continua se ejecuta en 5 etapas secuenciales:

1. **Push a rama main y construcción (Build):**
   - El desarrollador sube los cambios aprobados al repositorio.
   - Se ejecutan automáticamente las pruebas unitarias con pytest, el análisis estático de código (linting) y los escaneos de seguridad en busca de vulnerabilidades.

2. **Despliegue a staging y pruebas de integración:**
   - Si el paso anterior es exitoso, AWS SAM despliega los artefactos en un entorno de pruebas ( _staging_ ) idéntico a producción.
   - Se ejecutan 5 validaciones automáticas de pruebas de integración para certificar la comunicación entre endpoints y bases de datos.

3. **Aprobación manual ( _gate_ de control):**
   - Se establece una pausa de control donde un responsable técnico o líder del proyecto valida los resultados de staging y aprueba explícitamente el paso a producción.

4. **Despliegue progresivo en producción (Canary):**
   - El despliegue a producción no se hace de golpe; AWS SAM enruta inicialmente solo el 10% del tráfico real a la nueva versión.
   - De forma controlada, el tráfico se incrementa en un 10% adicional cada minuto hasta alcanzar el 100% de los usuarios si las condiciones operativas son estables.

5. **Monitoreo y reversión automática ( _rollback_ ):**
   - Durante el despliegue canary, se evalúan constantemente las métricas en CloudWatch.
   - Si la tasa de errores del sistema supera el 3% (error rate > 3%), el pipeline interrumpe el despliegue y ejecuta un rollback automático instantáneo hacia la versión previa estable, evitando afectaciones masivas a las ventanas de despliegue.

### 1.4.4 Diagrama de flujo de despliegue

![Diagrama de flujo de despliegue (elaborado en Draw.io)](arquitectura%20parcial%201.drawio.png)

_Diagrama elaborado en Draw.io (fuente editable: DiagramaShopPipeline_v2.drawio)._

## Referencias

Amazon Web Services. (2025, 19 de noviembre). *Machine Learning Lens — AWS Well-Architected Framework*. Recuperado el 22 de septiembre de 2026, de https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html

Kreuzberger, D., Kühl, N., & Hirschl, S. (2023). Machine Learning Operations (MLOps): Overview, Definition, and Architecture. *IEEE Access*, *11*, 31866–31879. https://doi.org/10.1109/ACCESS.2023.3262138

Testi, M., Ballabio, M., Frontoni, E., Iannello, G., Moccia, S., Soda, P., & Vessio, G. (2022). MLOps: A taxonomy and a methodology. *IEEE Access*, *10*, 63606–63618. https://doi.org/10.1109/ACCESS.2022.3181730

The Codest. (s. f.). *Deployment strategies*. Recuperado el 22 de septiembre de 2026, de https://thecodest.co/en/dictionary/deployment-strategies/

## Declaración de uso de herramientas de IA generativa

Durante el desarrollo de este trabajo se utilizaron herramientas de inteligencia artificial generativa como apoyo al proceso de investigación, redacción y revisión. El uso de estas herramientas se resume a continuación, indicando la herramienta empleada y el propósito específico en cada caso:

| Herramienta | Propósito de uso |
|---|---|
| [VERIFICAR: p. ej. ChatGPT / Gemini / Copilot] | Redacción inicial, reestructuración y revisión de coherencia y estilo de las secciones del informe. |
| [VERIFICAR: p. ej. ChatGPT / GitHub Copilot / Mermaid AI] | Generación de borradores de código (plantillas AWS SAM, flujos de GitHub Actions) y bocetos de diagramas de arquitectura, posteriormente editados por el equipo. |
| Documentación técnica oficial (AWS, GitHub) y verificación manual | Todo el contenido técnico —arquitectura, servicios, estrategia de despliegue canary y referencias— fue contrastado y verificado por el equipo contra la documentación oficial antes de su inclusión; la responsabilidad del contenido final es del equipo. |

[VERIFICAR: nombre exacto de cada herramienta, versión/modelo y fecha de uso, según lo que realmente empleó el equipo.]
