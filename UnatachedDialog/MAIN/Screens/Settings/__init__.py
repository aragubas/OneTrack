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
import Core, pygame
from OneTrack.MAIN.Screens.Editor import InstanceVar as var
from OneTrack.MAIN import UI

WidgetController = UI.Widget.Widget_Controller
Root_Process = None
LastThemeName = ""
LastAnimationScale = ""
LastVolumeMultiplier = ""

def Initialize(pRoot_Process):
    global WidgetController
    global Root_Process

    Root_Process = pRoot_Process
    pRoot_Process.DISPLAY = pygame.Surface((420, 320))
    Root_Process.TITLEBAR_TEXT = "OneTrack Settings"

    WidgetController = UI.Widget.Widget_Controller((0, 0, pRoot_Process.DISPLAY.get_width(), pRoot_Process.DISPLAY.get_height()))
    ReloadUI()

def ReloadUI():
    WidgetController.Clear()

    # Smooth Scroll Option
    WidgetController.Append(UI.Widget.Widget_Button(var.DefaultContent.Get_RegKey("/options/smooth_scroll"), 14, 5, 5, 0))
    WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Smooth Scrolling", 14, (230, 230, 230), UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", 14, "False") + 10, 5, 1))

    # Disable Dynamic Color Option
    WidgetController.Append(UI.Widget.Widget_Button(var.DefaultContent.Get_RegKey("/options/disabled_block_color"), 14, 5, 35, 2))
    WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Dynamic Block Color", 14, (230, 230, 230), UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", 14, "False") + 10, 35, 3))

    # Trackpointer Animation Option
    WidgetController.Append(UI.Widget.Widget_Button(var.DefaultContent.Get_RegKey("/options/trackpointer_animation"), 14, 5, 65, 4))
    WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Animated Trackpointer", 14, (230, 230, 230), UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", 14, "False") + 10, 65, 5))

    # Selected Theme
    WidgetController.Append(UI.Widget.Widget_Textbox("/Ubuntu.ttf", var.DefaultContent.Get_RegKey("/selected_theme"), 14, (230, 230, 230), 120, 95, 230, 6))
    WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "UI Theme", 14, (230, 230, 230), 5, 95, 7))
    WidgetController.Append(UI.Widget.Widget_Button("Apply", 14, 75, 95, 8))

    # Animation Scale
    WidgetController.Append(UI.Widget.Widget_Textbox("/Ubuntu.ttf", var.DefaultContent.Get_RegKey("/options/animation_scale"), 14, (230, 230, 230), 160, 125, 230, 9))
    WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Animation Scale", 14, (230, 230, 230), 5, 125, 10))
    WidgetController.Append(UI.Widget.Widget_Button("Apply", 14, 115, 125, 11))

    # Volume Multiplier
    WidgetController.Append(UI.Widget.Widget_Textbox("/Ubuntu.ttf", var.DefaultContent.Get_RegKey("/options/VolumeMultiplier"), 14, (230, 230, 230), 170, 155, 230, 12))
    WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Volume Multiplier", 14, (230, 230, 230), 5, 155, 13))
    WidgetController.Append(UI.Widget.Widget_Button("Apply", 14, 127, 155, 14))


def Update():
    global LastThemeName
    global WidgetController
    global LastAnimationScale
    global LastVolumeMultiplier

    WidgetController.Update()

    # SmoothScrolling Option
    if WidgetController.LastInteractionID == 0:
        if var.DefaultContent.Get_RegKey("/options/smooth_scroll", bool):
            var.DefaultContent.Write_RegKey("/options/smooth_scroll", "False")
        else:
            var.DefaultContent.Write_RegKey("/options/smooth_scroll", "True")
        ReloadUI()

    # Disabled Block Color
    if WidgetController.LastInteractionID == 2:
        if var.DefaultContent.Get_RegKey("/options/disabled_block_color", bool):
            var.DefaultContent.Write_RegKey("/options/disabled_block_color", "False")
        else:
            var.DefaultContent.Write_RegKey("/options/disabled_block_color", "True")
        ReloadUI()

    # Trackpointer Animation
    if WidgetController.LastInteractionID == 4:
        if var.DefaultContent.Get_RegKey("/options/trackpointer_animation", bool):
            var.DefaultContent.Write_RegKey("/options/trackpointer_animation", "False")
        else:
            var.DefaultContent.Write_RegKey("/options/trackpointer_animation", "True")
        ReloadUI()

    # Theme Name textbox
    if WidgetController.LastInteractionID == 6:
        CurrentText = WidgetController.LastInteractionType

        if len(CurrentText) == 0:
            CurrentText = "default"

        CurrentText = CurrentText.replace(" ", "_")

        # Check if theme exists
        LastThemeName = CurrentText

    # Theme Apply
    if WidgetController.LastInteractionID == 8:
        # Check if theme exists
        try:
            UwU = var.DefaultContent.Get_RegKey(LastThemeName)

        except:
            UwU = "default"

        var.DefaultContent.Write_RegKey("/selected_theme", UwU)

        ReloadUI()

    # Animation Scale Textbox
    if WidgetController.LastInteractionID == 9:
        CurrentText = WidgetController.LastInteractionType

        if not CurrentText.isdigit():
            CurrentText = "10"

        if len(CurrentText) == 0:
            CurrentText = "10"

        # Check if theme exists
        LastAnimationScale = CurrentText

    # Animation Apply
    if WidgetController.LastInteractionID == 11:
        UwU = LastAnimationScale
        if not UwU.isdigit():
            UwU = "10"

        # Check if theme exists
        var.DefaultContent.Write_RegKey("/options/animation_scale", UwU)

        ReloadUI()

    # Volume Multiplier Textbox
    if WidgetController.LastInteractionID == 11:
        CurrentText = WidgetController.LastInteractionType

        if CurrentText.isdigit():
            CurrentText = "0.1"

        #str.isalnum()

        if len(CurrentText) == 0:
            CurrentText = "0.1"

        # Check if theme exists
        LastVolumeMultiplier = CurrentText

    # Volume Multiplier Apply
    if WidgetController.LastInteractionID == 14:
        UwU = LastVolumeMultiplier
        if not UwU.isdigit():
            UwU = "0.1"

        # Check if theme exists
        var.DefaultContent.Write_RegKey("/options/VolumeMultiplier", UwU)

        ReloadUI()


def Draw(DISPLAY):
    WidgetController.Draw(DISPLAY)

def EventUpdate(event):
    WidgetController.ClickOffset = (Root_Process.POSITION[0], Root_Process.POSITION[1] + Root_Process.TITLEBAR_RECTANGLE[3])
    WidgetController.EventUpdate(event)

def WhenClosing():
    global Root_Process

    # Reload UI Theme
    var.LoadDefaultValues()
    UI.ThemesManager_LoadTheme(UI.ContentManager.Get_RegKey("/selected_theme"))
    var.GenerateSoundCache = True
