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
import pygame, traceback
from OneTrack import MAIN as Main
from OneTrack.MAIN import UI
from Applications.OneTrack.MAIN.Screens.Editor import InstanceVar as var

from System.Core import MAIN
from System.Core import Utils
from System.Core import Shape

LagIndicatorSurface = pygame.Surface
LagTextWidth = 0
LagTextHeight = 0
LagTextColor = ()
LagEnabled = False
Alpha = 0
FPS = 0
FlashingAnimation = Utils.AnimationController
ProcessInstanceRefence = None

def Initialize(self):
    global LagIndicatorSurface
    global LagTextWidth
    global LagTextHeight
    global LagTextColor
    global FlashingAnimation
    global ProcessInstanceRefence

    ProcessInstanceRefence = self

    LagTextWidth = UI.ContentManager.GetFont_width("/PressStart2P.ttf", 14, "LAG")
    LagTextHeight = UI.ContentManager.GetFont_height("/PressStart2P.ttf", 14, "LAG")

    LagIndicatorSurface = pygame.Surface((LagTextWidth + 4, LagTextHeight + 4))
    LagTextColor = (255, 0, 0)
    FlashingAnimation = Utils.AnimationController(5, 255, multiplierRestart=True)

def Draw(DISPLAY):
    global LagIndicatorSurface
    global LagTextColor
    global LagEnabled
    global Alpha
    global FPS

    if not LagEnabled:
        return

    LagText = "LAG: " + Utils.FormatNumber(FPS, 2)
    LagTextWidth = UI.ContentManager.GetFont_width("/PressStart2P.ttf", 14, LagText)
    LagTextHeight = UI.ContentManager.GetFont_height("/PressStart2P.ttf", 14, LagText)

    Shape.Shape_Rectangle(DISPLAY, (0, 0, 0), (5 - 2, 5 - 2, LagTextWidth + 4, LagTextHeight + 4), 0, 3)
    UI.ContentManager.FontRender(DISPLAY, "/PressStart2P.ttf", 14, LagText, LagTextColor, 5, 5)

def Update():
    global Alpha
    global LagEnabled
    global LagTextColor
    global FlashingAnimation
    global FPS

    if ProcessInstanceRefence is None:
        return

    FPS = ProcessInstanceRefence.CalcFPS

    if FPS >= 57:
        Alpha = 0

    else:
        Alpha = 255

    if Alpha == 0:
        LagEnabled = False

    else:
        LagEnabled = True

    if not LagEnabled:
        return

    FlashingAnimation.Update()
    # -- Aways Active the Animation Controller -- #
    FlashingAnimation.Enabled = True

    LagTextColor = (FlashingAnimation.Value, 0, 0)

