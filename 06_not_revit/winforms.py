import clr
import System
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import *
from System.Drawing import Size, Point, Font, Color, Image

class HelloWorldForm(System.Windows.Forms.Form):
    def __init__(self):
        self.Text = 'Hello World'
        self.Name = 'Hello World'

        # self.label = Label()
        # self.label.Text = "Choose"
        # self.label.Location = Point(25, 100)
        # self.label.Height = 25
        # self.label.Width = 225
        # self.label.Font = Font("OpenSans",12)

form = HelloWorldForm()
Application.Run(form)

OUT = 0