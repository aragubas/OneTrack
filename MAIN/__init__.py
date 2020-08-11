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
import pygame, os
from ENGINE import cntMng
from ENGINE import MAIN
from OneTrack.MAIN import UI

DefaultContents = cntMng.ContentManager
track_list = UI.TrackList

def Initialize(DISPLAY):
    global DefaultContents
    global track_list

    DefaultContents = cntMng.ContentManager()
    DefaultContents.SetFontPath("Data/Font")
    DefaultContents.InitSoundSystem()

    MAIN.ReceiveCommand(5, "OneTrack v1.0")

    Path = "./OneTrack/Library/default.otmf"

    MusFileData = open(Path, "r").read().rstrip().replace("\n", "").split(";")
    track_list = UI.TrackList(MusFileData)
    track_list.Rectangle = pygame.Rect(0, 100, 800, 400)




def GameDraw(DISPLAY):
    global track_list
    DISPLAY.fill((40, 30, 35))

    track_list.Render(DISPLAY)

def Update():
    global track_list

    track_list.Update()

def EventUpdate(event):
    global track_list

    track_list.EventUpdate(event)
