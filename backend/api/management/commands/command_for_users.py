from users.models import Role
from .support_def import clear_db, create_simple_db


# Create
def create_role_db():
    """Функция для наполнения базы данных Ролей из файла role.json"""
    create_simple_db(name_model=Role, name_json_file='role')


def clear_role_db():
    """Функция для удаления базы данных Ролей."""
    return clear_db(name_model=Role)
