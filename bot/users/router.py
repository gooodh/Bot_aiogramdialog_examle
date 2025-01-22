from aiogram.filters import CommandObject, CommandStart
from loguru import logger
from aiogram.types import Message
from aiogram.dispatcher.router import Router

from sqlalchemy.ext.asyncio import AsyncSession

from users.dao import UserDAO
from users.schemas import TelegramIDModel, UserModel
from users.utils import get_refer_id_or_none

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(
    message: Message, command: CommandObject, session_with_commit: AsyncSession
):
    try:
        user = message.from_user
        user_info = await UserDAO.find_one_or_none(
            session=session_with_commit, filters=TelegramIDModel(telegram_id=user.id)
        )
        ref_id = get_refer_id_or_none(command_args=command.args, user_id=user.id)

        if user_info is None or not user_info.telegram_id:
            user_data = UserModel(
                telegram_id=user.id,
                username=user.username,
                referral_id=ref_id,
            )

            await UserDAO.add(session=session_with_commit, values=user_data)
            message_text = f"<b>👋 Привет, {message.from_user.full_name}!</b>"
            if ref_id:
                message_text += f" Вы успешно закреплены за пользователем с ID {ref_id}."

            await message.answer(message_text)
            
        else:
            user_data = UserModel(
                telegram_id=user.id,
                username=user.username,
            )
            await UserDAO.update(
                session=session_with_commit,
                filters=TelegramIDModel(telegram_id=user.id),
                values=user_data,
            )
            
            await message.answer(
                f"<b>👋 Привет, {message.from_user.full_name} я рад что ты вернулся!</b>"
            )

    except Exception as e:
        logger.error(
            f"Ошибка при выполнении команды /start для пользователя {message.from_user.id}: {e}"
        )
        await message.answer(
            "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже."
        )
