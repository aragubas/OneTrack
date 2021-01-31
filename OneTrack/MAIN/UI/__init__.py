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
from System import Core
from OneTrack import MAIN as Main
from OneTrack.MAIN.Screens import Editor
from OneTrack.MAIN.UI import Widget as Widget
from OneTrack.MAIN.Screens.Editor import InstanceVar as var
import Library.CorePrimitives as Shape
import Library.CoreEffects as Fx
import Library.CorePaths as AppData
import Library.CoreUtils as Utils
from System.Core import CntMng
from math import log2, pow


#region Theme Manager
ThemesList_Properties = list()
ThemesList_PropertyNames = list()

def ThemesManager_LoadTheme(ThemeName):
    global ThemesList_Properties
    global ThemesList_PropertyNames

    ThemesList_Properties.clear()
    ThemesList_PropertyNames.clear()

    print("OneTrackUI : Loading UI Theme '" + ThemeName + "'")
    for key in var.DefaultContent.Get_RegKey("/theme/{0}".format(ThemeName)).splitlines():
        if key.startswith("#"):
            continue

        if len(key) < 3:
            continue

        ThemeDataTag = key.split(";")[0]
        ThemeDataType = key.split(";")[1]
        ThemeData = key.split(";")[2]
        ThemeRawData = None

        if ThemeDataType == "tuple":
            ThemeRawData = Utils.Convert.Parse_Tuple(ThemeData)

        if ThemeDataType == "int":
            ThemeRawData = int(ThemeData)

        if ThemeDataType == "str":
            ThemeRawData = str(ThemeData)

        print("Property: '{0}' of type '{1}' loaded with value '{2}'".format(ThemeDataTag, ThemeDataType, ThemeData))

        ThemesManager_AddProperty(ThemeDataTag, ThemeRawData)

    print("OneTrack : Theme Loaded sucefully")

def ThemesManager_GetProperty(pPropertyName):
    Index = ThemesList_PropertyNames.index(pPropertyName)

    return ThemesList_Properties[Index]

def ThemesManager_AddProperty(PropertyName, PropertyValue):
    ThemesList_Properties.append(PropertyValue)
    ThemesList_PropertyNames.append(PropertyName)

#endregion

ContentManager = CntMng.ContentManager

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
        self.Rectangle = Utils.Convert.List_PygameRect(Rectangle)
        self.Value = Value
        self.InactiveColor = False
        self.SelectedCharIndex = 0
        self.SplitedAlgarims = list(self.Value)
        self.IsActive = True
        self.Color = (155, 155, 155)
        self.AlgarimsWidth = 0
        self.AllowNotNumbers = False
        self.YOffset = 0
        self.FontSize = FontSize

    def SetValueInString(self, NewValue):
        self.Value = NewValue
        self.SplitedAlgarims = list(self.Value)

    def Render(self, DISPLAY):
        for i, Algarims in enumerate(self.SplitedAlgarims):
            if self.IsActive:
                if i == self.SelectedCharIndex:
                    self.Color = ThemesManager_GetProperty("EditableNumberView_ColorSelected")

                else:
                    self.Color = ThemesManager_GetProperty("EditableNumberView_ColorActive")

            else:
                self.Color = ThemesManager_GetProperty("EditableNumberView_ColorDeactive")

            if self.InactiveColor:
                self.Color = ThemesManager_GetProperty("EditableNumberView_ColorDeactive")

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


def pitch(pFreq):
    if pFreq == "00000":
        return "?"
    freq = int(pFreq)
    Path = "/note_by_pitch/{0}".format(str(freq))

    try:
        ReadVal = ContentManager.Get_RegKey(Path)

    except ValueError:
        ReadVal = "?"

    return ReadVal

