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
from OneTrack.MAIN.UI import Widget as Widget
from OneTrack.MAIN.Screens.Editor import InstanceVar as var
from Core import shape
from Core import fx
from Core import appData
from Core import utils
from math import log2, pow

# -- Color List -- #
TrackBlock_FrequencyBGColor_Active = (90, 84, 75)
TrackBlock_DurationBGColor_Active = (40, 54, 75)
TrackBlock_FrequencyBGColor_Deactive = (30, 20, 37)
TrackBlock_DurationBGColor_Deactive = (0, 0, 10)
TrackBlock_FrequencyBGColor_Hightlight1 = (50, 30, 47)
TrackBlock_DurationBGColor_Hightlight1 = (18, 7, 19)
TrackBlock_FrequencyBGColor_Hightlight2 = (98, 77, 78)
TrackBlock_DurationBGColor_Hightlight2 = (45, 42, 55)
TrackBlock_InstanceLabelActiveColor = (255, 255, 255)
TrackBlock_InstanceLabelDeactiveColor = (55, 55, 55)
TrackBlock_NoteLabel_UnknowNote = (110, 90, 125)
TrackBlock_NoteLabel_KnowNote = (220, 190, 225)
# -----------------------#
EditableNumberView_ColorSelected = (255, 255, 255)
EditableNumberView_ColorActive = (100, 100, 100)
EditableNumberView_ColorDeactive = (50, 50, 50)
# -----------------------#
Button_Active_IndicatorColor = (46, 196, 182)
Button_Active_BackgroundColor = (15, 27, 44)
Button_Inactive_IndicatorColor = (255, 51, 102)
Button_Inactive_BackgroundColor = (1, 22, 39)
Button_BackgroundColor = (12, 22, 14)
# -----------------------#
InputBox_COLOR_INACTIVE = (1, 22, 39)
InputBox_COLOR_ACTIVE = (15, 27, 44)
InputBox_FontFile = "/Ubuntu.ttf"
# -------------------------#
TrackPointerColor = (250, 70, 95)
TrackSelectedPattern_PlayMode_BackgroundColor = (10, 15, 15)
TrackSelectedPattern_PlayMode_FontColor = (255, 255, 255)
TrackSelectedPattern_BackgroundColor = (100, 105, 115)
TrackSelectedPattern_FontColor = (265, 230, 255)
# ------------------------#
BackgroundColor = (62, 62, 116)
# ------------------------ #
ContentManager = None

def LoadColorSchema(FolderName):
    pass


def StringToColorList(Input):
    ColorLst = Input.split(',')

    ColorR = ColorLst[0]
    ColorG = ColorLst[1]
    ColorB = ColorLst[2]
    ColorA = ColorLst[3]

    return (ColorR, ColorG, ColorB, ColorA)

def ColorListToString(Input):
    return ''.join((Input[0], ",", Input[1], ",", Input[2], ",", Input[3]))


class EditableNumberView:
    def __init__(self, Rectangle, Value, FontSize=12):
        self.Rectangle = utils.Convert.List_PygameRect(Rectangle)
        self.Value = Value
        self.SelectedCharIndex = 0
        self.SplitedAlgarims = list(self.Value)
        self.IsActive = True
        self.Color = (155, 155, 155)
        self.AlgarimsWidth = 0
        self.AllowNotNumbers = False
        self.YOffset = 0
        self.FontSize = FontSize

    def Render(self, DISPLAY):
        for i, Algarims in enumerate(self.SplitedAlgarims):
            if self.IsActive:
                if i == self.SelectedCharIndex:
                    self.Color = EditableNumberView_ColorSelected

                else:
                    self.Color = EditableNumberView_ColorActive

            else:
                self.Color = EditableNumberView_ColorDeactive

            ContentManager.FontRender(DISPLAY, "/PressStart2P.ttf", self.FontSize, str(Algarims), self.Color, self.Rectangle[0] + self.AlgarimsWidth * i, self.YOffset + self.Rectangle[1])

    def Update(self):
        if not self.IsActive:
            return

        # -- Update the Color -- #
        for i, Algarims in enumerate(self.SplitedAlgarims):
            self.AlgarimsWidth = ContentManager.GetFont_width("/PressStart2P.ttf", self.FontSize, str(Algarims))

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
                for i in range(0, 5):
                    self.ChangeValueInPos(i, "-")

    def ChangeValueInPos(self, Index, NewValue):
        self.SplitedAlgarims[Index] = NewValue
        self.Value = ""
        for algarims in self.SplitedAlgarims:
            self.Value += str(algarims)


