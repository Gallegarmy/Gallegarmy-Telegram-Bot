# Bot de Telegram en Python

Este es el bot de Telegram de Sysarmy Galicia. Este bot está diseñado para manejar la gestión de karma entre usuarios, información sobre eventos, dividir la cuenta en las AdminCañas y algunas opciones divertidas para interactuar.

## Indice
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Comandos](#comandos)
- [Contribución](#contribución)

## Requisitos

- Python 3.7 o superior
- Librería python-telegram-bot
- Cualquier otra dependencia especificada en el archivo requirements.txt

## Instalación

1. **Clona el repositorio en tu máquina local:**
   
```bash
git clone https://github.com/tuusuario/tu-repositorio.git
cd tu-repositorio
```

2. **Instala las dependencias necesarias:**

```bash
pip install -r requirements.txt
```

3. **Configura el bot con tu token de Telegram. Crea un archivo .env en el directorio raíz y añade la siguiente línea:**

```bash
TELEGRAM_TOKEN=tu_token_aqui
```

4. **Ejecuta el bot:**

```bash
python main.py
```

## Comandos

**Comandos generales:**

* /start: Este comando envía un mensaje de bienvenida cuando un usuario inicia una conversación con el bot. Se utiliza para corroborar que el bot esté funcionando.

* /cerveza: Proporciona información sobre el próximo evento de "admin cañas", nuestro evento social mensual (El 1º viernes de cada mes ;) ).

* /pineapple: Envía un mensaje divertido sobre la piña, considerada por algunos como un manjar tropical.

* /help: Muestra una lista de todos los comandos habilitados en el bot, brindando una guía rápida para los usuarios.

* /festivos: Informa sobre el próximo día festivo en Galicia. Este comando acepta un parámetro opcional (str) para indicar un departamento específico y obtener detalles sobre fiestas regionales.


```bash
/festivos Arteixo
```

**Comandos de Karma:**
* /kup [usuario]: Aumenta el karma de un usuario o cosa en uno. Ideal para reconocer buenas acciones o comentarios.
```bash
/kup @Qrow01
```

* /kdown [usuario]: Disminuye el karma de un usuario o cosa en uno. Se utiliza para marcar comportamientos o comentarios inapropiados.
```bash
/kdown Java
```

*/kshow [usuario]: Muestra el nivel de karma actual de un usuario o cosa en específico.
```bash
/kshow @Qrow01
```

* /klist: Muestra un ranking de usuarios y cosas con más y menos karma, permitiendo ver quién es el más apreciado (o menos) en el grupo.

**Comandos de Menú:**

(Estos comandos solo están habilitados para el canal 'Pedidos comida', el cual permanece cerrado hasta el día de las admin cañas. Si quieres adaptar este bot para tus propios prositos modifica el FOOD_THREAD_ID en dinner.py con tu propio thread_id)

(Los administradores deben iniciar la cena para que estos comandos se habiliten)

* /order [id_number]: Permite a los usuarios ordenar un ítem del menú basado en un número de identificación proporcionado. Adicionalmente se puede proporcionar un número (int) como segundo argumento para ordernar más de un item
```bash
/order 23 2
```
* /beer: Agrega un vaso de cerveza a la cuenta del usuario que envía el comando. Este comando es útil para dividir la cuenta al final de un evento, gracias a la idea de @jjqrs.

## Contribución

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
3. Realiza tus cambios y haz un commit (git commit -am 'Agrega nueva funcionalidad').
4. Haz un push a la rama (git push origin feature/nueva-funcionalidad).
5. Crea un Pull Request.