class TrackBlock:
    def __init__(self, TrackData):
        self.TrackData = list(TrackData)
        self.Instance = -1
        self.TextWidth = ContentManager.GetFont_width("/PressStart2P.ttf", 12, var.DefaultContent.Get_RegKey("/default/pitch_value"))
        self.TextHeight = ContentManager.GetFont_height("/PressStart2P.ttf", 12, var.DefaultContent.Get_RegKey("/default/pitch_value"))
        self.Scroll = 0
        self.Rectangle = pygame.Rect(5, self.Scroll + (self.TextHeight + 10) * self.Instance, ContentManager.GetFont_width("/PressStart2P.ttf", 12, var.DefaultContent.Get_RegKey("/default/pitch_value")) * 2 + 5, ContentManager.GetFont_height("/PressStart2P.ttf", 12, var.DefaultContent.Get_RegKey("/default/pitch_value")) + 2)
        self.LastRect = self.Rectangle
        self.FrequencyNumber = EditableNumberView(pygame.Rect(10, 2, self.TextWidth, self.TextHeight), str(self.TrackData[0]), 10)
        self.DurationNumber = EditableNumberView(pygame.Rect(self.FrequencyNumber.Rectangle[0], 2, self.TextWidth, self.TextHeight), str(self.TrackData[1]), 10)
        self.DurationNumber.AllowNotNumbers = True
        self.Active = True
        self.SelectedField = 0
        self.MaxFields = 1
        self.Highlight = 0
        self.RootActivated = False
        self.HighlightUpdated = False

        TrackPitch = TrackData[0]
        if TrackPitch == "-----":
            TrackPitch = var.DefaultContent.Get_RegKey("/default/pitch_value")
        self.PitchLabel = pitch(TrackPitch)

        self.ResetSurface()
        self.SurfaceUpdateTrigger = True
        self.DisabledTrigger = True
        self.ReRender()
        self.NoteLabelWidth = ContentManager.GetFont_width("/PressStart2P.ttf", 10, "0000")

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
        if self.Active and self.RootActivated:
            FrequencyBGColor = ThemesManager_GetProperty("TrackBlock_FrequencyBGColor_Active")
            DurationBGColor = ThemesManager_GetProperty("TrackBlock_DurationBGColor_Active")

        else:
            FrequencyBGColor = ThemesManager_GetProperty("TrackBlock_FrequencyBGColor_Deactive")
            DurationBGColor = ThemesManager_GetProperty("TrackBlock_DurationBGColor_Deactive")

        if self.Highlight == 1:
            FrequencyBGColor = ThemesManager_GetProperty("TrackBlock_FrequencyBGColor_Hightlight1")
            DurationBGColor = ThemesManager_GetProperty("TrackBlock_DurationBGColor_Hightlight1")

        elif self.Highlight == 2:
            FrequencyBGColor = ThemesManager_GetProperty("TrackBlock_FrequencyBGColor_Hightlight2")
            DurationBGColor = ThemesManager_GetProperty("TrackBlock_DurationBGColor_Hightlight2")

        if self.Active and self.RootActivated:
            FrequencyBGColor = ThemesManager_GetProperty("TrackBlock_FrequencyBGColor_Active")
            DurationBGColor = ThemesManager_GetProperty("TrackBlock_DurationBGColor_Active")

        if self.PitchLabel == "?":
            PitchLabelColor = ThemesManager_GetProperty("TrackBlock_NoteLabel_UnknowNote")
        else:
            PitchLabelColor = ThemesManager_GetProperty("TrackBlock_NoteLabel_KnowNote")

        # Update Pitch Label
        self.UpdatePitchLabel()

        # Fill the Background
        self.BlockSurface.fill(ThemesManager_GetProperty("BackgroundColor"))

        if var.DefaultContent.Get_RegKey("/options/disabled_block_color").lower() in ("true"):
            if not self.RootActivated or not self.Active:
                self.FrequencyNumber.InactiveColor = True
                self.DurationNumber.InactiveColor = True

        if self.Active and self.RootActivated:
            self.FrequencyNumber.InactiveColor = False
            self.DurationNumber.InactiveColor = False

        Shape.Shape_Rectangle(self.BlockSurface, FrequencyBGColor, (self.FrequencyNumber.Rectangle[0] - 1, self.FrequencyNumber.Rectangle[1] - 2, self.FrequencyNumber.Rectangle[2] + 1, self.FrequencyNumber.Rectangle[3] + 1), 0, 0, 5, 0, 5, 0)
        self.FrequencyNumber.Render(self.BlockSurface)

        # -- Render the Duration Region
        DurationX = (self.FrequencyNumber.Rectangle[0] + self.TextWidth)
        Shape.Shape_Rectangle(self.BlockSurface, DurationBGColor, (DurationX - 1, self.DurationNumber.Rectangle[1] - 2, self.TextWidth + 1, self.DurationNumber.Rectangle[3] + 1), 0, 0, 0, 5, 0, 5)
        self.DurationNumber.Render(self.BlockSurface)

        if not self.Active:
            LabelColor = ThemesManager_GetProperty("TrackBlock_InstanceLabelDeactiveColor")
        else:
            LabelColor = ThemesManager_GetProperty("TrackBlock_InstanceLabelActiveColor")

        if not self.RootActivated:
            LabelColor = ThemesManager_GetProperty("TrackBlock_InstanceLabelDeactiveColor")

        ContentManager.FontRender(self.BlockSurface, "/PressStart2P.ttf", 10, str(self.Instance).zfill(2), LabelColor, (DurationX + self.TextWidth) + 3, 1)

        # -- Render Note Label -- #
        ContentManager.FontRender(self.BlockSurface, "/PressStart2P.ttf", 10, self.PitchLabel, PitchLabelColor, 0, 0)

    def ResetSurface(self):
        self.BlockSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))

    def Update(self):
        if self.Active or self.SurfaceUpdateTrigger:
            self.Rectangle = pygame.Rect(self.Rectangle[0], (self.TextHeight + 10) * self.Instance, self.NoteLabelWidth + self.FrequencyNumber.Rectangle[2] + self.DurationNumber.Rectangle[2] + 25, self.Rectangle[3])

            if not self.LastRect == self.Rectangle:
                self.LastRect = self.Rectangle
                self.FrequencyNumber.Rectangle = pygame.Rect(self.NoteLabelWidth, 1, self.TextWidth, self.TextHeight)
                self.DurationNumber.Rectangle = pygame.Rect(self.FrequencyNumber.Rectangle[0] + self.FrequencyNumber.Rectangle[2] + 2, 1, self.TextWidth, self.TextHeight)

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

                # -- Get the note by pygame KeyCode -- #
                KeyPath = "/note_by_key/" + str(event.key)

                if var.DefaultContent.KeyExists(KeyPath):
                    self.FrequencyNumber.Value = str(GetNote(var.DefaultContent.Get_RegKey(KeyPath), var.Editor_CurrentOctave))

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
    Path = "/note_databank/{0}/{1}".format(NoteName, Octave)
    ReturnVal = "00000"

    try:
        ReturnVal = ContentManager.Get_RegKey(Path)

    except ValueError:
        print("OneTrack : GetNote_Error, note {0} octave {1} does not exist".format(NoteName, Octave))

    return ReturnVal

