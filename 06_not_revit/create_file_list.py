# -*- coding: utf-8 -*-
import os
# path = r'C:\Users\sssh\OneDrive\Desktop\Новая папка'
path = input('Укажите куда сохранить файл: ')

def get_files(path, file_name='result.txt'):
    with open(os.path.join(path, file_name), 'w') as out:
        for root, dirs, files in os.walk(path):
            for _file in files:
                if _file.endswith('.rvt'):
                    out.write(os.path.join(root, _file) + '\n')
        return print('Everything is awesome')


get_files(path)
