#!/usr/bin/python3.7
#   Copyright 2020 Aragubas
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
import pygame, os, pickle, io
import Core
from Core import cntMng
from Core import MAIN
from Core import appData
import Core as tge
from OneTrack.MAIN.Screens import Editor
from OneTrack.MAIN import LagIndicator
from OneTrack.MAIN import UI
from OneTrack.MAIN.Screens.Editor import InstanceVar as var

class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE, pInitArgs):
        self.PID = pPID
        self.NAME = pProcessName
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = True
        self.INIT_ARGS = pInitArgs
        self.DISPLAY = pygame.Surface((800, 600))
        self.LAST_SURFACE = self.DISPLAY.copy()
        self.APPLICATION_HAS_FOCUS = True
        self.POSITION = (0, 0)
        self.FULLSCREEN = True
        self.TITLEBAR_RECTANGLE = pygame.Rect(self.POSITION[0], self.POSITION[1], self.DISPLAY.get_width(), 15)
        self.TITLEBAR_TEXT = "OneTrack"
        self.WindowDragEnable = False

    def Initialize(self):
        # Initialize Variables
        self.CurrentScreenToUpdate = Editor

        # Initialize Content Manager
        self.DefaultContents = cntMng.ContentManager()
        self.DefaultContents.SetSourceFolder("OneTrack/")
        self.DefaultContents.SetFontPath("Data/fonts")
        self.DefaultContents.LoadImagesInFolder("Data/img")
        self.DefaultContents.LoadRegKeysInFolder("Data/reg")
        self.DefaultContents.InitSoundSystem()

        # Set the default content manager for the UI
        UI.ContentManager = self.DefaultContents
        var.DefaultContent = self.DefaultContents

        # Load UI Theme
        UI.ThemesManager_LoadTheme(self.DefaultContents.Get_RegKey("/selected_theme"))

        MAIN.ReceiveCommand(0, 60)

        self.TITLEBAR_TEXT = "OneTrack v{0}".format(self.DefaultContents.Get_RegKey("/version"))

        var.ProcessReference = self
        Editor.Initialize()
        LagIndicator.Initialize()



    def Draw(self):
        self.CurrentScreenToUpdate.GameDraw(self.DISPLAY)

        LagIndicator.Draw(self.DISPLAY)

        self.LAST_SURFACE = self.DISPLAY.copy()
        return self.DISPLAY

    def Update(self):
        if not self.APPLICATION_HAS_FOCUS and var.AwaysUpdate is False:
            return

        self.CurrentScreenToUpdate.Update()

        LagIndicator.Update()

    def EventUpdate(self, event):
        self.CurrentScreenToUpdate.EventUpdate(event)

