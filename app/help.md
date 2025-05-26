├── app/ # Ядро приложения
│ ├── core/ # Основная бизнес-логика
│ │ ├── models/ # Модели данных
│ │ │ ├── init.py
│ │ │ ├── base.py # BaseRecord
│ │ │ └── record.py # Record
│ │ ├── reports/ # Генерация отчетов
│ │ │ ├── init.py
│ │ │ ├── base.py # BaseReport
│ │ │ ├── json.py # JsonReport
│ │ │ └── show.py # ShowReport
│ │ └── utils/ # Вспомогательные утилиты
│ │ ├── init.py
│ │ ├── parsers.py # file_parse
│ │ └── decorators.py # resolve_aliases
│ └── config.py # Конфигурация приложения
│
├── service/ # Сервисный слой
│ ├── cli/ # Обработка командной строки
│ │ ├── init.py
│ │ ├── commands.py # Обработчики команд
│ │ └── parser.py # args_parser
│ └── web/ # (Для будущего Web API)
│
├── tests/ # Тесты
└── main.py # Точка входа