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
import OneTrack.MAIN.Screens.Editor as Main
from OneTrack.MAIN.Screens.Editor import InstanceVar as var
from ENGINE import fx


# -- Window's Controls -- #
Window = UI.Window
Enabled = False
FolderList = UI.VerticalListWithDescription
OptionsBar = UI.ButtonsBar
SelectedFile = ""
AnimationController = utils.AnimationController
AnimationNumb = 0
WindowDrawnSurface = pygame.Surface((0, 0))
LastWindowRect = pygame.Rect((0, 0, 0, 0))
BluredScreen_Surface = pygame.Surface((5, 5))

Inputbox_FileName = UI.InputBox
EnterFileNameEnabled = False
FileListUpdate = False

def Initialize():
    global Window
    global FolderList
    global OptionsBar
    global AnimationController
    global Inputbox_FileName

    Window = UI.Window(pygame.Rect(-600, -420, 600, 420), "Save Music File", False, False)
    FolderList = UI.VerticalListWithDescription(pygame.Rect(0, 24, 600, 400))
    UpdateFileList()

    ButtonsList = list()

    ButtonsList.append(UI.Button(pygame.Rect(0, 0, 0, 0), "Select", 14))
    ButtonsList.append(UI.Button((0, 0, 0, 0), "New", 14))

    OptionsBar = UI.ButtonsBar((3, -10, 0, 0), ButtonsList)
    AnimationController = utils.AnimationController(3.5, multiplierRestart=True)

    Inputbox_FileName = UI.InputBox(5, 25, 250, 25, "Default", 14)

def UpdateFileList():
    global FolderList

    print("Save : Updating File List...")
    FolderList.ClearItems()
    AllFilesInDir = utils.Directory_FilesList(tge.TaiyouPath_AppDataFolder)

    for file in AllFilesInDir:
        FileAllPath = file
        FileName = file.replace(tge.TaiyouPath_AppDataFolder, "")

        ItemName = FileName[1:]
        ItemDescription = "Saved on: {0}".format(FileAllPath)

        FolderList.AddItem(ItemName, ItemDescription)

def Draw(DISPLAY):
    global Enabled
    global Window
    global FolderList
    global OptionsBar
    global WindowDrawnSurface
    global BluredScreen_Surface

    # Render the Blured Screen
    if not Enabled: return
    DISPLAY.blit(BluredScreen_Surface, (0, 0))

    Window.Render(DISPLAY)
    if not LastWindowRect == Window.WindowRectangle:
        WindowDrawnSurface = pygame.Surface((Window.WindowRectangle[2], Window.WindowRectangle[3]), pygame.SRCALPHA)

    WindowDrawnSurface.set_alpha(AnimationController.Value)

    # -- Render the Folder List -- #
    FolderList.Render(WindowDrawnSurface)

    # -- Render the Buttons List -- #
    OptionsBar.Render(WindowDrawnSurface)

    if EnterFileNameEnabled:
        Inputbox_FileName.Render(WindowDrawnSurface)

    DISPLAY.blit(WindowDrawnSurface, (Window.WindowSurface_Rect[0], Window.WindowSurface_Rect[1]))

def UpdateWindow():
    global Enabled
    global Window
    global AnimationController
    global AnimationNumb
    global FileListUpdate
    global SelectedFile

    AnimationController.Update()

    # -- Window Animation -- #
    AnimationNumb = AnimationController.Value - 255
    Window.Opacity = AnimationController.Value
    Window.TitleBarRectangle[1] = (600 / 2 - Window.WindowRectangle[3] / 2) - AnimationNumb
    Window.TitleBarRectangle[0] = (800 / 2 - Window.WindowRectangle[2] / 2) - AnimationNumb

    if AnimationController.Enabled is True and AnimationController.CurrentMode is False and AnimationController.Value < 1:
        AnimationController.Enabled = True
        AnimationController.CurrentMode = True
        AnimationController.Value = 0
        AnimationController.ValueMultiplier = 0
        AnimationController.DisableSignal = False
        AnimationNumb = 0
        var.DisableControls = False
        FileListUpdate = False
        SelectedFile = "null"
        Enabled = False

def Update():
    global Enabled
    global FolderList
    global SelectedFile
    global Window
    global EnterFileNameEnabled
    global BluredScreen_Surface
    global FileListUpdate

    if not Enabled: return
    if not FileListUpdate:
        FileListUpdate = True
        UpdateFileList()

    UpdateWindow()

    if AnimationController.Enabled:
        BluredScreen_Surface = fx.Surface_Blur(var.CopyOfScreen, max(1.0, AnimationController.Value - 150))


    #-------------------------------
    FolderList.Set_W(Window.WindowRectangle[2])
    FolderList.Set_H(Window.WindowRectangle[3] - 200)
    FolderList.ColisionXOffset = Window.WindowSurface_Rect[0] + FolderList.Rectangle[0]
    FolderList.ColisionYOffset = Window.WindowSurface_Rect[1] + FolderList.Rectangle[1]
    #-------------------------------
    OptionsBar.ColisionXOffset = Window.WindowSurface_Rect[0]
    OptionsBar.ColisionYOffset = Window.WindowSurface_Rect[1]
    #--------------------------------
    Inputbox_FileName.ColisionOffsetX = Window.WindowSurface_Rect[0]
    Inputbox_FileName.ColisionOffsetY = Window.WindowSurface_Rect[1]

    OptionsBar.Update()

    if not EnterFileNameEnabled:
        SelectedFile = FolderList.LastItemClicked

        if OptionsBar.ClickedButtonIndex == 0:
            OptionsBar.ClickedButtonIndex = -1

            if not SelectedFile == "null":
                Main.SaveMusicData(tge.TaiyouPath_AppDataFolder + "/" + SelectedFile)
                print("Music Data has been saved. on\n{0}".format(SelectedFile))

                AnimationController.Enabled = True

        if OptionsBar.ClickedButtonIndex == 1:
            OptionsBar.ClickedButtonIndex = -1

            EnterFileNameEnabled = True
    else:
        if OptionsBar.ClickedButtonIndex == 1:
            OptionsBar.ClickedButtonIndex = -1

            # -- Write the File -- #
            if not Inputbox_FileName.text == "":
                Inputbox_FileName.text = Inputbox_FileName.text.replace(" ", "_")
                Main.SaveMusicData(tge.TaiyouPath_AppDataFolder + "/" + Inputbox_FileName.text)
                print("Music Data has been created. on\n{0}".format(Inputbox_FileName.text))

                UpdateFileList()
                EnterFileNameEnabled = False
                AnimationController.Enabled = True

def EventUpdate(event):
    global Enabled
    global Window
    global FolderList
    global OptionsBar
    global EnterFileNameEnabled

    Window.EventUpdate(event)
    OptionsBar.EventUpdate(event)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_ESCAPE:
            AnimationController.Enabled = True

    if not EnterFileNameEnabled:
        FolderList.Update(event)
    else:
        Inputbox_FileName.Update(event)
