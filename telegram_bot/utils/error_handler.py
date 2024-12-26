import structlog
from .messaging import MessagingService
class ErrorHandler:
    def __init__(self):
        self.logger = structlog.get_logger()

    async def handle_runtime_error(self, error, context, chat_id=None, thread_id=None):
        """
        Logs the error and sends a user-friendly error message via bot.
        """
        self.logger.error("Runtime error occurred", error=str(error))
        messaging = MessagingService(context.bot)
        await messaging.send_message(chat_id, "Un erro inesperado ha ocorrido. Por favor, inténtao máis tarde.", thread_id)
