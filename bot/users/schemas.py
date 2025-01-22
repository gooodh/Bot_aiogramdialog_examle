from pydantic import BaseModel, ConfigDict

from typing import Optional


class TelegramIDModel(BaseModel):
    telegram_id: int

    model_config = ConfigDict(from_attributes=True)


class UserModel(TelegramIDModel):
    username: str | None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    referral_id: Optional[str] = None

