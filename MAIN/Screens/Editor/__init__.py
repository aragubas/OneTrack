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
from Core import cntMng
from Core import MAIN
from Core import appData
from Core import shape
import Core as tge
from OneTrack.MAIN import UI
from OneTrack.MAIN import SaveFileDialog
from OneTrack.MAIN import OpenFileDialog
from OneTrack.MAIN.Screens.Editor import OptionsBar
from OneTrack.MAIN.Screens.Editor import EditorBar
from OneTrack.MAIN.Screens.Editor import InstanceVar as var
from OneTrack.MAIN.Screens.Editor import SoundCacheMessage
import OneTrack.MAIN as Main

track_list = UI.TrackList

# -- Top Toolbar -- #
TopBarControls = UI.ButtonsBar
DropDownFileMenu = UI.DropDownMenu

def Initialize():
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
    OptionsBar.Initialize()
    EditorBar.Initialize()
    SoundCacheMessage.Initialize()

    OpenFileDialog.Enabled = True


def GameDraw(DISPLAY):
    global track_list
    global TopBarControls
    global DropDownFileMenu

    if not var.DisableControls:
        DISPLAY.fill((UI.ThemesManager_GetProperty("BackgroundColor")))

        track_list.Render(DISPLAY)
        TopBarControls.Render(DISPLAY)

        OptionsBar.Draw(DISPLAY)
        EditorBar.Draw(DISPLAY)

        # -- Render DropDown Menus -- #
        if var.FileMenuEnabled:
            DropDownFileMenu.Render(DISPLAY)

        SoundCacheMessage.Draw(DISPLAY)
        var.CopyOfScreen = DISPLAY.copy()

    SaveFileDialog.Draw(DISPLAY)

def SaveMusicData(FilePath):
    global track_list

    # -- Remove Pygame.Surface Object Before Dumping -- #
    for track in track_list.PatternList:
        for patternCol in track.Tracks:
            for block in patternCol.Tracks:
                block.BlockSurface = None
                block.SurfaceUpdateTrigger = True
                block.Active = True

    pickle.dump(track_list.PatternList, open(FilePath, "wb"))

    # -- Affter Dumping, Re-Crease the Surface -- #
    for track in track_list.PatternList:
        for patternCol in track.Tracks:
            for block in patternCol.Tracks:
                block.ResetSurface()
                block.SurfaceUpdateTrigger = True
                block.Active = True


def LoadMusicData(FileName):
    global track_list

    # -- Unload the Current SoundCahce -- #
    UI.ContentManager.UnloadSoundTuneCache()
    # -- Unload the Loaded TrackBlocks Surfaces -- #
    for track in track_list.PatternList:
        for patternCol in track.Tracks:
            for block in patternCol.Tracks:
                block.ResetSurface()

    # -- Load the List to RAM -- #
    patterns_list = pickle.load(open(FileName, "rb"))

    # -- Clear the Current Patterns -- #
    track_list.PatternList.clear()

    # -- Add Objects One-By-One -- #
    SavedBPM = 0
    SavedRows = 0
    SavedHighlightOne = 0
    SavedHighlightTwo = 0
    SavedPatterns = 0

    for i, obj in enumerate(patterns_list):
        # -- If in first pattern, read Music Properties -- #
        try:
            if i == 0:
                SavedBPM = int(obj.MusicProperties[0])
                SavedRows = int(obj.MusicProperties[1])
                SavedHighlightOne = int(obj.MusicProperties[2])
                SavedHighlightTwo = int(obj.MusicProperties[3])
                SavedPatterns = int(obj.MusicProperties[4])

        except:
            obj.MusicProperties = list()
            obj.MusicProperties.append(150) # BMP
            obj.MusicProperties.append(32) # ROWS
            obj.MusicProperties.append(4) # HIGH1
            obj.MusicProperties.append(16) # HIGH2
            obj.MusicProperties.append(2) # PATTERN

            SavedBPM = int(obj.MusicProperties[0])
            SavedRows = int(obj.MusicProperties[1])
            SavedHighlightOne = int(obj.MusicProperties[2])
            SavedHighlightTwo = int(obj.MusicProperties[3])
            SavedPatterns = int(obj.MusicProperties[4])

        # -- Add the Object -- #
        track_list.PatternList.append(obj)

        for patternCol in obj.Tracks:
            # -- Restart Track Collections Variables -- #
            patternCol.SelectedTrack = 0

            # -- Update TrackBlocks Code -- #
            for block in patternCol.Tracks:
                block.Reset(block.TrackData)
                block.Active = True

    # -- Set to the Pattern 0 -- #
    track_list.SetCurrentPattern_ByID(0)

    Obj = OptionsBar.WidgetCollection.GetWidget(1)
    Obj.Changer.Value = str(SavedBPM).zfill(3)
    Obj = OptionsBar.WidgetCollection.GetWidget(2)
    Obj.Changer.Value = str(SavedRows).zfill(3)

    var.BPM = SavedBPM
    var.Rows = SavedRows
    var.GenerateSoundCache = True
    var.SelectedTrack = 0
    var.Highlight = SavedHighlightOne
    var.HighlightSecond = SavedHighlightTwo
    var.Patterns = SavedPatterns

    OptionsBar.Update()

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

    SaveFileDialog.Update()
    OpenFileDialog.Update()

    if var.DisableControls: return

    TopBarControls.Update()
    track_list.Update()
    OptionsBar.Update()
    EditorBar.Update()
    SoundCacheMessage.Update()

    if var.FileMenuEnabled:
        DropDownFileMenu.Update()

    #region Top Bar Update
    if TopBarControls.ClickedButtonIndex == 0:
        if not var.FileMenuEnabled:
            var.FileMenuEnabled = True

        else:
            var.FileMenuEnabled = False

    #region File DropDown Menu
    if var.FileMenuEnabled:
        if DropDownFileMenu.SelectedItem == "Save":
            DropDownFileMenu.SelectedItem = ""
            var.FileMenuEnabled = False
            var.DisableControls = True

            SaveFileDialog.Enabled = True

        if DropDownFileMenu.SelectedItem == "Load":
            DropDownFileMenu.SelectedItem = ""
            var.FileMenuEnabled = False
            var.DisableControls = True

            OpenFileDialog.Enabled = True

        if DropDownFileMenu.SelectedItem == "New File":
            DropDownFileMenu.SelectedItem = ""
            var.FileMenuEnabled = False

            NewMusicFile()

    #endregion


def EventUpdate(event):
    global track_list
    global TopBarControls
    global DropDownFileMenu

    if not var.DisableControls:
        TopBarControls.EventUpdate(event)
        track_list.EventUpdate(event)
        OptionsBar.EventUpdate(event)
        EditorBar.EventUpdate(event)

        if var.FileMenuEnabled: DropDownFileMenu.EventUpdate(event)
    else:
        SaveFileDialog.EventUpdate(event)