# -*- coding: utf-8 -*-
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference("System.ComponentModel")
from System.Windows.Forms import Form, Application, Button, MessageBox, FormStartPosition, DockStyle, Label, Padding, \
    TextBox, FormBorderStyle, GroupBox, CheckBox
from System.Drawing import Size, Point, Color, Font

cats = []
cats.append('Стены')
cats.append('Крыши')
cats.append('Перекрытия')
cats.append('Двери')
cats.append('Окна')


class MyForm(Form):
    def __init__(self):
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.Text = 'Текст'
        self.Name = 'Имя'
        self.Size = Size(500, 250)
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.msg = []

        gb = GroupBox()
        gb.Text = "Категории"
        gb.Size = Size(120, 110)
        gb.Location = Point(20, 20)
        gb.Parent = self

        j = 25
        for c in cats:
            self.cb = CheckBox()
            self.cb.Text = c
            self.cb.Location = Point(25, j)
            j += 25
            self.cb.Width = 200
            self.cb.Checked += self.OnChanged
            gb.Size = Size(120, 20 + j)
            gb.Controls.Add(self.cb)
        
        self.label = Label()
        self.label.Text = "Результат"
        self.label.Location = Point(225, 20)
        self.label.Height = 25
        self.label.Width = 225
        self.Controls.Add(self.label)
        self.label.Text = "".join(self.msg)

    def OnChanged(self, sender, event):
        if sender.Checked:
            self.msg.append(sender.Text)

        MessageBox.Show('Hello world')

    def button1_Click(self, sender, event):
        MessageBox.Show('Hello world')

    def textBox1_TextChanged(self, sender, event):
        self.label.Text = self.textbox.Text

    def update(self, sender, event):
        for f in self.checkval:
            self.output1.append(f.Checked)

        self.Close()


Application.EnableVisualStyles()
Application.Run(MyForm())

OUT = msg
