# -*- coding: utf-8 -*-
import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference("System.ComponentModel")
import System
import System.Windows.Forms as FORM
import System.Drawing as DRAW


# class MyForm(FORM.Form):
# 	def __init__(self):
# 		self.start_position = FORM.FormStartPosition.CenterScreen
# 		self.FormBorderStyle = FormBorderStyle.FixedDialog
#         self.Text = 'Текст'
#         self.Name = 'Имя'
#         self.Size = Size(500, 250)
#         self.MaximizeBox = False
#         self.MinimizeBox = False

help(clr)