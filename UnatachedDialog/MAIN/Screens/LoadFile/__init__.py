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

def Initialize(pRoot_Process):
    global RootProcess
    global FolderList
    global OptionsBar
    global FileListUpdated
    RootProcess = pRoot_Process

    # Set the correct screen size
    RootProcess.DISPLAY = pygame.Surface((300, 350))

    FolderList = UI.VerticalListWithDescription(pygame.Rect(0, 24, 300, 15))
    ButtonsList = list()
    ButtonsList.append(UI.Button(pygame.Rect(0, 0, 0, 0), "Select", 12))
    OptionsBar = UI.ButtonsBar((0, 0, 0, 0), ButtonsList)
    RootProcess.TITLEBAR_TEXT = "Open File"
    FileListUpdated = False


def Draw(DISPLAY):
    # -- Render the Folder List -- #
    FolderList.Render(DISPLAY)

    # -- Render the Buttons -- #
    OptionsBar.Render(DISPLAY)

def Update():
    global FolderList
    global OptionsBar
    global FileListUpdated

    if not FileListUpdated:
        FileListUpdated = True
        UpdateFileList()

    FolderList.Set_W(RootProcess.DISPLAY.get_width())
    FolderList.Set_H(RootProcess.DISPLAY.get_height() - 35)

    # -------------------------------------------------
    FolderList.ColisionXOffset = RootProcess.POSITION[0] + FolderList.Rectangle[0]
    FolderList.ColisionYOffset = RootProcess.POSITION[1] + 15 + FolderList.Rectangle[1]

    OptionsBar.Update()
    #-------------------------------
    OptionsBar.ColisionXOffset = RootProcess.POSITION[0]
    OptionsBar.ColisionYOffset = RootProcess.POSITION[1] + 15

    SelectedFile = FolderList.LastItemClicked

    if OptionsBar.ClickedButtonIndex == 0:
        OptionsBar.ClickedButtonIndex = -1

        if not SelectedFile == "null":
            RootProcess.RootProcess.CurrentScreenToUpdate.LoadMusicData(Core.GetAppDataFromAppName("OneTrack") + Core.TaiyouPath_CorrectSlash + SelectedFile)
            Core.wmm.WindowManagerSignal(RootProcess, 1)

def EventUpdate(event):
    FolderList.Update(event)
    OptionsBar.EventUpdate(event)


def UpdateFileList():
    global FolderList

    print("Load : Updating File List...")
    FolderList.ClearItems()
    AllFilesInDir = utils.Directory_FilesList(Core.GetAppDataFromAppName("OneTrack"))

    for file in AllFilesInDir:
        # Check if file is a valid OneTrack Project
        if file.endswith(".oneprj"):
            FileAllPath = file
            FileName = file.replace(Core.GetAppDataFromAppName("OneTrack"), "").replace(".oneprj", "")

            ItemName = FileName[1:]
            ItemDescription = "Saved on: {0}".format(FileAllPath)

            FolderList.AddItem(ItemName, ItemDescription)

def WhenClosing():
    pass
