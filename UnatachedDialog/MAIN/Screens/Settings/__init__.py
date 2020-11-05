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
from OneTrack.MAIN import UI

WidgetController = UI.Widget.Widget_Controller
Root_Process = None

def Initialize(pRoot_Process):
    global WidgetController
    global Root_Process

    Root_Process = pRoot_Process
    pRoot_Process.DISPLAY = pygame.Surface((420, 320))
    Root_Process.TITLEBAR_TEXT = "OneTrack Settings"

    WidgetController = UI.Widget.Widget_Controller((0, 0, pRoot_Process.DISPLAY.get_width(), pRoot_Process.DISPLAY.get_height()))

    WidgetController.Append(UI.Widget.Widget_Button("True", 14, 5, 5, 0))
    WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Smooth Scrolling", 14, (230, 230, 230), UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", 14, "False") + 10, 5, 1))

def ReloadUI():
    del WidgetController
    WidgetController = UI.Widget.Widget_Controller((0, 0, pRoot_Process.DISPLAY.get_width(), pRoot_Process.DISPLAY.get_height()))

    WidgetController.Append(UI.Widget.Widget_Button("True", 14, 5, 5, 0))
    WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Smooth Scrolling", 14, (230, 230, 230), UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", 14, "False") + 10, 5, 1))


def Update():
    WidgetController.Update()

    # SmoothScrolling Option
    if WidgetController.LastInteractionID == 1:
        print("Placeholder : Smooth Scroll option")

def Draw(DISPLAY):
    WidgetController.Draw(DISPLAY)

def EventUpdate(event):
    WidgetController.ClickOffset = (Root_Process.POSITION[0], Root_Process.POSITION[1] + Root_Process.TITLEBAR_RECTANGLE[3])
    WidgetController.EventUpdate(event)
