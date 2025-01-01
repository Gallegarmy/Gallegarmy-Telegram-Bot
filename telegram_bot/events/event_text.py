def create_message_text(event_name: str, event_date:str, event_time: str, event_link) -> str:
    event_message=(
        f"Próximo evento de Sysarmy Galicia:\n\n"
        f"{event_name}\n\n"
        f"Data: {event_date}\n"
        f"Hora: {event_time}\n\n"
        f"Link: {event_link}\n\n"
    )
    return event_message