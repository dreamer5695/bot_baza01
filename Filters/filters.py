from aiogram.filters import BaseFilter
from aiogram.types import Message
from Config_data.config import Config, load_config

config: Config = load_config()


# Создаём новый класс
class IsAdmin(BaseFilter):
    admin_id = config.admin.Admin

    # ADMIN_ID получаем из файла .env путём config.admin.Admin
    async def __call__(self, message: Message) -> bool:
        # функция __call__ получает данные на ранних стадиях и может ими оперировать
        # получает Message и сравнивает, равен ли он admin_id из config.admin.Admin
        return str(message.from_user.id) == self.admin_id
