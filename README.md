Определение токсичных комментариев на русском языке. <br>
Для обучения используется следующий датасет: https://www.kaggle.com/blackmoon/russian-language-toxic-comments (в основном ненормативная лексика и срач на тему Украины). <br>
С помощью Flask реализован API для классификации комментрия. Можно обратиться либо через функцию (ноутбук /model_creation/model_test.ipynb), либо через web-интерфейс. <br>
В папке model_creation находится создание и проверка модели, а так же датасеты. <br>
Файл run_server.py - для запуска Flask на локальной машине. <br>
application.py - для загрузки на heroku (ссылка на приложение https://babalich1.herokuapp.com/ )



