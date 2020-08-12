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
from OneTrack.MAIN import UI

DefaultContents = cntMng.ContentManager
track_list = UI.TrackList

# -- Top Toolbar -- #
TopBarControls = UI.ButtonsBar
DropDownFileMenu = UI.DropDownMenu

FileMenuEnabled = False

def Initialize(DISPLAY):
    global DefaultContents
    global track_list
    global TopBarControls
    global DropDownFileMenu

    DefaultContents = cntMng.ContentManager()
    DefaultContents.SetFontPath("Data/Font")
    DefaultContents.InitSoundSystem()

    MAIN.ReceiveCommand(5, "OneTrack v1.0")

    track_list = UI.TrackList()
    LoadMusicData()
    track_list.Rectangle = pygame.Rect(0, 100, 800, 400)

    ButtonsList = list()
    ButtonsList.append(UI.Button(pygame.Rect(0, 0, 0, 0), "File", 14))

    TopBarControls = UI.ButtonsBar((0, 0, 800, 32), ButtonsList)

    DropDownFileMenuList = ("Load", "Save", "New File")

    DropDownFileMenu = UI.DropDownMenu(pygame.Rect(10, 35, 120, 65), DropDownFileMenuList)

def GameDraw(DISPLAY):
    global track_list
    global TopBarControls
    global DropDownFileMenu

    DISPLAY.fill((40, 30, 35))

    track_list.Render(DISPLAY)
    TopBarControls.Render(DISPLAY)

    # -- Render DropDown Menus -- #
    if FileMenuEnabled:
        DropDownFileMenu.Render(DISPLAY)


def SaveMusicData():
    global track_list

    pass

def LoadMusicData():
    global track_list

    track_list.LoadMusicData(appData.ReadAppData_WithTry("/default", str, "0000:0000;0000:0000").split(';'))

def NewMusicFile():
    SaveMusicData()

    track_list.NewMusicFile()


def Update():
    global track_list
    global TopBarControls
    global DropDownFileMenu
    global FileMenuEnabled
    global TrackMenuEnabled

    TopBarControls.Update()
    track_list.Update()

    if FileMenuEnabled:
        DropDownFileMenu.Update()

    #region Top Bar Update
    if TopBarControls.ClickedButtonText == "File":
        TrackMenuEnabled = False
        if not FileMenuEnabled:
            FileMenuEnabled = True

        else:
            FileMenuEnabled = False

    if TopBarControls.ClickedButtonText == "Track":
        FileMenuEnabled = False
        if not TrackMenuEnabled:
            TrackMenuEnabled = True

        else:
            TrackMenuEnabled = False
    #endregion

    #region File DropDown Menu
    if FileMenuEnabled:
        if DropDownFileMenu.SelectedItem == "Save":
            DropDownFileMenu.SelectedItem = ""
            FileMenuEnabled = False
            SaveMusicData()

        if DropDownFileMenu.SelectedItem == "Load":
            DropDownFileMenu.SelectedItem = ""
            FileMenuEnabled = False
            LoadMusicData()

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

    TopBarControls.EventUpdate(event)
    track_list.EventUpdate(event)

    if FileMenuEnabled: DropDownFileMenu.EventUpdate(event)
