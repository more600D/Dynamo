import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

# from System.Windows.Forms import Application, Form, StatusBar
# from System.Windows.Forms import RadioButton, GroupBox, CheckBox, Label, Button, 
# AnchorStyles, DockStyle, PictureBox, PictureBoxSizeMode, TextBox
# from System.Windows.Forms import TrackBar, TickStyle
from System.Windows.Forms import *
from System.Drawing import Size, Point, Font, Color, Image

in1 = IN[0]

class IForm(Form):

    def __init__(self):
        self.checkval = []
        self.output1 = []
        self.output2 = []
        self.Font = Font("Arial",12)
        self.BackColor = Color.White
        
        self.label = Label()
        self.label.Text = "Choose"
        self.label.Location = Point(25, 100)
        self.label.Height = 25
        self.label.Width = 225
        self.label.Font = Font("OpenSans",12)
            
        j=150
        for i in range(len(in1)):
            self.checkbox = CheckBox()
            self.checkbox.Text=in1[i]
            self.checkbox.Location = Point(25,j)
            j+=25
            self.checkbox.Width = 200
            self.checkbox.Font= Font("OpenSans",10)
            self.Controls.Add(self.checkbox)
            self.checkval.append(self.checkbox)
        
        self.button1 = Button()
        self.button1.Text = 'apply and close'
        self.button1.Location = Point(25, j+50)
        self.button1.Click += self.update
        self.button1.Width = 250

        self.AcceptButton = self.button1

        self.Controls.Add(self.label)
        self.Controls.Add(self.button1)
                
        self.CenterToScreen()
        self.AutoSize = True
        
        gb = GroupBox()
        gb.Text = "Week"
        gb.Size = Size(120, 110)
        gb.Location = Point(20, 20)
        gb.Parent = self

        week1 = RadioButton()
        week1.Text = "Week 1"
        week1.Parent = gb
        week1.Location = Point(10, 30)
        week1.CheckedChanged += self.OnChanged

        week2 = RadioButton()
        week2.Text = "week2"
        week2.Parent = gb
        week2.Location = Point(10, 60)
        week2.CheckedChanged += self.OnChanged
        
    def OnChanged(self, sender, event):
        if sender.Checked:
            self.output2.append(sender.Text)        

    def update(self, sender, event):
        for f in self.checkval:
            self.output1.append(f.Checked)

        self.Close()

form = IForm()
Application.Run(form)
OUT = form.output1, form.output2
