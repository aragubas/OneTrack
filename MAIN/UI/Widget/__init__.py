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
from ENGINE import utils
from ENGINE import shape
from OneTrack import MAIN as Main
from OneTrack.MAIN import UI

class Widget_Controller:
    def __init__(self, Rectangle):
        self.Rectangle = utils.Convert.List_PygameRect(Rectangle)
        self.WidgetCollection = list()
        self.LastInteractionID = -1
        self.LastInteractionType = None
        self.Active = False

    def Draw(self, DISPLAY):
        for widget in self.WidgetCollection:
            widget.Render(DISPLAY)

        if not self.LastInteractionID == -1:
            self.WidgetCollection[self.LastInteractionID].InteractionType = None

        self.LastInteractionID = -1
        self.LastInteractionType = None

    def Append(self, Widget):
        self.WidgetCollection.append(Widget)

    def Update(self):
        self.Active = self.Rectangle.collidepoint(pygame.mouse.get_pos())

        if not self.Active:
            for widget in self.WidgetCollection:
                widget.Active = False
            return

        for widget in self.WidgetCollection:
            widget.Update()

            if not widget.InteractionType == None:
                self.LastInteractionID = widget.ID
                self.LastInteractionType = widget.InteractionType

    def EventUpdate(self, event):
        if not self.Active:
            return

        for widget in self.WidgetCollection:
            ColideRect = pygame.Rect(self.Rectangle[0] + widget.Rectangle[0], self.Rectangle[1] + widget.Rectangle[1], widget.Rectangle[2], widget.Rectangle[3])
            if ColideRect.collidepoint(pygame.mouse.get_pos()):
                widget.EventUpdate(event)
                widget.Active = True
            else:
                widget.Active = False

    def GetWidget(self, WidgetID):
        for widget in self.WidgetCollection:
            if widget.ID == WidgetID:
                return widget

class Widget_PictureBox:
    def __init__(self, Rectangle, ImageName, WidgetID):
        if WidgetID == -1:
            raise ValueError("WidgetID cannot be -1")

        self.Rectangle = utils.Convert.List_PygameRect(Rectangle)
        self.ImageName = ImageName
        self.ID = WidgetID
        self.InteractionType = None
        self.Active = False

    def Render(self, DISPLAY):
        Main.DefaultContents.ImageRender(DISPLAY, self.ImageName, self.Rectangle[0], self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

    def Update(self):
        pass

    def EventUpdate(self, event):
        pass

class Widget_ValueChanger:
    def __init__(self, Position, TitleName, ChangerInitialValue, WidgetID):
        if WidgetID == -1:
            raise ValueError("WidgetID cannot be -1")

        self.Rectangle = utils.Convert.List_PygameRect((Position[0], Position[1], 48, 34))
        self.TitleName = TitleName
        self.ID = WidgetID
        self.Changer = UI.EditableNumberView(pygame.Rect(self.Rectangle[0], self.Rectangle[1] + 17, self.Rectangle[2], self.Rectangle[3] - 17), ChangerInitialValue)
        self.LastValue = ChangerInitialValue
        self.InteractionType = None
        self.Active = False

    def Render(self, DISPLAY):
        # -- Render Background -- #
        BGColor = UI.Button_Active_BackgroundColor
        LineColor = UI.Button_Active_IndicatorColor

        if not self.Active:
            BGColor = UI.Button_Inactive_BackgroundColor
            LineColor = UI.Button_Inactive_IndicatorColor

        shape.Shape_Rectangle(DISPLAY, BGColor, self.Rectangle)
        shape.Shape_Rectangle(DISPLAY, LineColor, self.Rectangle, 1)

        # -- Render Change Title -- #
        Main.DefaultContents.FontRender(DISPLAY, "/Ubuntu_Thin.ttf", 12, self.TitleName, (230, 230, 230), self.Rectangle[0] + Main.DefaultContents.GetFont_width("/Ubuntu_Thin.ttf", 12, self.TitleName) / 2, self.Rectangle[1])

        # -- Render EditableNumberView -- #
        self.Changer.Render(DISPLAY)

    def Update(self):
        self.Changer.Update()

        if not self.Changer.Value == self.LastValue:
            self.LastValue = self.Changer.Value
            self.InteractionType = self.Changer.Value

        self.Changer.Rectangle[0] = self.Rectangle[0] + self.Rectangle[2] / 2 - Main.DefaultContents.GetFont_width("/PressStart2P.ttf", 12, self.Changer.Value) / 2

    def EventUpdate(self, event):
        self.Changer.EventUpdate(event)

