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
from OneTrack.MAIN.Screens.Editor import InstanceVar as var
from OneTrack import MAIN as Main
from OneTrack.MAIN import UI


MessageSeenDelay = 0
LoadingAnimationFrame = 0

def Initialize():
    pass

def Draw(DISPLAY):
    global LoadingAnimationFrame
    if not var.GenerateSoundCache and not var.GenerateSoundCache_MessageSeen:
        return

    GeneratingCacheMessage = var.ProcessReference.DefaultContents.Get_RegKey("/strings/generating_cache")

    Area = pygame.Rect(DISPLAY.get_width() / 2 - (UI.ContentManager.GetFont_width("/PressStart2P.ttf", 14, GeneratingCacheMessage) + 27) / 2, 75, UI.ContentManager.GetFont_width("/PressStart2P.ttf", 14, GeneratingCacheMessage) + 27, UI.ContentManager.GetFont_height("/PressStart2P.ttf", 14, GeneratingCacheMessage) + 5)

    Core.Fx.BlurredRectangle(DISPLAY, Area, 15, 150)
    UI.ContentManager.FontRender(DISPLAY, "/PressStart2P.ttf", 14, GeneratingCacheMessage, (255, 255, 255), Area[0] + Area[3] - 4 + 5, Area[1] + 3)

    # Draw the Loading Wax
    LoadingAnimationFrame += 1
    if LoadingAnimationFrame >= 34:
        LoadingAnimationFrame = 1

    UI.ContentManager.ImageRender(DISPLAY, "/loading_anim/cursor_{0}.png".format(LoadingAnimationFrame), Area[0] + 2, Area[1] + 2, Area[3] - 4, Area[3] - 4, True)


def Update():
    global MessageSeenDelay
    if not var.GenerateSoundCache and not var.GenerateSoundCache_MessageSeen:
        return

    MessageSeenDelay += 1

    if MessageSeenDelay >= 1:
        var.GenerateSoundCache_MessageSeen = 0
        var.GenerateSoundCache_MessageSeen = True
