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
from Core import utils
from Core import shape
from OneTrack import MAIN as Main
from OneTrack.MAIN import UI

class Widget_Controller:
    def __init__(self, Rectangle):
        self.Rectangle = utils.Convert.List_PygameRect(Rectangle)
        self.WidgetCollection = list()
        self.LastInteractionID = -1
        self.LastInteractionType = None
        self.Active = False
        self.ClickOffset = (0, 0)

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
        self.Active = pygame.Rect(self.Rectangle[0] + self.ClickOffset[0], self.Rectangle[1] + self.ClickOffset[1], self.Rectangle[2], self.Rectangle[3]).collidepoint((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

        if not self.Active:
            for widget in self.WidgetCollection:
                widget.Active = False
            return

        for widget in self.WidgetCollection:
            widget.Update()

            if not widget.InteractionType is None:
                self.LastInteractionID = widget.ID
                self.LastInteractionType = widget.InteractionType

    def EventUpdate(self, event):
        for widget in self.WidgetCollection:
            if widget.AwaysUpdate:  # -- If always update, update it no matter what
                if widget.EventUpdateable:
                    widget.EventUpdate(event)
                    continue

            else:  # -- If not, only update when mouse is hovering it
                ColideRect = pygame.Rect(self.ClickOffset[0] + self.Rectangle[0] + widget.Rectangle[0], self.ClickOffset[1] + self.Rectangle[1] + widget.Rectangle[1], widget.Rectangle[2], widget.Rectangle[3])

                if ColideRect.collidepoint(pygame.mouse.get_pos()):
                    if widget.EventUpdateable:
                        widget.CursorOffset = (ColideRect[0], ColideRect[1])
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
        self.EventUpdateable = False
        self.AwaysUpdate = False
        self.CursorOffset = (0, 0)

    def Render(self, DISPLAY):
        UI.ContentManager.ImageRender(DISPLAY, self.ImageName, self.Rectangle[0], self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

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
        self.EventUpdateable = True
        self.AwaysUpdate = False
        self.CursorOffset = (0, 0)

    def Render(self, DISPLAY):
        # -- Render Background -- #
        BGColor = UI.ThemesManager_GetProperty("Button_BackgroundColor")
        LineColor = UI.ThemesManager_GetProperty("Button_Active_IndicatorColor")

        if not self.Active:
            LineColor = UI.ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

        shape.Shape_Rectangle(DISPLAY, BGColor, self.Rectangle)
        shape.Shape_Rectangle(DISPLAY, LineColor, self.Rectangle, 1)

        # -- Render Change Title -- #
        TitleX = self.Rectangle[0] + self.Rectangle[2] / 2 - UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", 12, self.TitleName) / 2

        UI.ContentManager.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 12, self.TitleName, (230, 230, 230), TitleX, self.Rectangle[1])

        # -- Render EditableNumberView -- #
        self.Changer.Render(DISPLAY)

    def Update(self):
        self.Changer.Update()

        if not self.Changer.Value == self.LastValue:
            self.LastValue = self.Changer.Value
            self.InteractionType = self.Changer.Value

        if UI.ContentManager.GetFont_width("/PressStart2P.ttf", 12, self.Changer.Value) > self.Rectangle[2]:
            self.Rectangle[2] = self.Rectangle[2] + UI.ContentManager.GetFont_width("/PressStart2P.ttf", 12, self.Changer.Value) + 5

        if UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", 12, self.TitleName) > self.Rectangle[2]:
            self.Rectangle[2] = self.Rectangle[2] + UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", 12, self.TitleName)

        self.Changer.Rectangle[0] = self.Rectangle[0] + self.Rectangle[2] / 2 - UI.ContentManager.GetFont_width("/PressStart2P.ttf", 12, self.Changer.Value) / 2

    def EventUpdate(self, event):
        self.Changer.EventUpdate(event)

class Widget_Label:
    def __init__(self, FontName, Text, FontSize, Color, X, Y, WidgetID):
        if WidgetID == -1:
            raise ValueError("WidgetID cannot be -1")

        self.ID = WidgetID
        self.InteractionType = None
        self.Active = False
        self.EventUpdateable = False
        self.Text = Text
        self.FontSize = FontSize
        self.FontName = FontName
        self.Color = Color
        self.X = X
        self.Y = Y
        self.Rectangle = utils.Convert.List_PygameRect((X, Y, UI.ContentManager.GetFont_width(self.FontName, FontSize, self.Text), UI.ContentManager.GetFont_height(self.FontName, FontSize, self.Text)))
        self.AwaysUpdate = False
        self.CursorOffset = (0, 0)

    def Render(self, DISPLAY):
        UI.ContentManager.FontRender(DISPLAY, self.FontName, self.FontSize, self.Text, self.Color, self.Rectangle[0], self.Rectangle[1])

    def Update(self):
        self.Rectangle = utils.Convert.List_PygameRect((self.X, self.Y, UI.ContentManager.GetFont_width(self.FontName, self.FontSize, self.Text), UI.ContentManager.GetFont_height(self.FontName, self.FontSize, self.Text)))

    def EventUpdate(self, event):
        pass

class Widget_PianoKeys:
    def __init__(self, X, Y, WidgetID):
        if WidgetID == -1:
            raise ValueError("WidgetID cannot be -1")

        self.ID = WidgetID
        self.InteractionType = None
        self.Active = True
        self.EventUpdateable = True
        self.X = X
        self.Y = Y
        self.Rectangle = utils.Convert.List_PygameRect((X, Y, 380, 45))
        self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))
        self.LastRect = pygame.Rect(0, 0, 0, 0)
        self.LastNote = -1
        self.AwaysUpdate = True
        self.CursorOffset = (0, 0)
        pygame.key.set_repeat(0, 0)

    def Render(self, DISPLAY):
        if not self.LastRect == self.Rectangle:
            self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))

        # -- Render Background -- #
        self.Surface.fill((190, 190, 190))
        shape.Shape_Rectangle(self.Surface, (100, 100, 100), (0, 0, self.Rectangle[2], self.Rectangle[3]), 5)

        for i in range(12):
            NoteLabel = self.GetNote_ByIndex(i)

            # -- Variables -- #
            Width = 30
            Height = 25
            X = i * (Width + 2)
            Y = self.Rectangle[3] - Height
            BackgroundColor = (100, 105, 155)
            TextColor = (0, 5, 100)
            IsHighNote = False

            if "#" in NoteLabel:
                Width = 30
                X = i * (Width + 2)
                Width = 35
                X -= 2
                Y = 0
                BackgroundColor = (10, 15, 25)
                TextColor = (200, 205, 255)
                IsHighNote = True

            TextX = X + (Width / 2 - UI.ContentManager.GetFont_width("/PressStart2P.ttf", 12, NoteLabel) / 2)

            if self.LastNote == i:
                BackgroundColor = (200, 205, 255)
                TextColor = (0, 0, 0)

            if not IsHighNote:
                shape.Shape_Rectangle(self.Surface, BackgroundColor, (X, Y, Width, Height), 0, 0, 5, 5)
            else:
                shape.Shape_Rectangle(self.Surface, BackgroundColor, (X, Y, Width, Height), 0, 0, 0, 0, 5, 5)

            UI.ContentManager.FontRender(self.Surface, "/PressStart2P.ttf", 12, NoteLabel, TextColor, TextX, Y + 5)

        DISPLAY.blit(self.Surface, (self.Rectangle[0], self.Rectangle[1]))

    def GetNote_ByIndex(self, i):
        if i == 0:
            return "C"

        elif i == 1:
            return "C#"

        elif i == 2:
            return "D"

        elif i == 3:
            return "D#"

        elif i == 4:
            return "E"

        elif i == 5:
            return "F"

        elif i == 6:
            return "F#"

        elif i == 7:
            return "G"

        elif i == 8:
            return "G#"

        elif i == 9:
            return "A"

        elif i == 10:
            return "A#"

        elif i == 11:
            return "B"

    def Update(self):
        pass

    def EventUpdate(self, event):
        if event.type == pygame.KEYUP:
            self.LastNote = -1

        if event.type == pygame.KEYDOWN:
            # -- Note C -- #
            if event.key == pygame.K_z:
                self.LastNote = 0

            # -- Note C# -- #
            if event.key == pygame.K_s:
                self.LastNote = 1

            # -- Note D -- #
            if event.key == pygame.K_x:
                self.LastNote = 2

            # -- Note D# -- #
            if event.key == pygame.K_d:
                self.LastNote = 3

            # -- Note E -- #
            if event.key == pygame.K_c:
                self.LastNote = 4

            # -- Note F -- #
            if event.key == pygame.K_v:
                self.LastNote = 5

            # -- Note F# -- #
            if event.key == pygame.K_g:
                self.LastNote = 6

            # -- Note G -- #
            if event.key == pygame.K_b:
                self.LastNote = 7

            # -- Note G# -- #
            if event.key == pygame.K_h:
                self.LastNote = 8

            # -- Note A -- #
            if event.key == pygame.K_n:
                self.LastNote = 9

            # -- Note A# -- #
            if event.key == pygame.K_j:
                self.LastNote = 10

            # -- Note B -- #
            if event.key == pygame.K_m:
                self.LastNote = 11

