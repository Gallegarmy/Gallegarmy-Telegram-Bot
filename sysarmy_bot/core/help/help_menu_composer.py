GENERAL_MENU = """
Commandos actualmente habilitados en el bot:
/start - Mensaje de bienvenida
/events - Informacion del proximo evento de admin cañas
/pineapple - Un manjar tropical
/help - Listado de comandos habilitados
/festivos - Indica el festivo más próximo de Galicia, acepta un parametro str indicando un departamento especifico para buscar fiestas regionales
Comandos Karma:
/kup [usuario] - Agrega uno de karma a un usuario
/kdown [usuario] - Quita uno de karma a un usuario
/kshow [usuario] - Muestra el karma de un usuario
/klist - Muestra un top de usuarios con más y menos karma
/qadd - Se ejecuta respondiendo a un mensaje, añade ese mensaje a la tabla quotes
/q (opcional)[usuario] - Muestra una quote al azar o 3 quotes al azar de un usuario
"""

USER_ALLOWED_CMDS = """
Commandos de Menu:
/order [id_number] - Ordena un item del menú
/beer - Agrega un vaso de cerveza a nombre de quien envió el comando (Se usa para dividir la cuenta, cortesía de @jjqrs)
"""

ADMIN_ALLOWED_CMDS = """
Commandos de Menu:
/startdinner - Inicia la cena habilitando a los usuarios a pedir
/order [id_number] (Optional)[amount]- Ordena un item del menú
/roundorder - Cierra una ronda de pedidos y muestra los pedidos ingresados para hacer al camarero
/pricechange [id_number] [new_price]- Cambia el precio de un item con el id pasado
/enddinner (Optional)[Opciones_para dividir] - Termina la cena, se puede dividir toda la cuenta entre todo, o dividir toda la cuenta salvo "bebidas", "postres" o "bebidasypostres"
/beer - Agrega un vaso de cerveza a nombre de quien envió el comando (Se usa para dividir la cuenta, cortesía de @jjqrs)
/menuchange [id_number] [new_name] [new_price] - Si el item existe en el menú, modifica su nombre y su precio, si no existe lo agrega
/orderchange [id_number] (Optional)[amount] - Elimina el id enviado una x cantidad de veces de la ronda, si no se pasa cantidad lo elimina solo una vez
"""


class HelpMenuComposer:

    def compose(self, is_admin: bool) -> str:
        if is_admin:
            return GENERAL_MENU + ADMIN_ALLOWED_CMDS
        return GENERAL_MENU + USER_ALLOWED_CMDS
