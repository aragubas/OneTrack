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
import pygame, os
from OneTrack import MAIN as Main
from OneTrack.MAIN.Screens import Editor
from ENGINE import shape
from ENGINE import fx
from ENGINE import appData
from ENGINE import utils

# -- Color List -- #
TrackBlock_FrequencyBGColor_Active = (100, 94, 85)
TrackBlock_DurationBGColor_Active = (20, 34, 55)
TrackBlock_FrequencyBGColor_Deactive = (80, 70, 60)
TrackBlock_DurationBGColor_Deactive = (0, 10, 30)
#-----------------------#
EditableNumberView_ColorSelected = (255, 255, 255)
EditableNumberView_ColorActive = (155, 155, 155)
EditableNumberView_ColorDeactive = (90, 90, 90)
#-----------------------#
Button_Active_IndicatorColor = (46, 196, 182)
Button_Active_BackgroundColor = (15, 27, 44, 150)
Button_Inactive_IndicatorColor = (255, 51, 102)
Button_Inactive_BackgroundColor = (1, 22, 39, 150)
Button_BackgroundColor = (12, 22, 14)



class EditableNumberView:
    def __init__(self, Rectangle, Value):
        self.Rectangle = Rectangle
        self.Value = Value
        self.SelectedCharIndex = 0
        self.SplitedAlgarims = list(self.Value)
        self.IsActive = True
        self.Color = (155, 155, 155)
        self.AlgarimsWidth = 0
        self.AllowNotNumbers = False

    def Render(self, DISPLAY):
        for i, Algarims in enumerate(self.SplitedAlgarims):
            if self.IsActive:
                if i == self.SelectedCharIndex:
                    self.Color = EditableNumberView_ColorSelected

                else:
                    self.Color = EditableNumberView_ColorActive

            else:
                self.Color = EditableNumberView_ColorDeactive

            Main.DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", 12, str(Algarims), self.Color, self.Rectangle[0] + self.AlgarimsWidth * i, self.Rectangle[1])

    def Update(self):
        if not self.IsActive:
            return

        # -- Update the Color -- #
        for i, Algarims in enumerate(self.SplitedAlgarims):
            self.AlgarimsWidth = Main.DefaultContents.GetFont_width("/PressStart2P.ttf", 12, str(Algarims))

    def EventUpdate(self, event):
        if not self.IsActive:
            return

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.SelectedCharIndex -= 1

                if self.SelectedCharIndex <= -1:
                    self.SelectedCharIndex = len(self.SplitedAlgarims) - 1

            if event.key == pygame.K_RIGHT:
                self.SelectedCharIndex += 1

                if self.SelectedCharIndex >= len(self.SplitedAlgarims):
                    self.SelectedCharIndex = 0

            PressedKey = pygame.key.name(event.key).upper()
            if len(PressedKey) == 1:
                if self.AllowNotNumbers:
                    self.ChangeValueInPos(self.SelectedCharIndex, PressedKey)

                elif PressedKey.isdigit():
                    self.ChangeValueInPos(self.SelectedCharIndex, PressedKey)

            if event.key == pygame.K_DELETE:
                for i in range(0, 4):
                    self.ChangeValueInPos(i, "-")

    def ChangeValueInPos(self, Index, NewValue):
        self.SplitedAlgarims[Index] = NewValue
        self.Value = ""
        for algarims in self.SplitedAlgarims:
            self.Value += str(algarims)


