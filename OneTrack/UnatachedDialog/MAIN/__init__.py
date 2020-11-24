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
import System.Core as Core
from System.Core import Fx
from System.Core import CntMng
from OneTrack.UnatachedDialog.MAIN.Screens import LoadFile as LoadFileScreen
from OneTrack.UnatachedDialog.MAIN.Screens import SaveFile as SaveFileScreen
from OneTrack.UnatachedDialog.MAIN.Screens import DialogOkOnly as DialogOkOnlyScreen
from OneTrack.UnatachedDialog.MAIN.Screens import Settings as DialogSettingsScreen
from OneTrack.MAIN import UI

class Process(Core.Process):
    def Initialize(self):
        print("Initialize OneTrack Dialog")
        self.SetVideoMode(False, (400, 320))
        self.SetTitle("OneTrack Dialog")
        self.RootDefaultContents = None
        # Focus to this window
        Core.wmm.WindowManagerSignal(self, 0)

        # Initialize Content Manager
        self.DefaultContents = CntMng.ContentManager()
        self.DefaultContents.SetSourceFolder("OneTrack_data/UnatachedDialog/")
        self.DefaultContents.SetFontPath("fonts")
        self.DefaultContents.SetImageFolder("img")
        self.DefaultContents.SetRegKeysPath("reg")

        self.DefaultContents.LoadRegKeysInFolder()
        self.DefaultContents.LoadImagesInFolder()

        self.DefaultContents.InitSoundSystem()

        self.RootProcess = self.INIT_ARGS[0]
        self.OperationType = self.INIT_ARGS[1]

        try:
            self.OptionalParameters = self.INIT_ARGS[3]
            print("Optional parameters set")

        except IndexError:
            self.OptionalParameters = None
            print("No optional parameters set")

        self.SelectedModuleMode = None

        if self.OperationType == "OPEN":
            self.SelectedModuleMode = LoadFileScreen.Screen(self)

        elif self.OperationType == "SAVE":
            self.SelectedModuleMode = SaveFileScreen.Screen(self)

        elif self.OperationType == "DIALOG_OK":
            self.SelectedModuleMode = DialogOkOnlyScreen.Screen(self)

        elif self.OperationType == "DIALOG_SETTINGS":
            self.SelectedModuleMode = DialogSettingsScreen.Screen(self)

        else:
            raise Exception("Invalid Operation Type")

        self.POSITION = (Core.MAIN.ScreenWidth / 2 - self.DISPLAY.get_width() / 2, Core.MAIN.ScreenHeight / 2 - self.DISPLAY.get_height() / 2)

        self.RootDefaultContents = self.RootProcess.DefaultContents
        if self.RootDefaultContents is None:
            raise Exception("Fatal Error")

        try:
            self.BGColor = UI.ThemesManager_GetProperty("Dialog_BG_Color")

        except:
            self.BGColor = (16, 14, 18)

        self.Initialized = True
        self.Timer = pygame.time.Clock()
        print("OneTrack Dialog initialized.")

    def Draw(self):
        if not self.Initialized:
            self.DISPLAY.fill(self.BGColor)

            self.DefaultContents.FontRender(self.DISPLAY, "/Ubuntu.ttf", 18, "Loading...", (255, 255, 255), 5, 5)
            return self.DISPLAY

        if self.RootDefaultContents.Get_RegKey("/options/looking_glass", bool):
            self.DISPLAY.blit(Fx.Simple_BlurredRectangle(Core.MAIN.DISPLAY, (self.POSITION[0], self.POSITION[1], self.DISPLAY.get_width(), self.DISPLAY.get_height())), (0, 0))

        else:
            self.DISPLAY.fill(self.BGColor)

        self.SelectedModuleMode.Draw(self.DISPLAY)

        return self.DISPLAY

    def Update(self):
        while self.Running:
            if not self.Initialized:
                continue

            self.Timer.tick(100)
            self.SelectedModuleMode.Update()

    def CloseDialog(self):
        Core.wmm.WindowManagerSignal(self, 1)
        Core.wmm.WindowManagerSignal(self.RootProcess, 0)

    def EventUpdate(self, event):
        if not self.Initialized:
            return

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.CloseDialog()

        self.SelectedModuleMode.EventUpdate(event)