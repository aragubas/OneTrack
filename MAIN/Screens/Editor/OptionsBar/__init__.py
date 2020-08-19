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
from ENGINE import utils
import OneTrack.MAIN as Main
from OneTrack.MAIN import UI
from OneTrack.MAIN.Screens import Editor

WidgetCollection = UI.Widget.Widget_Controller
OptionsBarSurface = pygame.Surface


def Initialize():
    global WidgetCollection
    global OptionsBarSurface

    OptionsBarSurface = pygame.Surface((680, 90))

    WidgetCollection = UI.Widget.Widget_Controller((0, 5, 680, 90))
    WidgetCollection.Append(UI.Widget.Widget_PictureBox((5, 5, 203, 81), "/logo.png", 0))
    WidgetCollection.Append(UI.Widget.Widget_ValueChanger((5, 5), "BPM", "150", 1))

    obj = WidgetCollection.GetWidget(0)
    obj.Rectangle[0] = (WidgetCollection.Rectangle[2] - obj.Rectangle[2])


def EventUpdate(event):
    global WidgetCollection

    WidgetCollection.EventUpdate(event)

def Update():
    global WidgetCollection

    WidgetCollection.Update()

    if WidgetCollection.LastInteractionID == 1:
        Editor.BPM = int(WidgetCollection.LastInteractionType)

    else:
        obj = WidgetCollection.GetWidget(1)
        obj.Changer.Value = str(Editor.BPM).zfill(3)
        obj.Changer.SplitedAlgarims = list(obj.Changer.Value)

def Draw(DISPLAY):
    global WidgetCollection

    OptionsBarSurface.fill((62, 62, 116))

    WidgetCollection.Draw(OptionsBarSurface)

    DISPLAY.blit(OptionsBarSurface, (800 / 2 - OptionsBarSurface.get_width() / 2 + 15, 5))
    WidgetCollection.Rectangle[0] = 800 / 2 - OptionsBarSurface.get_width() / 2 + 15