class TrackBlock:
    def __init__(self, TrackData):
        self.TrackData = list(TrackData)
        self.Instance = -1
        self.TextWidth = Main.DefaultContents.GetFont_width("/PressStart2P.ttf", 12, "0000")
        self.TextHeight = Main.DefaultContents.GetFont_height("/PressStart2P.ttf", 12, "0000")
        self.Scroll = 0
        self.Rectangle = pygame.Rect(5, self.Scroll + (self.TextHeight + 10) * self.Instance, Main.DefaultContents.GetFont_width("/PressStart2P.ttf", 12, "0000"), Main.DefaultContents.GetFont_height("/PressStart2P.ttf", 12, "0000"))
        self.FrequencyNumber = EditableNumberView(pygame.Rect(self.Rectangle[0], self.Rectangle[1], self.TextWidth, self.TextHeight), str(self.TrackData[0]))
        self.DurationNumber = EditableNumberView(pygame.Rect(self.Rectangle[0] + self.TextWidth - 5, self.Rectangle[1], self.TextWidth, self.TextHeight), str(self.TrackData[1]))
        self.DurationNumber.AllowNotNumbers = True
        self.Active = False
        self.SelectedField = 0
        self.MaxFields = 1

    def Render(self, DISPLAY):
        if self.Active:
            FrequencyBGColor = TrackBlock_FrequencyBGColor_Active
            DurationBGColor = TrackBlock_DurationBGColor_Active
        else:
            FrequencyBGColor = TrackBlock_FrequencyBGColor_Deactive
            DurationBGColor = TrackBlock_DurationBGColor_Deactive

        # Render the Frequency Region
        shape.Shape_Rectangle(DISPLAY, FrequencyBGColor, (self.Rectangle[0] - 2, self.Rectangle[1] - 2, self.Rectangle[2] + 4, self.Rectangle[3] + 4), 0, 0, 5, 0, 5, 0)
        self.FrequencyNumber.Render(DISPLAY)

        # Render the Duration Region
        DurationX = (self.Rectangle[0] + self.TextWidth)
        shape.Shape_Rectangle(DISPLAY, DurationBGColor, (DurationX, self.Rectangle[1] - 2, (self.TextWidth) + 4, self.Rectangle[3] + 4), 0, 0, 0, 5, 0, 5)
        self.DurationNumber.Render(DISPLAY)

    def Update(self):
        self.Rectangle = pygame.Rect(10, self.Scroll + (self.TextHeight + 10) * self.Instance, self.TextWidth, self.TextHeight)

        self.DurationNumber.Rectangle = pygame.Rect(self.Rectangle[0] + self.TextWidth + 5, self.Rectangle[1], self.TextWidth, self.TextHeight)
        self.FrequencyNumber.Rectangle = pygame.Rect(self.Rectangle[0], self.Rectangle[1], self.TextWidth, self.TextHeight)

        self.FrequencyNumber.Update()
        self.FrequencyNumber.IsActive = self.SelectedField == 0

        self.DurationNumber.Update()
        self.DurationNumber.IsActive = self.SelectedField == 1

        # -- Update the Track Data -- #
        self.TrackData[0] = self.FrequencyNumber.Value
        self.TrackData[1] = self.DurationNumber.Value

    def EventUpdate(self, event):
        if not self.Active:
            return

        if self.SelectedField == 0:
            self.FrequencyNumber.EventUpdate(event)

        elif self.SelectedField == 1:
            self.DurationNumber.EventUpdate(event)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEDOWN:
                self.SelectedField -= 1

                if self.SelectedField <= 0:
                    self.SelectedField = 0

            if event.key == pygame.K_PAGEUP:
                self.SelectedField += 1

                if self.SelectedField >= self.MaxFields:
                    self.SelectedField = self.MaxFields

