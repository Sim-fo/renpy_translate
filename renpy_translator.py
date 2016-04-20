# -*- coding: utf-8 -*-
'''
Скрипт для автоматического... ну ладно, полуавтоматического перевода renpy игр
через гуглтранслейт. :)
Работает под Windows на python 3.4, на других версиях и ОС не проверял.
Для работы требуется textblob (textblob.readthedocs.org).

Использование:

Для начала нужно получить файлы для перевода.
В окне renpy жмем на "Создать переводы". Вводим имя папки на латинице, например rus.
Движок создаст папку tl с нужными файлами в папке game.

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

Скрипт создаст две папки transl и orig_copy
В папке transl будут лежать переведенные файлы,
а в orig_copy файлы с копией оригинального текста, просто в пустые кавычки
вставляется оригинальный текст.
Эти файлы могут пригодиться, если часть файлов нужно оставить без перевода.

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
'''


import re, os
from textblob import TextBlob


os.mkdir('transl')
os.mkdir('orig_copy')
all_files = []
for top, dirs, files in os.walk('.'):
    for nm in files:
        all_files.append(os.path.join(top, nm))
to_translate = list(filter(lambda x: x.endswith('.rpy'), all_files)) 
print(to_translate)
print(all_files)


def foo(file):
    def read_all():
        with open(file) as f:
            all_file = f.read()
            all = all_file.split('\n')
        return all
    old_rpy = read_all()

    file_name = str(re.findall(r'[\w ]*?.rpy', file))

    # Подставляет оригинальный текст в пустые кавычки "" и сохраняет в файлы
    # Может быть полезно для неполного перевода.
    #
    count = -1
    for i in old_rpy:
        count += 1
        if '    new ""' in old_rpy[count]:
            old_rpy[count] = '    new' + old_rpy[count - 1][7:]
        elif '    ""' in old_rpy[count]:
            old_rpy[count] = '    ' + old_rpy[count - 1][6:]
        elif re.findall(r'    [\w]+? ""', old_rpy[count]):
            old_rpy[count] = '    ' + old_rpy[count - 1][6:]
    
    new_rpy =  open('orig_copy\\' + file_name[2:-6] + '.rpy', 'w')
    for i in old_rpy:
        new_rpy.write(i + '\n')
    new_rpy.close()


# Перевод текста
    count2 = -1
    for i in old_rpy:
        count2 += 1
        if re.findall(r'    old "[\w,\'.!\?_ \\\":-]*?"', i):
            en_blob = TextBlob(str(i[9:-1]))
            try:
                old_rpy[count2 + 1] = '    new "' + str(en_blob.translate(to='ru'))+'"'
                old_rpy[count2 + 1] = old_rpy[count2+1].replace('\\ "', '\\"')
                print(old_rpy[count2 + 1])
            except:
                pass

        if re.findall(r'# extend', i):
            pass

        elif re.findall(r'    # "[\w,\'.!\?_ \\\":-]*?"', i):
            en_blob = TextBlob(str(i[7:-1]))
            try:
                old_rpy[count2 + 1] = '    "' + str(en_blob.translate(to='ru')) + '"'
                print(old_rpy[count2 + 1])
            except:
                pass

        elif re.findall(r'    #[\w_ ]*?"[\w,\'.!\?_ \\\":-]*?"', i):
            en_blob = TextBlob(str(i[5:]))
            try:
                old_rpy[count2 + 1] = '    ' + str(en_blob.translate(to='ru'))
                old_rpy[count2 + 1] = old_rpy[count2 + 1].replace('\\ "', '\\"')
                print(old_rpy[count2 + 1])
            except:
                pass

        elif re.findall(r'    # "[\w,\'.!\?_ \\\":-]*?\[', i):
            en_blob = TextBlob(str(i[7:-1]))
            try:
                old_rpy[count2 + 1] = '    "' + str(en_blob.translate(to='ru')) + '"'
                print(old_rpy[count2 + 1])
            except:
                pass

        elif re.findall(r'    #[\w ]*?"[\w,\'.!\? \\\":-]*?\[', i):
            en_blob = TextBlob(str(i[6:]))
            try:
                old_rpy[count2 + 1] = '    ' + str(en_blob.translate(to='ru'))
                print(old_rpy[count2 + 1])
            except:
                pass

    new_rpy_tr = open('transl\\' + file_name[2:-6] + '.rpy', 'w', encoding= 'utf-8')
    for i in old_rpy:
        new_rpy_tr.write(str(i) + '\n')
    new_rpy_tr.close()


for i in to_translate:
    print('working... {}'.format(i))
    foo(i)

