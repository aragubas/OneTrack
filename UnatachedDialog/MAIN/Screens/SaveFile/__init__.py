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
FolderList = UI.VerticalListWithDescription
OptionsBar = UI.ButtonsBar
FileListUpdated = False

Inputbox_FileName = UI.InputBox
EnterFileNameEnabled = False
FileListUpdated = False
FileListUpdate = False

def Initialize(pRoot_Process):
    global RootProcess
    global FolderList
    global OptionsBar
    global FileListUpdated
    global FileListUpdate
    global Inputbox_FileName
    global EnterFileNameEnabled
    RootProcess = pRoot_Process

    # Set the correct screen size
    RootProcess.DISPLAY = pygame.Surface((300, 350))

    FolderList = UI.VerticalListWithDescription(pygame.Rect(0, 24, 300, 15))
    ButtonsList = list()
    ButtonsList.append(UI.Button(pygame.Rect(0, 0, 0, 0), "Select", 14))
    ButtonsList.append(UI.Button((0, 0, 0, 0), "New", 14))

    OptionsBar = UI.ButtonsBar((0, 0, 0, 0), ButtonsList)
    RootProcess.TITLEBAR_TEXT = "Save File"
    Inputbox_FileName = UI.InputBox(5, 25, 250, 25, "Default", 14)

    FileListUpdated = False
    FileListUpdate = False
    EnterFileNameEnabled = False

def Draw(DISPLAY):
    global FolderList
    global OptionsBar
    global Inputbox_FileName

    # -- Render the Folder List -- #
    FolderList.Render(DISPLAY)

    # -- Render the Buttons List -- #
    OptionsBar.Render(DISPLAY)

    if EnterFileNameEnabled:
        Inputbox_FileName.Render(DISPLAY)

def Update():
    global FolderList
    global SelectedFile
    global FileListUpdate
    global EnterFileNameEnabled
    global FileListUpdated

    if not FileListUpdate:
        FileListUpdate = True
        UpdateFileList()

    #-------------------------------
    FolderList.Set_W(RootProcess.DISPLAY.get_width())
    FolderList.Set_H(RootProcess.DISPLAY.get_height() - 35)
    FolderList.ColisionXOffset = RootProcess.POSITION[0] + FolderList.Rectangle[0]
    FolderList.ColisionYOffset = RootProcess.POSITION[1] + 15 + FolderList.Rectangle[1]
    #-------------------------------
    OptionsBar.ColisionXOffset = RootProcess.POSITION[0]
    OptionsBar.ColisionYOffset = RootProcess.POSITION[1] + 15
    #--------------------------------
    Inputbox_FileName.ColisionOffsetX = RootProcess.POSITION[0]
    Inputbox_FileName.ColisionOffsetY = RootProcess.POSITION[1] + 15

    OptionsBar.Update()

    if not EnterFileNameEnabled:
        SelectedFile = FolderList.LastItemClicked

        if OptionsBar.ClickedButtonIndex == 0:
            OptionsBar.ClickedButtonIndex = -1

            if not SelectedFile == "null":
                RootProcess.RootProcess.CurrentScreenToUpdate.SaveMusicData(Core.GetAppDataFromAppName("OneTrack") + Core.TaiyouPath_CorrectSlash + SelectedFile)
                print("Music Data has been saved. on\n{0}".format(SelectedFile))
                Core.wmm.WindowManagerSignal(RootProcess, 1)

        if OptionsBar.ClickedButtonIndex == 1:

            EnterFileNameEnabled = True
    else:
        if OptionsBar.ClickedButtonIndex == 1:

            # -- Write the File -- #
            if not Inputbox_FileName.text == "":
                Inputbox_FileName.text = Inputbox_FileName.text.replace(" ", "_")
                RootProcess.RootProcess.CurrentScreenToUpdate.SaveMusicData(Core.GetAppDataFromAppName("OneTrack") + Core.TaiyouPath_CorrectSlash + Inputbox_FileName.text)

                print("Music Data has been created. on\n{0}".format(Inputbox_FileName.text))
                Core.wmm.WindowManagerSignal(RootProcess, 1)

def EventUpdate(event):
    global Enabled
    global Window
    global FolderList
    global OptionsBar
    global EnterFileNameEnabled

    OptionsBar.EventUpdate(event)

    if not EnterFileNameEnabled:
        FolderList.Update(event)
    else:
        Inputbox_FileName.Update(event)


def UpdateFileList():
    global FolderList

    print("Save : Updating File List...")
    FolderList.ClearItems()
    AllFilesInDir = utils.Directory_FilesList(Core.GetAppDataFromAppName("OneTrack"))

    for file in AllFilesInDir:
        FileAllPath = file
        FileName = file.replace(Core.GetAppDataFromAppName("OneTrack"), "").replace(".oneprj", "")

        ItemName = FileName[1:]
        ItemDescription = "Saved on: {0}".format(FileAllPath)

        FolderList.AddItem(ItemName, ItemDescription)