class Pattern:
    def __init__(self, PatternID, Rectangle):
        self.PatternID = PatternID
        self.Tracks = list()
        self.Scroll = 0
        self.PlayMode = False
        self.SelectedTrack = 0
        self.PlayMode_TrackDelay = 0
        self.PlayMode_CurrentTonePlayed = False
        self.BPM = 100
        self.Hz = 60
        self.PlayMode_LastSoundChannel = -1
        self.Rectangle = Rectangle

        for _ in range(24):
            self.AddBlankTrack()

    def AddBlankTrack(self):
        self.Tracks.append(TrackBlock(("0000", "0001")))

    def Draw(self, DISPLAY):
        for track in self.Tracks:
            if track.Instance == self.SelectedTrack:
                PointerRect = (2, track.Rectangle[1], 4, track.Rectangle[3])
                shape.Shape_Rectangle(DISPLAY, (230, 50, 75), PointerRect)

                self.Scroll = self.Rectangle[3] / 4 - (self.SelectedTrack * track.Rectangle[3])

            if track.Rectangle[1] >= DISPLAY.get_height() + track.TextHeight or track.Rectangle[1] <= -track.TextHeight:
                continue

            track.Render(DISPLAY)

            track.Active = track.Instance == self.SelectedTrack

    def Update(self):
        for i, track in enumerate(self.Tracks):
            track.Scroll = self.Scroll
            track.Instance = i
            track.Update()

        if self.PlayMode:
            self.PlayMode_TrackDelay += 1
            CurrentTrackObj = self.Tracks[self.SelectedTrack]
            BMP = abs(1000 / self.BPM)
            print(BMP)

            if self.PlayMode_TrackDelay >= BMP:
                self.SelectedTrack += 1
                self.PlayMode_TrackDelay = 0
                CurrentTrackData = CurrentTrackObj.TrackData

                if CurrentTrackData[0] == "----":
                    if "----" in CurrentTrackData[1]:
                        Main.DefaultContents.StopAllChannels()

                    elif CurrentTrackData[1].startswith("F"):
                        SplitedAgrs = list(CurrentTrackData[1])
                        FadeTime = ""

                        for i, arg in enumerate(SplitedAgrs):
                            if i > 1:
                                FadeTime += arg

                        FadeTime = int(FadeTime)

                        Main.DefaultContents.FadeoutSound(self.PlayMode_LastSoundChannel, FadeTime)

                    elif CurrentTrackData[1].startswith("J"):
                        SplitedAgrs = list(CurrentTrackData[1])
                        print(SplitedAgrs)
                        JmpTrackID = ""

                        for i, arg in enumerate(SplitedAgrs):
                            if i > 1:
                                print(arg)
                                JmpTrackID += arg

                        JmpTrackID = int(JmpTrackID)
                        Editor.track_list.PatternJump(JmpTrackID)
                        self.EndPlayMode()

                    elif CurrentTrackData[1].startswith("END"):
                        self.EndPlayMode()

                else:
                    SoundDuration = 0
                    SoundTune = 0

                    try:
                        SoundDuration = float("0.{0}".format(CurrentTrackObj.TrackData[1].replace("0", "")))
                    except ValueError:
                        pass

                    try:
                        SoundTune = int(CurrentTrackData[0])
                    except ValueError:
                        pass

                    if not SoundTune == 0:
                        self.PlayMode_LastSoundChannel = Main.DefaultContents.PlayTune(SoundTune, SoundDuration)

                if self.SelectedTrack >= len(self.Tracks):
                    self.EndPlayMode()

    def EndPlayMode(self):
        self.SelectedTrack = 0
        self.PlayMode = 0
        self.PlayMode_TrackDelay = 0
        self.PlayMode_CurrentTonePlayed = False
        self.Scroll = 25
        self.PlayMode_LastSoundChannel = -1

    def EventUpdate(self, event):
        for track in self.Tracks:
            track.EventUpdate(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not self.PlayMode:
                    self.PlayMode = True
                    self.PlayMode_TrackDelay = 0
                    self.PlayMode_CurrentTonePlayed = False

                else:
                    self.PlayMode = False
                    self.PlayMode_TrackDelay = 0
                    self.PlayMode_CurrentTonePlayed = False

            # -- Disable Edit Controls when in Play Mode -- #
            if not self.PlayMode:
                if event.key == pygame.K_DOWN:
                    self.SelectedTrack += 1
                    if self.SelectedTrack >= len(self.Tracks):
                        self.SelectedTrack = 0

                if event.key == pygame.K_UP:
                    if self.SelectedTrack <= 0:
                        self.SelectedTrack = len(self.Tracks)

                    self.SelectedTrack -= 1

                if event.key == pygame.K_F1:
                    if len(self.Tracks) > 1:
                        self.Tracks[self.SelectedTrack] = TrackBlock(("0000", "0001"))

                if event.key == pygame.K_F2:
                    if len(self.Tracks) < 24:
                        self.AddBlankTrack()

class TrackList:
    def __init__(self):
        self.Rectangle = pygame.Rect(5, 120, 300, 400)
        self.CurrentPatternID = 0
        self.PatternList = list()
        self.CurrentPattern = None
        self.TracksSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        self.LastRect = pygame.Rect(0, 0, 0, 0)

        self.AddNewPattern()

    def LoadMusicData(self, MusFileName):
        pass

    def SaveMusicData(self, MusFileName):
        pass

    def NewMusicFile(self):
        self.PatternList.clear()

        self.CurrentPattern = None
        self.AddNewPattern()

    def AddNewPattern(self):
        NewPatternID = len(self.PatternList)
        print(NewPatternID)
        self.PatternList.append(Pattern(len(self.PatternList), self.Rectangle))

        self.SetCurrentPattern_ByID(NewPatternID)

    def SetCurrentPattern_ByID(self, PatternID):
        self.CurrentPattern = self.PatternList[PatternID]

    def PatternJump(self, PatternID):
        if PatternID < len(self.PatternList):
            self.CurrentPattern = self.PatternList[PatternID]
            self.CurrentPattern.PlayMode = True
            self.CurrentPattern.SelectedTrack = 0


    def Render(self, DISPLAY):
        self.TracksSurface.fill((0, 0, 0, 0))
        self.CurrentPattern.Draw(self.TracksSurface)

        # -- Render the Pattern Name -- #
        fx.BlurredRectangle(self.TracksSurface, (0, 0, DISPLAY.get_width(), 24), 20, 100, (55, 55, 55))
        Main.DefaultContents.FontRender(self.TracksSurface, "/PressStart2P.ttf", 14, "Pattern: {0}/{1}".format(self.CurrentPatternID, len(self.PatternList) - 1), (255, 255, 255), 5, 5)

        DISPLAY.blit(self.TracksSurface, (self.Rectangle[0], self.Rectangle[1]))

    def Update(self):
        self.CurrentPattern.Update()
        self.CurrentPatternID = self.CurrentPattern.PatternID

        # -- Update the Surface Size -- #
        if not self.LastRect == self.Rectangle:
            self.TracksSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
            self.LastRect = self.Rectangle

    def EventUpdate(self, event):
        self.CurrentPattern.EventUpdate(event)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F3:
                self.AddNewPattern()

            if event.key == pygame.K_F5:
                PatternID = self.CurrentPatternID - 1

                if PatternID <= 0:
                    PatternID = 0

                self.SetCurrentPattern_ByID(PatternID)

            if event.key == pygame.K_F6:
                PatternID = self.CurrentPatternID + 1

                if PatternID >= len(self.PatternList) - 1:
                    PatternID = len(self.PatternList) - 1

                self.SetCurrentPattern_ByID(PatternID)

class Button:
    def __init__(self, Rectangle, ButtonText, TextSize):
        self.Rectangle = pygame.Rect(Rectangle[0], Rectangle[1], Rectangle[2], Rectangle[3])
        self.ButtonText = ButtonText
        self.TextSize = TextSize
        self.ButtonState = 0 # 0 - INACTIVE, 1 - DOWN, 2 - UP
        self.FontFile = "/PressStart2P.ttf"
        self.IsButtonEnabled = True
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1], Main.DefaultContents.GetFont_width(self.FontFile, self.TextSize, self.ButtonText) + 5, Main.DefaultContents.GetFont_height(self.FontFile, self.TextSize, self.ButtonText) + 6)
        self.LastRect = self.Rectangle
        self.CursorSettedToggle = False
        self.ButtonDowed = False
        self.ColisionRectangle = self.Rectangle
        self.BackgroundColor = Button_BackgroundColor
        self.SurfaceUpdated = False
        self.LastRect = pygame.Rect(0, 0, 0, 0)
        self.Surface = pygame.Surface((Rectangle[2], Rectangle[3]))
        self.ColisionXOffset = 0
        self.ColisionYOffset = 0

    def Update(self, event):
        # -- Set the Custom Colision Rectangle -- #
        self.ColisionRectangle = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

        if self.IsButtonEnabled:  # -- Only update the button, when is enabled.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Set the button to the DOWN state
                if self.ColisionRectangle.collidepoint(pygame.mouse.get_pos()):
                    self.ButtonState = 1
                    self.ButtonDowed = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Set the button to the UP state
                if self.ButtonDowed:
                    self.ButtonState = 2
                    self.ButtonDowed = False

            if event.type == pygame.MOUSEMOTION:  # Change the Cursor
                if self.ColisionRectangle.collidepoint(pygame.mouse.get_pos()):
                    self.CursorSettedToggle = True
                else:
                    if self.CursorSettedToggle:
                        self.CursorSettedToggle = False
                        self.ButtonState = 0

        else:
            self.ButtonState = 0
            if self.CursorSettedToggle:
                self.CursorSettedToggle = False

    def Set_X(self, Value):
        self.Rectangle[0] = Value

    def Set_Y(self, Value):
        self.Rectangle[1] = Value

    def Set_Width(self, Value):
        self.Rectangle[2] = Value

    def Set_Height(self, Value):
        self.Rectangle[3] = Value

    def Set_ColisionX(self, Value):
        self.ColisionXOffset = Value

    def Set_ColisionY(self, Value):
        self.ColisionYOffset = Value

    def Set_Text(self, Value):
        self.ButtonText = Value

    def Render(self, DISPLAY):
        # -- Update the Surface -- #
        self.Rectangle = pygame.Rect(self.Rectangle[0], self.Rectangle[1], Main.DefaultContents.GetFont_width(self.FontFile, self.TextSize, self.ButtonText) + 5, Main.DefaultContents.GetFont_height(self.FontFile, self.TextSize, self.ButtonText) + 6)

        # -- Update the Rect Wheen Needed -- #
        if self.Rectangle == self.LastRect:
            self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))

        # -- Update Surface when the size is changed -- #
        if not self.LastRect == self.Rectangle:
            self.SurfaceUpdated = False
            self.LastRect = self.Rectangle

        # -- Set the Button Colors -- #
        IndicatorColor = (0, 0, 0)

        if self.ButtonState == 0:
            IndicatorColor = Button_Inactive_IndicatorColor
            self.BackgroundColor = Button_Inactive_BackgroundColor

        elif self.ButtonState == 1:
            IndicatorColor = Button_Active_IndicatorColor
            self.BackgroundColor = Button_Active_BackgroundColor

        # -- Render Background -- #
        self.Surface.fill(self.BackgroundColor)

        # -- Indicator Bar -- #
        shape.Shape_Rectangle(self.Surface, IndicatorColor, (0, 0, self.Rectangle[2], 2), 0, 0)

        # -- Text -- #
        Main.DefaultContents.FontRender(self.Surface, self.FontFile, self.TextSize, self.ButtonText, (200, 200, 200), 3, 3)

        # -- Draw the Button -- #
        DISPLAY.blit(self.Surface, (self.Rectangle[0], self.Rectangle[1]))

        if self.ButtonState == 2:
            self.ButtonState = 0

