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
import pygame, os, pickle, io
from ENGINE import cntMng
from ENGINE import MAIN
from ENGINE import appData
import ENGINE as tge
from OneTrack.MAIN import UI
from OneTrack.MAIN import SaveFileDialog
from OneTrack.MAIN import OpenFileDialog
from OneTrack.MAIN.Screens.Editor import OptionsBar


DefaultContents = cntMng.ContentManager
track_list = UI.TrackList

# -- Top Toolbar -- #
TopBarControls = UI.ButtonsBar
DropDownFileMenu = UI.DropDownMenu

FileMenuEnabled = False
DisableControls = False
CopyOfScreen = pygame.Surface((5, 5))
BPM = 150
TotalBlocks = 32

def Initialize(DISPLAY):
    global DefaultContents
    global track_list
    global TopBarControls
    global DropDownFileMenu

    NewMusicFile()

    ButtonsList = list()
    ButtonsList.append(UI.Button(pygame.Rect(0, 0, 0, 0), "File", 14))

    TopBarControls = UI.ButtonsBar((3, 5, 800, 32), ButtonsList)

    DropDownFileMenuList = ("Load", "Save", "New File")

    DropDownFileMenu = UI.DropDownMenu(pygame.Rect(10, 35, 120, 65), DropDownFileMenuList)

    SaveFileDialog.Initialize()
    OpenFileDialog.Initialize()
    OptionsBar.Initialize()

def GameDraw(DISPLAY):
    global track_list
    global TopBarControls
    global DropDownFileMenu
    global CopyOfScreen
    global DisableControls

    if not DisableControls:
        DISPLAY.fill((62, 62, 116))

        track_list.Render(DISPLAY)
        TopBarControls.Render(DISPLAY)

        # -- Render DropDown Menus -- #
        if FileMenuEnabled:
            DropDownFileMenu.Render(DISPLAY)

        OptionsBar.Draw(DISPLAY)

        CopyOfScreen = DISPLAY.copy()

    SaveFileDialog.Draw(DISPLAY)
    OpenFileDialog.Draw(DISPLAY)

def SaveMusicData(FilePath):
    global track_list

    pickle.dump(track_list.PatternList, open(FilePath, "wb"))

def LoadMusicData(FileName):
    global track_list
    global BPM

    # -- Load the List to RAM -- #
    patterns_list = pickle.load(open(FileName, "rb"))

    # -- Clear the Current Patterns -- #
    track_list.PatternList.clear()

    # -- Add Objects One-By-One -- #
    SavedBPM = 0

    for i, obj in enumerate(patterns_list):
        # -- If in first pattern, read Music Properties -- #
        try:
            if i == 0:
                SavedBPM = int(obj.MusicProperties[0])

        except AttributeError:
            obj.MusicProperties = list()
            obj.MusicProperties.append("150")

        except TypeError:
            obj.MusicProperties = list()
            obj.MusicProperties.append("150")


        # -- Add the Object -- #
        track_list.PatternList.append(obj)

    # -- Set to the Pattern 0 -- #
    track_list.SetCurrentPattern_ByID(0)

    # -- Set Properties -- #
    Obj = OptionsBar.WidgetCollection.GetWidget(1)

    Obj.Changer.Value = SavedBPM

    if SavedBPM <= 1:
        SavedBPM = 150
    BPM = SavedBPM



def NewMusicFile():
    global track_list
    del track_list
    tge.utils.GarbageCollector_Collect()

    track_list = UI.TrackList()
    track_list.Rectangle = pygame.Rect(0, 100, 800, 400)

def Update():
    global track_list
    global TopBarControls
    global DropDownFileMenu
    global FileMenuEnabled
    global DisableControls

    SaveFileDialog.Update()
    OpenFileDialog.Update()

    if not DisableControls:
        TopBarControls.Update()
        track_list.Update()
        OptionsBar.Update()

        if FileMenuEnabled:
            DropDownFileMenu.Update()

        #region Top Bar Update
        if TopBarControls.ClickedButtonIndex == 0:
            if not FileMenuEnabled:
                FileMenuEnabled = True

            else:
                FileMenuEnabled = False

        #region File DropDown Menu
        if FileMenuEnabled:
            if DropDownFileMenu.SelectedItem == "Save":
                DropDownFileMenu.SelectedItem = ""
                FileMenuEnabled = False
                DisableControls = True

                SaveFileDialog.Enabled = True

            if DropDownFileMenu.SelectedItem == "Load":
                DropDownFileMenu.SelectedItem = ""
                FileMenuEnabled = False
                DisableControls = True

                OpenFileDialog.Enabled = True

            if DropDownFileMenu.SelectedItem == "New File":
                DropDownFileMenu.SelectedItem = ""
                FileMenuEnabled = False

                NewMusicFile()

        #endregion


def EventUpdate(event):
    global track_list
    global TopBarControls
    global DropDownFileMenu
    global FileMenuEnabled
    global DisableControls

    if not DisableControls:
        TopBarControls.EventUpdate(event)
        track_list.EventUpdate(event)
        OptionsBar.EventUpdate(event)

        if FileMenuEnabled: DropDownFileMenu.EventUpdate(event)

    SaveFileDialog.EventUpdate(event)
    OpenFileDialog.EventUpdate(event)