def GetWaveTypeByWaveCode(pWaveCode):
    if pWaveCode == "SQUR":
        return "square"

    if pWaveCode == "SINE":
        return "sine"

    if pWaveCode == "SQSI":
        return "sine_square"

    print("Invalid wave type: ({0})".format(pWaveCode))
    return "square"


class TrackColection:
    def __init__(self, pID, ZeroFillTracks=True):
        self.Tracks = list()
        self.Scroll = 0
        self.LastScroll = 0
        self.PlayMode = False
        self.SelectedTrack = 0
        self.PlayMode_TrackDelay = 0
        self.PlayMode_CurrentTonePlayed = False
        self.PlayMode_LastSoundChannel = -1
        self.Rectangle = pygame.Rect(5, 120, 300, 400)
        self.Active = False
        self.ScreenSize = (0, 0)
        self.ID = pID
        self.UpdatePatternsCache = False
        self.LastSineWave = "square"
        self.LastDefaultDuration = 20
        self.LastVolume = 1.0
        self.TargetScroll = 0
        self.LastScrollValue = 0
        self.ScrollAnimationScale = 5
        self.UpdateTrigger = False
        self.TargetTrackpointerHeight = 0
        self.TrackpointerHeight = 0

        if ZeroFillTracks:
            for _ in range(var.Rows):
                self.AddBlankTrack()

            self.UpdateTracksPos()

    def AddBlock(self, pBlockObject):
        self.Tracks.append(pBlockObject)
        self.UpdateTracksPos()

    def UpdateTracksPos(self):
        for track in self.Tracks:
            track.Rectangle[0] = self.Rectangle[0]

    def AddBlankTrack(self):
        self.Tracks.append(TrackBlock((var.ProcessReference.DefaultContents.Get_RegKey("/default/pitch_value").zfill(5), var.ProcessReference.DefaultContents.Get_RegKey("/default/note_duration").zfill(5))))

    def GenerateCache(self):
        for i, track in enumerate(self.Tracks):
            print(i)
            Frequency = int(track.TrackData[0])
            Duration = int(track.TrackData[1])
            SinewaveType = "square"

            ContentManager.GetTune_FromTuneCache(Frequency, Duration, 44000, SinewaveType)

    def UpdateTrackBlocks(self):
        print("Updating all trackblocks...")
        for block in self.Tracks:
            block.Active = True
            block.SurfaceUpdateTrigger = True
            block.RootActivated = True
            block.HighlightUpdated = False
            block.Update()
            block.ReRender()
            block.ResetSurface()

    def Draw(self, DISPLAY):
        self.ScreenSize = (DISPLAY.get_width(), DISPLAY.get_height())

        for track in self.Tracks:
            # -- Set the Track Scroll -- #
            if track.Active:
                # -- Set the Track Scroll -- #
                if not var.PlayMode:
                    if var.DefaultContent.Get_RegKey("/options/per_track_scroll").lower() == "true":
                        if self.Active:
                            self.UpdateTrackScroll(track)
                    else:
                        self.UpdateTrackScroll(track)

                else:
                    self.UpdateTrackScroll(track)

            # -- Render the Track Pointer -- #
            if self.Active and track.Instance == self.SelectedTrack and not var.PlayMode:
                if var.DefaultContent.Get_RegKey("/options/trackpointer_animation").lower() in ("true"):
                    self.TargetTrackpointerHeight = track.Rectangle[3] - (abs(self.Scroll - self.TargetScroll) / self.ScrollAnimationScale)

                    if self.TrackpointerHeight > self.TargetTrackpointerHeight:
                        self.TrackpointerHeight -= abs(self.TrackpointerHeight - self.TargetTrackpointerHeight) / self.ScrollAnimationScale

                    if self.TrackpointerHeight < self.TargetTrackpointerHeight:
                        self.TrackpointerHeight += abs(self.TrackpointerHeight - self.TargetTrackpointerHeight) / self.ScrollAnimationScale
                else:
                    self.TrackpointerHeight = track.Rectangle[3]

                # Render Trackpointer
                if var.DefaultContent.Get_RegKey("/options/block_trackpointer").lower() == "true":
                    var.DefaultContent.ImageRender(DISPLAY, "/pointer.png", self.Rectangle[0] - 12, self.Scroll + track.Rectangle[1], max(0, self.TrackpointerHeight - 1), track.Rectangle[3], SmoothScaling=True)
                else:
                    Shape.Shape_Rectangle(DISPLAY, ThemesManager_GetProperty("TrackPointerColor"), (abs(self.Rectangle[0] - 10), abs(self.Scroll + track.Rectangle[1]), max(0, self.TrackpointerHeight - 8), abs(track.Rectangle[3])), DontUseCache=True)

            if self.Scroll + track.Rectangle[1] >= DISPLAY.get_height() + track.TextHeight or self.Scroll + track.Rectangle[1] <= -track.TextHeight:
                continue

            # Render the Track
            track.Render(DISPLAY)

    def UpdateTrackScroll(self, track):
        if var.DefaultContent.Get_RegKey("/options/smooth_scroll").lower() in ("true"):
            self.TargetScroll = self.Rectangle[3] / 2 - track.Rectangle[3] - track.Rectangle[1]

            if self.Scroll > self.TargetScroll:
                self.Scroll -= abs(self.Scroll - self.TargetScroll) / self.ScrollAnimationScale

            if self.Scroll < self.TargetScroll:
                self.Scroll += abs(self.Scroll - self.TargetScroll) / self.ScrollAnimationScale

        else:
            self.Scroll = self.Rectangle[3] / 2 - track.Rectangle[3] - track.Rectangle[1]

    def AlingRowsNumber(self):
        if self.UpdateTrigger and len(self.Tracks) == var.Rows:
            self.UpdateTrigger = False

            self.UpdateTrackBlocks()

        # If row number is higher than current rows number
        if len(self.Tracks) > var.Rows:
            self.Tracks.pop()
            self.SelectedTrack = 0
            var.SelectedTrack = 0
            self.UpdatePatternsCache = True
            var.PatternIsUpdating = True
            self.UpdateTrigger = True

        if len(self.Tracks) < var.Rows:
            self.AddBlankTrack()
            self.SelectedTrack = 0
            var.SelectedTrack = 0
            self.UpdatePatternsCache = True
            var.PatternIsUpdating = True
            self.UpdateTrigger = True

    def Update(self):
        if not self.Active:
            self.TargetTrackpointerHeight = 0
            self.TrackpointerHeight = 0

        self.ScrollAnimationScale = int(var.DefaultContent.Get_RegKey("/options/animation_scale"))

        i = -1
        for track in self.Tracks:
            i += 1
            track.Scroll = self.Scroll
            track.Instance = i
            track.RootActivated = self.Active

            if self.PlayMode:
                track.RootActivated = True

            #  Set Track Active State
            track.Active = track.Instance == self.SelectedTrack

            if var.DefaultContent.Get_RegKey("/options/per_track_scroll").lower() == "true" and not var.PlayMode:
                track.Active = track.Instance == self.SelectedTrack and self.Active

            #  Align X
            if track.Active or track.SurfaceUpdateTrigger:
                track.Rectangle[0] = self.Rectangle[0]

            #  Set Track Highlight Type
            if not track.HighlightUpdated:
                track.HighlightUpdated = True
                track.SurfaceUpdateTrigger = True
                if track.Instance % max(1, var.Highlight) == 0:
                    track.Highlight = 1

                if track.Instance % max(1, var.HighlightSecond) == 0:
                    track.Highlight = 2

                if not track.Instance % max(1, var.HighlightSecond) == 0 and not track.Instance % max(1, var.Highlight) == 0:
                    track.Highlight = 0

            #  Update Track Code
            track.Update()

        # -- Align the Rows Number -- #
        self.AlingRowsNumber()

        # -- Update the Rectangle -- #
        self.Rectangle = pygame.Rect(self.Rectangle[0], self.Rectangle[1], self.Tracks[self.SelectedTrack].Rectangle[2], self.Rectangle[3])

        var.PlayMode = self.PlayMode

        # Play Mode
        if self.PlayMode:
            self.PlayMode_TrackDelay += 1
            CurrentTrackObj = self.Tracks[self.SelectedTrack]
            # Beats per minute waiting
            BMP = 1000 / max(1, var.BPM)

            if self.PlayMode_TrackDelay >= BMP:
                self.SelectedTrack += 1
                self.PlayMode_TrackDelay = 0

                try:
                    # -- StopSoundChannels Command -- #
                    if "-----" in CurrentTrackObj.TrackData[0]:
                        ContentManager.StopAllChannels()

                    # -- Fade Command -- # F---- 4 digits
                    elif CurrentTrackObj.TrackData[1].startswith("F"):
                        FadeTime = CurrentTrackObj.TrackData[1][1:]

                        FadeTime = int(FadeTime.replace("-", ""))
                        ContentManager.FadeoutSound(self.PlayMode_LastSoundChannel, FadeTime)

                    # -- Fade All Command -- # A---- 4 digits
                    elif CurrentTrackObj.TrackData[1].startswith("A"):
                        FadeTime = CurrentTrackObj.TrackData[1][1:]

                        FadeTime = int(FadeTime.replace("-", ""))
                        ContentManager.FadeoutAllSounds(FadeTime)

                    # -- Duration Command -- # D---- 4 digits
                    elif CurrentTrackObj.TrackData[1].startswith("D"):
                        DurationTime = CurrentTrackObj.TrackData[1][1:]

                        self.LastDefaultDuration = int(DurationTime.replace("-", ""))

                    # -- Volume Command -- # V---- 4 digits
                    elif CurrentTrackObj.TrackData[1].startswith("V"):
                        Volume = CurrentTrackObj.TrackData[1][1:]

                        # THE FRICKING SOLUTION
                        VolumeValue = int(Volume.replace("-", "0"))
                        if VolumeValue <= 100 and VolumeValue >= 0:
                            VolumeValue = VolumeValue / 100
                            print("Volume value was set to: " + str(VolumeValue))

                        else:
                            VolumeValue = 1
                            print("Invalid volume value")

                        self.LastVolume = VolumeValue
                        ContentManager.SetChannelVolume(self.PlayMode_LastSoundChannel, self.LastVolume)

                    # -- Waveform Command -- # X---- 4 digits
                    elif CurrentTrackObj.TrackData[1].startswith("W"):
                        WaveformCommand = CurrentTrackObj.TrackData[1][1:]
                        # X---- 4 Digits
                        self.LastSineWave = GetWaveTypeByWaveCode(WaveformCommand)

                    # -- Pattern Jump Command -- # J---- 4 digits
                    elif CurrentTrackObj.TrackData[1].startswith("J"):
                        JmpTrackID = CurrentTrackObj.TrackData[1][1:]

                        JmpTrackID = int(JmpTrackID.replace("-", ""))

                        Editor.track_list.PatternJump(JmpTrackID)
                        self.EndPlayMode()

                    # -- END Command -- #
                    elif CurrentTrackObj.TrackData[1].startswith("END"):
                        self.EndPlayMode()
                except:
                    pass

                # Define SoundTune variable
                SoundTune = 0

                # -- Convert the Sample Time to the Correct Time -- #
                try:
                    SoundDuration = int(CurrentTrackObj.TrackData[1]) / var.BPM
                except ValueError:
                    SoundDuration = self.LastDefaultDuration / var.BPM

                # -- Get SoundTune value -- #
                try:
                    SoundTune = int(CurrentTrackObj.TrackData[0])
                except ValueError:
                    pass

                # -- If AutoBalance is enabled, override volume command -- #
                if var.ProjectSetting_AutoBalanceVolume:
                    self.LastVolume = var.Volume / var.Patterns

                # -- Play the Tune -- #
                CurrentPlayID = ContentManager.PlayTune(SoundTune, SoundDuration, Volume=self.LastVolume, FrequencyType=self.LastSineWave)

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
        self.PlayMode_LastSoundChannel = -1
        self.LastSineWave = "square"
        self.LastVolume = 1.0
        var.SoundsBeingPlayedNow = 0
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
                    self.LastSineWave = "square"
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
                        TrackBlockInQuestion = self.Tracks[self.SelectedTrack]

                        TrackBlockInQuestion.Active = True
                        TrackBlockInQuestion.FrequencyNumber.SetValueInString(ContentManager.Get_RegKey("/default/pitch_value").zfill(5))

                        TrackBlockInQuestion.Active = True
                        TrackBlockInQuestion.DurationNumber.SetValueInString(ContentManager.Get_RegKey("/default/note_duration").zfill(5))

                if event.key == pygame.K_F2:
                    if len(self.Tracks) < 24:
                        self.AddBlankTrack()


