import asyncio
import signal
import sys
import tracemalloc

from kink import Container
from telegram.ext import Application

from sysarmy_bot.config import Config
from sysarmy_bot.dependency_injection import bootstrap_di
from sysarmy_bot.shared.logger import Logger
from sysarmy_bot.shared.telegram_utils import init_bot, shutdown_bot


def main():
    event_loop = asyncio.get_event_loop()

    di: Container = event_loop.run_until_complete(bootstrap_di())
    app_logger = di[Logger]

    def signal_handler(sig, frame):
        if isinstance(frame, asyncio.BaseEventLoop) and frame.is_running() and not frame.is_closed():
            frame.stop()
            frame.close()
        sys.exit(0)

    event_loop.add_signal_handler(signal.SIGHUP, signal_handler)
    event_loop.add_signal_handler(signal.SIGQUIT, signal_handler)
    event_loop.add_signal_handler(signal.SIGTERM, signal_handler)

    bot = di[Application]

    try:
        if di[Config].environment.is_testing():
            tracemalloc.start()

        app_logger.warning(f'Starting bot main loop')
        event_loop.run_until_complete(init_bot(bot))
        event_loop.run_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        app_logger.error('An unexpected exception occurred', exc_info=e)
    finally:
        event_loop.run_until_complete(shutdown_bot(bot))
        app_logger.warning(f'Shutting down bot main loop')


if __name__ == '__main__':
    main()
