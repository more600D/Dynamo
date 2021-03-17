# -*- coding: utf-8 -*-
import os
path = r'C:\Users\sssh\OneDrive\Desktop\Новая папка'


def rename_all_files(path):
    for root, dirs, files in os.walk(path):
        for _file in files:
            if _file.endswith('.txt'):
                file_name = _file.split('.')
                remove_part = file_name[0][:len(file_name[0]) - 4]
                name = '{}_R19.txt'.format(remove_part)
                new_name = os.path.join(root, name)
                old_name = os.path.join(root, _file)
                os.rename(old_name, new_name)
                print(name)


rename_all_files(path)