class Pattern:
    def __init__(self, PatternID, ZeroFillPatterns=True):
        self.PatternID = PatternID
        self.Tracks = list()
        self.ActiveTrackID = 0
        self.Rectangle = pygame.Rect(5, 120, 300, 400)

        if ZeroFillPatterns:
            for _ in range(var.Patterns):
                self.AddBlankTrack()

            self.UpdateTracksPosition()

    def UpdateTracksPosition(self):
        print("Updating Track Positions...")
        for i, track in enumerate(self.Tracks):
            # -- Update Tracks Position -- #
            if i == 0:
                track.Rectangle[0] = 5
            else:
                track.Rectangle[0] = self.Tracks[i - 1].Rectangle[0] + self.Tracks[i - 1].Rectangle[2]

    def UpdateTracksBlocks(self):
        for track in self.Tracks:
            track.UpdateTrackBlocks()
            track.Update()
            track.UpdateTracksPos()

    def AddBlankTrack(self):
        self.Tracks.append(TrackColection(len(self.Tracks)))

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

        # -- Align the Patterns Number -- #
        if len(self.Tracks) > var.Patterns:
            self.Tracks.pop()
            self.ActiveTrackID = 0
            var.PatternIsUpdating = True

            for track in self.Tracks:
                track.UpdateTrackBlocks()

        if len(self.Tracks) < var.Patterns:
            self.ActiveTrackID = 0
            self.AddBlankTrack()
            var.PatternIsUpdating = True

            for track in self.Tracks:
                track.UpdateTrackBlocks()

        if not len(self.Tracks) < var.Patterns and not len(self.Tracks) > var.Patterns:
            var.PatternIsBeingUpdated = False

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
        var.PatternIsUpdating = True
        NewPatternID = len(self.PatternList)

        self.PatternList.append(Pattern(len(self.PatternList)))
        self.SetCurrentPattern_ByID(NewPatternID)

    def SetCurrentPattern_ByID(self, PatternID):
        self.CurrentPattern = self.PatternList[PatternID]
        self.CurrentPatternID = self.CurrentPattern.PatternID

    def PatternJump(self, PatternID):
        # -- Ensure that all tracks has been stopped before jumping -- #
        for patternCol in self.CurrentPattern.Tracks:
            patternCol.EndPlayMode()

        if PatternID < len(self.PatternList):
            self.CurrentPattern = self.PatternList[PatternID]
            self.PatternList[PatternID].PlayAllTracks()
            self.CurrentPatternID = self.CurrentPattern.PatternID

    def Render(self, DISPLAY):
        self.TracksSurface.fill(ThemesManager_GetProperty("BackgroundColor"))
        self.CurrentPattern.Draw(self.TracksSurface)

        # -- Render the Pattern Name -- #
        PatternName_BackgroundColor = ThemesManager_GetProperty("TrackSelectedPattern_BackgroundColor")
        PatternName_FontColor = ThemesManager_GetProperty("TrackSelectedPattern_FontColor")
        SelectedPatternText = "Pattern: {0}/{1}".format(self.CurrentPatternID, len(self.PatternList) - 1)

        # Set the color for Playmode
        if var.PlayMode:
            PatternName_BackgroundColor = ThemesManager_GetProperty("TrackSelectedPattern_PlayMode_BackgroundColor")
            PatternName_FontColor = ThemesManager_GetProperty("TrackSelectedPattern_PlayMode_FontColor")

        Shape.Shape_Rectangle(self.TracksSurface, PatternName_BackgroundColor, (0, 0, DISPLAY.get_width(), 18))
        ContentManager.FontRender(self.TracksSurface, "/PressStart2P.ttf", 12, SelectedPatternText, PatternName_FontColor, 5, 4)

        DISPLAY.blit(self.TracksSurface, (self.Rectangle[0], self.Rectangle[1]))

    def Update(self):
        self.Active = self.Rectangle.collidepoint(pygame.mouse.get_pos())

        if not self.Active:
            self.CurrentPattern.Active = False

        # -- Update the Current Pattern -- #
        self.CurrentPattern.Update()

        # -- Pattern Update Routine -- #
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
            print("OneTrack : Generating SoundCache...")
            for patterns in self.PatternList:
                for track in patterns.Tracks:
                    CollectionLastSinewaveForm = "square"
                    CollectionLastDuration = 20

                    for collactions in track.Tracks:
                        try:
                            collactions.SurfaceUpdateTrigger = True
                            collactions.Active = True
                            SinewaveType = CollectionLastSinewaveForm

                            # Set the Waveform
                            if collactions.TrackData[1].startswith("W"):
                                WaveformCommand = collactions.TrackData[1][1:]
                                CollectionLastSinewaveForm = GetWaveTypeByWaveCode(WaveformCommand)

                            # Set the default duration
                            if collactions.TrackData[1].startswith("D"):
                                DurationTime = collactions.TrackData[1][1:]

                                CollectionLastDuration = int(DurationTime.replace("-", ""))

                            try:
                                Freqn = int(collactions.TrackData[0])
                            except:
                                Freqn = 0

                            try:
                                SoundDuration = int(collactions.TrackData[1]) / var.BPM
                            except:
                                SoundDuration = CollectionLastDuration / var.BPM

                            ContentManager.GetTune_FromTuneCache(Freqn, SoundDuration, 44000, SinewaveType)

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
        self.Rectangle = Utils.Convert.List_PygameRect(Rectangle)
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
        self.BackgroundColor = ThemesManager_GetProperty("Button_BackgroundColor")
        self.SurfaceUpdated = False
        self.LastRect = pygame.Rect(0, 0, 0, 0)
        self.Surface = pygame.Surface((Rectangle[2], Rectangle[3]))
        self.ColisionXOffset = 0
        self.ColisionYOffset = 0
        self.ClearState = False

    def EventUpdate(self, event):
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
                    self.ClearState = True

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

    def Update(self):
        if self.ClearState:
            self.ClearState = False
            self.ButtonState = 0

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

        self.BackgroundColor = ThemesManager_GetProperty("Button_BackgroundColor")

        if self.ButtonState == 0:
            IndicatorColor = ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

        elif self.ButtonState == 1:
            IndicatorColor = ThemesManager_GetProperty("Button_Active_IndicatorColor")

        # -- Render Background -- #
        self.Surface.fill(self.BackgroundColor)

        # -- Indicator Bar -- #
        Shape.Shape_Rectangle(self.Surface, IndicatorColor, (0, 0, self.Rectangle[2], self.Rectangle[3]), 1, 0)

        # -- Text -- #
        X = self.Rectangle[2] / 2 - ContentManager.GetFont_width(self.FontFile, self.TextSize, self.ButtonText) / 2
        Y = self.Rectangle[3] / 2 - ContentManager.GetFont_height(self.FontFile, self.TextSize, self.ButtonText) / 2

        ContentManager.FontRender(self.Surface, self.FontFile, self.TextSize, self.ButtonText, (200, 200, 200), X, Y)

        # -- Draw the Button -- #
        DISPLAY.blit(self.Surface, (self.Rectangle[0], self.Rectangle[1]))


