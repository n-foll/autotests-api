pytest_plugins = (
    "fixtures.users",
    "fixtures.files",  # Добавляем фикстуры для работы с файлами
    "fixtures.courses",  # Добавляем фикстуры для работы с курсами
    "fixtures.authentication",
    "fixtures.exercises"
)