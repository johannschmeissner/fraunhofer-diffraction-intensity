# fraunhofer-diffraction-intensity
Fraunhofer diffraction intensity visualization

Интерактивное приложение на Python для визуализации интенсивности при дифракции Фраунгофера:

- на одной щели
- на двойной щели
- на решётке из N щелей

## Структура проекта

```
fraunhofer-diffraction-intensity/
├── src/
│   └── main.py           # Основной скрипт с GUI и логикой расчета
├── requirements.txt      # Список зависимостей Python
├── README.md             # Этот файл
└── LICENSE               # Лицензия проекта
```

## 🚀 Возможности

- Интерактивные ползунки для изменения параметров:
  - Длина волны (λ)
  - Ширина щели (b)
  - Расстояние между щелями (d)
  - Количество щелей (N)
- Автоматическое масштабирование интенсивности
- Переключение отображения каждого графика с динамическим обновлением легенды

## 🛠️ Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/johannschmeissner/fraunhofer-diffraction-intensity.git
cd fraunhofer-diffraction-intensity
```

### 2. Создать и активировать виртуальное окружение (рекомендуется):

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\\Scripts\\activate     # Windows
```

### 3. Установить зависимости:

```bash
pip install -r ../requirements.txt
```

### 4. Запуск:

```bash
python main.py
```

## Зависимости

* Python 3.8+
* NumPy
* Matplotlib

Установить:

```bash
pip install numpy matplotlib
```

## Вклад и развитие

PRs и issues приветствуются!

## Лицензия

Этот проект распространяется под лицензией MIT. Смотрите файл LICENSE для подробностей.
