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
import pygame, re
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
    WidgetCollection.Append(UI.Widget.Widget_ValueChanger((5, 42), "ROWS", "31", 2))
    WidgetCollection.Append(UI.Widget.Widget_ValueChanger((58, 5), "HIGHLIGHT", "04x16", 3))

    obj = WidgetCollection.GetWidget(0)
    obj.Rectangle[0] = (WidgetCollection.Rectangle[2] - obj.Rectangle[2])

    for obj in WidgetCollection.WidgetCollection:
        obj.Update()

def EventUpdate(event):
    global WidgetCollection

    WidgetCollection.EventUpdate(event)

def Update():
    global WidgetCollection

    WidgetCollection.Update()

    UpdateBPMSelector()
    UpdateRowsSelector()
    UpdateHighlightSelector()

def UpdateBPMSelector():
    if WidgetCollection.LastInteractionID == 1:
        Editor.BPM = int(WidgetCollection.LastInteractionType)

    else:
        obj = WidgetCollection.GetWidget(1)
        obj.Changer.Value = str(Editor.BPM).zfill(3)
        obj.Changer.SplitedAlgarims = list(obj.Changer.Value)

def UpdateRowsSelector():
    if WidgetCollection.LastInteractionID == 2:
        # -- Validate the Current Value -- #
        CurrentValue = WidgetCollection.LastInteractionType
        RowsValue = int(CurrentValue)

        if RowsValue > 99:
            RowsValue = 99

        Editor.TotalBlocks = RowsValue

        # -- Get the Changer Object -- #
        obj = WidgetCollection.GetWidget(2)
        # -- Re-Format the String -- #
        obj.Changer.Value = str(RowsValue).zfill(2)
        obj.Changer.SplitedAlgarims = list(obj.Changer.Value)

def UpdateHighlightSelector():
    if WidgetCollection.LastInteractionID == 3:
        # -- Validate the Current Value -- #
        CurrentValue = WidgetCollection.LastInteractionType
        HightLightValue = list(CurrentValue)

        FirstVal = ''.join((HightLightValue[0], HightLightValue[1]))
        SecondVal = ''.join((HightLightValue[3], HightLightValue[4]))

        if int(FirstVal) > 32:
            FirstVal = 32

        if int(SecondVal) > 32:
            SecondVal = 32

        Editor.Highlight = FirstVal
        Editor.HighlightSecond = SecondVal

        # -- Get the Changer Object -- #
        obj = WidgetCollection.GetWidget(3)
        # -- Re-Format the String -- #4
        obj.Changer.Value = ''.join((str(FirstVal).zfill(2), "x", str(SecondVal).zfill(2)))
        obj.Changer.SplitedAlgarims = list(obj.Changer.Value)


def Draw(DISPLAY):
    global WidgetCollection

    OptionsBarSurface.fill((62, 62, 116))

    WidgetCollection.Draw(OptionsBarSurface)

    DISPLAY.blit(OptionsBarSurface, (800 / 2 - OptionsBarSurface.get_width() / 2 + 15, 5))
    WidgetCollection.Rectangle[0] = 800 / 2 - OptionsBarSurface.get_width() / 2 + 15
