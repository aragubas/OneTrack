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
import Core
import pygame
from OneTrack.MAIN import UI
from Core import utils

RootProcess = None

def Initialize(pRoot_Process):
    global RootProcess
    RootProcess = pRoot_Process

    # Set the correct screen size
    RootProcess.DISPLAY = pygame.Surface((400, 150))

    Args = RootProcess.INIT_ARGS[2].split(';')


def Draw(DISPLAY):
    pass

def Update():
    pass

def EventUpdate(event):
    pass