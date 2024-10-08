import json


def get_json(name_json_file):
    """Вспомогательная функция для открытия json файла и передачи его содержимого."""
    with open(f"files_for_filling_db/{name_json_file}.json", "r", encoding='utf-8') as file:
        result_data = json.load(file)
        return result_data


def create_simple_db(name_model, name_json_file):
    """Функция для наполнения базы данных данными из файла json. Алгоритм для баз данных с одинаковой структурой."""
    if not name_model.objects.count():
        data = get_json(name_json_file=name_json_file)
        for db in data:
            name_model(
                title=db['name'],
            ).save()


def clear_db(name_model) -> int:
    """Общая функция для удаления базы данных нужно только ввести название модели name_model в качестве аргумента."""
    count = name_model.objects.count()
    name_model.objects.all().delete()
    return count
