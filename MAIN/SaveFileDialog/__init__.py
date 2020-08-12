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
from OneTrack.MAIN import UI
from ENGINE import utils
import ENGINE as tge

# -- Window's Controls -- #
Window = UI.Window
Enabled = False
FolderList = UI.VerticalListWithDescription
OptionsBar = UI.ButtonsBar

def Initialize():
    global Window
    global FolderList
    global OptionsBar
    Window = UI.Window(pygame.Rect(55, 55, 400, 400), "Save Music Data", True)
    FolderList = UI.VerticalListWithDescription(pygame.Rect(0, 24, 491, 300))

    AllFilesInDir = utils.Directory_FilesList(tge.TaiyouPath_AppDataFolder)

    for file in AllFilesInDir:
        FileAllPath = file
        FileName = file.replace(tge.TaiyouPath_AppDataFolder, "")

        ItemName = FileName
        ItemDescription = "Located on: {0}".format(FileAllPath)

        FolderList.AddItem(ItemName, ItemDescription)

    ButtonsList = (UI.Button((0, 0, 0, 0), "Select", 14, True), UI.Button((0, 0, 0, 0), "New", 14, True))

    OptionsBar = UI.ButtonsBar((0, 0, 0, 0), ButtonsList)

def Draw(DISPLAY):
    global Enabled
    global Window
    global FolderList
    global OptionsBar

    if not Enabled: return

    Window.Render(DISPLAY)
    WindowDrawnSurface = pygame.Surface((Window.WindowRectangle[2], Window.WindowRectangle[3]), pygame.SRCALPHA)

    # -- Render the Folder List -- #
    FolderList.Render(WindowDrawnSurface)

    # -- Render the Buttons List -- #
    OptionsBar.Render(WindowDrawnSurface)

    DISPLAY.blit(WindowDrawnSurface, (Window.WindowSurface_Rect[0], Window.WindowSurface_Rect[1]))

def Update():
    global Enabled
    global FolderList
    global Window
    global OptionsBar

    if not Enabled: return

    FolderList.Set_W(Window.WindowRectangle[2])
    FolderList.Set_H(Window.WindowRectangle[3] - 200)
    # -------------------------------------------------
    FolderList.ColisionXOffset = Window.WindowSurface_Rect[0] + FolderList.Rectangle[0]
    FolderList.ColisionYOffset = Window.WindowSurface_Rect[1] + FolderList.Rectangle[1]

    OptionsBar.Update()
    #-------------------------------
    OptionsBar.ColisionXOffset = Window.WindowSurface_Rect[0]
    OptionsBar.ColisionYOffset = Window.WindowSurface_Rect[1]

def EventUpdate(event):
    global Enabled
    global Window
    global FolderList
    global OptionsBar

    if not Enabled: return

    FolderList.Update(event)
    Window.EventUpdate(event)
    OptionsBar.EventUpdate(event)