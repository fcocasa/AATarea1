Como ejecutar el codigo y correr pruebas?

- Setear las variables para la prueba, tanto los pesos en el json como params en el modelo y el algoritmo
- En el root del proyecto ejecutar 
```bash
python3 train.py > /pruebas/train.txt
```
- El archivo generado contiene el resultado del entrenamiento, y se puede usar para obtener informacion sobre el progreso de los parametros wi (ver parse_results_for_graph.py)
- Copiar los parametros obtenidos en `g08_model.json` a `my_model.json` (este es el archivo que busca test.py)
- En el root del proyecto ejecutar 
```bash
python3 train.py > /pruebas/test.txt
```
- El archivo generado contiene el resultado de los tests y puede ser usado para establecer el rendimiento de la solucion entrenada