class DropDownMenu:
    def __init__(self, Rectangle, ItemsList):
        self.Rectangle = Rectangle
        self.MenuItems = list()
        self.SelectedItem = ""

        for i, item in enumerate(ItemsList):
            self.MenuItems.append(Button(pygame.Rect(self.Rectangle[0] + 5, self.Rectangle[1] + 5 * i + 32, 0, 0), item, 12))

    def Render(self, DISPLAY):
        BluredBackground = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))
        BluredBackground.blit(DISPLAY, (0, 0), self.Rectangle)
        shape.Shape_Rectangle(DISPLAY, (30, 15, 32), self.Rectangle, 5)
        DISPLAY.blit(fx.Surface_Blur(BluredBackground, 20), self.Rectangle)

        for button in self.MenuItems:
            button.Render(DISPLAY)

        self.SelectedItem = ""

    def Update(self):
        for i, button in enumerate(self.MenuItems):
            button.Rectangle[1] = self.Rectangle[1] + i * button.Rectangle[3] + 5

            if button.ButtonState == 2:
                self.SelectedItem = button.ButtonText

    def EventUpdate(self, event):
        for item in self.MenuItems:
            item.Update(event)

class ButtonsBar:
    def __init__(self, Rectangle, ButtonsList):
        self.Rectangle = pygame.Rect(Rectangle[0], Rectangle[1], Rectangle[2], Rectangle[3])
        self.ButtonsList = ButtonsList
        self.ClickedButtonIndex = ""
        self.ColisionXOffset = 0
        self.ColisionYOffset = 0

    def Render(self, DISPLAY):
        for button in self.ButtonsList:
            button.Render(DISPLAY)

        self.ClickedButtonIndex = -1

    def Update(self):
        for i, button in enumerate(self.ButtonsList):
            if i == 0:
                button.Rectangle[0] = self.Rectangle[0]

            else:
                button.Rectangle[0] = (self.ButtonsList[i - 1].Rectangle[0] + self.ButtonsList[i - 1].Rectangle[2]) + 5

            button.ColisionXOffset = self.ColisionXOffset
            button.ColisionYOffset = self.ColisionYOffset

            if button.ButtonState == 2:
                self.ClickedButtonIndex = i

    def EventUpdate(self, event):
        for button in self.ButtonsList:
            button.Update(event)


