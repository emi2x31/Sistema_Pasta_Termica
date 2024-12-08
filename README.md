
![image](https://github.com/emi2x31/Sistema_Pasta_Termica/blob/main/reports/figures/bgh.png)

![image](https://github.com/emi2x31/Sistema_Pasta_Termica/blob/main/reports/figures/pasta_termica.jpg)

Bloque: Desarrollo de Sistemas de IA      Año: 2024

Autores: Ortega, Emilio Victor, Matias Daniel jerez, Carlos Manuel ghio, Gabriel garcia


--------------

SISTEMA DETECCION DE PASTA TERMICA
---------
Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial.

Politécnico Malvinas Argentinas. https://politecnico.tdf.gob.ar/

💡

# Indice

- [Objetivo del Proyecto](#Objetivo)
- [Contexto](#Contexto)
- [Conclusiones](#Conclusiones)

- [Dataset Utilizados](https://github.com/emi2x31/Congelamiento_del_Suelo/tree/main/data/external)
- [Descripción sobre origen y tipo de datos](./docs/Descripcion%20de%20los%20Datos.md)
- [Notebook del trabajo final_rutarelativa](./notebooks/Version3_PredecirCongelamientodelSuelo.ipynb)
- [Notebook del trabajo final_ruta_drive](./notebooks/Version3.1_PredecirCongelamientodelSuelo.ipynb)
- [Modelo y Analisis de Resultados](./reports/Reporte%20de%20Resultados.md)
- [Video explicativo del proyecto](/references/Emilio_ORTEGA_Congelamiento_del_Suelo_31_07_24_Aprendizaje_automatico.mp4)


# Objetivo:
----------------
Este proyecto tiene como objetivo abordar un desafío crítico en el contexto de una línea de producción electrónica de la fábrica BGH S.A.; de la ciudad de Río Grande, Tierra del Fuego.
El desafío radica en garantizar la correcta aplicación y detección de pasta térmica, un componente fundamental en el ensamblaje de dispositivos electrónicos que contribuye a la eficiencia térmica y al funcionamiento óptimo de los equipos fabricados.  
La detección precisa de la pasta térmica ya sea por ausencia, exceso o distribución incorrecta, es esencial para evitar defectos que puedan comprometer la calidad del producto final y aumentar los costos asociados a reprocesos o fallas en el uso. A pesar de los esfuerzos manuales de inspección, los errores humanos y la subjetividad en la evaluación representan un desafío significativo en la implementación de controles de calidad consistentes.  


**[⬆ Volver al Indice](#Indice)**


# Contexto
----------

Identificación del Problema  
En la producción de dispositivos electrónicos, específicamente transistores, se requiere una combinación de pasos manuales y automatizados para garantizar un ensamblaje eficiente y de alta calidad. Los pasos clave de este proceso incluyen:  
1. Colocación del disipador térmico en una plantilla que puede alojar varias unidades simultáneamente.  
2. Aplicación de pasta térmica utilizando un brazo mecánico equipado con un dosificador, asegurando que esta actúe como aislante térmico adecuado entre el disipador y el transistor.  
3. Ensamblaje del transistor sobre el disipador, fijándose mediante un destornillador neumático.  
Durante este procedimiento, la pasta térmica desempeña un papel crucial para asegurar la transferencia eficiente de calor desde el transistor hacia el disipador, lo que prolonga la vida útil y el rendimiento del dispositivo. Sin embargo, los problemas más comunes observados son:  
- Ausencia de pasta térmica, que provoca un aumento de la temperatura operativa y reduce la eficiencia del dispositivo.  
- Exceso de pasta térmica, que puede causar fugas hacia otras áreas del ensamblaje, comprometiendo la integridad del producto.  
Estos defectos no solo afectan la calidad final del producto, sino que también aumentan los costos debido a retrabajos, desperdicio de materiales y, en el peor de los casos, la devolución de productos defectuosos por parte del cliente.  



**[⬆ Volver al Indice](#Indice)**



# Conclusiones
-----------

Este proyecto tiene como objetivo no solo automatizar el control de calidad en la detección de pasta térmica, sino también sentar un precedente importante en el uso de inteligencia artificial aplicada a procesos industriales específicos. La implementación exitosa de este sistema podría transformar significativamente la forma en que se gestionan los procesos de inspección en la fábrica, mejorando la precisión, la eficiencia y la calidad del producto final.
La capacidad del sistema para detectar errores en tiempo real y reducir la dependencia de la intervención humana permitirá una mayor consistencia en la producción, además de establecer un estándar para futuras aplicaciones de inteligencia artificial en otros procesos de manufactura. Esta solución, diseñada específicamente para este entorno, puede servir como modelo para la adopción de tecnologías similares en otras líneas de producción dentro de la fábrica, ampliando su impacto positivo a largo plazo.
Impacto Esperado
- Mejora de la calidad del producto final
  La automatización del proceso de inspección garantizará que cada unidad de producto cumpla con los estándares de calidad establecidos. Al reducir la probabilidad de errores humanos en la aplicación de pasta térmica, el sistema asegurará que los productos defectuosos sean identificados y corregidos de manera más eficiente, mejorando la fiabilidad y la durabilidad del producto final.
- Reducción de costos operativos al minimizar errores humanos
  El uso de inteligencia artificial para la detección de fallos reducirá la tasa de productos defectuosos, lo que a su vez disminuirá los costos asociados con devoluciones, reprocesos y reparaciones. Al minimizar los errores humanos, también se reducirá la necesidad de intervenciones manuales, optimizando la eficiencia de los operarios y permitiendo una mayor productividad en la línea de producción.
- Incremento de la competitividad de la fábrica mediante la adopción de tecnologías avanzadas
  La implementación de tecnologías avanzadas como la inteligencia artificial en la manufactura puede ser un diferenciador clave en el mercado, posicionando a la fábrica como líder en innovación dentro de la industria. La adopción de IA no solo mejorará los procesos internos, sino que también puede incrementar la percepción de la fábrica como una entidad moderna, eficiente y capaz de adaptarse rápidamente a las tendencias tecnológicas emergentes. Esto potenciará su competitividad frente a otras fábricas que aún dependen de procesos manuales o tradicionales.
- Potencial para la escalabilidad y replicabilidad en otras líneas de producción 
  Si el sistema demuestra ser eficaz en la detección de pasta térmica, su arquitectura podrá adaptarse fácilmente a otros procesos dentro de la fábrica, como la inspección de otros componentes electrónicos o productos de manufactura. Esta escalabilidad permitirá que el sistema se utilice en varias líneas de producción, multiplicando sus beneficios y generando un impacto positivo en la planta en general.
En conclusión, este proyecto no solo mejorará los procesos de producción inmediatos, sino que también establecerá un precedente para la integración de inteligencia artificial en la industria, con el potencial de expandirse y evolucionar hacia aplicaciones más amplias y avanzadas dentro de la fábrica y más allá. 



**[⬆ Volver al Indice](#Indice)**



Organizacion del Proyecto
----------------------------------


    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
