# -*- coding: utf-8 -*-
import re
import os
import time
import random
# from googletrans import Translator     # googletrans
from textblob import TextBlob            # TextBlob


# translator = Translator()

files_to_translate = []  # все файлы для перевода

# создаем дирректорию для файлов с переводом (если нужно)
os.mkdir('transl')

# Находим файлы для перевода в дирректории
all_files = []  # все файлы
for top, dirs, files in os.walk('./tl/rus/'):
    for nm in files:
        all_files.append(os.path.join(top, nm))
files_to_translate = list(filter(lambda x: x.endswith('.rpy'), all_files))
#########################################################################


def read_all(file):  # Возвращает имя текущего файла и его текст
    with open(file) as f:
        file_name = str(re.findall(r'[\w-]*?.rpy', file))
        all_file = f.read()
        current_file_text = all_file.split('\n')
        print(file_name)
    return current_file_text, file_name


def translate(line):  # возвращает перевод текущей строки
    r = random.randrange(1, 4, 1)                  # Рандомная пауза между запросами на перевод (от 1 до 4 секунд)
    time.sleep(r)
    en_blob = TextBlob(str(line))                  # TextBlob
    per = str(en_blob.translate(to='ru'))          # TextBlob
    # per = translator.translate(line, dest='ru')  # googletrans
    # print(per.text)                              # googletrans
    print(per)                                     # TextBlob

    print('working... {}'.format(currentFilename))

    # return str(per.text)                         # googletrans
    per = str(per)
    per = per.replace(r'\ "', r' \"')
    per = per.replace(r' \"', r'\"')
    return per


r1 = re.compile(r'"{i}(.*[^\\"]){/i}"$'), 4, -5  # курсив
r2 = re.compile(r'"{b}(.*[^\\"]){/b}"$'), 4, -5  # курсив

r_last = re.compile(r'"(.*)"$'), 1, -1  # просто кавычки
# print(reg1)
# exit()


def search_line_for_translate(all_file_text):  # Ищем строку для перевода
    count = -1
    tmp_text = all_file_text
    length_text = len(all_file_text)
    for line in all_file_text:
        count += 1
        if re.search(r1[0], line):
            result = re.search(r1[0], line)
            orig_line = str(result.group(0))[r1[1]:r1[2]]
            print(orig_line)
            try:
                zzz = str(tmp_text[count+1]).replace(str(orig_line), translate(orig_line))
                tmp_text[count+1] = zzz
            except:
                pass

        elif re.search(r2[0], line):
            result = re.search(r2[0], line)
            orig_line = str(result.group(0))[r2[1]:r2[2]]
            print(orig_line)
            try:
                zzz = str(tmp_text[count+1]).replace(str(orig_line), translate(orig_line))
                tmp_text[count+1] = zzz
            except:
                pass

        elif re.search(r_last[0], line):
            print('{} percents'.format(round(count / (int(length_text)), 4) * 100))
            result = re.search(r_last[0], line)
            orig_line = str(result.group(0))[r_last[1]:r_last[2]]
            print(orig_line)
            try:
                zzz = str(tmp_text[count + 1]).replace(str(orig_line), translate(orig_line))
                tmp_text[count + 1] = zzz
            except:
                pass

    # Запись в файл
    print('пишем в файл')
    # str(tmp_text[0]).replace('п»ї', '')
    new_rpy_tr = open('transl\\{}'.format(str(currentFilename)), 'w', encoding='utf-8')
    for i in tmp_text:
        new_rpy_tr.write(str(i) + '\n')
    new_rpy_tr.close()


for i in files_to_translate:
    currentTextFromFile = read_all(i)[0]
    currentFilename = (read_all(i)[1])[2:-2]
    search_line_for_translate(currentTextFromFile)
    print('working... {}'.format(i))




