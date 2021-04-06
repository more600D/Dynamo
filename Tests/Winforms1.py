import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference("System.ComponentModel")

import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

class Form1(Form):
	def __init__(self):
		self.InitializeComponent()
	
	def InitializeComponent(self):
		resources = System.Resources.ResourceManager("Form1", System.Reflection.Assembly.GetEntryAssembly())
		self._splitContainer1 = System.Windows.Forms.SplitContainer()
		self._splitContainer2 = System.Windows.Forms.SplitContainer()
		self._button1 = System.Windows.Forms.Button()
		self._pictureBox1 = System.Windows.Forms.PictureBox()
		self._splitContainer1.BeginInit()
		self._splitContainer1.Panel1.SuspendLayout()
		self._splitContainer1.Panel2.SuspendLayout()
		self._splitContainer1.SuspendLayout()
		self._splitContainer2.BeginInit()
		self._splitContainer2.Panel2.SuspendLayout()
		self._splitContainer2.SuspendLayout()
		self._pictureBox1.BeginInit()
		self.SuspendLayout()
		# 
		# splitContainer1
		# 
		self._splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill
		self._splitContainer1.Location = System.Drawing.Point(0, 0)
		self._splitContainer1.Name = "splitContainer1"
		# 
		# splitContainer1.Panel1
		# 
		self._splitContainer1.Panel1.Controls.Add(self._splitContainer2)
		# 
		# splitContainer1.Panel2
		# 
		self._splitContainer1.Panel2.Controls.Add(self._pictureBox1)
		self._splitContainer1.Size = System.Drawing.Size(800, 600)
		self._splitContainer1.SplitterDistance = 394
		self._splitContainer1.TabIndex = 0
		# 
		# splitContainer2
		# 
		self._splitContainer2.Dock = System.Windows.Forms.DockStyle.Fill
		self._splitContainer2.Location = System.Drawing.Point(0, 0)
		self._splitContainer2.Name = "splitContainer2"
		self._splitContainer2.Orientation = System.Windows.Forms.Orientation.Horizontal
		# 
		# splitContainer2.Panel2
		# 
		self._splitContainer2.Panel2.Controls.Add(self._button1)
		self._splitContainer2.Size = System.Drawing.Size(394, 600)
		self._splitContainer2.SplitterDistance = 329
		self._splitContainer2.TabIndex = 0
		# 
		# button1
		# 
		self._button1.Dock = System.Windows.Forms.DockStyle.Bottom
		self._button1.Location = System.Drawing.Point(0, 244)
		self._button1.Name = "button1"
		self._button1.Size = System.Drawing.Size(394, 23)
		self._button1.TabIndex = 0
		self._button1.Text = "button1"
		self._button1.UseVisualStyleBackColor = True
		# 
		# pictureBox1
		# 
		self._pictureBox1.Dock = System.Windows.Forms.DockStyle.Fill
		self._pictureBox1.Image = resources.GetObject("pictureBox1.Image")
		self._pictureBox1.Location = System.Drawing.Point(0, 0)
		self._pictureBox1.Name = "pictureBox1"
		self._pictureBox1.Size = System.Drawing.Size(402, 600)
		self._pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.CenterImage
		self._pictureBox1.TabIndex = 0
		self._pictureBox1.TabStop = False
		# 
		# Form1
		# 
		self.ClientSize = System.Drawing.Size(800, 600)
		self.Controls.Add(self._splitContainer1)
		self.Name = "Form1"
		self.Text = "Form1"
		self._splitContainer1.Panel1.ResumeLayout(False)
		self._splitContainer1.Panel2.ResumeLayout(False)
		self._splitContainer1.EndInit()
		self._splitContainer1.ResumeLayout(False)
		self._splitContainer2.Panel2.ResumeLayout(False)
		self._splitContainer2.EndInit()
		self._splitContainer2.ResumeLayout(False)
		self._pictureBox1.EndInit()
		self.ResumeLayout(False)


Application.EnableVisualStyles()
Application.Run(Form1())

