# -*- coding: utf-8 -*-
"""
Created on Sun May 14 07:41:19 2023

@author: Wesni
"""
#Nuke variables before running app. Sometimes it starts in a weird state
import sys
sys.modules[__name__].__dict__.clear()

import sys
from PyQt5.QtWidgets import QApplication
from GUI import WinForm

#Launch app in 'GUI'
app=QApplication(sys.argv)
form=WinForm()
form.show()
sys.exit(app.exec_())