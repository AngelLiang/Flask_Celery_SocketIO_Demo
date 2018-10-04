# coding=utf-8

import os
import re
import shutil

curr_dir = os.path.dirname(os.path.realpath(__file__))

# python venv path
python_venv_path = os.path.join(curr_dir, '.venv')

pywin32_system32_path = os.path.join(
    python_venv_path, 'Lib', 'site-packages', 'pywin32_system32')
win32_path = os.path.join(
    python_venv_path, 'Lib', 'site-packages', 'win32')
win32com_path = os.path.join(
    python_venv_path, 'Lib', 'site-packages', 'win32com')


def patch():
    if not os.path.exists(pywin32_system32_path):
        print(pywin32_system32_path + ' is not exist!')
        return
    files = os.listdir(pywin32_system32_path)
    for f in files:
        src_file_abspath = os.path.join(pywin32_system32_path, f)
        if f[:10] == 'pywintypes':
            dst_dir = win32_path
        elif f[:9] == 'pythoncom':
            continue
            # dst_dir = win32com_path
        else:
            continue

        dst_file_abspath = os.path.join(dst_dir, f)
        if os.path.exists(dst_file_abspath):
            print(f + ' is exist!')
            continue

        shutil.copy(src_file_abspath, dst_dir)
        print('copy ' + src_file_abspath + ' to ' + dst_file_abspath)


if __name__ == '__main__':
    patch()
