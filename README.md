# Entregable Tarea 05

**Módulos**
    
Hice un modulo llamado FronEnd que corresponde al FrontEnd (obviamente xd) y es donde se ejecuta el juego. Sin embargo el BackEnd lo dividí en los demás modulos, donde creo la clase entidades, jugadores, tiendas, los widgets que necesité, etc. Además tengo un modulo de funciones y uno de textos y datos que ocupé para las stylesheet o otros fines.

**Archivos**
    
Tengo una gran cantidad de archivos pero es porque personalicé mucho la interfaz, asique pido perdón de antemano por hacerte bajarte muchas cosas :c. (Sólo quería hacer un juego que podría jugar mi hermana chica :$)
    
**Alcances**


- **Entidades**:

    El jugador lo cree a partir de un QThreads y los enemigos por medio de un QTimer. Están bien definidos el tamaño, la vida, el ataque y la velocidad de ataque. Sin embargo, no entendí bien como modificar la velocidad de ataque del jugador principal, ya que pensé que todos los ataques eran bidireccionales, entonces, no me pareció lógico que aumentara su velocidad. En el fondo sería como aumentar la velocidad de ataque tanto de enemigos como del jugador. Sin embargo, deje que tuviesen que esperar un segundo entre los ataques.

- **Personaje Principal**:

    El personaje principal está bien definido. Al llegar a 500 ptos de experiencia crece y al pasar de nivel también (1000 ptos). Con un tamaño máximo de 10. El movimiento también está correctamente definido.
    
- **Enemigos**:

    Los enemigos están bien definidos. Si el personaje entra en el rango de visión, entonces se activa el rango de escape. Luego si el enemigo es más chico que él, entonces lo perseguirá hasta salir de su rango de escape, y si es más grande que él, se escapará hasta salir del rango. Finalmente si son del mismo tamaño, con probabilidad 0.5 hará uno y la otra. Respecto a la inteligencia, lo configuré de manera que se moviera más natural. Esto es con probabilidad 0.25 avanza, con probabilidad 0.25 retrocede y con las otras gira en un sentido o en otro, sin embargo esto lo hice en intervalos de 0.2 segundos.

    
- **Colisiones**:

    Las colisiones están bien logradas. Programé el choque entre personajes de tal manera que cuando el personaje principal choca con el enemigo, ambos siempre se atacarán mirándose, ya que no tiene sentido sino atacar ambos de espaldas o uno si y otro no, y que ambos sean dañados de todas maneras. 
    
    
- **Etapas**:
    
    - Cambio de tamaño: escogí un tamaño incial decente para que se notaran las entidades y para que a nivel diez no sea taaan inmenso. 
    - Elementos del juego: 
        1. La bomba (en mi cazo es una trampa para osos por la temática) está bien lograda pero en vez de diez unidades (que era muuy poco:c) decidí ponerle el area misma de la imagen que además me parecia más intuitivo.
        2. La safe zone (cueva) están bien e incluso los enemigos no te persiguen o escapan si estás en ella (como corresponde xd) y no se resetean al pasar de nivel. Al comienzo había configurado para que apareciera una solamente pero luego ví que tenian que salir con la misma frecuencia que los demás objetos por lo que a veces parece que se sobrecargara de safes zones :c.
        3. Puntos extras (monedas) entregan mil puntos correctamente. Parece que por un problema de imagen como que se "lagea" al tomarla pero es minimo. :c
        4. Vida extra (comida o bambu dependiendo que oso se escoja) recupera la totalidad de tus puntos.
        5. Todos aparecen en lugares random.


- **Aparición de enemigos**:
    
    - En el módulo textos copie los datos de la tabla del enunciado de donde saqué los datos para el tamaño  y la frecuencia (expovariate de parámetro dependiendo del nivel).
    - Al pasar de nivel se chequea si el nivel en el que estaba era 5, donde si es que lo era, se termina el juego (funcion pasar_nivel() del front end y también se actualiza el tamaño del jugador principal. También reseteaba los objetos excepto las cuevas que son estáticas por el resto de la partida.
    
    
- **Puntaje**:
    
    - Se me fue complamente lo de la lectura del archivo, de hecho lo empece a hacer a las 23:50 del lunes pero terminé a las 12:10 y ya habían retirado los commits u.u (not even close) por lo que los puntajes se pueden solamente obtener mediante las monedas. Sin embargo, si hice eso de pedir el puntaje una vez finalizado la partida. Y efectivamente se guarda y se carga al cerrar y abrir el juego.
    

- **Tienda**:
    
    - La tienda se accede por el boton tienda o por el comando ctrt+t y tiende los tres objetos. Sin embargo y como dije que no me resultaba logico lo de la velocidad de ataque, este bonus lo programé como ataque. Es decir comprar el objeto de velocidad de ataque equivale a hacer 15% más de daño. Los demás objetos están como corresponde. 
    - El inventario de la tienda está correcto y se deben arrastras ahí los objetos para comprarlos. Se puede reemplazar un objeto por otro pero nunca más tener más de 5 objetos. No se puede comprar si no alcanza y se descuenta correctamente al comprar. Para programar el arrastre lo hice mediante coordenadas y press and release events (busqué cómo hacerlo con Qgraphics sin embargo no entendí bien y me había resultado ya de esta manera xd). 
    - Otro cambio que hice fue que al comprar el item de vida, se iba a recuperar la vida del player. Esto lo hice para que no fuera imposible avanzar en el juego.


- **Interfaz**:
    
    - Mis spritesheet son de osos (polar, panda, pardo). Se puede apreciar correctamente el daño (un poco sangriento xd), movimiento y el ataque. El botón de salida te lleva a una ventana para guardar el puntaje y luego en el menu te muestra el puntaje obtenido.
    

- **Bonus**:
    
    - Estiloso: 
        1. Sprites: cambie las sprites por unas que encontré sin embargo solo contenían el movimiento, por lo que tuve que modificarlas para poder representar el daño y la muerte.
        2. Fondo: Todos los botones y fondos están enchulados jeje.
    - Desarrollador: 
        1. efectos sonoros: hay efectos sonoros en todo, botones, ataque, muerte, comida, monedas y trampas.
        2. busqueda de música: me faltó , fallé, perdí (lo siento xd).
        3. Fullscreen: todo se ajusta correctamente.
        
    - Cooperativo:
        1. Me faltó tiempo porque me fui a macabear el finde completo :'(
        
- **Si tienes tiempo**:
    - Si te gustó algo mi tarea, fuera de plazo la arreglé y ahora tiene todo menos el modo dos jugador y poder escoger la playlist. Por si quieres echarle una mirada.
    No hay problema si no te gustó o no tienes tiempo :p suerte corrigiendo :)!
    

## Datos del alumno

| Nombre | Mail UC |
| :-: | :-: |
| Javier Bahamondes | jfbahamondes@uc.cl |

