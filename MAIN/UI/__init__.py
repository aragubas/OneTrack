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
import pygame, os, subprocess
from OneTrack import MAIN as Main
from ENGINE import shape

class EditableNumberView:
    def __init__(self, Rectangle, Value):
        self.Rectangle = Rectangle
        self.Value = Value
        self.SelectedCharIndex = 0
        self.SplitedAlgarims = list(self.Value)
        self.IsActive = True
        self.Color = (155, 155, 155)
        self.AlgarimsWidth = 0

    def Render(self, DISPLAY):

        for i, Algarims in enumerate(self.SplitedAlgarims):
            self.Color = (155, 155, 155)

            if i == self.SelectedCharIndex:
                self.Color = (255, 255, 255)

            if not self.IsActive:
                self.Color = (155, 155, 155)

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

                if self.SelectedCharIndex <= 0:
                    self.SelectedCharIndex = 0

            if event.key == pygame.K_RIGHT:
                self.SelectedCharIndex += 1

                if self.SelectedCharIndex >= len(self.SplitedAlgarims):
                    self.SelectedCharIndex = len(self.SplitedAlgarims) - 1

            if event.key == pygame.K_0:
                self.ChangeValueInPos(self.SelectedCharIndex, 0)

            if event.key == pygame.K_1:
                self.ChangeValueInPos(self.SelectedCharIndex, 1)

            if event.key == pygame.K_2:
                self.ChangeValueInPos(self.SelectedCharIndex, 2)

            if event.key == pygame.K_3:
                self.ChangeValueInPos(self.SelectedCharIndex, 3)

            if event.key == pygame.K_4:
                self.ChangeValueInPos(self.SelectedCharIndex, 4)

            if event.key == pygame.K_5:
                self.ChangeValueInPos(self.SelectedCharIndex, 5)

            if event.key == pygame.K_6:
                self.ChangeValueInPos(self.SelectedCharIndex, 6)

            if event.key == pygame.K_7:
                self.ChangeValueInPos(self.SelectedCharIndex, 7)

            if event.key == pygame.K_8:
                self.ChangeValueInPos(self.SelectedCharIndex, 8)

            if event.key == pygame.K_9:
                self.ChangeValueInPos(self.SelectedCharIndex, 9)

    def ChangeValueInPos(self, Index, NewValue):
        self.SplitedAlgarims[Index] = NewValue
        self.Value = ""
        for algarims in self.SplitedAlgarims:
            self.Value += str(algarims)


class TrackBlock:
    def __init__(self, TrackData):
        self.TrackData = list(TrackData)
        self.Instance = -1
        self.Ypos = Main.DefaultContents.GetFont_height("/PressStart2P.ttf", 12, "0000") * self.Instance
        self.Rectangle = pygame.Rect(5, self.Ypos, Main.DefaultContents.GetFont_width("/PressStart2P.ttf", 12, "0000"), Main.DefaultContents.GetFont_height("/PressStart2P.ttf", 12, "0000"))
        self.TextWidth = Main.DefaultContents.GetFont_width("/PressStart2P.ttf", 12, "0000")
        self.TextHeight = Main.DefaultContents.GetFont_height("/PressStart2P.ttf", 12, "0000")
        self.Scroll = 0
        self.FrequencyNumber = EditableNumberView(pygame.Rect(self.Rectangle[0], self.Rectangle[1], self.TextWidth, self.TextHeight), str(self.TrackData[0]))
        self.DurationNumber = EditableNumberView(pygame.Rect(self.Rectangle[0] + self.TextWidth, self.Rectangle[1], self.TextWidth, self.TextHeight), str(self.TrackData[1]))
        self.Active = False
        self.SelectedField = 0
        self.MaxFields = 1

    def Render(self, DISPLAY):
        # Render the Frequency Region
        shape.Shape_Rectangle(DISPLAY, (100, 94, 85), (self.Rectangle[0] - 2, self.Rectangle[1] - 2, self.Rectangle[2] + 4, self.Rectangle[3] + 4), 0, 0, 5, 0, 5, 0)
        #Main.DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", 12, str(self.TrackData[0]), (230, 230, 230), self.Rectangle[0], self.Ypos)
        self.FrequencyNumber.Render(DISPLAY)


        # Render the Duration Region
        DurationX = (self.Rectangle[0] + self.TextWidth)
        shape.Shape_Rectangle(DISPLAY, (20, 34, 55), (DurationX, self.Rectangle[1] - 2, (self.TextWidth) + 4, self.Rectangle[3] + 4), 0, 0, 0, 5, 0, 5)
        #Main.DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", 12, str(self.TrackData[1]), (230, 230, 230), DurationX + 5, self.Ypos)
        self.DurationNumber.Render(DISPLAY)


    def Update(self):
        self.Rectangle = pygame.Rect(10, self.Ypos, self.TextWidth, self.TextHeight)
        self.Ypos = self.Scroll + (self.TextHeight + 10) * self.Instance

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
            if event.key == pygame.K_a:
                self.SelectedField -= 1

                if self.SelectedField <= 0:
                    self.SelectedField = 0

            if event.key == pygame.K_d:
                self.SelectedField += 1

                if self.SelectedField >= self.MaxFields:
                    self.SelectedField = self.MaxFields