class Widget_Button:
    def __init__(self, Text, FontSize, X, Y, WidgetID):
        if WidgetID == -1:
            raise ValueError("WidgetID cannot be -1")
        self.ID = WidgetID
        self.InteractionType = None
        self.Active = True
        self.EventUpdateable = True
        self.AwaysUpdate = False
        self.X = X
        self.Y = Y
        self.Text = Text
        self.FontSize = FontSize
        self.TextWidth = UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", self.FontSize, self.Text)
        self.TextHeight = UI.ContentManager.GetFont_height("/Ubuntu_Bold.ttf", self.FontSize, self.Text)
        self.Rectangle = utils.Convert.List_PygameRect((X - 2, Y - 2, self.TextWidth + 4, self.TextHeight + 4))
        self.LastRect = self.Rectangle
        self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))
        self.Centred_X = self.Rectangle[2] / 2 - UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text) / 2
        self.Centred_Y = self.Rectangle[3] / 2 - UI.ContentManager.GetFont_height("/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text) / 2
        self.ButtonState = 0
        self.CursorOffset = (0, 0)
        self.BgColor = UI.ThemesManager_GetProperty("Button_BackgroundColor")
        self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

    def Render(self, DISPLAY):
        # -- Render Background -- #
        shape.Shape_Rectangle(self.Surface, self.BgColor, (0, 0, self.Rectangle[2], self.Rectangle[3]))
        # -- Render Indicator -- #
        shape.Shape_Rectangle(self.Surface, self.IndicatorColor, (0, 0, self.Rectangle[2], self.Rectangle[3]), 1)

        # -- Render the Button Text -- #
        UI.ContentManager.FontRender(self.Surface, "/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text, (240, 240, 240), self.Centred_X, self.Centred_Y)

        DISPLAY.blit(self.Surface, (self.Rectangle[0], self.Rectangle[1]))

        if self.ButtonState == 2:
            self.ButtonState = 0

    def Update(self):
        # -- Check if surface has the correct size -- #
        if not self.LastRect == self.Rectangle:
            self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))

            # -- Update all Size and Position Variables -- #
            self.TextWidth = UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", self.FontSize, self.Text)
            self.TextHeight = UI.ContentManager.GetFont_height("/Ubuntu_Bold.ttf", self.FontSize, self.Text)
            self.Rectangle = utils.Convert.List_PygameRect((self.Rectangle[0] - 2, self.Rectangle[1] - 2, self.TextWidth + 4, self.TextHeight + 4))
            self.Centred_X = self.Rectangle[2] / 2 - UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text) / 2
            self.Centred_Y = self.Rectangle[3] / 2 - UI.ContentManager.GetFont_height("/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text) / 2

            self.LastRect = self.Rectangle

        self.BgColor = UI.ThemesManager_GetProperty("Button_BackgroundColor")
        self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

        if not self.Active:
            self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

            return

        if self.ButtonState == 0:
            self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

        elif self.ButtonState == 1:
            self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Active_IndicatorColor")

    def EventUpdate(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.ButtonState = 1

        if event.type == pygame.MOUSEBUTTONUP:
            self.ButtonState = 0
            self.InteractionType = True

