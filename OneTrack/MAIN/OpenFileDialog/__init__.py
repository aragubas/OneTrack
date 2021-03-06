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
import System.Core as Core
import OneTrack.MAIN.Screens.Editor as Main
from OneTrack.MAIN.Screens.Editor import InstanceVar as var
import Library.CoreEffects as Fx
import Library.CoreUtils as Utils
from Library import CoreAccess
from Library import CoreWMControl

# -- Window's Controls -- #
UnatachedDialogOpened = False
Enabled = False
OtherProcessPID = 0

def Update():
    global UnatachedDialogOpened
    global Enabled
    global OtherProcessPID

    if not Enabled:
        return

    # Open Dialog Process
    if not UnatachedDialogOpened:
        UnatachedDialogOpened = True
        Main.var.DisableControls = True
        Main.var.AwaysUpdate = True
        OtherProcessPID = CoreAccess.CreateProcess("OneTrack/UnatachedDialog", "OneTrack File Operation", (var.ProcessReference, "OPEN"))

    # Operation has been completed
    if not OtherProcessPID in CoreAccess.ProcessAccess_PID:
        var.AwaysUpdate = False
        var.DisableControls = False
        Enabled = False
        UnatachedDialogOpened = False

        CoreWMControl.WindowManagerSignal(var.ProcessReference, 0)

