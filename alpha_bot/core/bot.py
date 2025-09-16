
import time

from alpha_bot.core.strategy import BotStrategy

if __name__ == '__main__':
    bot = BotStrategy()

    print("🤖 Бот запущено. Ctrl+C для зупинки.")
    try:
        while True:
            bot.step()
    except KeyboardInterrupt:
        print("🛑 Бот зупинено вручну.")
