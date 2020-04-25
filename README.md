Скрипт для автоматического... ну ладно, полуавтоматического перевода renpy игр
через гуглтранслейт. :)
Работает под Windows на python 3.7, на других версиях и ОС не проверял.
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
Ощибок стало меньше, но до идеала далеко. 

После перевода нужно проверить результат. Вот такие вещи надо исправить

    old "{size=+4}{color=#ffffff}Some text{/color}{/size}"
    new "{Размер = + 4} {цвет = # FFFFFF} {Какой-то текст / цвет} {/ размер}"
    
    # K "{i}Hai{/i}."
    K "{Я} Хай {/ I}."
    
    # D "{i}Three. {b}Sleep!{/b}{/i}"
    D "{i}Три. {Ь} Спать! {/ Б}{/i}"   
    
    # s "Dr. [player_surname], [patient_name] [patient_surname] is here."
    s "Доктор [фамилия игрока], [имя пациента] [фамилия пациента] здесь."

    
Полезные регулярки для правки переведенного текста:

    \[[^A-Za-z]+\]           # Не английские буквы в переменных
    \{.*?([^A-Za-z])+\}      # Не английские буквы в тегах
    ^(    [^#]) "[A-Za-z]    # Не переведенные строчки
    ".*?".*?".*?"            # Двойные кавычки внутри двойных кавычек
    
    Для правок удобно использовать Notepad++
