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
import pygame
import Core
from Core import cntMng
from OneTrack.UnatachedDialog.MAIN.Screens import LoadFile as LoadFileScreen


class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE, pInitArgs):
        self.PID = pPID
        self.NAME = pProcessName
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = True
        self.INIT_ARGS = pInitArgs
        self.DISPLAY = pygame.Surface((300, 100))
        self.LAST_SURFACE = self.DISPLAY.copy()
        self.APPLICATION_HAS_FOCUS = True
        self.POSITION = (50, 50)
        self.FULLSCREEN = False
        self.TITLEBAR_RECTANGLE = pygame.Rect(self.POSITION[0], self.POSITION[1], self.DISPLAY.get_width(), 15)
        self.TITLEBAR_TEXT = "OneTrack Dialog"
        self.WindowDragEnable = False

    def Initialize(self):
        # Focus to this window
        Core.wmm.WindowManagerSignal(self, 0)

        # Initialize Content Manager
        self.DefaultContents = cntMng.ContentManager()
        self.DefaultContents.SetSourceFolder("OneTrack/UnatachedDialog/")
        self.DefaultContents.SetFontPath("Data/fonts")
        self.DefaultContents.LoadImagesInFolder("Data/img")
        self.DefaultContents.LoadRegKeysInFolder("Data/reg")
        self.DefaultContents.InitSoundSystem()

        self.RootProcess = self.INIT_ARGS[0]
        self.OperationType = self.INIT_ARGS[1]
        self.SelectedModuleMode = LoadFileScreen

        if self.OperationType == "LOAD":
            self.SelectedModuleMode = LoadFileScreen

        self.SelectedModuleMode.Initialize(self)

        self.POSITION = (800 / 2 - self.DISPLAY.get_width() / 2, 600 / 2 - self.DISPLAY.get_height() / 2)

    def Draw(self):
        self.DISPLAY.fill((150, 150, 150))

        self.SelectedModuleMode.Draw(self.DISPLAY)

        return self.DISPLAY

    def Update(self):
        self.SelectedModuleMode.Update()

    def EventUpdate(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                Core.wmm.WindowManagerSignal(self, 1)

        self.SelectedModuleMode.EventUpdate(event)