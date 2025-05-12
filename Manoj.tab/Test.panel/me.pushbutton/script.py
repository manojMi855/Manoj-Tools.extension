import os
import System
import clr
from pyrevit import forms
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Windows.Forms import Form, Label, Button, Panel
from System.Drawing import Color, Point, Size, Font, FontStyle, Image, ContentAlignment

class StyledAboutMeForm(Form):
    def __init__(self):
        # Form styling
        self.Text = "About Manoj"
        self.Size = Size(450, 350)
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.BackColor = Color.FromArgb(240, 240, 240)  # Light gray background
        self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
        self.MaximizeBox = False

        # Create main panel
        main_panel = Panel()
        main_panel.Dock = System.Windows.Forms.DockStyle.Fill
        main_panel.BackColor = Color.White

        # Profile Picture (Placeholder - replace with actual path if you have a profile image)
        profile_pic = Label()
        profile_pic.BackColor = Color.FromArgb(52, 152, 219)  # Flat blue color
        profile_pic.Location = Point(150, 20)
        profile_pic.Size = Size(150, 150)
        profile_pic.Text = "M"  # First letter as placeholder
        profile_pic.Font = Font("Segoe UI", 72, FontStyle.Bold)
        profile_pic.ForeColor = Color.White
        profile_pic.TextAlign = ContentAlignment.MiddleCenter

        # Name Label
        name_label = Label()
        name_label.Text = "Manoj Mittal"
        name_label.Font = Font("Segoe UI", 16, FontStyle.Bold)
        name_label.ForeColor = Color.FromArgb(44, 62, 80)  # Dark blue-gray
        name_label.Location = Point(100, 180)
        name_label.Size = Size(250, 30)
        name_label.TextAlign = ContentAlignment.MiddleCenter

        # Job Title Label
        job_label = Label()
        job_label.Text = "Assistant Architect\nat Surbana Jurong"
        job_label.Font = Font("Segoe UI", 10)
        job_label.ForeColor = Color.FromArgb(127, 140, 141)  # Soft gray
        job_label.Location = Point(100, 220)
        job_label.Size = Size(250, 50)
        job_label.TextAlign = ContentAlignment.MiddleCenter

        # VS Code Button with modern styling
        open_vs_button = Button()
        open_vs_button.Text = "Try Code"
        open_vs_button.Font = Font("Segoe UI", 10, FontStyle.Bold)
        open_vs_button.Location = Point(100, 280)
        open_vs_button.Size = Size(250, 40)
        open_vs_button.BackColor = Color.FromArgb(52, 152, 219)  # Flat blue
        open_vs_button.ForeColor = Color.White
        open_vs_button.FlatStyle = System.Windows.Forms.FlatStyle.Flat
        open_vs_button.Click += self.open_vs_code

        # Add controls to panel
        main_panel.Controls.Add(profile_pic)
        main_panel.Controls.Add(name_label)
        main_panel.Controls.Add(job_label)
        main_panel.Controls.Add(open_vs_button)

        # Add panel to form
        self.Controls.Add(main_panel)

    def open_vs_code(self, sender, event):
        try:
            os.startfile("code")  # Open VS Code
        except Exception as e:
            forms.alert("Error opening VS Code: " + str(e), exitscript=True)

# Show the window
form = StyledAboutMeForm()
form.ShowDialog()