import structlog


logger = structlog.get_logger()

def construct_callout(city: str) ->str:
    message = ""

    if city == "Vigo":

        with open("vigo.txt", "r", encoding="utf-8") as vigo_attendees:
            for line in vigo_attendees:
                message += line + " "
    elif city == "Coruña":

        with open("coruna.txt", "r", encoding="utf-8") as vigo_attendees:
            for line in vigo_attendees:
                message += line + " "
    
    return message