class DropDownMenu:
    def __init__(self, pPosition, pItemsList):
        self.Position = pPosition
        self.ItemsList = pItemsList
        self.Rectangle = pygame.Rect(pPosition[0], pPosition[1], 32, 32)
        self.MenuItems = list()
        self.SelectedItem = ""
        self.SizeUpdated = False

        for i, item in enumerate(self.ItemsList):
            self.MenuItems.append(Button(pygame.Rect(self.Rectangle[0] + 5, self.Rectangle[1] + 5 * i + 32, 0, 0), item[0], 12))

    def Render(self, DISPLAY):
        DISPLAY.blit(Fx.Simple_BlurredRectangle(DISPLAY, self.Rectangle), self.Rectangle)
        Shape.Shape_Rectangle(DISPLAY, ThemesManager_GetProperty("DropDownMenu_BorderColor"), self.Rectangle, 1, 3)

        for button in self.MenuItems:
            button.Render(DISPLAY)

        self.SelectedItem = ""

    def Update(self):
        for i, button in enumerate(self.MenuItems):
            button.Rectangle[1] = self.Rectangle[1] + i * (button.Rectangle[3] + 2) + 2

            if button.ButtonState == 2:
                self.ItemsList[i][1]()

            button.Update()

        if not self.SizeUpdated:
            self.SizeUpdated = True
            self.UpdateSize()

        # Align the Position with the Rectangle
        self.Rectangle[0] = self.Position[0]
        self.Rectangle[1] = self.Position[1]

    def UpdateSize(self):
        AllButtonsWidth = 0
        AllButtonsHeight = 0

        for button in self.MenuItems:
            AllButtonsHeight += button.Rectangle[3] + 3

            if button.Rectangle[2] > AllButtonsWidth:
                AllButtonsWidth = button.Rectangle[2] + 10

        self.Rectangle[3] = AllButtonsHeight
        self.Rectangle[2] = AllButtonsWidth

    def EventUpdate(self, event):
        for item in self.MenuItems:
            item.EventUpdate(event)

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

            button.Update()

    def EventUpdate(self, event):
        for button in self.ButtonsList:
            button.EventUpdate(event)

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

            BackgroundColor = ThemesManager_GetProperty("VerticalListWithDescription_Inactive_BackgroundColor")
            ItemNameFontColor = ThemesManager_GetProperty("VerticalListWithDescription_Inactive_ItemNameFontColor")
            BorderColor = ThemesManager_GetProperty("VerticalListWithDescription_Inactive_BorderColor")
            TextsX = 5
            if self.ItemSprite[i] != "null":
                TextsX = 45

            if self.LastItemClicked == itemNam:  # -- When the Item is Selected
                BackgroundColor = ThemesManager_GetProperty("VerticalListWithDescription_Active_BackgroundColor")
                ItemNameFontColor = ThemesManager_GetProperty("VerticalListWithDescription_Active_ItemNameFontColor")
                BorderColor = ThemesManager_GetProperty("VerticalListWithDescription_Active_BorderColor")

            if self.ItemSelected[i]:  # -- When the Item is Clicked
                BackgroundColor = ThemesManager_GetProperty("VerticalListWithDescription_Selected_BackgroundColor")
                ItemNameFontColor = ThemesManager_GetProperty("VerticalListWithDescription_Selected_ItemNameFontColor")
                BorderColor = ThemesManager_GetProperty("VerticalListWithDescription_Selected_BorderColor")

            # -- Background -- #
            Shape.Shape_Rectangle(self.ListSurface, BackgroundColor, ItemRect, DontUseCache=True)

            # -- Indicator Bar -- #
            Shape.Shape_Rectangle(self.ListSurface, BorderColor, ItemRect, 1, DontUseCache=True)

            # -- Render Item Name -- #
            ContentManager.FontRender(self.ListSurface, ThemesManager_GetProperty("VerticalListWithDescription_ItemNameFont"), 14, itemNam, ItemNameFontColor, TextsX + ItemRect[0], ItemRect[1] + 5)

            # -- Render Item Description -- #
            ContentManager.FontRender(self.ListSurface, ThemesManager_GetProperty("VerticalListWithDescription_ItemDescriptionFont"), 12, self.ItemsDescription[i], ItemNameFontColor, TextsX + ItemRect[0], ItemRect[1] + 25)

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
        self.color = ThemesManager_GetProperty("InputBox_COLOR_ACTIVE")
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
            self.color = ThemesManager_GetProperty("InputBox_COLOR_ACTIVE") if self.active else ThemesManager_GetProperty("InputBox_COLOR_INACTIVE")
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
                self.width = max(100, ContentManager.GetFont_width(ThemesManager_GetProperty("InputBox_FontFile"), self.FontSize, self.text) + 10)
            self.rect[2] = self.width
            self.rect[3] = ContentManager.GetFont_height(ThemesManager_GetProperty("InputBox_FontFile"), self.FontSize, self.text)
            self.LastHeight = self.rect[3]
        except:
            if not self.CustomWidth:
                self.rect[2] = 100
            self.rect[3] = self.LastHeight

        self.colisionRect = pygame.Rect(self.rect[0] + self.ColisionOffsetX, self.rect[1] + self.ColisionOffsetY, self.rect[2], self.rect[3])

        # Blit the rect.
        Shape.Shape_Rectangle(screen, (15, 15, 15), self.rect)

        if self.text == self.DefaultText:
            ContentManager.FontRender(screen, ThemesManager_GetProperty("InputBox_FontFile"), self.FontSize, self.text, (140, 140, 140), self.rect[0], self.rect[1])
        else:
            if not self.text == "":
                ContentManager.FontRender(screen, ThemesManager_GetProperty("InputBox_FontFile"), self.FontSize, self.text, (240, 240, 240), self.rect[0], self.rect[1])

        if not self.active:
            Shape.Shape_Rectangle(screen, (255, 51, 102), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))
        else:
            Shape.Shape_Rectangle(screen, (46, 196, 182), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))
