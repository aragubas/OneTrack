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
from Core import cntMng
from Core import MAIN
from Core import appData
import Core as tge
from OneTrack.MAIN.Screens import Editor
from OneTrack.MAIN import LagIndicator
import cProfile

## Required Variables ##
PROCESS_PID = 0
PROCESS_NAME = 0
IS_GRAPHICAL = True
FULLSCREEN = True
POSITION = (0, 0)
DISPLAY = pygame.Surface((800, 600))
APPLICATION_HAS_FOCUS = True

DefaultContents = cntMng.ContentManager

CurrentScreenToUpdate = Editor
CurrentCursor = 0
def Initialize():
    global DefaultContents

    DefaultContents = cntMng.ContentManager()
    DefaultContents.SetSourceFolder("OneTrack/")
    DefaultContents.SetFontPath("Data/fonts")
    DefaultContents.LoadImagesInFolder("Data/img")
    DefaultContents.LoadRegKeysInFolder("Data/reg")
    DefaultContents.InitSoundSystem()

    MAIN.ReceiveCommand(5, "OneTrack v{0}".format(DefaultContents.Get_RegKey("/version")))
    MAIN.ReceiveCommand(0, 60)

    Editor.Initialize()
    LagIndicator.Initialize()

    # -- Set Invisible Mouse -- #
    pygame.mouse.set_visible(False)

def Draw():
    global CurrentScreenToUpdate
    global DefaultContents

    CurrentScreenToUpdate.GameDraw(DISPLAY)

    LagIndicator.Draw(DISPLAY)

    return DISPLAY

def Update():
    global CurrentScreenToUpdate

    tge.MAIN.clock.tick(60)

    CurrentScreenToUpdate.Update()

    LagIndicator.Update()

    tge.MAIN.clock.tick(0)


def EventUpdate(event):
    global CurrentScreenToUpdate

    CurrentScreenToUpdate.EventUpdate(event)