name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def pitch(freq):
    freq = int(freq)

    if freq == 32:  # C1
        return ''.join((name[0], "1"))

    elif freq == 65:  # C2
        return ''.join((name[0], "2"))

    elif freq == 130:  # C3
        return ''.join((name[0], "3"))

    elif freq == 261:  # C4
        return ''.join((name[0], "4"))

    elif freq == 523:  # C5
        return ''.join((name[0], "5"))

    elif freq == 1046:  # C6
        return ''.join((name[0], "6"))

    elif freq == 2093:  # C7
        return ''.join((name[0], "7"))

    elif freq == 4186:  # C8
        return ''.join((name[0], "8"))

    elif freq == 34:  # C#1
        return ''.join((name[1], "1"))

    elif freq == 69:  # C#2
        return ''.join((name[1], "2"))

    elif freq == 138:  # C#3
        return ''.join((name[1], "3"))

    elif freq == 277:  # C#4
        return ''.join((name[1], "4"))

    elif freq == 554:  # C#5
        return ''.join((name[1], "5"))

    elif freq == 1108:  # C#6
        return ''.join((name[1], "6"))

    elif freq == 2217:  # C#7
        return ''.join((name[1], "7"))

    elif freq == 4434:  # C#8
        return ''.join((name[1], "8"))

    elif freq == 36:  # D1
        return ''.join((name[2], "1"))

    elif freq == 73:  # D2
        return ''.join((name[2], "2"))

    elif freq == 146:  # D3
        return ''.join((name[2], "3"))

    elif freq == 293:  # D4
        return ''.join((name[2], "4"))

    elif freq == 587:  # D5
        return ''.join((name[2], "5"))

    elif freq == 1174:  # D6
        return ''.join((name[2], "6"))

    elif freq == 2349:  # D7
        return ''.join((name[2], "7"))

    elif freq == 4698:  # D8
        return ''.join((name[2], "8"))

    elif freq == 38:  # D#1
        return ''.join((name[3], "1"))

    elif freq == 77:  # D#2
        return ''.join((name[3], "2"))

    elif freq == 155:  # D#3
        return ''.join((name[3], "3"))

    elif freq == 311:  # D#4
        return ''.join((name[3], "4"))

    elif freq == 622:  # D#5
        return ''.join((name[3], "5"))

    elif freq == 1244:  # D#6
        return ''.join((name[3], "6"))

    elif freq == 2489:  # D#7
        return ''.join((name[3], "7"))

    elif freq == 4978:  # D#8
        return ''.join((name[3], "8"))

    elif freq == 41:  # E1
        return ''.join((name[4], "1"))

    elif freq == 82:  # E2
        return ''.join((name[4], "2"))

    elif freq == 164:  # E3
        return ''.join((name[4], "3"))

    elif freq == 329:  # E4
        return ''.join((name[4], "4"))

    elif freq == 659:  # E5
        return ''.join((name[4], "5"))

    elif freq == 1318:  # E6
        return ''.join((name[4], "6"))

    elif freq == 2637:  # E7
        return ''.join((name[4], "7"))

    elif freq == 5274:  # E8
        return ''.join((name[4], "8"))

    elif freq == 43:  # F1
        return ''.join((name[5], "1"))

    elif freq == 87:  # F2
        return ''.join((name[5], "2"))

    elif freq == 174:  # F3
        return ''.join((name[5], "3"))

    elif freq == 349:  # F4
        return ''.join((name[5], "4"))

    elif freq == 698:  # F5
        return ''.join((name[5], "5"))

    elif freq == 1396:  # F6
        return ''.join((name[5], "6"))

    elif freq == 2793:  # F7
        return ''.join((name[5], "7"))

    elif freq == 46:  # F#1
        return ''.join((name[6], "1"))

    elif freq == 92:  # F#2
        return ''.join((name[6], "2"))

    elif freq == 184:  # F#3
        return ''.join((name[6], "3"))

    elif freq == 369:  # F#4
        return ''.join((name[6], "4"))

    elif freq == 739:  # F#5
        return ''.join((name[6], "5"))

    elif freq == 1479:  # F#6
        return ''.join((name[6], "6"))

    elif freq == 2959:  # F#7
        return ''.join((name[6], "7"))

    elif freq == 5919:  # F#8
        return ''.join((name[6], "8"))

    elif freq == 48:  # G1
        return ''.join((name[7], "1"))

    elif freq == 97:  # G2
        return ''.join((name[7], "2"))

    elif freq == 195:  # G3
        return ''.join((name[7], "3"))

    elif freq == 391:  # G4
        return ''.join((name[7], "4"))

    elif freq == 783:  # G5
        return ''.join((name[7], "5"))

    elif freq == 1567:  # G6
        return ''.join((name[7], "6"))

    elif freq == 3135:  # G7
        return ''.join((name[7], "7"))

    elif freq == 6271:  # G8
        return ''.join((name[7], "8"))

    elif freq == 51:  # G#1
        return ''.join((name[8], "1"))

    elif freq == 103:  # G#2
        return ''.join((name[8], "2"))

    elif freq == 207:  # G#3
        return ''.join((name[8], "3"))

    elif freq == 415:  # G#4
        return ''.join((name[8], "4"))

    elif freq == 830:  # G#5
        return ''.join((name[8], "5"))

    elif freq == 1661:  # G#6
        return ''.join((name[8], "6"))

    elif freq == 3322:  # G#7
        return ''.join((name[8], "7"))

    elif freq == 6644:  # G#8
        return ''.join((name[8], "8"))

    elif freq == 27:  # A0
        return ''.join((name[9], "0"))

    elif freq == 55:  # A1
        return ''.join((name[9], "1"))

    elif freq == 110:  # A2
        return ''.join((name[9], "2"))

    elif freq == 220:  # A3
        return ''.join((name[9], "3"))

    elif freq == 440:  # A4
        return ''.join((name[9], "4"))

    elif freq == 880:  # A5
        return ''.join((name[9], "5"))

    elif freq == 1760:  # A6
        return ''.join((name[9], "6"))

    elif freq == 3520:  # A7
        return ''.join((name[9], "7"))

    elif freq == 7040:  # A8
        return ''.join((name[9], "8"))

    elif freq == 29:  # A#0
        return ''.join((name[10], "0"))

    elif freq == 58:  # A#1
        return ''.join((name[10], "1"))

    elif freq == 116:  # A#2
        return ''.join((name[10], "2"))

    elif freq == 233:  # A#3
        return ''.join((name[10], "3"))

    elif freq == 466:  # A#4
        return ''.join((name[10], "4"))

    elif freq == 932:  # A#5
        return ''.join((name[10], "5"))

    elif freq == 1864:  # A#6
        return ''.join((name[10], "6"))

    elif freq == 3729:  # A#7
        return ''.join((name[10], "7"))

    elif freq == 7458:  # A#8
        return ''.join((name[10], "7"))

    elif freq == 30:  # B0
        return ''.join((name[11], "0"))

    elif freq == 61:  # B1
        return ''.join((name[11], "1"))

    elif freq == 123:  # B2
        return ''.join((name[11], "2"))

    elif freq == 246:  # B3
        return ''.join((name[11], "3"))

    elif freq == 493:  # B4
        return ''.join((name[11], "4"))

    elif freq == 987:  # B5
        return ''.join((name[11], "5"))

    elif freq == 1975:  # B6
        return ''.join((name[11], "6"))

    elif freq == 3951:  # B7
        return ''.join((name[11], "7"))

    elif freq == 7902:  # B8
        return ''.join((name[11], "8"))

    return "?"


