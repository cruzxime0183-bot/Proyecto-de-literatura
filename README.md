## ¿Cómo funciona el programa?

El programa **TEST LITERATURA** es un cuestionario interactivo desarrollado en Python que permite al usuario poner a prueba sus conocimientos mediante preguntas de opción múltiple.

Su funcionamiento se divide en los siguientes pasos:

1. **Carga de preguntas:** El programa busca y lee un archivo de texto llamado `PREGUNTAS EJERCICIO 10.txt`, donde se encuentran almacenadas las preguntas, sus cuatro opciones y las respuestas correctas.

2. **Organización de preguntas:** Lee la información del archivo y organiza cada pregunta con sus respectivas opciones y respuesta correcta. Puede reconocer preguntas escritas en una sola línea o distribuidas en varias líneas.

3. **Menú principal:** Al iniciar, muestra tres opciones:
   - Jugar.
   - Ver puntaje actual.
   - Salir del programa.

4. **Selección de preguntas:** Cuando el usuario selecciona jugar, puede elegir cuántas preguntas desea responder. El programa selecciona las preguntas de manera aleatoria para que cada ronda pueda ser diferente.

5. **Resolución del cuestionario:** Las preguntas aparecen una por una con cuatro opciones de respuesta (A, B, C y D). El usuario debe ingresar la letra que considere correcta. El programa valida que la respuesta ingresada sea válida.

6. **Verificación de respuestas:** Después de responder, el programa muestra cuál era la opción correcta y señala la respuesta seleccionada por el usuario.

7. **Sistema de puntuación:** Por cada respuesta correcta se otorgan 10 puntos. El programa registra los aciertos y mantiene un puntaje acumulado durante la ejecución.

8. **Resultados finales:** Al terminar cada ronda, muestra la cantidad de respuestas correctas, el porcentaje de aciertos, los puntos obtenidos y el puntaje total acumulado.

9. **Finalización:** El usuario puede consultar su puntaje, iniciar otra ronda o seleccionar la opción de salir para finalizar el programa.

### Objetivo del programa

Facilitar el aprendizaje y la práctica de literatura mediante un cuestionario dinámico, organizado y sencillo de utilizar, que permita evaluar los conocimientos del usuario y llevar un registro de sus resultados.
