from dao.base import BaseDAO
from users.models import User


class UserDAO(BaseDAO[User]):
    model = User
