from typing import Optional

class MessagingService:
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, chat_id: Optional[int], text: str, thread_id: Optional[int] = None):
        """Sends a message to the specified chat."""
        if chat_id is not None:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                message_thread_id=thread_id,
            )