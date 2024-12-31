from time import sleep
from pyrogram.client import Client


def verify_response(expected_value: str, received_value: str) -> None:
    if received_value is None:
        print("No hay respuesta del bot")
    elif expected_value in received_value:
        print(f"Test successfull, expected value is correct")        
    else:
        print(f"{expected_value} failed. Please review the logs")


def delay(seconds=2):
    sleep(seconds)


def run_test(app, send_value: str, expected_value: str) -> None:
    msg = app.send_message(-1001920687768, send_value, message_thread_id=4226)
    delay(1)
    msg = app.get_messages(-1001920687768, msg.id + 1, message_thread_id=4226)    
    delay(1)
    verify_response(expected_value, msg.text)




if __name__ == "__main__":
    test_list=(
        #("/q", "Quote ao azar de Sysarmy Galicia"),
        ("/help", "Commandos actualmente habilitados en el bot:"),
        ("/festivos", "O próximo festivo")
    )
    api_id = 22303447
    api_hash = "968dbece694a87954287c22cb0a0fd76"
    username = "Gallegarmy_test_bot"
    app1 = Client("my_account", api_id, api_hash).start()
    for test in test_list:
        run_test(app1, test[0], test[1])