class Window:
    def __init__(self, Rectangle, Title, Resiziable, Movable=True):
        self.WindowRectangle = Rectangle
        self.Title = Title
        self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], 20)
        self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[3] - 16, self.WindowRectangle[1] + self.WindowRectangle[3] - 16, 16, 16)
        self.Window_IsBeingGrabbed = False
        self.Window_IsBeingResized = False
        self.Window_MinimunW = Rectangle[2]
        self.Window_MinimunH = Rectangle[3]
        self.Resiziable = Resiziable
        self.OriginalMinumunHeight = 0
        self.OriginalResiziable = False
        self.WindowSurface_Rect = (0, 0, 200, 200)
        self.SurfaceSizeFixed = False
        self.Moveable = Movable
        self.Opacity = 255
        self.WindowSurface = pygame.Surface((5, 5))
        self.LastWindowRect = pygame.Rect((0, 0, 0, 0))

    def Render(self, DISPLAY):
        # -- Window Rectangle -- #
        self.WindowRectangle[0] = self.TitleBarRectangle[0]
        self.WindowRectangle[1] = self.TitleBarRectangle[1]
        # -- Title Bar Rectangle -- #
        self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], 20)

        # -- Resize Button Rectangle -- #
        if self.Resiziable:
            self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[2] - 10,
                                               self.WindowRectangle[1] + self.WindowRectangle[3], 10, 10)
        # -- Update Window Surface Destination -- #
        self.WindowSurface_Rect = (self.WindowRectangle[0], self.WindowRectangle[1] + 20, self.WindowRectangle[2], self.WindowRectangle[3] - 20)

        # -- Update Window Border -- #
        if not self.Resiziable:
            WindowBorderRectangle = self.WindowRectangle
        else:
            WindowBorderRectangle = (self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], self.WindowRectangle[3] + 12)

        # -- Draw the Window Blurred Background -- #
        if not self.WindowRectangle == self.LastWindowRect:
            self.LastWindowRect = self.WindowRectangle
            self.WindowSurface = pygame.Surface((WindowBorderRectangle[2], WindowBorderRectangle[3]))
        self.WindowSurface.set_alpha(self.Opacity)

        BluredBackground = pygame.Surface((WindowBorderRectangle[2], WindowBorderRectangle[3]))
        BluredBackground.blit(DISPLAY, (0, 0), self.WindowRectangle)
        fx.BlurredRectangle(BluredBackground, (0, 0, WindowBorderRectangle[2], WindowBorderRectangle[3]), 75, 100, (100, 100, 100))
        self.WindowSurface.blit(BluredBackground, (0, 0))

        # -- Draw the Resize Block -- #
        if self.Resiziable:
            Main.DefaultContents.ImageRender(self.WindowSurface, "/window/resize.png", self.WindowRectangle[2] - 12, self.WindowRectangle[3], self.ResizeRectangle[2], self.ResizeRectangle[3], True)

        # -- Draw the window title -- #
        fx.BlurredRectangle(self.WindowSurface, (0, 0, self.TitleBarRectangle[2], self.TitleBarRectangle[3] + 2), 5, 100, (100, 100, 100))
        Main.DefaultContents.FontRender(self.WindowSurface, "/Ubuntu_Thin.ttf", 20, self.Title, (250, 250, 255), self.TitleBarRectangle[2] / 2 - Main.DefaultContents.GetFont_width("/Ubuntu_Thin.ttf", 20, self.Title) / 2, -1)

        # -- Draw the Window Border -- #
        shape.Shape_Rectangle(self.WindowSurface, (0, 0, 0), (0, 0, WindowBorderRectangle[2], WindowBorderRectangle[3]), 1)

        DISPLAY.blit(self.WindowSurface, (self.WindowRectangle[0], self.WindowRectangle[1]))

    def EventUpdate(self, event):
        # -- Grab the Window -- #
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.TitleBarRectangle.collidepoint(pygame.mouse.get_pos()):
                self.Window_IsBeingGrabbed = True

            if self.ResizeRectangle.collidepoint(pygame.mouse.get_pos()) and self.Resiziable:
                self.Window_IsBeingResized = True
        # -- Ungrab the Window -- #
        if event.type == pygame.MOUSEBUTTONUP:
            if self.Window_IsBeingResized:
                self.Window_IsBeingResized = False

            if self.Window_IsBeingGrabbed:
                self.Window_IsBeingGrabbed = False

        # -- Grab Window -- #
        if self.Window_IsBeingGrabbed and self.Moveable:
            self.TitleBarRectangle[0] = pygame.mouse.get_pos()[0] - self.WindowRectangle[2] / 2
            self.TitleBarRectangle[1] = pygame.mouse.get_pos()[1] - self.TitleBarRectangle[3] / 2

        # -- Resize Window -- #
        if self.Window_IsBeingResized and self.Resiziable:
            # -- Limit Window Size -- #
            if self.WindowRectangle[2] >= self.Window_MinimunW:
                self.WindowRectangle[2] = pygame.mouse.get_pos()[0] - self.WindowRectangle[0]

            if self.WindowRectangle[3] >= self.Window_MinimunH: # <- Resize the Window
                self.WindowRectangle[3] = pygame.mouse.get_pos()[1] - self.WindowRectangle[1]

        # -- Dont Allow the Window to be resized lower than Minimum Size -- #
        if self.WindowRectangle[2] < self.Window_MinimunW:
            self.WindowRectangle[2] = self.Window_MinimunW

        if self.WindowRectangle[3] < self.Window_MinimunH:
            self.WindowRectangle[3] = self.Window_MinimunH

