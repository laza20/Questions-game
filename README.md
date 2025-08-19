# CATEGORY'S GAME (Back end) 🎯

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

Una pregunta que se encuentre dentro de una nano categoria, sera ademas pregunta de las categorias superiores y de esta manera sucesivamente. Asi que, mientras mas grande sea tu comunidad mayor probabilidades de que una pregunta aparezca de manera general.


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
