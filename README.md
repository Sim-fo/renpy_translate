Скрипт для автоматического... ну ладно, полуавтоматического перевода renpy игр
через гуглтранслейт. :)
Работает под Windows на python 3.4, на других версиях и ОС не проверял.
Для работы требуется textblob https://textblob.readthedocs.org

Использование:

Для начала нужно получить файлы для перевода.
Для этого окне renpy жмем на "Создать переводы". Вводим имя папки на латинице, например rus.
В папке game движок создаст папку tl с нужными файлами.

Добавляем в главное меню выбор языка игры.
Для этого в файл screens.rpy вставляем эти строки.

            frame:
                style_group "pref"
                has vbox

                label _("Language")
                textbutton "English" action Language(None)
                textbutton "Russian" action Language("rus")

Если на предыдущем шаге папку для переводов вы назвали не rus,
а как-то po_drugomu, то измените Language("rus") на Language("po_drugomu")
Для примера можно посмотреть файл screens.rpy из обучающей игры, если сомневаетесь
куда именно вставить этот код.

Создаем временную папку, например D:\tmp (русских букв в пути быть не должно)
Копируем туда скрипт renpy_translator.py и папку tl.
Запускаем командную строку, переходим во временную папку и запускаем скрипт.
python3 renpy_translator.py

Скрипт создаст папку transl.
В папке transl будут лежать переведенные файлы,

Копируем файлы из папки transl в папку game/tl
Запускаем проект.
Смотрим на лист ошибок :) Скорее всего они будут, особенно, если игра большая.
Гуглтранслейт иногда переносит точку за кавычки ".
Или добавляет пробелы в экранированные \ " кавычки \ ""
Всё предусмотреть у меня не получилось, и такие ошибки надо исправлять руками.

Да, игра должна быть разархивирована. Если игра в архиве, то инструкции по распаковке
можно найти тут https://github.com/Shizmob/rpatool
Если шрифт, указанный в игре не содержит кирилицу, и вместо русского текста у вас квадраты
то в файле options.rpy замените шрифты на кирилические. Например constan.ttf

Поддерживается перевод на любые языки, которые поддерживает гуглтранслейт. Для этого в коде
скрипта надо заменить (to='ru') на нужную пару языков. Инструкции тут:
https://textblob.readthedocs.org/en/dev/quickstart.html#translation-and-language-detection


UPDATE 05.04.2019
При создании файлов перевода в Renpy, убедитесь, что опция Generate empty strings for translations НЕ выбрана.
Ощибок стало меньше, но до идеала далеко. Особенно внимательно стоит проверить переменные (в квадратных скобках). 
В переводе они должны быть такие же как в оригинале. 

Полезные регулярки:
\[[А-Яа-я]*?\]   # Для поиска случайно переведенных переменных
^(    [^#]) "[A-Za-z]    # Не переведенные строчки