class VerticalListWithDescription:
    def __init__(self, Rectangle):
        self.Rectangle = pygame.Rect(Rectangle[0], Rectangle[1], Rectangle[2], Rectangle[3])
        self.LastRectangle = pygame.Rect(0, 0, 0, 0)
        self.ItemsName = list()
        self.ItemsDescription = list()
        self.ItemOrderID = list()
        self.ItemSprite = list()
        self.ItemSelected = list()
        self.LastItemClicked = "null"
        self.LastItemOrderID = None
        self.ScrollY = 0
        self.ListSurface = pygame.Surface
        self.ClickedItem = ""
        self.ColisionXOffset = 0
        self.ColisionYOffset = 0
        self.ButtonUpRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonDownRectangle = pygame.Rect(34, 0, 32, 32)
        self.ListSurfaceUpdated = False

    def Render(self,DISPLAY):
        if not self.Rectangle[2] == self.LastRectangle[2] or not self.Rectangle[3] == self.LastRectangle[3]:
            self.LastRectangle[2] = self.Rectangle[2]
            self.LastRectangle[3] = self.Rectangle[3]

            self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)

        self.ListSurface.fill((0, 0, 0, 0))

        for i, itemNam in enumerate(self.ItemsName):
            ItemRect = (self.Rectangle[0], self.ScrollY + self.Rectangle[1] + 42 * i, self.Rectangle[2], 40)

            BackgroundColor = (20, 42, 59, 50)
            ItemNameFontColor = (250, 250, 250)
            BorderColor = (32, 164, 243)
            TextsX = 5
            if self.ItemSprite[i] != "null":
                TextsX = 45

            if self.LastItemClicked == itemNam: # -- When the Item is Selected
                BackgroundColor = (20, 42, 59, 100)
                ItemNameFontColor = (255, 255, 255)
                BorderColor = (46, 196, 182)

            if self.ItemSelected[i]:  # -- When the Item is Clicked
                BackgroundColor = (30, 52, 69, 150)
                ItemNameFontColor = (250, 250, 250)
                BorderColor = (255, 51, 102)

            # -- Background -- #
            shape.Shape_Rectangle(self.ListSurface, BackgroundColor, ItemRect)

            # -- Indicator Bar -- #
            shape.Shape_Rectangle(self.ListSurface, BorderColor, ItemRect, 1)

            # -- Render Item Name -- #
            Main.DefaultContents.FontRender(self.ListSurface, "/Ubuntu_Bold.ttf", 14, itemNam, ItemNameFontColor, TextsX + ItemRect[0], ItemRect[1] + 5)

            # -- Render Item Description -- #
            Main.DefaultContents.FontRender(self.ListSurface, "/Ubuntu.ttf", 12, self.ItemsDescription[i], ItemNameFontColor, TextsX + ItemRect[0], ItemRect[1] + 25)

            # -- Render the Item Sprite -- #
            if self.ItemSprite[i] != "null":
                Main.DefaultContents.ImageRender(self.ListSurface, self.ItemSprite[i], ItemRect[0] + 4, ItemRect[1] + 4, 36, 32)

        # -- Blit All Work to Screen -- #
        DISPLAY.blit(self.ListSurface,(self.Rectangle[0], self.Rectangle[1]))

    def Update(self, event):
        ColisionRect = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

        if ColisionRect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.ScrollY += 5
                    return

                elif event.button == 4:
                    self.ScrollY -= 5
                    return

            # -- Select the Clicked Item -- #
            for i, itemNam in enumerate(self.ItemsName):
                ItemRect = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.ScrollY + self.Rectangle[1] + 42 * i, self.Rectangle[2], 40)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if ItemRect.collidepoint(pygame.mouse.get_pos()):
                        self.LastItemClicked = itemNam
                        self.ItemSelected[i] = True
                        self.LastItemOrderID = self.ItemOrderID[i]
                if event.type == pygame.MOUSEBUTTONUP:
                    self.ItemSelected[i] = False

    def Set_X(self, Value):
        self.Rectangle[0] = int(Value)

    def Set_Y(self, Value):
        self.Rectangle[1] = int(Value)

    def Set_W(self, Value):
        self.Rectangle[2] = int(Value)

    def Set_H(self, Value):
        self.Rectangle[3] = int(Value)

    def AddItem(self,ItemName, ItemDescription, ItemSprite="null"):
        self.ItemsName.append(ItemName)
        self.ItemsDescription.append(ItemDescription)
        self.ItemSprite.append(ItemSprite)
        self.ItemSelected.append(False)
        self.ItemOrderID.append((len(self.ItemOrderID) - 2) + 1)

    def ClearItems(self):
        self.ItemsName.clear()
        self.ItemsDescription.clear()
        self.ItemSprite.clear()
        self.ItemSelected.clear()
        self.ItemOrderID.clear()
