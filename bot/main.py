import asyncio
import tracemalloc

from aiohttp import web
from loguru import logger

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import BotCommand, BotCommandScopeDefault


from dao.database_middleware import DatabaseMiddlewareWithCommit, DatabaseMiddlewareWithoutCommit
from config import BASE_URL, HOST, PORT, WEBHOOK_PATH, bot, admins, dp

from users.router import user_router

async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),

    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, "Я запущен🥳.")

        response = await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
        if response:
            logger.info(f"Вебхук успешно установлен: {response}.")
        else:
            logger.warning(f"Вебхук не установлен, ответ пуст: {response}.")
    except Exception as e:
        logger.error(f"Ошибка при установке вебхука: {e}")
    logger.info(f"Сервер запущен на {HOST}:{PORT}")


async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, "Бот остановлен. За что?😔")
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.session.close()
    except Exception as e:
        logger.error(e)
    logger.error("Бот остановлен!")


async def main():
    tracemalloc.start()

        # регистрация мидлварей
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())
    # регистрация роутеров
    dp.include_router(user_router)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    # Запускаем веб-сервер на указанном хосте и порте
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=HOST, port=PORT)
    await site.start()

    # Бесконечный цикл, чтобы сервер работал
    try:
        while True:
            await asyncio.sleep(3600)  # Ждем 1 час
    except KeyboardInterrupt:
        pass  # Позволяет остановить сервер с помощью Ctrl+C
    finally:
        # Здесь можно добавить код для завершения соединений или других ресурсов
        await runner.cleanup()  # Закрываем веб-сервер
        print("Ресурсы очищены.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена пользователем.")
