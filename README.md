# Juego Retro Bomberman

## Descripción
Este es un juego estilo retro de Bomberman desarrollado en Python utilizando la biblioteca Pygame. El juego cuenta con múltiples niveles de dificultad creciente, varios tipos de enemigos incluyendo un jefe final, y opciones de personalización del jugador como skins y nombres. El objetivo es navegar por los niveles, evitar enemigos y trampas, encontrar llaves y llegar al portal para avanzar.

## Instalación

1. Asegúrate de tener Python 3.x instalado en tu sistema.
2. Instala las dependencias necesarias usando pip:
   ```
   pip install pygame pygame-menu
   ```
3. Clona o descarga este repositorio en tu máquina local.

## Cómo Ejecutar

Ejecuta el script del menú principal para iniciar el juego:
```
python main_menu.py
```

## Características del Juego

- **Múltiples Niveles:** Cuatro niveles con dificultad creciente y diferentes tipos de enemigos.
- **Personalización del Jugador:** Elige tu nombre y selecciona entre tres skins diferentes.
- **Enemigos:** Varios tipos de enemigos con comportamientos únicos, incluyendo un jefe desafiante.
- **Mecánica de Bombas:** Coloca bombas estratégicamente para derrotar enemigos y despejar obstáculos.
- **Sistema de Puntuación:** Lleva un registro de tu puntaje y compite por los 5 mejores puntajes.
- **Audio:** Música de fondo con opción para activar o desactivar el sonido.
- **Controles:**
  - W: Mover Arriba
  - A: Mover Izquierda
  - S: Mover Abajo
  - D: Mover Derecha
  - Espacio: Colocar Bomba

## Estructura del Proyecto

- `main_menu.py`: Menú principal y lanzador del juego con opciones de personalización, configuración, puntajes y acerca de.
- `game.py`: Lógica principal del juego, incluyendo el ciclo de juego, gestión de niveles, generación de enemigos y renderizado.
- `player.py`: Implementación del personaje jugador.
- `enemy.py`: Tipos y comportamientos de enemigos.
- `bomb.py`: Mecánica de colocación y explosión de bombas.
- `maps.py`: Mapas de niveles y configuración del entorno.
- `user_manager.py`: Gestión de datos de usuarios y puntajes.
- `finalScreen.py`: Pantalla final del juego.
- `colisions.py`: Detección y manejo de colisiones.
- `elements.py`: Elementos del juego como el gestor de puntajes y el portal.
- `show_information.py`: Elementos de la interfaz como textos y barras de estado.
- `constans.py`: Constantes del juego como colores, tamaño de ventana, fuentes y títulos.
- `Assets/`: Contiene todos los recursos del juego incluyendo imágenes, sonidos, fuentes y archivos de datos.
- `scripts/`: Scripts utilitarios para cargar animaciones y gestionar rutas.

## Datos de Usuarios y Puntajes

Los nombres de usuario, skins seleccionados y puntajes se guardan en un archivo JSON ubicado en `Assets/data/scores.json`. El juego registra y muestra los 5 mejores puntajes en el menú principal.

## Créditos
Este proyecto fue desarrollado por estudiantes del Tecnológico de Costa Rica:
- Jason Martínez Gutiérrez (j.martinez.4@estudiantec.cr)
- Mainor Martínez Sánchez (m.martinez.3@estudiantec.cr)
Este proyecto se encuentra en github en el siguiente enlace: https://github.com/Jason-Martinez/Bomberman
