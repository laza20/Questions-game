¡Bienvenido al repositorio del back-end de **Category's Game**! Este es un proyecto de juego de preguntas desarrollado en **Python** con el framework **FastAPI** y **MongoDB** como base de datos. Nuestro objetivo es crear una plataforma donde la comunidad sea el motor principal del contenido, permitiendo a los usuarios crear y gestionar sus propias micro y nano categorías, así como preguntas, para que la experiencia de juego sea siempre fresca y en constante crecimiento.

Este proyecto fomenta la conexión entre diversas comunidades, dándoles la posibilidad de entrelazarse y colaborar. Además, los usuarios ocasionales podrán disfrutar de una experiencia de juego casual con preguntas aleatorias de categorías generales.

## 🕹️ Modos de juego

Un usuario podrá jugar en las siguientes modalidades:

* **Categorías generales:** Juega con preguntas de todas las categorías de forma aleatoria.
* **Categorías seleccionables:** El usuario elige una categoría principal (Ej. Historia).
* **Subcategorías seleccionables:** El usuario elige una subcategoría dentro de una categoría principal (Ej. Historia -> Historia argentina).
* **Microcategorías:** Selecciona una microcategoría dentro de una subcategoría (Ej. Historia -> Historia argentina -> Próceres).
* **Nanocategorías:** Elige una nanocategoría dentro de una microcategoría (Ej. Historia -> Historia argentina -> Próceres -> San Martín).

---

## 🤝 Contribuciones de la comunidad

El pilar de este juego es su comunidad. El contenido, desde las preguntas hasta las categorías, dependerá al 100% de la colaboración de los usuarios. Más contribuciones significan más opciones y un juego más rico para todos.

Una vez que un usuario cumple ciertas condiciones (alcanzables incluso para jugadores ocasionales), se le desbloquea la posibilidad de contribuir con:

* **Creación de micro y nanocategorías.**
* **Creación de preguntas.**
* **Creación de logros para la comunidad:** Estos son desafíos o hitos que los jugadores pueden alcanzar, creados por la misma comunidad.

---

## Funcionamiento de las preguntas

Una pregunta que se encuentre dentro de una nano categoría, será además pregunta de las categorías superiores, y de esta manera sucesivamente. Mientras más grande sea tu comunidad, mayor la probabilidad de que una pregunta aparezca de forma general.

### Niveles de dificultad

Una pregunta nueva comienza con un **nivel medio**. Su nivel de dificultad subirá o bajará dependiendo de las respuestas de los usuarios.

* **Muy fácil:** Nivel de 0 puntos.
    * **Respuesta correcta:** +2 puntos para el usuario.
    * **Respuesta incorrecta:** -6 puntos para el usuario.
* **Fácil:** Nivel entre 1 y 399 puntos.
    * **Respuesta correcta:** +3 puntos para el usuario.
    * **Respuesta incorrecta:** -5 puntos para el usuario.
* **Medio:** Nivel entre 400 y 699 puntos.
    * **Respuesta correcta:** +5 puntos para el usuario.
    * **Respuesta incorrecta:** -4 puntos para el usuario.
* **Difícil:** Nivel entre 700 y 899 puntos.
    * **Respuesta correcta:** +7 puntos para el usuario.
    * **Respuesta incorrecta:** -2 puntos para el usuario.
* **Imposible:** Nivel entre 900 y 999 puntos.
    * **Respuesta correcta:** +9 puntos para el usuario.
    * **Respuesta incorrecta:** -1 punto para el usuario.
* **Infinito:** Nivel de 1000 puntos.
    * **Respuesta correcta:** +10 puntos para el usuario.
    * **Respuesta incorrecta:** -1 punto para el usuario.

### Selección de preguntas

La selección de preguntas es aleatoria, lo que mantiene a los usuarios en suspenso hasta la ronda final. Las probabilidades de aparición de cada nivel son:

* **Niveles Muy Fácil y Fácil:** 40% de probabilidad de aparecer.
* **Nivel Medio:** 30% de probabilidad de aparecer.
* **Nivel Difícil:** 20% de probabilidad de aparecer.
* **Niveles Imposible e Infinito:** 10% de probabilidad de aparecer.

---

## 🔒 Normativas y moderación

El contenido creado por los usuarios (preguntas, micro y nanocategorías) estará sujeto a un sistema de reportes y revisiones. Esto asegura que la calidad y el respeto se mantengan en la plataforma.

---

## 🧰 Tecnologías Utilizadas

* **Python 3.x:** Lenguaje principal de desarrollo.
* **FastAPI:** Framework web de alto rendimiento.
* **Uvicorn:** Servidor ASGI para ejecutar la aplicación.
* **MongoDB:** Base de datos NoSQL.
* **Pydantic:** Librería para la validación de datos.

---

## 🚀 Cómo ejecutar el proyecto

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar el servidor
uvicorn main:app --reload