class TrackList:
    def __init__(self, MusicData):
        self.Rectangle = pygame.Rect(5, 120, 300, 400)
        self.Tracks = list()
        self.Scroll = 0
        self.PlayMode = False
        self.SelectedTrack = 0
        self.PlayMode_TrackDelay = 0
        self.PlayMode_CurrentTonePlayed = False

        for i, data in enumerate(MusicData):
            if len(data) > 1:
                SplitedData = data.split(':')
                self.Tracks.append(TrackBlock((SplitedData[0].zfill(4), SplitedData[1].zfill(4))))
                print("Added Data:\n" + str(data))

    def Render(self, DISPLAY):
        TracksSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))
        for track in self.Tracks:
            if track.Ypos >= TracksSurface.get_height() + track.TextHeight or track.Ypos <= -track.TextHeight:
                continue

            track.Render(TracksSurface)

            if track.Instance == self.SelectedTrack:
                track.Active = True
                PointerRect = (2, track.Ypos, 4, track.Rectangle[3])
                shape.Shape_Rectangle(TracksSurface, (230, 50, 75), PointerRect)

                if self.PlayMode:
                    self.Scroll = -(self.SelectedTrack * track.Rectangle[3]) + 5

            else:
                track.Active = False

        DISPLAY.blit(TracksSurface, (self.Rectangle[0], self.Rectangle[1]))

    def Update(self):
        for i, track in enumerate(self.Tracks):
            track.Scroll = self.Scroll
            track.Instance = i
            track.Update()

        if self.PlayMode:
            self.PlayMode_TrackDelay += 0.01
            CurrentTrackObj = self.Tracks[self.SelectedTrack]
            if self.PlayMode_TrackDelay >= float("0.{0}".format(CurrentTrackObj.TrackData[1].replace("0", ""))):
                self.SelectedTrack += 1
                self.PlayMode_TrackDelay = 0
                PlayTone((CurrentTrackObj.TrackData[0], float("0.{0}".format(CurrentTrackObj.TrackData[1].replace("0", "")))))
                print((CurrentTrackObj.TrackData[0], float("0.{0}".format(CurrentTrackObj.TrackData[1].replace("0", "")))))

                if self.SelectedTrack >= len(self.Tracks):
                    self.SelectedTrack = 0
                    self.PlayMode = 0
                    self.PlayMode_TrackDelay = 0
                    self.PlayMode_CurrentTonePlayed = False
                    self.Scroll = 0

    def EventUpdate(self, event):
        for track in self.Tracks:
            track.EventUpdate(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.Scroll -= 5

            elif event.button == 5:
                self.Scroll += 5

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not self.PlayMode:
                    self.PlayMode = True
                    self.PlayMode_TrackDelay = 0
                    self.PlayMode_CurrentTonePlayed = False
                    self.Scroll = 0

                else:
                    self.PlayMode = False
                    self.PlayMode_TrackDelay = 0
                    self.PlayMode_CurrentTonePlayed = False
                    self.Scroll = 0

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

                if event.key == pygame.K_q:
                    if len(self.Tracks) > 1:
                        self.Tracks.pop()

                if event.key == pygame.K_e:
                    self.Tracks.append(TrackBlock(("0000", "0001")))



def PlayTone(Args):
    CorrectTone = int(Args[0])

    if not float(Args[1]) < 0.05:
        CommandSyntax = "play -nq -t alsa synth {1} sine {0}".format(CorrectTone, str(Args[1]))

        # -- Run the Command -- #
        subprocess.Popen(CommandSyntax, shell=True)