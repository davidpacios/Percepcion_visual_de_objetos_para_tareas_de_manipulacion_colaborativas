# Resumen

El robot cuenta con una cámara RGB-D y sensores táctiles para tratar de generar un modelo 3d del objeto, esto se consigué a través de diferentes técnicas como Ball Pivoting algorithm y Poisson surface reconstruction que trabajan sobre la nube de puntos y contruyen el modelo 3d.

Los sensores táctiles y la cámara necesitan de una buena calibración para evitar errores, además la cámara necesita una condiciones óptimas de luz...

Para la recontrucción del modelo 3D, se analiza el objeto si su simetría es: exacat, aproximada, simetría local, simetría global, simetría extrínseca o intrínsica. Encontrar la simetría de ciertos objetos es muy complejo, por ello hoy en día se centra en utilizar una vista simple de una cámara RGB-D.

La pipeline: De forma paralela se consigue información del objeto:

            RGB-D: Depth image --> raw pointcloud --> cleaned pointcloud -->
                                                                                Joined pointcloud
            Gelsight: Height map y Contact Mask --> Processed image -->

# Vocabulario

Los parámetros intrínsecos específicos de cada cámara permiten mapear entre las coordenadas de los píxeles y las coordenadas de la cámara en el marco de la imagen; estos parámetros incluyen la distancia focal, el centro óptico y el coeficiente de inclinación. La distancia focal y los centros ópticos se pueden utilizar para crear una matriz de cámara, que se puede utilizar para eliminar la distorsión causada por las lentes de una cámara en particular. La matriz de la cámara es exclusiva de una cámara en particular, por lo que una vez calculada se puede reutilizar para otras imágenes tomadas con la misma cámara. Se expresa como una matriz de 3x3.

Los parámetros extrínsecos describen la orientación y posición del cámara. Esto se refiere a la rotación y traslación de la cámara con respecto a algunos sistemas de coordenadas mundiales. Los parámetros extrínsecos se pueden definir como una matriz de traslación T y una matriz de rotación R.

# Preguntas

¿Se van a utilizar objetos prefijados o se va a utilizar lo de Marc, complejidad de la simetría?
¿Taxim uso?
¿FCRN entiendo que es el nombre de todo el sistema, cámara RGB-D y los sensores tácticos?
¿Resultados: For height map estimation, the custom FCRN outperforms the benchmark with an average RMSE of 0.1370 over the 30 objects with 60 images in each object from the YCB-Sight dataset, while the benchmark method obtained an average RMSE of 5.1430.
For the contact mask estimator, the average IoU obtained by the custom FCRN network is 0.3320, while the image thresholding method used as a baseline obtained results of 0.7740, which is lower?

# Proceso

Pipeline: Pipeline de Marc(se obtiene un modelo 3d del objeto) | Pipeline de David(movimiento del brazo robot)intrinsic and extrinsic parameters

# Algoritmos

Pivote de Bola(BPA): Se generan cada tres puntos triángulos.
Reconstrucción de superficies de Poisson: Obtener una superficie más suave (entiendo que evitar picos por vértices de los triángulos generados en el Algoritmo de Pivote de Bola).

# Evaluadores

RMSE: Root mean squared error --> Sumatorio de las diferencias entre el valor verdadero y la estimación del modelo.
IoU: Intersection over Union --> Calcula la superposición entre cuadro delimitador previsto o región segmentada y su verdad fundamental valores, proporcionando una medida de qué tan bien se predijo la máscara o el marco delimitador coincide con el objetivo real.
Chamfer Distance: Métrica que evalua la distancia entre dos conjuntos de puntos.

# Librerias y Tecnologías

RVIZ with ROS: permite generar la nube de puntos de toda la escena a la que apunta la camara.
Open3D: para eliminar los puntos que no pertenecen al objeto.
Taxim: simulador de modelos (uso??)
SymetryNet: librería que permite predecir la simetría especular(asociación punto a punto) y simetría rotacional(misma forma despues de aplicarle una rotación) a través de la imagen de la cámara RGBA-D
Open NI: libreria de ROS para calibrar la cámara.

# Apéndice

Calibración de la cámara, necesario calibrar los parámetros intrinsecos y extrinsicos: se generan las siguientes matrices:

2D Coordenadas(imagen virtual)[3,1] = M.Intrinseca(Centro optico, escalado...)[3,3] _ M.Extrínseca[3,4] _ 3D Coordenadas[4,1]

# Continuación

Lo único que faltaba era la capacidad de detectar automáticamente la posición del objeto y mover el brazo para que el tacto fuera autónomo. Esta es una tarea que requiere mucho tiempo, ya que la manipulación automática del robot no es una implementación sencilla.

# Código

Dos redes neuronales:

FCRN_CPU
├── custom_dataloader.py
├── custom_dataloader_test.py
├── environment.yml
├── fcrn.py
├── inference.py
├── loader.py
├── train.py
└── weights.py

FCRN_mask_CPU
├── custom_dataloader.py
├── custom_dataloader_test.py
├── environment.yml
├── fcrn.py
├── inference.py
├── loader.py
├── train.py
└── weights.py

custom_point_cloud_analysis.py
fcrn_metrics_extractor.ipynb
final_results_numbers.xlsx
join_pointcloud.ipynb
object_reconstruction.ipynb