class TrackBlock:
    def __init__(self, TrackData):
        self.Reset(TrackData)

    def Reset(self, TrackData):
        self.TrackData = list(TrackData)
        self.Instance = -1
        self.TextWidth = ContentManager.GetFont_width("/PressStart2P.ttf", 12, "00000")
        self.TextHeight = ContentManager.GetFont_height("/PressStart2P.ttf", 12, "00000")
        self.Scroll = 0
        self.Rectangle = pygame.Rect(5, self.Scroll + (self.TextHeight + 10) * self.Instance, ContentManager.GetFont_width("/PressStart2P.ttf", 12, "00000") * 2 + 5, ContentManager.GetFont_height("/PressStart2P.ttf", 12, "00000") + 2)
        self.LastRect = self.Rectangle
        self.FrequencyNumber = EditableNumberView(pygame.Rect(10, 2, self.TextWidth, self.TextHeight), str(self.TrackData[0]), 10)
        self.DurationNumber = EditableNumberView(pygame.Rect(self.FrequencyNumber.Rectangle[0], 2, self.TextWidth, self.TextHeight), str(self.TrackData[1]), 10)
        self.DurationNumber.AllowNotNumbers = True
        self.Active = False
        self.SelectedField = 0
        self.MaxFields = 1
        self.Highlight = 0
        TrackPitch = TrackData[0]
        if TrackPitch == "-----":
            TrackPitch = "00000"
        self.PitchLabel = pitch(TrackPitch)
        self.ResetSurface()
        self.SurfaceUpdateTrigger = True
        self.DisabledTrigger = True
        self.ReRender()

    def Render(self, DISPLAY):
        # -- If surface needs to be Updated -- #
        if self.SurfaceUpdateTrigger:
            self.ReRender()
            self.SurfaceUpdateTrigger = False

        # -- Re-Render the Block one time when Block is Disabled -- #
        if not self.Active and not self.DisabledTrigger:
            self.DisabledTrigger = True
            self.SurfaceUpdateTrigger = True
            self.ReRender()

        # -- Set Disabled Trigger to False -- #
        if self.Active:
            self.DisabledTrigger = False
            self.ReRender()

        DISPLAY.blit(self.BlockSurface, (self.Rectangle[0], self.Scroll + self.Rectangle[1]))

    def ReRender(self):
        # -- Set the Color Scheme -- #
        if self.Active:
            FrequencyBGColor = TrackBlock_FrequencyBGColor_Active
            DurationBGColor = TrackBlock_DurationBGColor_Active

        else:
            FrequencyBGColor = TrackBlock_FrequencyBGColor_Deactive
            DurationBGColor = TrackBlock_DurationBGColor_Deactive

        if self.Highlight == 1:
            FrequencyBGColor = TrackBlock_FrequencyBGColor_Hightlight1
            DurationBGColor = TrackBlock_DurationBGColor_Hightlight1

        elif self.Highlight == 2:
            FrequencyBGColor = TrackBlock_FrequencyBGColor_Hightlight2
            DurationBGColor = TrackBlock_DurationBGColor_Hightlight2

        if self.Active:
            FrequencyBGColor = TrackBlock_FrequencyBGColor_Active
            DurationBGColor = TrackBlock_DurationBGColor_Active

        if self.PitchLabel == "?":
            PitchLabelColor = TrackBlock_NoteLabel_UnknowNote
        else:
            PitchLabelColor = TrackBlock_NoteLabel_KnowNote

        # Fill the Background
        self.BlockSurface.fill(BackgroundColor)

        # -- Render the Frequency Region
        shape.Shape_Rectangle(self.BlockSurface, FrequencyBGColor, (self.FrequencyNumber.Rectangle[0], self.FrequencyNumber.Rectangle[1], self.FrequencyNumber.Rectangle[2], self.FrequencyNumber.Rectangle[3]), 0, 0, 5, 0, 5, 0)
        self.FrequencyNumber.Render(self.BlockSurface)

        # -- Render the Duration Region
        DurationX = (self.FrequencyNumber.Rectangle[0] + self.TextWidth)
        shape.Shape_Rectangle(self.BlockSurface, DurationBGColor, (DurationX, self.DurationNumber.Rectangle[1], (self.TextWidth), self.DurationNumber.Rectangle[3]), 0, 0, 0, 5, 0, 5)
        self.DurationNumber.Render(self.BlockSurface)

        LabelColor = TrackBlock_InstanceLabelActiveColor
        if not self.Active:
            LabelColor = TrackBlock_InstanceLabelDeactiveColor

        ContentManager.FontRender(self.BlockSurface, "/PressStart2P.ttf", 10, str(self.Instance).zfill(2), LabelColor, (DurationX + self.TextWidth) + 3, 1)

        # -- Render Note Label -- #
        ContentManager.FontRender(self.BlockSurface, "/PressStart2P.ttf", 10, self.PitchLabel, PitchLabelColor, 0, 0)

    def ResetSurface(self):
        self.BlockSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))

    def Update(self):
        FrequencyWidthMax = ContentManager.GetFont_width("/PressStart2P.ttf", 10, "000")

        self.Rectangle = pygame.Rect(self.Rectangle[0], (self.TextHeight + 10) * self.Instance, FrequencyWidthMax + self.FrequencyNumber.Rectangle[2] + self.DurationNumber.Rectangle[2] + 25, self.Rectangle[3])
        self.FrequencyNumber.Rectangle = pygame.Rect(FrequencyWidthMax, 1, self.TextWidth, self.TextHeight)
        self.DurationNumber.Rectangle = pygame.Rect(self.FrequencyNumber.Rectangle[0] + self.FrequencyNumber.Rectangle[2] + 2, 1, self.TextWidth, self.TextHeight)

        if not self.LastRect == self.Rectangle:
            self.LastRect = self.Rectangle
            self.ResetSurface()

        self.FrequencyNumber.Update()
        self.FrequencyNumber.IsActive = self.SelectedField == 0

        self.DurationNumber.Update()
        self.DurationNumber.IsActive = self.SelectedField == 1

        # -- Update the Track Data -- #
        self.TrackData[0] = self.FrequencyNumber.Value
        self.TrackData[1] = self.DurationNumber.Value

    def UpdatePitchLabel(self):
        if not self.FrequencyNumber.Value == "-----":
            try:
                NewPitchValue = pitch(self.FrequencyNumber.Value)
                if NewPitchValue == None:
                    NewPitchValue = "?"
                self.PitchLabel = NewPitchValue
            except:
                self.PitchLabel = "?"

    def EventUpdate(self, event):
        if not self.Active:
            return

        if self.SelectedField == 0:
            self.FrequencyNumber.EventUpdate(event)
            self.UpdatePitchLabel()

        elif self.SelectedField == 1:
            self.DurationNumber.EventUpdate(event)

        if event.type == pygame.KEYUP:
            self.SurfaceUpdateTrigger = True
            if event.key == pygame.K_PAGEDOWN:
                self.SelectedField -= 1

                if self.SelectedField <= 0:
                    self.SelectedField = 0

            if event.key == pygame.K_PAGEUP:
                self.SelectedField += 1

                if self.SelectedField >= self.MaxFields:
                    self.SelectedField = self.MaxFields

            if self.SelectedField == 0:
                # -- Higher -- #
                if event.key == pygame.K_HOME:
                    if not self.FrequencyNumber.Value == "-----":
                        CurrentValue = int(self.FrequencyNumber.Value)
                        Result = CurrentValue * 2

                        if Result >= 99999:
                            Result = 0

                        self.FrequencyNumber.Value = str(Result).zfill(5)
                        self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)

                # -- Lower -- #
                if event.key == pygame.K_END:
                    if not self.FrequencyNumber.Value == "-----":
                        CurrentValue = int(self.FrequencyNumber.Value)
                        Result = int(CurrentValue / 2)

                        if Result <= 0:
                            Result = 0

                        self.FrequencyNumber.Value = str(Result).zfill(5)
                        self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)

                # -- Note C -- #
                if event.key == pygame.K_z:
                    self.FrequencyNumber.Value = str(GetNote("C", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note C# -- #
                if event.key == pygame.K_s:
                    self.FrequencyNumber.Value = str(GetNote("C#", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note D -- #
                if event.key == pygame.K_x:
                    self.FrequencyNumber.Value = str(GetNote("D", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note D# -- #
                if event.key == pygame.K_d:
                    self.FrequencyNumber.Value = str(GetNote("D#", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note E -- #
                if event.key == pygame.K_c:
                    self.FrequencyNumber.Value = str(GetNote("E", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note F -- #
                if event.key == pygame.K_v:
                    self.FrequencyNumber.Value = str(GetNote("F", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note F# -- #
                if event.key == pygame.K_g:
                    self.FrequencyNumber.Value = str(GetNote("F#", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note G -- #
                if event.key == pygame.K_b:
                    self.FrequencyNumber.Value = str(GetNote("G", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note G# -- #
                if event.key == pygame.K_h:
                    self.FrequencyNumber.Value = str(GetNote("G#", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note A -- #
                if event.key == pygame.K_n:
                    self.FrequencyNumber.Value = str(GetNote("A", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note A# -- #
                if event.key == pygame.K_j:
                    self.FrequencyNumber.Value = str(GetNote("A#", var.Editor_CurrentOctave))

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Note B -- #
                if event.key == pygame.K_m:
                    self.FrequencyNumber.Value = str(GetNote("B", var.Editor_CurrentOctave))  # The most satanic line

                    self.FrequencyNumber.SplitedAlgarims.clear()
                    self.FrequencyNumber.SplitedAlgarims = list(self.FrequencyNumber.Value)
                    self.UpdatePitchLabel()

                # -- Increase Octave -- #
                if event.key == pygame.K_w:
                    var.Editor_CurrentOctave += 1

                    if var.Editor_CurrentOctave > 7:
                        var.Editor_CurrentOctave = 0

                # -- Decrease Octave -- #
                if event.key == pygame.K_q:
                    var.Editor_CurrentOctave -= 1

                    if var.Editor_CurrentOctave < 0:
                        var.Editor_CurrentOctave = 7

def GetNote(NoteName, Octave):
    # -- Note C
    if NoteName == "C" and Octave == 1:
        return "00032"
    elif NoteName == "C" and Octave == 2:
        return "00065"
    elif NoteName == "C" and Octave == 3:
        return "00130"
    elif NoteName == "C" and Octave == 4:
        return "00261"
    elif NoteName == "C" and Octave == 5:
        return "00523"
    elif NoteName == "C" and Octave == 6:
        return "01046"
    elif NoteName == "C" and Octave == 7:
        return "02093"
    elif NoteName == "C" and Octave == 8:
        return "04186"

    # -- Note C#

    elif NoteName == "C#" and Octave == 1:
        return "00034"
    elif NoteName == "C#" and Octave == 2:
        return "00069"
    elif NoteName == "C#" and Octave == 3:
        return "00138"
    elif NoteName == "C#" and Octave == 4:
        return "00277"
    elif NoteName == "C#" and Octave == 5:
        return "00554"
    elif NoteName == "C#" and Octave == 6:
        return "01108"
    elif NoteName == "C#" and Octave == 7:
        return "02217"
    elif NoteName == "C#" and Octave == 8:
        return "04434"

    # -- Note D

    elif NoteName == "D" and Octave == 1:
        return "00036"
    elif NoteName == "D" and Octave == 2:
        return "00073"
    elif NoteName == "D" and Octave == 3:
        return "00146"
    elif NoteName == "D" and Octave == 4:
        return "00293"
    elif NoteName == "D" and Octave == 5:
        return "00587"
    elif NoteName == "D" and Octave == 6:
        return "01174"
    elif NoteName == "D" and Octave == 7:
        return "02349"
    elif NoteName == "D" and Octave == 8:
        return "04698"

    # -- Note D#

    elif NoteName == "D#" and Octave == 1:
        return "00038"
    elif NoteName == "D#" and Octave == 2:
        return "00077"
    elif NoteName == "D#" and Octave == 3:
        return "00155"
    elif NoteName == "D#" and Octave == 4:
        return "00311"
    elif NoteName == "D#" and Octave == 5:
        return "00622"
    elif NoteName == "D#" and Octave == 6:
        return "01244"
    elif NoteName == "D#" and Octave == 7:
        return "02489"
    elif NoteName == "D#" and Octave == 8:
        return "04978"

    # -- Note E

    elif NoteName == "E" and Octave == 1:
        return "00041"
    elif NoteName == "E" and Octave == 2:
        return "00082"
    elif NoteName == "E" and Octave == 3:
        return "00164"
    elif NoteName == "E" and Octave == 4:
        return "00329"
    elif NoteName == "E" and Octave == 5:
        return "00659"
    elif NoteName == "E" and Octave == 6:
        return "01318"
    elif NoteName == "E" and Octave == 7:
        return "02637"
    elif NoteName == "E" and Octave == 8:
        return "05274"

    # -- Note F

    elif NoteName == "F" and Octave == 1:
        return "00043"
    elif NoteName == "F" and Octave == 2:
        return "00087"
    elif NoteName == "F" and Octave == 3:
        return "00174"
    elif NoteName == "F" and Octave == 4:
        return "00349"
    elif NoteName == "F" and Octave == 5:
        return "00698"
    elif NoteName == "F" and Octave == 6:
        return "01396"
    elif NoteName == "F" and Octave == 7:
        return "02793"
    elif NoteName == "F" and Octave == 8:
        return "05587"

    # -- Note F#

    elif NoteName == "F#" and Octave == 1:
        return "00046"
    elif NoteName == "F#" and Octave == 2:
        return "00092"
    elif NoteName == "F#" and Octave == 3:
        return "00184"
    elif NoteName == "F#" and Octave == 4:
        return "00369"
    elif NoteName == "F#" and Octave == 5:
        return "00739"
    elif NoteName == "F#" and Octave == 6:
        return "01479"
    elif NoteName == "F#" and Octave == 7:
        return "02959"
    elif NoteName == "F#" and Octave == 8:
        return "05919"

    # -- Note G

    elif NoteName == "G" and Octave == 1:
        return "00048"
    elif NoteName == "G" and Octave == 2:
        return "00097"
    elif NoteName == "G" and Octave == 3:
        return "00195"
    elif NoteName == "G" and Octave == 4:
        return "00391"
    elif NoteName == "G" and Octave == 5:
        return "00783"
    elif NoteName == "G" and Octave == 6:
        return "01567"
    elif NoteName == "G" and Octave == 7:
        return "03135"
    elif NoteName == "G" and Octave == 8:
        return "06271"

    # -- Note G#

    elif NoteName == "G#" and Octave == 1:
        return "00051"
    elif NoteName == "G#" and Octave == 2:
        return "00103"
    elif NoteName == "G#" and Octave == 3:
        return "00207"
    elif NoteName == "G#" and Octave == 4:
        return "00415"
    elif NoteName == "G#" and Octave == 5:
        return "00830"
    elif NoteName == "G#" and Octave == 6:
        return "01616"
    elif NoteName == "G#" and Octave == 7:
        return "03322"
    elif NoteName == "G#" and Octave == 8:
        return "06644"

    # -- Note A

    elif NoteName == "A" and Octave == 1:
        return "00055"
    elif NoteName == "A" and Octave == 2:
        return "00110"
    elif NoteName == "A" and Octave == 3:
        return "00220"
    elif NoteName == "A" and Octave == 4:
        return "00440"
    elif NoteName == "A" and Octave == 5:
        return "00880"
    elif NoteName == "A" and Octave == 6:
        return "01760"
    elif NoteName == "A" and Octave == 7:
        return "03520"
    elif NoteName == "A" and Octave == 8:
        return "07040"

    # -- Note A#

    elif NoteName == "A#" and Octave == 1:
        return "00058"
    elif NoteName == "A#" and Octave == 2:
        return "00116"
    elif NoteName == "A#" and Octave == 3:
        return "00233"
    elif NoteName == "A#" and Octave == 4:
        return "00466"
    elif NoteName == "A#" and Octave == 5:
        return "00932"
    elif NoteName == "A#" and Octave == 6:
        return "01864"
    elif NoteName == "A#" and Octave == 7:
        return "03729"
    elif NoteName == "A#" and Octave == 8:
        return "07458"

    # -- Note B

    elif NoteName == "B" and Octave == 1:
        return "00061"
    elif NoteName == "B" and Octave == 2:
        return "00123"
    elif NoteName == "B" and Octave == 3:
        return "00246"
    elif NoteName == "B" and Octave == 4:
        return "00493"
    elif NoteName == "B" and Octave == 5:
        return "00987"
    elif NoteName == "B" and Octave == 6:
        return "01975"
    elif NoteName == "B" and Octave == 7:
        return "03951"
    elif NoteName == "B" and Octave == 8:
        return "07902"

    return "00000"

class TrackColection:
    def __init__(self, Rectangle):
        self.Tracks = list()
        self.Scroll = 0
        self.PlayMode = False
        self.SelectedTrack = 0
        self.PlayMode_TrackDelay = 0
        self.PlayMode_CurrentTonePlayed = False
        self.PlayMode_LastSoundChannel = -1
        self.Rectangle = pygame.Rect(Rectangle[0], Rectangle[1], Rectangle[2], Rectangle[3])
        self.Active = False
        self.ScreenSize = (0, 0)
        self.ID = 0
        self.UpdatePatternsCache = False

        for _ in range(var.Rows):
            self.AddBlankTrack()

        self.UpdateTracksPos()

    def UpdateTracksPos(self):
        for track in self.Tracks:
            track.Rectangle[0] = self.Rectangle[0]

    def AddBlankTrack(self):
        self.Tracks.append(TrackBlock(("00000", "00100")))

    def GenerateCache(self):
        for i, track in enumerate(self.Tracks):
            print(i)
            Frequency = int(track.TrackData[0])
            Duration = int(track.TrackData[1])

            ContentManager.GetTune_FromTuneCache(Frequency, Duration, 44000)

    def Draw(self, DISPLAY):
        self.ScreenSize = (DISPLAY.get_width(), DISPLAY.get_height())

        for track in self.Tracks:
            # -- Set the Track Scroll -- #
            if track.Instance == self.SelectedTrack:
                # -- Set the Track Scroll -- #
                self.Scroll = self.Rectangle[3] / 2 - track.Rectangle[3] - track.Rectangle[1]

            # -- Render the Track Pointer -- #
            if track.Instance == self.SelectedTrack and self.Active or track.Instance == self.SelectedTrack and var.PlayMode:
                shape.Shape_Rectangle(DISPLAY, TrackPointerColor, (self.Rectangle[0] - 8, self.Scroll + track.Rectangle[1], 4, track.Rectangle[3]))

            if self.Scroll + track.Rectangle[1] >= DISPLAY.get_height() + track.TextHeight or self.Scroll + track.Rectangle[1] <= -track.TextHeight:
                continue

            if track.Instance % max(1, var.Highlight) == 0:
                track.Highlight = 1

            if track.Instance % max(1, var.HighlightSecond) == 0:
                track.Highlight = 2

            if not track.Instance % max(1, var.HighlightSecond) == 0 and not track.Instance % max(1, var.Highlight) == 0:
                track.Highlight = 0

            track.Render(DISPLAY)

    def Update(self):
        for i, track in enumerate(self.Tracks):
            track.Scroll = self.Scroll
            track.Instance = i

            track.Rectangle[0] = self.Rectangle[0]

            track.Active = track.Instance == self.SelectedTrack

            if not self.Active and not self.PlayMode:
                track.Active = False

            track.Update()

        # -- Alingh the Track Number -- #
        if len(self.Tracks) > var.Rows:
            self.Tracks.pop()
            self.SelectedTrack = 0
            var.SelectedTrack = 0
            self.UpdatePatternsCache = True
            var.PatternIsUpdating = True

            if not "APTN_T_GT".format(self.ID) in var.PatternUpdateEntry:
                var.PatternUpdateEntry.append("APTN_T_GT")

        if len(self.Tracks) < var.Rows:
            self.AddBlankTrack()
            self.UpdatePatternsCache = True
            self.SelectedTrack = 0
            var.SelectedTrack = 0
            var.PatternIsUpdating = True

            if not "APTN_T_LT" in var.PatternUpdateEntry:
                var.PatternUpdateEntry.append("APTN_T_LT")

            for block in self.Tracks:
                block.Active = True

        if not len(self.Tracks) < var.Rows and not len(self.Tracks) > var.Rows:
            if "APTN_T_GT" in var.PatternUpdateEntry:
                var.PatternUpdateEntry.remove("APTN_T_GT")

            if "APTN_T_LT" in var.PatternUpdateEntry:
                var.PatternUpdateEntry.remove("APTN_T_LT")

        # -- Update the Rectangle -- #
        self.Rectangle = pygame.Rect(self.Rectangle[0], self.Rectangle[1], self.Tracks[self.SelectedTrack].Rectangle[2], self.Rectangle[3])

        var.PlayMode = self.PlayMode

        if self.PlayMode:
            self.PlayMode_TrackDelay += 1
            CurrentTrackObj = self.Tracks[self.SelectedTrack]
            BMP = 1000 / max(1, var.BPM)

            if self.PlayMode_TrackDelay >= BMP:
                self.SelectedTrack += 1
                self.PlayMode_TrackDelay = 0

                # -- Play Command -- #
                if CurrentTrackObj.TrackData[0] == "-----":
                    # -- StopSoundChannels Command -- #
                    if "-----" in CurrentTrackObj.TrackData[1]:
                        ContentManager.StopAllChannels()

                    # -- Fade Command -- #
                    elif CurrentTrackObj.TrackData[1].startswith("F"):
                        SplitedAgrs = list(CurrentTrackObj.TrackData[1])
                        FadeTime = ""

                        for i, arg in enumerate(SplitedAgrs):
                            if i > 1:
                                FadeTime += arg
                        FadeTime = int(FadeTime.replace("-", ""))

                        ContentManager.FadeoutSound(self.PlayMode_LastSoundChannel, FadeTime)

                    # -- Pattern Jump Command -- #
                    elif CurrentTrackObj.TrackData[1].startswith("J"):
                        SplitedAgrs = list(CurrentTrackObj.TrackData[1])
                        JmpTrackID = ""

                        for i, arg in enumerate(SplitedAgrs):
                            if i > 1:
                                JmpTrackID += arg
                        JmpTrackID = int(JmpTrackID.replace("-", ""))

                        Editor.track_list.PatternJump(JmpTrackID)
                        self.EndPlayMode()

                    # -- END Command -- #
                    elif CurrentTrackObj.TrackData[1].startswith("END"):
                        self.EndPlayMode()

                else:  # -- If not, Play Note -- #
                    SoundDuration = 0
                    SoundTune = 0

                    # -- Convert the Time to the Correct Time -- #
                    try:
                        FirstDigits = CurrentTrackObj.TrackData[1][:2]
                        SecoundDigits = CurrentTrackObj.TrackData[1][2:]

                        SoundDuration = float("{0}.{1}".format(FirstDigits, SecoundDigits))
                    except ValueError:
                        pass

                    try:
                        SoundTune = int(CurrentTrackObj.TrackData[0])
                    except ValueError:
                        pass

                    # -- If not SoundTune is null, Play the Tune -- #
                    Volume = 1.0 / len(Editor.track_list.PatternList[Editor.track_list.CurrentPatternID].Tracks)
                    CurrentPlayID = ContentManager.PlayTune(SoundTune, SoundDuration, Volume=Volume)

                    if not CurrentPlayID is None:
                        self.PlayMode_LastSoundChannel = CurrentPlayID

                # -- Stop Playing song when it reach the end -- #
                if self.SelectedTrack >= len(self.Tracks):
                    self.EndPlayMode()
        else:
            self.SelectedTrack = var.SelectedTrack

    def EndPlayMode(self):
        self.SelectedTrack = 0
        self.PlayMode = False
        self.PlayMode_TrackDelay = 0
        self.PlayMode_CurrentTonePlayed = False
        self.Scroll = 25
        self.PlayMode_LastSoundChannel = -1
        var.PlayMode = False

    def EventUpdate(self, event):
        if self.Active:
            for track in self.Tracks:
                track.EventUpdate(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not self.PlayMode:
                    self.PlayMode = True
                    self.PlayMode_TrackDelay = 0
                    self.PlayMode_CurrentTonePlayed = False
                    self.SelectedTrack = 0
                    var.GenerateSoundCache = True
                    var.PlayMode = True
                    ContentManager.StopAllChannels()

                else:
                    self.PlayMode = False
                    self.PlayMode_TrackDelay = 0
                    self.PlayMode_CurrentTonePlayed = False
                    var.PlayMode = False
                    ContentManager.StopAllChannels()

            # -- Disable Edit Controls when in Play Mode -- #
            if not self.PlayMode and self.Active:
                if event.key == pygame.K_DOWN:
                    self.SelectedTrack += 1
                    if self.SelectedTrack >= len(self.Tracks):
                        self.SelectedTrack = 0
                    var.SelectedTrack = self.SelectedTrack

                if event.key == pygame.K_UP:
                    if self.SelectedTrack <= 0:
                        self.SelectedTrack = len(self.Tracks)

                    self.SelectedTrack -= 1
                    var.SelectedTrack = self.SelectedTrack

                if event.key == pygame.K_F1:
                    if len(self.Tracks) > 1:
                        self.Tracks[self.SelectedTrack] = TrackBlock(("00000", "00100"))

                if event.key == pygame.K_F2:
                    if len(self.Tracks) < 24:
                        self.AddBlankTrack()


class Pattern:
    def __init__(self, PatternID, Rectangle):
        self.PatternID = PatternID
        self.Tracks = list()
        self.ActiveTrackID = 0
        self.MusicProperties = list()
        self.Rectangle = Rectangle

        for _ in range(4):
            self.AddBlankTrack()

        for i, track in enumerate(self.Tracks):
            # -- Update Tracks Position -- #
            if i == 0:
                track.Rectangle[0] = 5
            else:
                track.Rectangle[0] = self.Tracks[i - 1].Rectangle[0] + self.Tracks[i - 1].Rectangle[2]


    def AddBlankTrack(self):
        self.Tracks.append(TrackColection(self.Rectangle))

    def PlayAllTracks(self):
        for i, track in enumerate(self.Tracks):
            track.PlayMode = True
            track.SelectedTrack = 0

    def Draw(self, DISPLAY):
        for track in self.Tracks:
            track.Draw(DISPLAY)

    def Update(self):
        for i, track in enumerate(self.Tracks):
            track.Update()

            track.Active = i == self.ActiveTrackID

            # -- Update Tracks Position -- #
            if i == 0:
                track.Rectangle[0] = 10
            else:
                track.Rectangle[0] = self.Tracks[i - 1].Rectangle[0] + self.Tracks[i - 1].Rectangle[2] + 10

        # -- Alingh the Patterns Number -- #
        if len(self.Tracks) > var.Patterns:
            self.Tracks.pop()
            self.ActiveTrackID = 0
            var.PatternIsUpdating = True

            if not "APN_GT" in var.PatternUpdateEntry:
                var.PatternUpdateEntry.append("APN_GT")

        if len(self.Tracks) < var.Patterns:
            self.ActiveTrackID = 0
            self.AddBlankTrack()
            var.PatternIsUpdating = True

            if not "APN_LT" in var.PatternUpdateEntry:
                var.PatternUpdateEntry.append("APN_LT")

        if not len(self.Tracks) < var.Patterns and not len(self.Tracks) > var.Patterns:
            var.PatternIsBeingUpdated = False

            if "APN_GT" in var.PatternUpdateEntry:
                Index1 = var.PatternUpdateEntry.index("APN_GT")
                var.PatternUpdateEntry.pop(Index1)

            if "APN_LT" in var.PatternUpdateEntry:
                Index2 = var.PatternUpdateEntry.index("APN_LT")
                var.PatternUpdateEntry.pop(Index2)

    def EventUpdate(self, event):
        for track in self.Tracks:
            track.EventUpdate(event)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F9:
                self.ActiveTrackID -= 1

                if self.ActiveTrackID <= -1:
                    self.ActiveTrackID = len(self.Tracks) - 1

            if event.key == pygame.K_F10:
                self.ActiveTrackID += 1

                if self.ActiveTrackID >= len(self.Tracks):
                    self.ActiveTrackID = 0


class TrackList:
    def __init__(self):
        self.Rectangle = pygame.Rect(5, 120, 300, 400)
        self.CurrentPatternID = 0
        self.PatternList = list()
        self.CurrentPattern = None
        self.TracksSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))
        self.LastRect = pygame.Rect(0, 0, 0, 0)
        self.Active = False
        self.AddNewPattern()

    def AddNewPattern(self):
        NewPatternID = len(self.PatternList)
        self.PatternList.append(Pattern(len(self.PatternList), pygame.Rect(5, 120, 300, 400)))

        self.SetCurrentPattern_ByID(NewPatternID)

    def SetCurrentPattern_ByID(self, PatternID):
        self.CurrentPattern = self.PatternList[PatternID]

    def PatternJump(self, PatternID):
        # -- Ensure that all tracks has been stopped before jumping -- #
        for patternCol in self.CurrentPattern.Tracks:
            patternCol.EndPlayMode()

        if PatternID < len(self.PatternList):
            self.CurrentPattern = self.PatternList[PatternID]
            self.PatternList[PatternID].PlayAllTracks()

    def Render(self, DISPLAY):
        self.TracksSurface.fill(BackgroundColor)
        self.CurrentPattern.Draw(self.TracksSurface)

        # -- Render the Pattern Name -- #
        PatternName_BackgroundColor = TrackSelectedPattern_BackgroundColor
        PatternName_FontColor = TrackSelectedPattern_FontColor
        SelectedPatternText = "Pattern: {0}/{1}".format(self.CurrentPatternID, len(self.PatternList) - 1)

        if var.PlayMode:
            PatternName_BackgroundColor = TrackSelectedPattern_PlayMode_BackgroundColor
            PatternName_FontColor = TrackSelectedPattern_PlayMode_FontColor

        shape.Shape_Rectangle(self.TracksSurface, PatternName_BackgroundColor, (0, 0, DISPLAY.get_width(), 18))
        ContentManager.FontRender(self.TracksSurface, "/PressStart2P.ttf", 12, SelectedPatternText, PatternName_FontColor, 5, 4)

        DISPLAY.blit(self.TracksSurface, (self.Rectangle[0], self.Rectangle[1]))

    def Update(self):
        self.Active = self.Rectangle.collidepoint(pygame.mouse.get_pos())

        if not self.Active:
            self.CurrentPattern.Active = False

        self.CurrentPatternID = self.CurrentPattern.PatternID
        if self.CurrentPatternID == 0:  # -- Save Music Properties only on the first pattern -- #
            self.CurrentPattern.MusicProperties.clear()
            self.CurrentPattern.MusicProperties.append(var.BPM)  # -- Save BPM Data -- #
            self.CurrentPattern.MusicProperties.append(var.Rows)  # -- Save Rows Data -- #
            self.CurrentPattern.MusicProperties.append(var.Highlight)  # -- Save Highlight Data -- #
            self.CurrentPattern.MusicProperties.append(var.HighlightSecond)  # -- Save Highlight Data -- #
            self.CurrentPattern.MusicProperties.append(var.Patterns)  # -- Save Pattern Data -- #

        # -- Update the Current Pattern -- #
        self.CurrentPattern.Update()

        # -- Pattern Update Routine -- #
        if len(var.PatternUpdateEntry) >= 1:
            for pattern in self.PatternList:
                pattern.Update()
                for block in pattern.Tracks:
                    block.Active = True

        else:
            if var.PatternIsUpdating:
                var.PatternIsUpdating = False
                var.GenerateSoundCache = True
                var.GenerateSoundCache_MessageSeen = False

                for pattern in self.PatternList:
                    pattern.Update()
                    for block in pattern.Tracks:
                        block.Active = True


        # -- Update the Surface Size -- #
        if not self.LastRect == self.Rectangle:
            self.TracksSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
            self.LastRect = self.Rectangle

        # -- Generate Sound Cache -- #
        if var.GenerateSoundCache and var.GenerateSoundCache_MessageSeen:
            print("Generating SoundCache...")
            for patterns in self.PatternList:
                for track in patterns.Tracks:
                    for collactions in track.Tracks:
                        try:
                            collactions.SurfaceUpdateTrigger = True
                            collactions.Active = True

                            if not collactions.TrackData[0] == "-----":
                                Freqn = int(collactions.TrackData[0])

                                FirstDigits = collactions.TrackData[1][:2]
                                SecoundDigits = collactions.TrackData[1][2:]

                                SoundDuration = float("{0}.{1}".format(FirstDigits, SecoundDigits))

                                ContentManager.GetTune_FromTuneCache(Freqn, SoundDuration, 44000)
                        except ValueError:
                            continue

            var.GenerateSoundCache = False
            var.GenerateSoundCache_MessageSeen = False
            print("SoundCache Generated sucefully.")

    def EventUpdate(self, event):
        if self.Rectangle.collidepoint(pygame.mouse.get_pos()):
            self.CurrentPattern.EventUpdate(event)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F3:
                    if len(self.PatternList) < 256:
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
        self.ButtonState = 0  # 0 - INACTIVE, 1 - DOWN, 2 - UP
        self.FontFile = "/PressStart2P.ttf"
        self.IsButtonEnabled = True
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1], ContentManager.GetFont_width(self.FontFile, self.TextSize, self.ButtonText) + 5, ContentManager.GetFont_height(self.FontFile, self.TextSize, self.ButtonText) + 6)
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
        self.Rectangle = pygame.Rect(self.Rectangle[0], self.Rectangle[1], ContentManager.GetFont_width(self.FontFile, self.TextSize, self.ButtonText) + 5, ContentManager.GetFont_height(self.FontFile, self.TextSize, self.ButtonText) + 6)

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
        ContentManager.FontRender(self.Surface, self.FontFile, self.TextSize, self.ButtonText, (200, 200, 200), 3, 3)

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
            ContentManager.ImageRender(self.WindowSurface, "/window/resize.png", self.WindowRectangle[2] - 12, self.WindowRectangle[3], self.ResizeRectangle[2], self.ResizeRectangle[3], True)

        # -- Draw the window title -- #
        fx.BlurredRectangle(self.WindowSurface, (0, 0, self.TitleBarRectangle[2], self.TitleBarRectangle[3] + 2), 5, 100, (100, 100, 100))
        ContentManager.FontRender(self.WindowSurface, "/Ubuntu_Thin.ttf", 20, self.Title, (250, 250, 255), self.TitleBarRectangle[2] / 2 - ContentManager.GetFont_width("/Ubuntu_Thin.ttf", 20, self.Title) / 2, -1)

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

            if self.WindowRectangle[3] >= self.Window_MinimunH:  # <- Resize the Window
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

    def Render(self, DISPLAY):
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

            if self.LastItemClicked == itemNam:  # -- When the Item is Selected
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
            ContentManager.FontRender(self.ListSurface, "/Ubuntu_Bold.ttf", 14, itemNam, ItemNameFontColor, TextsX + ItemRect[0], ItemRect[1] + 5)

            # -- Render Item Description -- #
            ContentManager.FontRender(self.ListSurface, "/Ubuntu.ttf", 12, self.ItemsDescription[i], ItemNameFontColor, TextsX + ItemRect[0], ItemRect[1] + 25)

            # -- Render the Item Sprite -- #
            if self.ItemSprite[i] != "null":
                ContentManager.ImageRender(self.ListSurface, self.ItemSprite[i], ItemRect[0] + 4, ItemRect[1] + 4, 36, 32)

        # -- Blit All Work to Screen -- #
        DISPLAY.blit(self.ListSurface, (self.Rectangle[0], self.Rectangle[1]))

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

    def AddItem(self, ItemName, ItemDescription, ItemSprite="null"):
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


class InputBox:
    def __init__(self, x, y, w, h, text='LO', FontSize=12):
        self.rect = pygame.Rect(x, y, w, h)
        self.colisionRect = pygame.Rect(x, y, w, h)
        self.color = InputBox_COLOR_ACTIVE
        self.text = text
        self.active = False
        self.DefaultText = text
        self.LastHeight = 1
        self.CustomWidth = False
        self.width = 1
        self.FontSize = FontSize
        self.CharacterLimit = 0
        self.ColisionOffsetX = 0
        self.ColisionOffsetY = 0

    def Set_X(self, Value):
        if not self.rect[0] == Value:
            self.rect = pygame.Rect(Value, self.rect[1], self.rect[2], self.rect[3])

    def Set_Y(self, Value):
        if not self.rect[1] == Value:
            self.rect = pygame.Rect(self.rect[0], Value, self.rect[2], self.rect[3])

    def Update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.colisionRect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = InputBox_COLOR_ACTIVE if self.active else InputBox_COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                    else:
                        self.text = self.DefaultText

                else:
                    if not self.CharacterLimit == 0:
                        if len(self.text) < self.CharacterLimit:
                            self.text += event.unicode
                    else:
                        self.text += event.unicode

    def Render(self, screen):
        # -- Resize the Textbox -- #
        try:
            if not self.CustomWidth:
                self.width = max(100, ContentManager.GetFont_width(InputBox_FontFile, self.FontSize, self.text) + 10)
            self.rect[2] = self.width
            self.rect[3] = ContentManager.GetFont_height(InputBox_FontFile, self.FontSize, self.text)
            self.LastHeight = self.rect[3]
        except:
            if not self.CustomWidth:
                self.rect[2] = 100
            self.rect[3] = self.LastHeight

        self.colisionRect = pygame.Rect(self.rect[0] + self.ColisionOffsetX, self.rect[1] + self.ColisionOffsetY, self.rect[2], self.rect[3])

        # Blit the rect.
        shape.Shape_Rectangle(screen, (15, 15, 15), self.rect)

        if self.text == self.DefaultText:
            ContentManager.FontRender(screen, InputBox_FontFile, self.FontSize, self.text, (140, 140, 140), self.rect[0], self.rect[1])
        else:
            if not self.text == "":
                ContentManager.FontRender(screen, InputBox_FontFile, self.FontSize, self.text, (240, 240, 240), self.rect[0], self.rect[1])

        if not self.active:
            shape.Shape_Rectangle(screen, (255, 51, 102), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))
        else:
            shape.Shape_Rectangle(screen, (46, 196, 182), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))
