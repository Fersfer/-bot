
import time

from alpha_bot.core.strategy import BotStrategy

if __name__ == '__main__':
    bot = BotStrategy()

    print("🤖 Бот запущено. Ctrl+C для зупинки.")
    steps = 0
    try:
        while  True:
            print("------------------------------------new step")
            bot.step()
            steps +=1
            print("------------------------------------end of step")

    except KeyboardInterrupt:
        print("🛑 Бот зупинено вручну.")
