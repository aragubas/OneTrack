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

DefaultContents = cntMng.ContentManager

CurrentScreenToUpdate = Editor
def Initialize(DISPLAY):
    global DefaultContents

    DefaultContents = cntMng.ContentManager()
    DefaultContents.SetFontPath("Data/Font")
    DefaultContents.LoadSpritesInFolder("Data/Sprite")
    DefaultContents.InitSoundSystem()

    MAIN.ReceiveCommand(5, "OneTrack v1.3")

    Editor.Initialize(DISPLAY)

def GameDraw(DISPLAY):
    global CurrentScreenToUpdate

    DISPLAY.fill((40, 30, 35))

    CurrentScreenToUpdate.GameDraw(DISPLAY)

    DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", 8, "FPS: {0}/{1}".format(MAIN.clock.get_fps(), MAIN.clock.get_time()), (255, 255, 255), 5, 5, backgroundColor=(0, 0, 0))

def Update():
    global CurrentScreenToUpdate
    CurrentScreenToUpdate.Update()

def EventUpdate(event):
    global CurrentScreenToUpdate

    CurrentScreenToUpdate.EventUpdate(event)