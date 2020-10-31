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
import Core
import pygame
from OneTrack.MAIN import UI
from Core import utils

RootProcess = None
DialogTitle = ""
DialogText = ""
DialogIcon = None
DialogIconDimensions = (128, 128)

def Initialize(pRoot_Process):
    global RootProcess
    global DialogTitle
    global DialogText
    global DialogIcon
    global DialogIconDimensions
    RootProcess = pRoot_Process

    # Set the correct screen size
    RootProcess.DISPLAY = pygame.Surface((400, 150))

    Args = RootProcess.INIT_ARGS[2].split(';')
    DialogTitle = Args[0]
    DialogText = Args[1] + "\n\nPress 'ESC' to close dialog"
    DialogIcon = None

    RootProcess.TITLEBAR_TEXT = DialogTitle

    if not RootProcess.OptionalParameters == None:
        SplitedParameters = RootProcess.OptionalParameters.split(",")

        for parameter in SplitedParameters:
            print(parameter)
            ParameterSplit = parameter.split(":")

            if ParameterSplit[0] == "icon":
                DialogIcon = ParameterSplit[1]
                print("DialogIcon set to: " + DialogIcon)
                continue

    if DialogIcon == "none":
        DialogIcon = None

    DialogSize = (RootProcess.DefaultContents.GetFont_width("/Ubuntu_Bold.ttf", 14, DialogText) + 10, RootProcess.DefaultContents.GetFont_height("/Ubuntu_Bold.ttf", 14, DialogText) + 5)
    DialogSize = list(DialogSize)

    if not DialogIcon == None:
        DialogSize = (RootProcess.DefaultContents.GetFont_width("/Ubuntu_Bold.ttf", 14, DialogText) + 10 + DialogIconDimensions[0] + 2, RootProcess.DefaultContents.GetFont_height("/Ubuntu_Bold.ttf", 14, DialogText) + 5)
        DialogSize = list(DialogSize)

        if DialogSize[0] < DialogIconDimensions[0]:
            DialogSize[0] += DialogIconDimensions[0]

        if DialogSize[1] < DialogIconDimensions[1]:
            DialogSize[1] += DialogIconDimensions[1]

    RootProcess.DISPLAY = pygame.Surface(DialogSize)


def Draw(DISPLAY):
    global DialogText
    global DialogIcon
    global DialogIconDimensions

    TextX = 5

    if not DialogIcon == None:
        TextX = DialogIconDimensions[0] + 2
        RootProcess.DefaultContents.ImageRender(DISPLAY, "/{0}.png".format(DialogIcon), 1, 5, 128, 128)

    RootProcess.DefaultContents.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 14, DialogText, (240, 240, 240), TextX, 5)


def Update():
    pass

def EventUpdate(event):
    pass