#!/usr/bin/python
#version 1.4.0
'''
Created on 27.03.2015

@author: crimsen
'''

from tendo import singleton
from controller.MainController import MainController



if __name__ == '__main__':
    
    me = singleton.SingleInstance()
    App = MainController()
    App.show()
