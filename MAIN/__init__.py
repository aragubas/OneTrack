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
from ENGINE import cntMng
from ENGINE import MAIN
from ENGINE import appData
import ENGINE as tge
from OneTrack.MAIN.Screens import Editor
import cProfile

DefaultContents = cntMng.ContentManager

CurrentScreenToUpdate = Editor
CurrentCursor = 0
def Initialize(DISPLAY):
    global DefaultContents

    DefaultContents = cntMng.ContentManager()
    DefaultContents.SetFontPath("Data/Font")
    DefaultContents.LoadSpritesInFolder("Data/Sprite")
    DefaultContents.LoadRegKeysInFolder("Data/Reg")
    DefaultContents.InitSoundSystem()

    MAIN.ReceiveCommand(5, "OneTrack v{0}".format(DefaultContents.Get_RegKey("/version")))
    MAIN.ReceiveCommand(0, 60)

    Editor.Initialize(DISPLAY)
    # -- Set Invisible Mouse -- #
    pygame.mouse.set_visible(False)

def GameDraw(DISPLAY):
    global CurrentScreenToUpdate
    global DefaultContents

    CurrentScreenToUpdate.GameDraw(DISPLAY)

    # -- Render Cursor -- #
    DefaultContents.ImageRender(DISPLAY, "/cursor.png", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", 8, "FPS: {0}/{1}".format(MAIN.clock.get_fps(), MAIN.clock.get_time()), (255, 255, 255), 5, 5, backgroundColor=(0, 0, 0))



def Update():
    global CurrentScreenToUpdate
    CurrentScreenToUpdate.Update()

def EventUpdate(event):
    global CurrentScreenToUpdate

    CurrentScreenToUpdate.EventUpdate(event)
