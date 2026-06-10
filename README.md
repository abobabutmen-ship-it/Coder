![Coder banner](assets/banner.svg)

# Coder

![logo](assets/logo.svg)

Coder — AI-проект для анализа, исправления и улучшения кода.

Коротко:
- Python-анализ (AST)
- Интеграция с ESLint (JS) и cppcheck (C++)
- Интерактивный режим, исправление и генерация кода

Как использовать добавленные изображения

- Логотип: `assets/logo.svg` — квадратный логотип, можно вставлять в README:

```markdown
![logo](assets/logo.svg)
```

- Баннер: `assets/banner.svg` — горизонтальный баннер. Пример вставки с контролем ширины:

```html
<img src="assets/banner.svg" alt="Coder banner" width="800" />
```

- Social preview: `assets/social_preview.svg` — используется как изображение для Open Graph (конвертируйте в PNG 1200×630 при необходимости).

PRs

- CI и фиксы кода (flake8/pytest/requirements/tests) в ветке `chore/ci-fixes`.
  Открыть PR: https://github.com/abobabutmen-ship-it/Coder/compare/main...chore/ci-fixes?expand=1

- Дизайн и изображения в ветке `feat/logo`.
  Открыть PR: https://github.com/abobabutmen-ship-it/Coder/compare/main...feat/logo?expand=1

Инструкции по локальной проверке CI и изображений

1. Переключиться на ветку с CI:

```bash
git fetch origin
git checkout chore/ci-fixes
```

2. Установить dev-зависимости и прогнать тесты/линтеры:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
flake8 .
pytest -q
```

3. Просмотр изображений (локально): откройте `assets/logo.svg` и `assets/banner.svg` в браузере.

Если нужно, я могу автоматически открыть PRs или создать PNG-версии логотипов — скажите, что предпочитаете.
