# Snake game

El juego de la serpiente escrito en python por [Python Engineer](https://www.youtube.com/watch?v=PJl4iabBEz0&list=PLd_UDW5HeT0WDjh2QYCLoCrl--zmAFsK6&index=3&t=43s) y utilizado para aprender a como hacer un `Reinforcement Learning`. 

El código original y limpio está en su [repositorio](https://github.com/python-engineer/snake-ai-pytorch) y yo lo emborronaré con comentarios para aprender.

Antes de seguir con esto, si quieres aprender tómatelo con calma y lee lo que viene aquí abajo, incluidos los enlaces integrados.

## Notas de interés 

**Reinforce learning** ayuda a optimizar el comportamiento de un [agente](https://es.wikipedia.org/wiki/Agente_(software)) en un ambiente.

**Deep Q Learning** predicción de acciones en base a deep learning.

La organización de los ficheros se hace de la siguiente forma: juego (`ai_game.py`), agente (`agente.py`) y modelo (`model.py`). Otros: `snake_game.py` es el juego **no-adaptado** para que sea un bucle contínuo y el control del entrenamiento (`helper.py`) que introduce la información en una gráfica conforme sucede el entrenamiento. 

### Juego 

Importante que tenga una función `play_step(accion)` que *mueve* a la serpiente, y después de cada *movimiento*, obtenemos los siguientes valores:
* recompensa
* game_over (true/false)
* puntuación actual

### Agente

Enlace entre el juego y el modelo. El comportamiento del agente (*entrenamiento*) se programa bajo este concepto. 

#### El entrenamiento: 
En base al juego, calculamos un estado (`estado`) y según él calculamos la siguiente `accion`, llamando a `model.predict()`

Tras hacer la acción, haremos un nuevo `play_step` obteniendo los valores mencionados en el juego (recompensa, game_over, puntuación actual) y calculamos el nuevo estado.

Después recordamos todos los valores generados del `estado nuevo`, `estado anterior`, `recompensa`, `game_over` y `puntuación actual` para entrenar el modelo `model.train()`.

### Modelo

El modelo de entrenamiento utilizado es `Linear_QNet` con algunas capas lineales y se alimenta a partir de la información vista en el entrenamiento (`estado nuevo`, `estado anterior`, `recompensa`, `game_over` y `puntuación actual`).

Mediante la funcion `model_predict(estado)` obtenemos la siguiente `acción`.

### Variables

#### Recompensa
* Comer comida: +10.
* Morir: -10.
* Otro caso: 0.

#### Acciones
Determina nuestro próximo movimiento:
* [1,0,0] --> seguir recto
* [0,1,0] --> girar derecha
* [0,0,1] --> girar izquierda

Definir así los giros ayuda a que siempre haya giros de 90º en base a la posición relativa en el espacio.

#### Estados 
Información que le damos a la serpiente sobre el juego (11 valores):
```
[peligro_seguirfrente, peligro_girarderecha, peligro_girar izquierda,
 direccionactual_izquierda, direccionactual_derecha, 
 direccionactual_arriba, direccionactual_abajo,

 comidaala_izquerida, comidaala_derecha,
 comidaala_arriba, comidaala_abajo]
```

#### Modelo 

* Input layer: estados (11 valores).
* Hidden layer.
* Output layer: acción (3 valores) (seguir recto `[1,0,0]`, girar derecha `[0,1,0]` o girar izquierda `[0,0,1]`).


#### Q Learning 

Objetivo a conseguir: la mejor calidad de la acción.
En el hands on: 
1. Inicializamos el modelo con algunos parámetros aleatorios, 
2. Elegimos acción (`model.predict(estado)` o `movimientoaleatorio` si no sabemos mucho del juego todavía)
3. Ejecutamos acción
4. Medimos valores (recomensa)
5. Actualizamos el valor Q y entrenamos el modelo*.

*Esto de entrenar el modelo se hace teniendo en cuenta una función `loss()` que es para optimizar o minimizar. 
La [Ecuación de Bellman](https://es.wikipedia.org/wiki/Ecuaci%C3%B3n_de_Bellman) utiliza el parámetro de *learning rate (alfa)*, *ratio de descuento (gamma)* y el estado anterior (o estado 0). Sus reglas se simplifican en
```
1) Q = model.predict(estado0)
2) Qnueva = R + gamma*max(Q(estado1))
```
Y la `loss function` es: `loss = (Qnueva - Q)^2


## Destacables del `snake_game.py`

### Clases y variables

La clase de direcciones se genera para facilitar la comprensión de la orientacón de la serpiente en cada momento. En un momento original, a la serpiente se le da valor de `Direction.DERECHA` y se modifica la dirección en la función `_move(self, direction)` que es propia de la Clase SnakeGame.

Los colores se utilizan como propiedad en los objetos y están definidos en RGB. Cuanto se utiliza la función `draw.rect` se agregan diferentes parámetros entre ellos el color. Los colores se utilizan en la función `_update_ui(self)` que es propia de la Clase SnakeGame.

La variable `Point` es el plato fuerte. Almacena las coordenadas de la serpiente y de la comida. Se utiliza en la función `_move()` e `__init__()` para la serpiente y en `_place_food()` para la comida.

Otras variables son la velocidad y el tamaño del bloque (BLOCK_SIZE) de la serpiente.

### Funciones de la clase SnakeGame

* `__init__(self, w, h)`
Se inicia la pantalla. Se define ancho y alto, se le pone título y se genera (`display`).
Se inicia el juego. Se agrega atributo de dirección, se genera cabeza y se genera la serpiente como la suma de la cabeza y un par de bloques más para el cuerpo.

* `_place_food(self)`. Establece un bloque de comida en una ubicación donde no esté la serpiente.

* `play_step(self)`. 6 pasos.

1. Captura la tecla que se pulsa
2. Genera un `_move` en la dirección pulsada.
3. Comprueba si es `game_over = True` mediante `_is_collision()`. 
4. Comprueba si alcanza comida y, en ese caso, genera comida. En caso contrario mueve posiciones.
5. Actualización de UI y de reloj.
6. La función devuelve el valor de `game_over` y `puntuación`.
  
* `_is_collision(self)`. Comprueba que las coordenadas (x,y) de la serpiente están dentro del tamaño del display (w, h). Y también comprueba si las coordenadas de la cabeza están dentro de las coordenadas del cuerpo.
  
* `_update_ui(self)`. Dibuja la interfaz. Llena el display de negro, agrega cada cuerpo de la serpiente y la comida. Agrega un texto para saber la puntuación.
  
* `_move(self, direccion)`. Con cada nueva tecla pulsada, la serpiente crece, sumando a la coordenada que corresponda (x o y) el valor del tamaño del bloque. Después de la actualización de la dirección, agrega como cabeza de serpiente el nuevo valor x o y.

#### Extras en la clase de SnakeGameAI

Fuera de `snake_game.py`, dentro de `ai_game.py` tenemos el mismo script pero con modificaciones para que el juego autoreinicie solo y para que las funciones de la clase SnakeGameAI puedan ser importadas desde otro fichero (necesario para el agente).

En el paso 3 de `play_step()` lleva un control para que si el frame_iteration supera un número de iteraciones, se considere `game_over = True`.

Principalmente se ha agregado `reward` para gestionar el valor de recompensa obtenido por la actuación.

En la función `move()` se ha modificado la lógica para simplificar el saber hacia donde gira, pero es algo complejo de entender.  

Desaparece el método de arranque `if __name__ == '__main__'`.

## Para correr el código

1. Genera una ambiente en conda para esto. (yo utilicé python 3.7.10). [Instalar conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)
```conda create --name snakeai python=3.7.10```

2. Accede al ambiente de conda creado
```conda activate snakeai```

3. Instala **requirements.txt** dentro del ambiente creado (snakeai)
``` pip3 install requirements.txt```

4. Ejecuta el fichero agente.py desde el ambiente creado (snakeai)

