#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.2),
    on June 08, 2023, at 13:32
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from license_and_terms
'''
Fish v. 15 software, running on PsychoPy (v.2023.1.2)

This software is adapted from software which was written by Catherine E. Myers 
under funding from the Department of Veterans Affairs, 
Office of Research and Development. 

Design is adapted from the task originally described in 
Myers et al. (2003) Journal of Cognitive Neuroscience, 15(2), 
185-193.

Fish v.15 is a neuroscience experiment to asses the generalization performance of individuals
Copyright (C) 2023  Jose Mojica Perez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Author's contact information: 
    email: jmojicaperez@acm.org
'''
# Run 'Before Experiment' code from face_fish_pairing
import random
import os
# File names of faces and fishes without extension
fishes = ["green", "blue", "purple", "red"]
faces = ["boy", "girl", "man", "woman"]

# Generating the random pairings
random_numbers = []
for _ in range(4):
    r = random.randint(0,3)
    while r in random_numbers:
        r = random.randint(0,3)
    random_numbers.append(r)

r1, r2, r3, r4 = random_numbers
exp_files_path = os.getcwd() + "/experimentFiles/"
pairs_filename = "face_fish_pairings.csv"
pairings_filepath = exp_files_path + pairs_filename
file = open(pairings_filepath, "w")
file.write("face,fish1,fish2\n")
file.write(f"{faces[r1]},{fishes[r1]},{fishes[r2]}\n")
file.write(f"{faces[r2]},{fishes[r1]},{fishes[r2]}\n")
file.write(f"{faces[r3]},{fishes[r3]},{fishes[r4]}\n")
file.write(f"{faces[r4]},{fishes[r3]},{fishes[r4]}\n")
file.close()
# Run 'Before Experiment' code from phase_gen
import csv
import os

def generate_phase_file(pairings, phase_faces, phase_fishes, filename):
    '''
    Generates a csv file with every valid combination of face 
    left_fish and right_fish. 
    Args:
        pairings: a dictionary containing all the face-fish pairings in the 
                  format pairings[face] = {fish1, fish2}
        phase_faces: a list of strings with the base file name of the faces that 
                     correspond to the desired phase
        phase_fishes: a list of strings with the base file name of the fishes 
                      that correspond to the desired phase
    Returns:
        None. It instead generates [filename].csv for the that lists the
        stimuli for the desired phase
    '''
    file = open(filename, "w")
    file.write("face,leftFish,rightFish,correctResponse\n")
    # filename format should be phaseX.csv where X is the phase number
    # phase_no = filename.split(".")[0][-1]
    
    for face in phase_faces:
        # Create a list of the fishes that the face above owns and does not own
        not_owned_fishes = []
        owned_fishes = []
        for fish in phase_fishes:
            if(fish in pairings[face]):
                owned_fishes.append(fish)
            else:
                not_owned_fishes.append(fish)
                
        if(len(owned_fishes) > 1):
            # All the other phases. Do it this way because range would be empty
            # if there's only 1 owned fish
            for i in range(len(owned_fishes)):
                correct = owned_fishes[i]
                incorrect = not_owned_fishes[i]
                file.write(f"{face},{correct},{incorrect},left\n")
                file.write(f"{face},{incorrect},{correct},right\n")
        else: # Phase 0
            correct = owned_fishes[0]
            incorrect = not_owned_fishes[0]
            file.write(f"{face},{correct},{incorrect},left\n")
            file.write(f"{face},{incorrect},{correct},right\n")
                
    file.close()

def remove_crit_pairs(faces, fishes, filename, pairings):
    '''
    Removes and returns the critical pairs from the phase file with 
    name `filename`. This should only be used for a phase which is not the test
    phase and was generated with all the faces and fishes, i.e. phase 2.
    Args:
        faces: a list of all the faces
        fishes: a list of all the fishes
        filaneme: the file name of the phase file to modify
        pairings: a dictionary containing all the face-fish pairings in the 
                  format pairings[face] = {fish1, fish2}
    Returns:
        a set of all stimuli containing critical pairs 
        in comma separated string format
    '''

    # Phase 3 critical pairs:
    # Face B: Fish c/d, Face D: fish c/d
    do_not_include = {faces[1]: pairings[faces[1]][1], faces[3]: pairings[faces[3]][1]}
    
    file = open(filename, "r")
    reader = csv.DictReader(file)
    adjusted_file_text = "face,leftFish,rightFish,correctResponse,phase_used\n"
    crit_pairs_stims = set()
    for row in reader:
        face = row["face"]
        fish1 = row["leftFish"]
        fish2 = row["rightFish"]
        correct = row["correctResponse"]
        # If the face is not one of the critical pairs of phase 3 then 
        # it should be included in phase 2
        should_include = not ((face in do_not_include) and (fish1 == do_not_include[face] or fish2 == do_not_include[face]))
        
        if (should_include): # not a critical pair
            adjusted_file_text += ",".join([face, fish1, fish2, correct]) + "\n"
        else: # critical pair
            stim =  ",".join([face, fish1, fish2, correct])
            crit_pairs_stims.add(stim)
            continue
    file.close()
    file = open(filename, "w")
    file.write(adjusted_file_text)
    file.close()
    return crit_pairs_stims
            
# Getting the pairings from previously generated pairings file
exp_files_path = os.getcwd() + "/experimentFiles/"
pairings = {}
#pairings_file = open(exp_files_path + "face_fish_pairings.csv", "r")
pairings_file = open(pairings_filepath, "r")
reader = csv.DictReader(pairings_file)
for row in reader:
    pairings[row["face"]] = [row["fish1"], row["fish2"]]
pairings_file.close()

# All faces
faces = list(pairings)
# All fishes
fishes = []
for face in faces:
    if len(fishes) == 4: #There are only 4 fishes
        break
    for fish in pairings[face]:
        if(fish not in fishes):
            fishes.append(fish)


# Face A and Face C
phase0_faces = [faces[0], faces[2]]
phase0_fishes = [pairings[faces[0]][0], pairings[faces[2]][0]]
phase0_file = exp_files_path + "phase0.csv"
generate_phase_file(pairings, phase0_faces, phase0_fishes, phase0_file)

phase1_faces = faces
phase1_fishes = phase0_fishes
phase1_file = exp_files_path + "phase1.csv"
generate_phase_file(pairings, phase1_faces, phase1_fishes, phase1_file)

phase2_faces = faces
phase2_fishes = fishes
phase2_file = exp_files_path + "phase2.csv"
generate_phase_file(pairings, phase2_faces, phase2_fishes, phase2_file)
# critical pairs are not supposed to be in phase 2
crit_pairs_stims = remove_crit_pairs(phase2_faces, phase2_fishes, phase2_file, pairings)

phase3_faces = faces
phase3_fishes = fishes
phase3_file = exp_files_path + "phase3.csv"
generate_phase_file(pairings, phase3_faces, phase3_fishes, phase3_file)
# Run 'Before Experiment' code from code_3
myFaceFileName="temp"
myLeftFishFileName="temp"
myRightFishFileName="temp"
showLeftFish="temp"
showRightFish="temp"
myFeedbackImpage="temp"
# Run 'Before Experiment' code from code_3
myFaceFileName="temp"
myLeftFishFileName="temp"
myRightFishFileName="temp"
showLeftFish="temp"
showRightFish="temp"
myFeedbackImpage="temp"
# Run 'Before Experiment' code from code_3
myFaceFileName="temp"
myLeftFishFileName="temp"
myRightFishFileName="temp"
showLeftFish="temp"
showRightFish="temp"
myFeedbackImpage="temp"
# Run 'Before Experiment' code from code_3
myFaceFileName="temp"
myLeftFishFileName="temp"
myRightFishFileName="temp"
showLeftFish="temp"
showRightFish="temp"
myFeedbackImpage="temp"


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.2'
expName = 'Fish15'  # from the Builder filename that created this script
expInfo = {
    'session': '001',
    'participant': '',
    'experimenter': '',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'psychopyOutput/%s_%s' % (expInfo['participant'], expName)

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\josel\\gluck_lab\\GluckLab\\fish15\\fish15_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1536, 960], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color='white', colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True)
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "startup" ---
License_And_Terms = visual.TextStim(win=win, name='License_And_Terms',
    text='Fish v. 15 software, running on PsychoPy (v.2023.1.2)\n\nThis software is adapted from software which was written by Catherine E. Myers  under funding from the Department of Veterans Affairs, Office of Research and Development. \n\nDesign is adapted from the task originally described in Myers et al. (2003) Journal of Cognitive Neuroscience, 15(2), 185-193.\n\nFish 15 is a neuroscience experiment to test the generalization performance of individuals\n   Copyright (C) 2023 Jose Mojica Perez\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU Affero General Public License as\n    published by the Free Software Foundation, either version 3 of the\n    License, or (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU Affero General Public License for more details.\n\n    You should have received a copy of the GNU Affero General Public License\n    along with this program.  If not, see <https://www.gnu.org/licenses/>.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=1.5, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
conditions_key = keyboard.Keyboard()

# --- Initialize components for Routine "train_instr" ---
train_instructions_text = visual.TextStim(win=win, name='train_instructions_text',
    text='Welcome to the experiment.\n\nYou will see drawings of people who each have some pet fish.\n\nDifferent people have different kinds of fish.\n\nYour job is to learn which kind of fish each person has.\n\nEach time you see a face, press the LEFT or RIGHT key, depending on which fish you think the person has. In the beginning, you will have to guess. The choice you make will be circled and you will be told whether it is correct or incorrect. Try to learn the correct answers, because you will be tested later.\n\nPress the LEFT or RIGHT key to begin.\n\n',
    font='Arial',
    pos=(0, 0), height=0.065, wrapWidth=1.5, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
train_instr_key = keyboard.Keyboard()
# Run 'Begin Experiment' code from code_train_instr
myISIduration=1.0
myTally=0

CriterionReached=False
myConsecutiveCorrect=0
myCriterion=4

myCircleHoriz = -0.15
myCircleVert = 0.01

myTrialCorrect = False
myErr1 = 0
myCrit1 = 0
myErr2 = 0
myCrit2 = 0
myErr3 = 0
myCrit3 = 0
myOldErr = 0
myNewErr = 0
myOldTrials = 0
myNewTrials = 0


# --- Initialize components for Routine "runTrial" ---
trial_face = visual.ImageStim(
    win=win,
    name='trial_face', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.45), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
trial_text = visual.TextStim(win=win, name='trial_text',
    text='Which fish does this person have?\nUse LEFT or RIGHT key to choose.',
    font='Arial',
    pos=(0, -.3), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
fishOnLeft = visual.ImageStim(
    win=win,
    name='fishOnLeft', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(-0.15, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
fishOnRight = visual.ImageStim(
    win=win,
    name='fishOnRight', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(+0.2, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
trial_response = keyboard.Keyboard()

# --- Initialize components for Routine "doFB1" ---
FB2_face = visual.ImageStim(
    win=win,
    name='FB2_face', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.45), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
FB2_Circle = visual.ImageStim(
    win=win,
    name='FB2_Circle', 
    image='fishPix/TheCircle.png', mask=None, anchor='center',
    ori=0, pos=[0,0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
FB1_leftFish = visual.ImageStim(
    win=win,
    name='FB1_leftFish', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(-0.15, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
FB1_rightFish = visual.ImageStim(
    win=win,
    name='FB1_rightFish', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(+0.2, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
FB1_text = visual.ImageStim(
    win=win,
    name='FB1_text', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, -0.3), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)

# --- Initialize components for Routine "next_stage" ---

# --- Initialize components for Routine "runTrial" ---
trial_face = visual.ImageStim(
    win=win,
    name='trial_face', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.45), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
trial_text = visual.TextStim(win=win, name='trial_text',
    text='Which fish does this person have?\nUse LEFT or RIGHT key to choose.',
    font='Arial',
    pos=(0, -.3), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
fishOnLeft = visual.ImageStim(
    win=win,
    name='fishOnLeft', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(-0.15, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
fishOnRight = visual.ImageStim(
    win=win,
    name='fishOnRight', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(+0.2, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
trial_response = keyboard.Keyboard()

# --- Initialize components for Routine "doFB2" ---
FB2_face_2 = visual.ImageStim(
    win=win,
    name='FB2_face_2', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.45), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
FB2_Circle_2 = visual.ImageStim(
    win=win,
    name='FB2_Circle_2', 
    image='fishPix/TheCircle.png', mask=None, anchor='center',
    ori=0, pos=[0,0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
FB2_leftFish = visual.ImageStim(
    win=win,
    name='FB2_leftFish', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(-0.15, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
FB2_rightFish = visual.ImageStim(
    win=win,
    name='FB2_rightFish', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(+0.2, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
FB2_text = visual.ImageStim(
    win=win,
    name='FB2_text', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, -0.3), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)

# --- Initialize components for Routine "next_stage" ---

# --- Initialize components for Routine "runTrial" ---
trial_face = visual.ImageStim(
    win=win,
    name='trial_face', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.45), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
trial_text = visual.TextStim(win=win, name='trial_text',
    text='Which fish does this person have?\nUse LEFT or RIGHT key to choose.',
    font='Arial',
    pos=(0, -.3), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
fishOnLeft = visual.ImageStim(
    win=win,
    name='fishOnLeft', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(-0.15, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
fishOnRight = visual.ImageStim(
    win=win,
    name='fishOnRight', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(+0.2, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
trial_response = keyboard.Keyboard()

# --- Initialize components for Routine "doFB3" ---
FB3_face = visual.ImageStim(
    win=win,
    name='FB3_face', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.45), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
FB3_Circle = visual.ImageStim(
    win=win,
    name='FB3_Circle', 
    image='fishPix/TheCircle.png', mask=None, anchor='center',
    ori=0, pos=[0,0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
FB3_leftFish = visual.ImageStim(
    win=win,
    name='FB3_leftFish', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(-0.15, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
FB3_rightFish = visual.ImageStim(
    win=win,
    name='FB3_rightFish', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(+0.2, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
FB3_text = visual.ImageStim(
    win=win,
    name='FB3_text', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, -0.3), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)

# --- Initialize components for Routine "test_instr" ---
test_text1 = visual.TextStim(win=win, name='test_text1',
    text='Good!',
    font='Arial',
    pos=(0, 0.55), height=0.075, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
test_text2 = visual.TextStim(win=win, name='test_text2',
    text='In this part of the experiment, you will need',
    font='Arial',
    pos=(0, 0.3), height=0.075, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
test_text3 = visual.TextStim(win=win, name='test_text3',
    text='Ito remember what you have learned so far.',
    font='Arial',
    pos=(0, 0.2), height=0.075, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
test_text4 = visual.TextStim(win=win, name='test_text4',
    text='You will NOT be shown the correct answers.',
    font='Arial',
    pos=(0, 0.1), height=0.075, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-3.0);
test_text5 = visual.TextStim(win=win, name='test_text5',
    text='At the end of the experiment, the computer will',
    font='Arial',
    pos=(0, -0.05), height=0.075, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-4.0);
test_text6 = visual.TextStim(win=win, name='test_text6',
    text='tell you how many you got right.',
    font='Arial',
    pos=(0, -0.15), height=0.075, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-5.0);
test_text7 = visual.TextStim(win=win, name='test_text7',
    text='Good luck!',
    font='Arial',
    pos=(0, -0.3), height=0.075, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-6.0);
test_text8 = visual.TextStim(win=win, name='test_text8',
    text='Press the LEFT or RIGHT key to begin.',
    font='Arial',
    pos=(0, -0.55), height=0.075, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-7.0);
test_instr_key = keyboard.Keyboard()

# --- Initialize components for Routine "runTrial" ---
trial_face = visual.ImageStim(
    win=win,
    name='trial_face', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.45), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
trial_text = visual.TextStim(win=win, name='trial_text',
    text='Which fish does this person have?\nUse LEFT or RIGHT key to choose.',
    font='Arial',
    pos=(0, -.3), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
fishOnLeft = visual.ImageStim(
    win=win,
    name='fishOnLeft', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(-0.15, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
fishOnRight = visual.ImageStim(
    win=win,
    name='fishOnRight', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(+0.2, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
trial_response = keyboard.Keyboard()

# --- Initialize components for Routine "noFB" ---
noFB_face = visual.ImageStim(
    win=win,
    name='noFB_face', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.45), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
noFB_Circle = visual.ImageStim(
    win=win,
    name='noFB_Circle', 
    image='fishPix/TheCircle.png', mask=None, anchor='center',
    ori=0, pos=[0,0], size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
noFB_leftFish = visual.ImageStim(
    win=win,
    name='noFB_leftFish', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(-0.15, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
noFB_rightFish = visual.ImageStim(
    win=win,
    name='noFB_rightFish', 
    image='default.png', mask=None, anchor='center',
    ori=0, pos=(+0.2, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)

# --- Initialize components for Routine "goodbye" ---
goodbye_text1 = visual.TextStim(win=win, name='goodbye_text1',
    text='The end.',
    font='Arial',
    pos=(0, 0.5), height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
goodbye_text2 = visual.TextStim(win=win, name='goodbye_text2',
    text='Your final point total was:',
    font='Arial',
    pos=(0, 0.1), height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
goodbye_tally = visual.TextStim(win=win, name='goodbye_tally',
    text='',
    font='Arial',
    pos=(0,0), height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
goodbye_text3 = visual.TextStim(win=win, name='goodbye_text3',
    text='Thanks for participating.',
    font='Arial',
    pos=(0, -.25), height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-3.0);
goodbye_text4 = visual.TextStim(win=win, name='goodbye_text4',
    text='Press the space bar to exit.',
    font='Arial',
    pos=(0, -.5), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-4.0);
goodbye_key = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "startup" ---
continueRoutine = True
# update component parameters for each repeat
conditions_key.keys = []
conditions_key.rt = []
_conditions_key_allKeys = []
# Run 'Begin Routine' code from start_data_log
import os
import datetime

participant = expInfo["participant"]
experimenter = expInfo["experimenter"]

data_path = os.getcwd() + "/data/"
data_filename = expName + "_" + participant + ".csv"
data_file = open(data_path + data_filename, "w")

expDateTime = datetime.datetime.now()
# Weekday(full name), Month(full name) Day(dd), Year(yyyy)
date = expDateTime.strftime("%A, %B %d, %Y")
# Hour(00-12):Minute(00-59):Second(00-59) AM/PM
time = expDateTime.strftime("%I:%M:%S %p")

# Getting the critical pairs
crit_pairs = []
for stim in crit_pairs_stims:
    face, fish1, fish2, correct = stim.split(",")
    pair1 = (face, fish1, fish2)
    pair2 = (face, fish2, fish1)
    if(pair1 not in crit_pairs and pair2 not in crit_pairs):
        crit_pairs.append(pair1)
        
# Keep track of phase number
current_phase = 0

data_file.write(f"{expName}\n")
data_file.write(f"Subject ID: {participant}\n")
data_file.write(f"Experimenter: {experimenter}\n")
data_file.write(f"\"{date}\"\n")
data_file.write(f"Time: {time}\n")
data_file.write(f"\"Note: Critical Pairs = {crit_pairs}\"\n")


# keep track of which components have finished
startupComponents = [License_And_Terms, conditions_key]
for thisComponent in startupComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "startup" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *License_And_Terms* updates
    
    # if License_And_Terms is starting this frame...
    if License_And_Terms.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        License_And_Terms.frameNStart = frameN  # exact frame index
        License_And_Terms.tStart = t  # local t and not account for scr refresh
        License_And_Terms.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(License_And_Terms, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'License_And_Terms.started')
        # update status
        License_And_Terms.status = STARTED
        License_And_Terms.setAutoDraw(True)
    
    # if License_And_Terms is active this frame...
    if License_And_Terms.status == STARTED:
        # update params
        pass
    
    # *conditions_key* updates
    waitOnFlip = False
    
    # if conditions_key is starting this frame...
    if conditions_key.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
        # keep track of start time/frame for later
        conditions_key.frameNStart = frameN  # exact frame index
        conditions_key.tStart = t  # local t and not account for scr refresh
        conditions_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(conditions_key, 'tStartRefresh')  # time at next scr refresh
        # update status
        conditions_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(conditions_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(conditions_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if conditions_key.status == STARTED and not waitOnFlip:
        theseKeys = conditions_key.getKeys(keyList=['space'], waitRelease=False)
        _conditions_key_allKeys.extend(theseKeys)
        if len(_conditions_key_allKeys):
            conditions_key.keys = _conditions_key_allKeys[-1].name  # just the last key pressed
            conditions_key.rt = _conditions_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in startupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "startup" ---
for thisComponent in startupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "startup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "train_instr" ---
continueRoutine = True
# update component parameters for each repeat
train_instr_key.keys = []
train_instr_key.rt = []
_train_instr_key_allKeys = []
# Run 'Begin Routine' code from start_phase_log_train
# Initialize phase number
current_phase = 0

# Initialize trials for the curent phase
current_trial = 1

# Initialize scores
# Ratio of correct answers/trials for phases 0,1,2
acquisition_score = 0
acquisition_trials = 0
# Ratio of correct answers/trials for non-critical
# pairs in phase 3 (pairs that were shown in previous phases)
retention_score = 0
retention_trials = 0
# Ratio of correct answers/trials for critical
# pairs in phase 3 (pairs that were not shown in previous phases)
generalization_score = 0
generalization_trials = 0

data_file.write(f"----- PHASE {current_phase} -----\n")
header = "Trial,Face,Left Fish,Right Fish,Correct Response,Subject Response,Response Time,Correct/Incorrect\n"
data_file.write(header)

# keep track of which components have finished
train_instrComponents = [train_instructions_text, train_instr_key]
for thisComponent in train_instrComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "train_instr" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *train_instructions_text* updates
    
    # if train_instructions_text is starting this frame...
    if train_instructions_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        train_instructions_text.frameNStart = frameN  # exact frame index
        train_instructions_text.tStart = t  # local t and not account for scr refresh
        train_instructions_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(train_instructions_text, 'tStartRefresh')  # time at next scr refresh
        # update status
        train_instructions_text.status = STARTED
        train_instructions_text.setAutoDraw(True)
    
    # if train_instructions_text is active this frame...
    if train_instructions_text.status == STARTED:
        # update params
        pass
    
    # *train_instr_key* updates
    waitOnFlip = False
    
    # if train_instr_key is starting this frame...
    if train_instr_key.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
        # keep track of start time/frame for later
        train_instr_key.frameNStart = frameN  # exact frame index
        train_instr_key.tStart = t  # local t and not account for scr refresh
        train_instr_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(train_instr_key, 'tStartRefresh')  # time at next scr refresh
        # update status
        train_instr_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(train_instr_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(train_instr_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if train_instr_key.status == STARTED and not waitOnFlip:
        theseKeys = train_instr_key.getKeys(keyList=['z','m','left','right'], waitRelease=False)
        _train_instr_key_allKeys.extend(theseKeys)
        if len(_train_instr_key_allKeys):
            train_instr_key.keys = _train_instr_key_allKeys[-1].name  # just the last key pressed
            train_instr_key.rt = _train_instr_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in train_instrComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "train_instr" ---
for thisComponent in train_instrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "train_instr" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials1 = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('experimentFiles/phase0.csv'),
    seed=None, name='trials1')
thisExp.addLoop(trials1)  # add the loop to the experiment
thisTrials1 = trials1.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrials1.rgb)
if thisTrials1 != None:
    for paramName in thisTrials1:
        exec('{} = thisTrials1[paramName]'.format(paramName))

for thisTrials1 in trials1:
    currentLoop = trials1
    # abbreviate parameter names if possible (e.g. rgb = thisTrials1.rgb)
    if thisTrials1 != None:
        for paramName in thisTrials1:
            exec('{} = thisTrials1[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "runTrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_3
    myFaceFileName= "fishPix/"+face+".png"
    myLeftFishFileName="fishPix/"+leftFish+".png"
    myRightFishFileName="fishPix/"+rightFish+".png"
    trial_face.setImage(myFaceFileName)
    fishOnLeft.setImage(myLeftFishFileName)
    fishOnRight.setImage(myRightFishFileName)
    trial_response.keys = []
    trial_response.rt = []
    _trial_response_allKeys = []
    # keep track of which components have finished
    runTrialComponents = [trial_face, trial_text, fishOnLeft, fishOnRight, trial_response]
    for thisComponent in runTrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "runTrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *trial_face* updates
        
        # if trial_face is starting this frame...
        if trial_face.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            trial_face.frameNStart = frameN  # exact frame index
            trial_face.tStart = t  # local t and not account for scr refresh
            trial_face.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_face, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_face.status = STARTED
            trial_face.setAutoDraw(True)
        
        # if trial_face is active this frame...
        if trial_face.status == STARTED:
            # update params
            pass
        
        # *trial_text* updates
        
        # if trial_text is starting this frame...
        if trial_text.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
            # keep track of start time/frame for later
            trial_text.frameNStart = frameN  # exact frame index
            trial_text.tStart = t  # local t and not account for scr refresh
            trial_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_text.status = STARTED
            trial_text.setAutoDraw(True)
        
        # if trial_text is active this frame...
        if trial_text.status == STARTED:
            # update params
            pass
        
        # *fishOnLeft* updates
        
        # if fishOnLeft is starting this frame...
        if fishOnLeft.status == NOT_STARTED and tThisFlip >= .25-frameTolerance:
            # keep track of start time/frame for later
            fishOnLeft.frameNStart = frameN  # exact frame index
            fishOnLeft.tStart = t  # local t and not account for scr refresh
            fishOnLeft.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fishOnLeft, 'tStartRefresh')  # time at next scr refresh
            # update status
            fishOnLeft.status = STARTED
            fishOnLeft.setAutoDraw(True)
        
        # if fishOnLeft is active this frame...
        if fishOnLeft.status == STARTED:
            # update params
            pass
        
        # *fishOnRight* updates
        
        # if fishOnRight is starting this frame...
        if fishOnRight.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
            # keep track of start time/frame for later
            fishOnRight.frameNStart = frameN  # exact frame index
            fishOnRight.tStart = t  # local t and not account for scr refresh
            fishOnRight.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fishOnRight, 'tStartRefresh')  # time at next scr refresh
            # update status
            fishOnRight.status = STARTED
            fishOnRight.setAutoDraw(True)
        
        # if fishOnRight is active this frame...
        if fishOnRight.status == STARTED:
            # update params
            pass
        
        # *trial_response* updates
        waitOnFlip = False
        
        # if trial_response is starting this frame...
        if trial_response.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            trial_response.frameNStart = frameN  # exact frame index
            trial_response.tStart = t  # local t and not account for scr refresh
            trial_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_response, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(trial_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(trial_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if trial_response.status == STARTED and not waitOnFlip:
            theseKeys = trial_response.getKeys(keyList=['z','m','left','right'], waitRelease=False)
            _trial_response_allKeys.extend(theseKeys)
            if len(_trial_response_allKeys):
                trial_response.keys = _trial_response_allKeys[-1].name  # just the last key pressed
                trial_response.rt = _trial_response_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in runTrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "runTrial" ---
    for thisComponent in runTrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if trial_response.keys in ['', [], None]:  # No response was made
        trial_response.keys = None
    trials1.addData('trial_response.keys',trial_response.keys)
    if trial_response.keys != None:  # we had a response
        trials1.addData('trial_response.rt', trial_response.rt)
    # Run 'End Routine' code from code
    nFBleft=0
    nFBright=0
    
    if(trial_response.keys == "z"):
        trial_response.keys = "left"
    if(trial_response.keys == "m"):
        trial_response.keys = "right"
        
    
    if (trial_response.keys=='left') :
        myChosen="left"
        myCircleHoriz = -0.13
    else :
        myChosen="right"
        myCircleHoriz = 0.22
    if (trial_response.keys==correctResponse) :
        myTrialCorrect=True
        thisExp.addData('Correct',1)
        myTally = myTally + 1
        myFeedbackImage="fishPix/win.png"
        myConsecutiveCorrect = myConsecutiveCorrect+1
        if (myConsecutiveCorrect >= myCriterion) :
            CriterionReached=True
    else :
        myTrialCorrect=False
        thisExp.addData('Correct',0)
        myFeedbackImage="fishPix/lose.png"
        myConsecutiveCorrect = 0
    if (correctResponse=="left") :
        showLeftFish=myLeftFishFileName
        showRightFish="fishPix/blank.png"
    else :
        showLeftFish="fishPix/blank.png"
        showRightFish=myRightFishFileName
    
    # Run 'End Routine' code from log_trial
    correct = ""
    if(trial_response.keys == correctResponse):
        # We do a string so we can concatenate an asterisk to it for critical pairs
        correct = "1" # 1 if correct, 0 otherwise
    else:
        correct = "0"
    
    # Add a star if this stimulus contains a critical pair
    stim_vars = [face, leftFish, rightFish, correctResponse]
    stim = ",".join(stim_vars)
    if (stim in crit_pairs_stims):
        correct += "*"
        
    # Keeping track of overall scores
    # phases < 3 are acquisition, phase 3 is testing retention and generalization
    if(current_phase < 3 and correct == "1"): 
        acquisition_score += 1
    elif(correct == "1"): # We are in phase 3, correct answer, but no critical pair
        retention_score += 1
    elif(correct == "1*"): # We are in phase 3, correct answer, but no critical pair
        generalization_score += 1
    
    # Update the number of trials 
    # phases < 3 are acquisition, phase 3 is testing retention and generalization
    if(current_phase < 3):
        acquisition_trials += 1
    # If not a critical pair (no asterisk), it is retention
    elif("*" not in correct):
        retention_trials += 1
    # if it is a critical pair then it is generalization
    else:
        generalization_trials += 1
        
    
    # Convert all the variables we want to log into strings and store them in a list
    # so we can join them later
    log_vars = [ str(x) for x in [current_trial, face, leftFish, rightFish, 
                correctResponse, trial_response.keys, trial_response.rt, correct]]
    
    log_text = ",".join(log_vars) + "\n"
    data_file.write(log_text)
    
    current_trial += 1
    # the Routine "runTrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "doFB1" ---
    continueRoutine = True
    # update component parameters for each repeat
    FB2_face.setImage(myFaceFileName)
    FB2_Circle.setPos([myCircleHoriz, myCircleVert])
    FB1_leftFish.setImage(showLeftFish)
    FB1_rightFish.setImage(showRightFish)
    FB1_text.setImage(myFeedbackImage)
    # keep track of which components have finished
    doFB1Components = [FB2_face, FB2_Circle, FB1_leftFish, FB1_rightFish, FB1_text]
    for thisComponent in doFB1Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "doFB1" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *FB2_face* updates
        
        # if FB2_face is starting this frame...
        if FB2_face.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB2_face.frameNStart = frameN  # exact frame index
            FB2_face.tStart = t  # local t and not account for scr refresh
            FB2_face.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB2_face, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB2_face.status = STARTED
            FB2_face.setAutoDraw(True)
        
        # if FB2_face is active this frame...
        if FB2_face.status == STARTED:
            # update params
            pass
        
        # if FB2_face is stopping this frame...
        if FB2_face.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB2_face.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB2_face.tStop = t  # not accounting for scr refresh
                FB2_face.frameNStop = frameN  # exact frame index
                # update status
                FB2_face.status = FINISHED
                FB2_face.setAutoDraw(False)
        
        # *FB2_Circle* updates
        
        # if FB2_Circle is starting this frame...
        if FB2_Circle.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            FB2_Circle.frameNStart = frameN  # exact frame index
            FB2_Circle.tStart = t  # local t and not account for scr refresh
            FB2_Circle.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB2_Circle, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB2_Circle.status = STARTED
            FB2_Circle.setAutoDraw(True)
        
        # if FB2_Circle is active this frame...
        if FB2_Circle.status == STARTED:
            # update params
            pass
        
        # if FB2_Circle is stopping this frame...
        if FB2_Circle.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB2_Circle.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB2_Circle.tStop = t  # not accounting for scr refresh
                FB2_Circle.frameNStop = frameN  # exact frame index
                # update status
                FB2_Circle.status = FINISHED
                FB2_Circle.setAutoDraw(False)
        
        # *FB1_leftFish* updates
        
        # if FB1_leftFish is starting this frame...
        if FB1_leftFish.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB1_leftFish.frameNStart = frameN  # exact frame index
            FB1_leftFish.tStart = t  # local t and not account for scr refresh
            FB1_leftFish.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB1_leftFish, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB1_leftFish.status = STARTED
            FB1_leftFish.setAutoDraw(True)
        
        # if FB1_leftFish is active this frame...
        if FB1_leftFish.status == STARTED:
            # update params
            pass
        
        # if FB1_leftFish is stopping this frame...
        if FB1_leftFish.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB1_leftFish.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB1_leftFish.tStop = t  # not accounting for scr refresh
                FB1_leftFish.frameNStop = frameN  # exact frame index
                # update status
                FB1_leftFish.status = FINISHED
                FB1_leftFish.setAutoDraw(False)
        
        # *FB1_rightFish* updates
        
        # if FB1_rightFish is starting this frame...
        if FB1_rightFish.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB1_rightFish.frameNStart = frameN  # exact frame index
            FB1_rightFish.tStart = t  # local t and not account for scr refresh
            FB1_rightFish.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB1_rightFish, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB1_rightFish.status = STARTED
            FB1_rightFish.setAutoDraw(True)
        
        # if FB1_rightFish is active this frame...
        if FB1_rightFish.status == STARTED:
            # update params
            pass
        
        # if FB1_rightFish is stopping this frame...
        if FB1_rightFish.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB1_rightFish.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB1_rightFish.tStop = t  # not accounting for scr refresh
                FB1_rightFish.frameNStop = frameN  # exact frame index
                # update status
                FB1_rightFish.status = FINISHED
                FB1_rightFish.setAutoDraw(False)
        
        # *FB1_text* updates
        
        # if FB1_text is starting this frame...
        if FB1_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB1_text.frameNStart = frameN  # exact frame index
            FB1_text.tStart = t  # local t and not account for scr refresh
            FB1_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB1_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB1_text.status = STARTED
            FB1_text.setAutoDraw(True)
        
        # if FB1_text is active this frame...
        if FB1_text.status == STARTED:
            # update params
            pass
        
        # if FB1_text is stopping this frame...
        if FB1_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB1_text.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB1_text.tStop = t  # not accounting for scr refresh
                FB1_text.frameNStop = frameN  # exact frame index
                # update status
                FB1_text.status = FINISHED
                FB1_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in doFB1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "doFB1" ---
    for thisComponent in doFB1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from FB1_code
    if (myTrialCorrect==False) :
        myErr1 += 1
    if (CriterionReached==True) :
        trials1.finished=True
        myCrit1 = 1
    # the Routine "doFB1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 5 repeats of 'trials1'


# --- Prepare to start Routine "next_stage" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from code_4
CriterionReached=False
myConsecutiveCorrect=0
myCriterion = myCriterion+4

# Run 'Begin Routine' code from start_phase_log
# Update phase number
current_phase += 1

# Initialize trials for the curent phase
current_trial = 1

data_file.write(f"----- PHASE {current_phase} -----\n")
header = "Trial,Face,Left Fish,Right Fish,Correct Response,Subject Response,Response Time,Correct/Incorrect\n"
data_file.write(header)

# keep track of which components have finished
next_stageComponents = []
for thisComponent in next_stageComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "next_stage" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in next_stageComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "next_stage" ---
for thisComponent in next_stageComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "next_stage" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials2 = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('experimentFiles/phase1.csv'),
    seed=None, name='trials2')
thisExp.addLoop(trials2)  # add the loop to the experiment
thisTrials2 = trials2.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrials2.rgb)
if thisTrials2 != None:
    for paramName in thisTrials2:
        exec('{} = thisTrials2[paramName]'.format(paramName))

for thisTrials2 in trials2:
    currentLoop = trials2
    # abbreviate parameter names if possible (e.g. rgb = thisTrials2.rgb)
    if thisTrials2 != None:
        for paramName in thisTrials2:
            exec('{} = thisTrials2[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "runTrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_3
    myFaceFileName= "fishPix/"+face+".png"
    myLeftFishFileName="fishPix/"+leftFish+".png"
    myRightFishFileName="fishPix/"+rightFish+".png"
    trial_face.setImage(myFaceFileName)
    fishOnLeft.setImage(myLeftFishFileName)
    fishOnRight.setImage(myRightFishFileName)
    trial_response.keys = []
    trial_response.rt = []
    _trial_response_allKeys = []
    # keep track of which components have finished
    runTrialComponents = [trial_face, trial_text, fishOnLeft, fishOnRight, trial_response]
    for thisComponent in runTrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "runTrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *trial_face* updates
        
        # if trial_face is starting this frame...
        if trial_face.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            trial_face.frameNStart = frameN  # exact frame index
            trial_face.tStart = t  # local t and not account for scr refresh
            trial_face.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_face, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_face.status = STARTED
            trial_face.setAutoDraw(True)
        
        # if trial_face is active this frame...
        if trial_face.status == STARTED:
            # update params
            pass
        
        # *trial_text* updates
        
        # if trial_text is starting this frame...
        if trial_text.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
            # keep track of start time/frame for later
            trial_text.frameNStart = frameN  # exact frame index
            trial_text.tStart = t  # local t and not account for scr refresh
            trial_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_text.status = STARTED
            trial_text.setAutoDraw(True)
        
        # if trial_text is active this frame...
        if trial_text.status == STARTED:
            # update params
            pass
        
        # *fishOnLeft* updates
        
        # if fishOnLeft is starting this frame...
        if fishOnLeft.status == NOT_STARTED and tThisFlip >= .25-frameTolerance:
            # keep track of start time/frame for later
            fishOnLeft.frameNStart = frameN  # exact frame index
            fishOnLeft.tStart = t  # local t and not account for scr refresh
            fishOnLeft.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fishOnLeft, 'tStartRefresh')  # time at next scr refresh
            # update status
            fishOnLeft.status = STARTED
            fishOnLeft.setAutoDraw(True)
        
        # if fishOnLeft is active this frame...
        if fishOnLeft.status == STARTED:
            # update params
            pass
        
        # *fishOnRight* updates
        
        # if fishOnRight is starting this frame...
        if fishOnRight.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
            # keep track of start time/frame for later
            fishOnRight.frameNStart = frameN  # exact frame index
            fishOnRight.tStart = t  # local t and not account for scr refresh
            fishOnRight.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fishOnRight, 'tStartRefresh')  # time at next scr refresh
            # update status
            fishOnRight.status = STARTED
            fishOnRight.setAutoDraw(True)
        
        # if fishOnRight is active this frame...
        if fishOnRight.status == STARTED:
            # update params
            pass
        
        # *trial_response* updates
        waitOnFlip = False
        
        # if trial_response is starting this frame...
        if trial_response.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            trial_response.frameNStart = frameN  # exact frame index
            trial_response.tStart = t  # local t and not account for scr refresh
            trial_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_response, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(trial_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(trial_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if trial_response.status == STARTED and not waitOnFlip:
            theseKeys = trial_response.getKeys(keyList=['z','m','left','right'], waitRelease=False)
            _trial_response_allKeys.extend(theseKeys)
            if len(_trial_response_allKeys):
                trial_response.keys = _trial_response_allKeys[-1].name  # just the last key pressed
                trial_response.rt = _trial_response_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in runTrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "runTrial" ---
    for thisComponent in runTrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if trial_response.keys in ['', [], None]:  # No response was made
        trial_response.keys = None
    trials2.addData('trial_response.keys',trial_response.keys)
    if trial_response.keys != None:  # we had a response
        trials2.addData('trial_response.rt', trial_response.rt)
    # Run 'End Routine' code from code
    nFBleft=0
    nFBright=0
    
    if(trial_response.keys == "z"):
        trial_response.keys = "left"
    if(trial_response.keys == "m"):
        trial_response.keys = "right"
        
    
    if (trial_response.keys=='left') :
        myChosen="left"
        myCircleHoriz = -0.13
    else :
        myChosen="right"
        myCircleHoriz = 0.22
    if (trial_response.keys==correctResponse) :
        myTrialCorrect=True
        thisExp.addData('Correct',1)
        myTally = myTally + 1
        myFeedbackImage="fishPix/win.png"
        myConsecutiveCorrect = myConsecutiveCorrect+1
        if (myConsecutiveCorrect >= myCriterion) :
            CriterionReached=True
    else :
        myTrialCorrect=False
        thisExp.addData('Correct',0)
        myFeedbackImage="fishPix/lose.png"
        myConsecutiveCorrect = 0
    if (correctResponse=="left") :
        showLeftFish=myLeftFishFileName
        showRightFish="fishPix/blank.png"
    else :
        showLeftFish="fishPix/blank.png"
        showRightFish=myRightFishFileName
    
    # Run 'End Routine' code from log_trial
    correct = ""
    if(trial_response.keys == correctResponse):
        # We do a string so we can concatenate an asterisk to it for critical pairs
        correct = "1" # 1 if correct, 0 otherwise
    else:
        correct = "0"
    
    # Add a star if this stimulus contains a critical pair
    stim_vars = [face, leftFish, rightFish, correctResponse]
    stim = ",".join(stim_vars)
    if (stim in crit_pairs_stims):
        correct += "*"
        
    # Keeping track of overall scores
    # phases < 3 are acquisition, phase 3 is testing retention and generalization
    if(current_phase < 3 and correct == "1"): 
        acquisition_score += 1
    elif(correct == "1"): # We are in phase 3, correct answer, but no critical pair
        retention_score += 1
    elif(correct == "1*"): # We are in phase 3, correct answer, but no critical pair
        generalization_score += 1
    
    # Update the number of trials 
    # phases < 3 are acquisition, phase 3 is testing retention and generalization
    if(current_phase < 3):
        acquisition_trials += 1
    # If not a critical pair (no asterisk), it is retention
    elif("*" not in correct):
        retention_trials += 1
    # if it is a critical pair then it is generalization
    else:
        generalization_trials += 1
        
    
    # Convert all the variables we want to log into strings and store them in a list
    # so we can join them later
    log_vars = [ str(x) for x in [current_trial, face, leftFish, rightFish, 
                correctResponse, trial_response.keys, trial_response.rt, correct]]
    
    log_text = ",".join(log_vars) + "\n"
    data_file.write(log_text)
    
    current_trial += 1
    # the Routine "runTrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "doFB2" ---
    continueRoutine = True
    # update component parameters for each repeat
    FB2_face_2.setImage(myFaceFileName)
    FB2_Circle_2.setPos([myCircleHoriz, myCircleVert])
    FB2_leftFish.setImage(showLeftFish)
    FB2_rightFish.setImage(showRightFish)
    FB2_text.setImage(myFeedbackImage)
    # keep track of which components have finished
    doFB2Components = [FB2_face_2, FB2_Circle_2, FB2_leftFish, FB2_rightFish, FB2_text]
    for thisComponent in doFB2Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "doFB2" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *FB2_face_2* updates
        
        # if FB2_face_2 is starting this frame...
        if FB2_face_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB2_face_2.frameNStart = frameN  # exact frame index
            FB2_face_2.tStart = t  # local t and not account for scr refresh
            FB2_face_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB2_face_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB2_face_2.status = STARTED
            FB2_face_2.setAutoDraw(True)
        
        # if FB2_face_2 is active this frame...
        if FB2_face_2.status == STARTED:
            # update params
            pass
        
        # if FB2_face_2 is stopping this frame...
        if FB2_face_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB2_face_2.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB2_face_2.tStop = t  # not accounting for scr refresh
                FB2_face_2.frameNStop = frameN  # exact frame index
                # update status
                FB2_face_2.status = FINISHED
                FB2_face_2.setAutoDraw(False)
        
        # *FB2_Circle_2* updates
        
        # if FB2_Circle_2 is starting this frame...
        if FB2_Circle_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            FB2_Circle_2.frameNStart = frameN  # exact frame index
            FB2_Circle_2.tStart = t  # local t and not account for scr refresh
            FB2_Circle_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB2_Circle_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB2_Circle_2.status = STARTED
            FB2_Circle_2.setAutoDraw(True)
        
        # if FB2_Circle_2 is active this frame...
        if FB2_Circle_2.status == STARTED:
            # update params
            pass
        
        # if FB2_Circle_2 is stopping this frame...
        if FB2_Circle_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB2_Circle_2.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB2_Circle_2.tStop = t  # not accounting for scr refresh
                FB2_Circle_2.frameNStop = frameN  # exact frame index
                # update status
                FB2_Circle_2.status = FINISHED
                FB2_Circle_2.setAutoDraw(False)
        
        # *FB2_leftFish* updates
        
        # if FB2_leftFish is starting this frame...
        if FB2_leftFish.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB2_leftFish.frameNStart = frameN  # exact frame index
            FB2_leftFish.tStart = t  # local t and not account for scr refresh
            FB2_leftFish.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB2_leftFish, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB2_leftFish.status = STARTED
            FB2_leftFish.setAutoDraw(True)
        
        # if FB2_leftFish is active this frame...
        if FB2_leftFish.status == STARTED:
            # update params
            pass
        
        # if FB2_leftFish is stopping this frame...
        if FB2_leftFish.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB2_leftFish.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB2_leftFish.tStop = t  # not accounting for scr refresh
                FB2_leftFish.frameNStop = frameN  # exact frame index
                # update status
                FB2_leftFish.status = FINISHED
                FB2_leftFish.setAutoDraw(False)
        
        # *FB2_rightFish* updates
        
        # if FB2_rightFish is starting this frame...
        if FB2_rightFish.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB2_rightFish.frameNStart = frameN  # exact frame index
            FB2_rightFish.tStart = t  # local t and not account for scr refresh
            FB2_rightFish.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB2_rightFish, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB2_rightFish.status = STARTED
            FB2_rightFish.setAutoDraw(True)
        
        # if FB2_rightFish is active this frame...
        if FB2_rightFish.status == STARTED:
            # update params
            pass
        
        # if FB2_rightFish is stopping this frame...
        if FB2_rightFish.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB2_rightFish.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB2_rightFish.tStop = t  # not accounting for scr refresh
                FB2_rightFish.frameNStop = frameN  # exact frame index
                # update status
                FB2_rightFish.status = FINISHED
                FB2_rightFish.setAutoDraw(False)
        
        # *FB2_text* updates
        
        # if FB2_text is starting this frame...
        if FB2_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB2_text.frameNStart = frameN  # exact frame index
            FB2_text.tStart = t  # local t and not account for scr refresh
            FB2_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB2_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB2_text.status = STARTED
            FB2_text.setAutoDraw(True)
        
        # if FB2_text is active this frame...
        if FB2_text.status == STARTED:
            # update params
            pass
        
        # if FB2_text is stopping this frame...
        if FB2_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB2_text.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB2_text.tStop = t  # not accounting for scr refresh
                FB2_text.frameNStop = frameN  # exact frame index
                # update status
                FB2_text.status = FINISHED
                FB2_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in doFB2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "doFB2" ---
    for thisComponent in doFB2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from FB2_code
    if (myTrialCorrect==False) :
        myErr2 += 1
    if (CriterionReached==True) :
        trials2.finished=True
        myCrit2 = 1
    # the Routine "doFB2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 5 repeats of 'trials2'


# --- Prepare to start Routine "next_stage" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from code_4
CriterionReached=False
myConsecutiveCorrect=0
myCriterion = myCriterion+4

# Run 'Begin Routine' code from start_phase_log
# Update phase number
current_phase += 1

# Initialize trials for the curent phase
current_trial = 1

data_file.write(f"----- PHASE {current_phase} -----\n")
header = "Trial,Face,Left Fish,Right Fish,Correct Response,Subject Response,Response Time,Correct/Incorrect\n"
data_file.write(header)

# keep track of which components have finished
next_stageComponents = []
for thisComponent in next_stageComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "next_stage" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in next_stageComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "next_stage" ---
for thisComponent in next_stageComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "next_stage" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials3 = data.TrialHandler(nReps=5, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('experimentFiles/phase2.csv'),
    seed=None, name='trials3')
thisExp.addLoop(trials3)  # add the loop to the experiment
thisTrials3 = trials3.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrials3.rgb)
if thisTrials3 != None:
    for paramName in thisTrials3:
        exec('{} = thisTrials3[paramName]'.format(paramName))

for thisTrials3 in trials3:
    currentLoop = trials3
    # abbreviate parameter names if possible (e.g. rgb = thisTrials3.rgb)
    if thisTrials3 != None:
        for paramName in thisTrials3:
            exec('{} = thisTrials3[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "runTrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_3
    myFaceFileName= "fishPix/"+face+".png"
    myLeftFishFileName="fishPix/"+leftFish+".png"
    myRightFishFileName="fishPix/"+rightFish+".png"
    trial_face.setImage(myFaceFileName)
    fishOnLeft.setImage(myLeftFishFileName)
    fishOnRight.setImage(myRightFishFileName)
    trial_response.keys = []
    trial_response.rt = []
    _trial_response_allKeys = []
    # keep track of which components have finished
    runTrialComponents = [trial_face, trial_text, fishOnLeft, fishOnRight, trial_response]
    for thisComponent in runTrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "runTrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *trial_face* updates
        
        # if trial_face is starting this frame...
        if trial_face.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            trial_face.frameNStart = frameN  # exact frame index
            trial_face.tStart = t  # local t and not account for scr refresh
            trial_face.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_face, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_face.status = STARTED
            trial_face.setAutoDraw(True)
        
        # if trial_face is active this frame...
        if trial_face.status == STARTED:
            # update params
            pass
        
        # *trial_text* updates
        
        # if trial_text is starting this frame...
        if trial_text.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
            # keep track of start time/frame for later
            trial_text.frameNStart = frameN  # exact frame index
            trial_text.tStart = t  # local t and not account for scr refresh
            trial_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_text.status = STARTED
            trial_text.setAutoDraw(True)
        
        # if trial_text is active this frame...
        if trial_text.status == STARTED:
            # update params
            pass
        
        # *fishOnLeft* updates
        
        # if fishOnLeft is starting this frame...
        if fishOnLeft.status == NOT_STARTED and tThisFlip >= .25-frameTolerance:
            # keep track of start time/frame for later
            fishOnLeft.frameNStart = frameN  # exact frame index
            fishOnLeft.tStart = t  # local t and not account for scr refresh
            fishOnLeft.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fishOnLeft, 'tStartRefresh')  # time at next scr refresh
            # update status
            fishOnLeft.status = STARTED
            fishOnLeft.setAutoDraw(True)
        
        # if fishOnLeft is active this frame...
        if fishOnLeft.status == STARTED:
            # update params
            pass
        
        # *fishOnRight* updates
        
        # if fishOnRight is starting this frame...
        if fishOnRight.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
            # keep track of start time/frame for later
            fishOnRight.frameNStart = frameN  # exact frame index
            fishOnRight.tStart = t  # local t and not account for scr refresh
            fishOnRight.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fishOnRight, 'tStartRefresh')  # time at next scr refresh
            # update status
            fishOnRight.status = STARTED
            fishOnRight.setAutoDraw(True)
        
        # if fishOnRight is active this frame...
        if fishOnRight.status == STARTED:
            # update params
            pass
        
        # *trial_response* updates
        waitOnFlip = False
        
        # if trial_response is starting this frame...
        if trial_response.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            trial_response.frameNStart = frameN  # exact frame index
            trial_response.tStart = t  # local t and not account for scr refresh
            trial_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_response, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(trial_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(trial_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if trial_response.status == STARTED and not waitOnFlip:
            theseKeys = trial_response.getKeys(keyList=['z','m','left','right'], waitRelease=False)
            _trial_response_allKeys.extend(theseKeys)
            if len(_trial_response_allKeys):
                trial_response.keys = _trial_response_allKeys[-1].name  # just the last key pressed
                trial_response.rt = _trial_response_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in runTrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "runTrial" ---
    for thisComponent in runTrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if trial_response.keys in ['', [], None]:  # No response was made
        trial_response.keys = None
    trials3.addData('trial_response.keys',trial_response.keys)
    if trial_response.keys != None:  # we had a response
        trials3.addData('trial_response.rt', trial_response.rt)
    # Run 'End Routine' code from code
    nFBleft=0
    nFBright=0
    
    if(trial_response.keys == "z"):
        trial_response.keys = "left"
    if(trial_response.keys == "m"):
        trial_response.keys = "right"
        
    
    if (trial_response.keys=='left') :
        myChosen="left"
        myCircleHoriz = -0.13
    else :
        myChosen="right"
        myCircleHoriz = 0.22
    if (trial_response.keys==correctResponse) :
        myTrialCorrect=True
        thisExp.addData('Correct',1)
        myTally = myTally + 1
        myFeedbackImage="fishPix/win.png"
        myConsecutiveCorrect = myConsecutiveCorrect+1
        if (myConsecutiveCorrect >= myCriterion) :
            CriterionReached=True
    else :
        myTrialCorrect=False
        thisExp.addData('Correct',0)
        myFeedbackImage="fishPix/lose.png"
        myConsecutiveCorrect = 0
    if (correctResponse=="left") :
        showLeftFish=myLeftFishFileName
        showRightFish="fishPix/blank.png"
    else :
        showLeftFish="fishPix/blank.png"
        showRightFish=myRightFishFileName
    
    # Run 'End Routine' code from log_trial
    correct = ""
    if(trial_response.keys == correctResponse):
        # We do a string so we can concatenate an asterisk to it for critical pairs
        correct = "1" # 1 if correct, 0 otherwise
    else:
        correct = "0"
    
    # Add a star if this stimulus contains a critical pair
    stim_vars = [face, leftFish, rightFish, correctResponse]
    stim = ",".join(stim_vars)
    if (stim in crit_pairs_stims):
        correct += "*"
        
    # Keeping track of overall scores
    # phases < 3 are acquisition, phase 3 is testing retention and generalization
    if(current_phase < 3 and correct == "1"): 
        acquisition_score += 1
    elif(correct == "1"): # We are in phase 3, correct answer, but no critical pair
        retention_score += 1
    elif(correct == "1*"): # We are in phase 3, correct answer, but no critical pair
        generalization_score += 1
    
    # Update the number of trials 
    # phases < 3 are acquisition, phase 3 is testing retention and generalization
    if(current_phase < 3):
        acquisition_trials += 1
    # If not a critical pair (no asterisk), it is retention
    elif("*" not in correct):
        retention_trials += 1
    # if it is a critical pair then it is generalization
    else:
        generalization_trials += 1
        
    
    # Convert all the variables we want to log into strings and store them in a list
    # so we can join them later
    log_vars = [ str(x) for x in [current_trial, face, leftFish, rightFish, 
                correctResponse, trial_response.keys, trial_response.rt, correct]]
    
    log_text = ",".join(log_vars) + "\n"
    data_file.write(log_text)
    
    current_trial += 1
    # the Routine "runTrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "doFB3" ---
    continueRoutine = True
    # update component parameters for each repeat
    FB3_face.setImage(myFaceFileName)
    FB3_Circle.setPos([myCircleHoriz, myCircleVert])
    FB3_leftFish.setImage(showLeftFish)
    FB3_rightFish.setImage(showRightFish)
    FB3_text.setImage(myFeedbackImage)
    # keep track of which components have finished
    doFB3Components = [FB3_face, FB3_Circle, FB3_leftFish, FB3_rightFish, FB3_text]
    for thisComponent in doFB3Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "doFB3" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *FB3_face* updates
        
        # if FB3_face is starting this frame...
        if FB3_face.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB3_face.frameNStart = frameN  # exact frame index
            FB3_face.tStart = t  # local t and not account for scr refresh
            FB3_face.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB3_face, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB3_face.status = STARTED
            FB3_face.setAutoDraw(True)
        
        # if FB3_face is active this frame...
        if FB3_face.status == STARTED:
            # update params
            pass
        
        # if FB3_face is stopping this frame...
        if FB3_face.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB3_face.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB3_face.tStop = t  # not accounting for scr refresh
                FB3_face.frameNStop = frameN  # exact frame index
                # update status
                FB3_face.status = FINISHED
                FB3_face.setAutoDraw(False)
        
        # *FB3_Circle* updates
        
        # if FB3_Circle is starting this frame...
        if FB3_Circle.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            FB3_Circle.frameNStart = frameN  # exact frame index
            FB3_Circle.tStart = t  # local t and not account for scr refresh
            FB3_Circle.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB3_Circle, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB3_Circle.status = STARTED
            FB3_Circle.setAutoDraw(True)
        
        # if FB3_Circle is active this frame...
        if FB3_Circle.status == STARTED:
            # update params
            pass
        
        # if FB3_Circle is stopping this frame...
        if FB3_Circle.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB3_Circle.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB3_Circle.tStop = t  # not accounting for scr refresh
                FB3_Circle.frameNStop = frameN  # exact frame index
                # update status
                FB3_Circle.status = FINISHED
                FB3_Circle.setAutoDraw(False)
        
        # *FB3_leftFish* updates
        
        # if FB3_leftFish is starting this frame...
        if FB3_leftFish.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB3_leftFish.frameNStart = frameN  # exact frame index
            FB3_leftFish.tStart = t  # local t and not account for scr refresh
            FB3_leftFish.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB3_leftFish, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB3_leftFish.status = STARTED
            FB3_leftFish.setAutoDraw(True)
        
        # if FB3_leftFish is active this frame...
        if FB3_leftFish.status == STARTED:
            # update params
            pass
        
        # if FB3_leftFish is stopping this frame...
        if FB3_leftFish.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB3_leftFish.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB3_leftFish.tStop = t  # not accounting for scr refresh
                FB3_leftFish.frameNStop = frameN  # exact frame index
                # update status
                FB3_leftFish.status = FINISHED
                FB3_leftFish.setAutoDraw(False)
        
        # *FB3_rightFish* updates
        
        # if FB3_rightFish is starting this frame...
        if FB3_rightFish.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB3_rightFish.frameNStart = frameN  # exact frame index
            FB3_rightFish.tStart = t  # local t and not account for scr refresh
            FB3_rightFish.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB3_rightFish, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB3_rightFish.status = STARTED
            FB3_rightFish.setAutoDraw(True)
        
        # if FB3_rightFish is active this frame...
        if FB3_rightFish.status == STARTED:
            # update params
            pass
        
        # if FB3_rightFish is stopping this frame...
        if FB3_rightFish.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB3_rightFish.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB3_rightFish.tStop = t  # not accounting for scr refresh
                FB3_rightFish.frameNStop = frameN  # exact frame index
                # update status
                FB3_rightFish.status = FINISHED
                FB3_rightFish.setAutoDraw(False)
        
        # *FB3_text* updates
        
        # if FB3_text is starting this frame...
        if FB3_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            FB3_text.frameNStart = frameN  # exact frame index
            FB3_text.tStart = t  # local t and not account for scr refresh
            FB3_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(FB3_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            FB3_text.status = STARTED
            FB3_text.setAutoDraw(True)
        
        # if FB3_text is active this frame...
        if FB3_text.status == STARTED:
            # update params
            pass
        
        # if FB3_text is stopping this frame...
        if FB3_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > FB3_text.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                FB3_text.tStop = t  # not accounting for scr refresh
                FB3_text.frameNStop = frameN  # exact frame index
                # update status
                FB3_text.status = FINISHED
                FB3_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in doFB3Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "doFB3" ---
    for thisComponent in doFB3Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from FB3_code
    if (myTrialCorrect==False) :
        myErr3 += 1
    if (CriterionReached==True) :
        trials3.finished=True
        myCrit3 = 1
    # the Routine "doFB3" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 5 repeats of 'trials3'


# --- Prepare to start Routine "test_instr" ---
continueRoutine = True
# update component parameters for each repeat
test_instr_key.keys = []
test_instr_key.rt = []
_test_instr_key_allKeys = []
# Run 'Begin Routine' code from start_phase_log_test
# Update phase number
current_phase += 1

# Initialize trials for the curent phase
current_trial = 1


data_file.write(f"----- PHASE {current_phase} -----\n")
header = "Trial,Face,Left Fish,Right Fish,Correct Response,Subject Response,Response Time,Correct/Incorrect\n"
data_file.write(header)

# keep track of which components have finished
test_instrComponents = [test_text1, test_text2, test_text3, test_text4, test_text5, test_text6, test_text7, test_text8, test_instr_key]
for thisComponent in test_instrComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "test_instr" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *test_text1* updates
    
    # if test_text1 is starting this frame...
    if test_text1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        test_text1.frameNStart = frameN  # exact frame index
        test_text1.tStart = t  # local t and not account for scr refresh
        test_text1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_text1, 'tStartRefresh')  # time at next scr refresh
        # update status
        test_text1.status = STARTED
        test_text1.setAutoDraw(True)
    
    # if test_text1 is active this frame...
    if test_text1.status == STARTED:
        # update params
        pass
    
    # *test_text2* updates
    
    # if test_text2 is starting this frame...
    if test_text2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        test_text2.frameNStart = frameN  # exact frame index
        test_text2.tStart = t  # local t and not account for scr refresh
        test_text2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_text2, 'tStartRefresh')  # time at next scr refresh
        # update status
        test_text2.status = STARTED
        test_text2.setAutoDraw(True)
    
    # if test_text2 is active this frame...
    if test_text2.status == STARTED:
        # update params
        pass
    
    # *test_text3* updates
    
    # if test_text3 is starting this frame...
    if test_text3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        test_text3.frameNStart = frameN  # exact frame index
        test_text3.tStart = t  # local t and not account for scr refresh
        test_text3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_text3, 'tStartRefresh')  # time at next scr refresh
        # update status
        test_text3.status = STARTED
        test_text3.setAutoDraw(True)
    
    # if test_text3 is active this frame...
    if test_text3.status == STARTED:
        # update params
        pass
    
    # *test_text4* updates
    
    # if test_text4 is starting this frame...
    if test_text4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        test_text4.frameNStart = frameN  # exact frame index
        test_text4.tStart = t  # local t and not account for scr refresh
        test_text4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_text4, 'tStartRefresh')  # time at next scr refresh
        # update status
        test_text4.status = STARTED
        test_text4.setAutoDraw(True)
    
    # if test_text4 is active this frame...
    if test_text4.status == STARTED:
        # update params
        pass
    
    # *test_text5* updates
    
    # if test_text5 is starting this frame...
    if test_text5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        test_text5.frameNStart = frameN  # exact frame index
        test_text5.tStart = t  # local t and not account for scr refresh
        test_text5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_text5, 'tStartRefresh')  # time at next scr refresh
        # update status
        test_text5.status = STARTED
        test_text5.setAutoDraw(True)
    
    # if test_text5 is active this frame...
    if test_text5.status == STARTED:
        # update params
        pass
    
    # *test_text6* updates
    
    # if test_text6 is starting this frame...
    if test_text6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        test_text6.frameNStart = frameN  # exact frame index
        test_text6.tStart = t  # local t and not account for scr refresh
        test_text6.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_text6, 'tStartRefresh')  # time at next scr refresh
        # update status
        test_text6.status = STARTED
        test_text6.setAutoDraw(True)
    
    # if test_text6 is active this frame...
    if test_text6.status == STARTED:
        # update params
        pass
    
    # *test_text7* updates
    
    # if test_text7 is starting this frame...
    if test_text7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        test_text7.frameNStart = frameN  # exact frame index
        test_text7.tStart = t  # local t and not account for scr refresh
        test_text7.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_text7, 'tStartRefresh')  # time at next scr refresh
        # update status
        test_text7.status = STARTED
        test_text7.setAutoDraw(True)
    
    # if test_text7 is active this frame...
    if test_text7.status == STARTED:
        # update params
        pass
    
    # *test_text8* updates
    
    # if test_text8 is starting this frame...
    if test_text8.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        test_text8.frameNStart = frameN  # exact frame index
        test_text8.tStart = t  # local t and not account for scr refresh
        test_text8.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_text8, 'tStartRefresh')  # time at next scr refresh
        # update status
        test_text8.status = STARTED
        test_text8.setAutoDraw(True)
    
    # if test_text8 is active this frame...
    if test_text8.status == STARTED:
        # update params
        pass
    
    # *test_instr_key* updates
    waitOnFlip = False
    
    # if test_instr_key is starting this frame...
    if test_instr_key.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
        # keep track of start time/frame for later
        test_instr_key.frameNStart = frameN  # exact frame index
        test_instr_key.tStart = t  # local t and not account for scr refresh
        test_instr_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(test_instr_key, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'test_instr_key.started')
        # update status
        test_instr_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(test_instr_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(test_instr_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if test_instr_key.status == STARTED and not waitOnFlip:
        theseKeys = test_instr_key.getKeys(keyList=['z','m','left','right'], waitRelease=False)
        _test_instr_key_allKeys.extend(theseKeys)
        if len(_test_instr_key_allKeys):
            test_instr_key.keys = _test_instr_key_allKeys[-1].name  # just the last key pressed
            test_instr_key.rt = _test_instr_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in test_instrComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "test_instr" ---
for thisComponent in test_instrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "test_instr" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
test_trials = data.TrialHandler(nReps=3, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('experimentFiles/phase3.csv'),
    seed=None, name='test_trials')
thisExp.addLoop(test_trials)  # add the loop to the experiment
thisTest_trial = test_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTest_trial.rgb)
if thisTest_trial != None:
    for paramName in thisTest_trial:
        exec('{} = thisTest_trial[paramName]'.format(paramName))

for thisTest_trial in test_trials:
    currentLoop = test_trials
    # abbreviate parameter names if possible (e.g. rgb = thisTest_trial.rgb)
    if thisTest_trial != None:
        for paramName in thisTest_trial:
            exec('{} = thisTest_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "runTrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_3
    myFaceFileName= "fishPix/"+face+".png"
    myLeftFishFileName="fishPix/"+leftFish+".png"
    myRightFishFileName="fishPix/"+rightFish+".png"
    trial_face.setImage(myFaceFileName)
    fishOnLeft.setImage(myLeftFishFileName)
    fishOnRight.setImage(myRightFishFileName)
    trial_response.keys = []
    trial_response.rt = []
    _trial_response_allKeys = []
    # keep track of which components have finished
    runTrialComponents = [trial_face, trial_text, fishOnLeft, fishOnRight, trial_response]
    for thisComponent in runTrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "runTrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *trial_face* updates
        
        # if trial_face is starting this frame...
        if trial_face.status == NOT_STARTED and tThisFlip >= 0.1-frameTolerance:
            # keep track of start time/frame for later
            trial_face.frameNStart = frameN  # exact frame index
            trial_face.tStart = t  # local t and not account for scr refresh
            trial_face.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_face, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_face.status = STARTED
            trial_face.setAutoDraw(True)
        
        # if trial_face is active this frame...
        if trial_face.status == STARTED:
            # update params
            pass
        
        # *trial_text* updates
        
        # if trial_text is starting this frame...
        if trial_text.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
            # keep track of start time/frame for later
            trial_text.frameNStart = frameN  # exact frame index
            trial_text.tStart = t  # local t and not account for scr refresh
            trial_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_text.status = STARTED
            trial_text.setAutoDraw(True)
        
        # if trial_text is active this frame...
        if trial_text.status == STARTED:
            # update params
            pass
        
        # *fishOnLeft* updates
        
        # if fishOnLeft is starting this frame...
        if fishOnLeft.status == NOT_STARTED and tThisFlip >= .25-frameTolerance:
            # keep track of start time/frame for later
            fishOnLeft.frameNStart = frameN  # exact frame index
            fishOnLeft.tStart = t  # local t and not account for scr refresh
            fishOnLeft.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fishOnLeft, 'tStartRefresh')  # time at next scr refresh
            # update status
            fishOnLeft.status = STARTED
            fishOnLeft.setAutoDraw(True)
        
        # if fishOnLeft is active this frame...
        if fishOnLeft.status == STARTED:
            # update params
            pass
        
        # *fishOnRight* updates
        
        # if fishOnRight is starting this frame...
        if fishOnRight.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
            # keep track of start time/frame for later
            fishOnRight.frameNStart = frameN  # exact frame index
            fishOnRight.tStart = t  # local t and not account for scr refresh
            fishOnRight.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fishOnRight, 'tStartRefresh')  # time at next scr refresh
            # update status
            fishOnRight.status = STARTED
            fishOnRight.setAutoDraw(True)
        
        # if fishOnRight is active this frame...
        if fishOnRight.status == STARTED:
            # update params
            pass
        
        # *trial_response* updates
        waitOnFlip = False
        
        # if trial_response is starting this frame...
        if trial_response.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
            # keep track of start time/frame for later
            trial_response.frameNStart = frameN  # exact frame index
            trial_response.tStart = t  # local t and not account for scr refresh
            trial_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_response, 'tStartRefresh')  # time at next scr refresh
            # update status
            trial_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(trial_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(trial_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if trial_response.status == STARTED and not waitOnFlip:
            theseKeys = trial_response.getKeys(keyList=['z','m','left','right'], waitRelease=False)
            _trial_response_allKeys.extend(theseKeys)
            if len(_trial_response_allKeys):
                trial_response.keys = _trial_response_allKeys[-1].name  # just the last key pressed
                trial_response.rt = _trial_response_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in runTrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "runTrial" ---
    for thisComponent in runTrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if trial_response.keys in ['', [], None]:  # No response was made
        trial_response.keys = None
    test_trials.addData('trial_response.keys',trial_response.keys)
    if trial_response.keys != None:  # we had a response
        test_trials.addData('trial_response.rt', trial_response.rt)
    # Run 'End Routine' code from code
    nFBleft=0
    nFBright=0
    
    if(trial_response.keys == "z"):
        trial_response.keys = "left"
    if(trial_response.keys == "m"):
        trial_response.keys = "right"
        
    
    if (trial_response.keys=='left') :
        myChosen="left"
        myCircleHoriz = -0.13
    else :
        myChosen="right"
        myCircleHoriz = 0.22
    if (trial_response.keys==correctResponse) :
        myTrialCorrect=True
        thisExp.addData('Correct',1)
        myTally = myTally + 1
        myFeedbackImage="fishPix/win.png"
        myConsecutiveCorrect = myConsecutiveCorrect+1
        if (myConsecutiveCorrect >= myCriterion) :
            CriterionReached=True
    else :
        myTrialCorrect=False
        thisExp.addData('Correct',0)
        myFeedbackImage="fishPix/lose.png"
        myConsecutiveCorrect = 0
    if (correctResponse=="left") :
        showLeftFish=myLeftFishFileName
        showRightFish="fishPix/blank.png"
    else :
        showLeftFish="fishPix/blank.png"
        showRightFish=myRightFishFileName
    
    # Run 'End Routine' code from log_trial
    correct = ""
    if(trial_response.keys == correctResponse):
        # We do a string so we can concatenate an asterisk to it for critical pairs
        correct = "1" # 1 if correct, 0 otherwise
    else:
        correct = "0"
    
    # Add a star if this stimulus contains a critical pair
    stim_vars = [face, leftFish, rightFish, correctResponse]
    stim = ",".join(stim_vars)
    if (stim in crit_pairs_stims):
        correct += "*"
        
    # Keeping track of overall scores
    # phases < 3 are acquisition, phase 3 is testing retention and generalization
    if(current_phase < 3 and correct == "1"): 
        acquisition_score += 1
    elif(correct == "1"): # We are in phase 3, correct answer, but no critical pair
        retention_score += 1
    elif(correct == "1*"): # We are in phase 3, correct answer, but no critical pair
        generalization_score += 1
    
    # Update the number of trials 
    # phases < 3 are acquisition, phase 3 is testing retention and generalization
    if(current_phase < 3):
        acquisition_trials += 1
    # If not a critical pair (no asterisk), it is retention
    elif("*" not in correct):
        retention_trials += 1
    # if it is a critical pair then it is generalization
    else:
        generalization_trials += 1
        
    
    # Convert all the variables we want to log into strings and store them in a list
    # so we can join them later
    log_vars = [ str(x) for x in [current_trial, face, leftFish, rightFish, 
                correctResponse, trial_response.keys, trial_response.rt, correct]]
    
    log_text = ",".join(log_vars) + "\n"
    data_file.write(log_text)
    
    current_trial += 1
    # the Routine "runTrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "noFB" ---
    continueRoutine = True
    # update component parameters for each repeat
    noFB_face.setImage(myFaceFileName)
    noFB_Circle.setPos([myCircleHoriz, myCircleVert])
    noFB_leftFish.setImage(myLeftFishFileName)
    noFB_rightFish.setImage(myRightFishFileName)
    # keep track of which components have finished
    noFBComponents = [noFB_face, noFB_Circle, noFB_leftFish, noFB_rightFish]
    for thisComponent in noFBComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "noFB" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *noFB_face* updates
        
        # if noFB_face is starting this frame...
        if noFB_face.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            noFB_face.frameNStart = frameN  # exact frame index
            noFB_face.tStart = t  # local t and not account for scr refresh
            noFB_face.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(noFB_face, 'tStartRefresh')  # time at next scr refresh
            # update status
            noFB_face.status = STARTED
            noFB_face.setAutoDraw(True)
        
        # if noFB_face is active this frame...
        if noFB_face.status == STARTED:
            # update params
            pass
        
        # if noFB_face is stopping this frame...
        if noFB_face.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > noFB_face.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                noFB_face.tStop = t  # not accounting for scr refresh
                noFB_face.frameNStop = frameN  # exact frame index
                # update status
                noFB_face.status = FINISHED
                noFB_face.setAutoDraw(False)
        
        # *noFB_Circle* updates
        
        # if noFB_Circle is starting this frame...
        if noFB_Circle.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            noFB_Circle.frameNStart = frameN  # exact frame index
            noFB_Circle.tStart = t  # local t and not account for scr refresh
            noFB_Circle.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(noFB_Circle, 'tStartRefresh')  # time at next scr refresh
            # update status
            noFB_Circle.status = STARTED
            noFB_Circle.setAutoDraw(True)
        
        # if noFB_Circle is active this frame...
        if noFB_Circle.status == STARTED:
            # update params
            pass
        
        # if noFB_Circle is stopping this frame...
        if noFB_Circle.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > noFB_Circle.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                noFB_Circle.tStop = t  # not accounting for scr refresh
                noFB_Circle.frameNStop = frameN  # exact frame index
                # update status
                noFB_Circle.status = FINISHED
                noFB_Circle.setAutoDraw(False)
        
        # *noFB_leftFish* updates
        
        # if noFB_leftFish is starting this frame...
        if noFB_leftFish.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            noFB_leftFish.frameNStart = frameN  # exact frame index
            noFB_leftFish.tStart = t  # local t and not account for scr refresh
            noFB_leftFish.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(noFB_leftFish, 'tStartRefresh')  # time at next scr refresh
            # update status
            noFB_leftFish.status = STARTED
            noFB_leftFish.setAutoDraw(True)
        
        # if noFB_leftFish is active this frame...
        if noFB_leftFish.status == STARTED:
            # update params
            pass
        
        # if noFB_leftFish is stopping this frame...
        if noFB_leftFish.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > noFB_leftFish.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                noFB_leftFish.tStop = t  # not accounting for scr refresh
                noFB_leftFish.frameNStop = frameN  # exact frame index
                # update status
                noFB_leftFish.status = FINISHED
                noFB_leftFish.setAutoDraw(False)
        
        # *noFB_rightFish* updates
        
        # if noFB_rightFish is starting this frame...
        if noFB_rightFish.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            noFB_rightFish.frameNStart = frameN  # exact frame index
            noFB_rightFish.tStart = t  # local t and not account for scr refresh
            noFB_rightFish.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(noFB_rightFish, 'tStartRefresh')  # time at next scr refresh
            # update status
            noFB_rightFish.status = STARTED
            noFB_rightFish.setAutoDraw(True)
        
        # if noFB_rightFish is active this frame...
        if noFB_rightFish.status == STARTED:
            # update params
            pass
        
        # if noFB_rightFish is stopping this frame...
        if noFB_rightFish.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > noFB_rightFish.tStartRefresh + myISIduration-frameTolerance:
                # keep track of stop time/frame for later
                noFB_rightFish.tStop = t  # not accounting for scr refresh
                noFB_rightFish.frameNStop = frameN  # exact frame index
                # update status
                noFB_rightFish.status = FINISHED
                noFB_rightFish.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in noFBComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "noFB" ---
    for thisComponent in noFBComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_5
    if ("*" in correct) :
        myNewTrials+=1
    else :
        myOldTrials+=1
    if (myTrialCorrect==False) :
        if ("*" in correct) :
            myNewErr+=1
        else :
            myOldErr+=1
    # the Routine "noFB" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 3 repeats of 'test_trials'


# --- Prepare to start Routine "goodbye" ---
continueRoutine = True
# update component parameters for each repeat
goodbye_key.keys = []
goodbye_key.rt = []
_goodbye_key_allKeys = []
# Run 'Begin Routine' code from end_data_log
# Calculate ratios and convert to string
generalization = str(generalization_score/generalization_trials)
retention = str(retention_score/retention_trials)
acquisition = str(acquisition_score/acquisition_trials)
# Join scores with commas
summary = ",".join([generalization, retention, acquisition, str(acquisition_trials)])

# Write summary to file
data_file.write("----- SUMMARY STATISTICS -----\n")
data_file.write("Generalization,Retention,Acquisition,Acquisition Trials\n")
data_file.write(summary)

# Close file
data_file.close()
# keep track of which components have finished
goodbyeComponents = [goodbye_text1, goodbye_text2, goodbye_tally, goodbye_text3, goodbye_text4, goodbye_key]
for thisComponent in goodbyeComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "goodbye" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *goodbye_text1* updates
    
    # if goodbye_text1 is starting this frame...
    if goodbye_text1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        goodbye_text1.frameNStart = frameN  # exact frame index
        goodbye_text1.tStart = t  # local t and not account for scr refresh
        goodbye_text1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(goodbye_text1, 'tStartRefresh')  # time at next scr refresh
        # update status
        goodbye_text1.status = STARTED
        goodbye_text1.setAutoDraw(True)
    
    # if goodbye_text1 is active this frame...
    if goodbye_text1.status == STARTED:
        # update params
        pass
    
    # *goodbye_text2* updates
    
    # if goodbye_text2 is starting this frame...
    if goodbye_text2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        goodbye_text2.frameNStart = frameN  # exact frame index
        goodbye_text2.tStart = t  # local t and not account for scr refresh
        goodbye_text2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(goodbye_text2, 'tStartRefresh')  # time at next scr refresh
        # update status
        goodbye_text2.status = STARTED
        goodbye_text2.setAutoDraw(True)
    
    # if goodbye_text2 is active this frame...
    if goodbye_text2.status == STARTED:
        # update params
        pass
    
    # *goodbye_tally* updates
    
    # if goodbye_tally is starting this frame...
    if goodbye_tally.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        goodbye_tally.frameNStart = frameN  # exact frame index
        goodbye_tally.tStart = t  # local t and not account for scr refresh
        goodbye_tally.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(goodbye_tally, 'tStartRefresh')  # time at next scr refresh
        # update status
        goodbye_tally.status = STARTED
        goodbye_tally.setAutoDraw(True)
    
    # if goodbye_tally is active this frame...
    if goodbye_tally.status == STARTED:
        # update params
        goodbye_tally.setText(myTally, log=False)
    
    # *goodbye_text3* updates
    
    # if goodbye_text3 is starting this frame...
    if goodbye_text3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        goodbye_text3.frameNStart = frameN  # exact frame index
        goodbye_text3.tStart = t  # local t and not account for scr refresh
        goodbye_text3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(goodbye_text3, 'tStartRefresh')  # time at next scr refresh
        # update status
        goodbye_text3.status = STARTED
        goodbye_text3.setAutoDraw(True)
    
    # if goodbye_text3 is active this frame...
    if goodbye_text3.status == STARTED:
        # update params
        pass
    
    # *goodbye_text4* updates
    
    # if goodbye_text4 is starting this frame...
    if goodbye_text4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        goodbye_text4.frameNStart = frameN  # exact frame index
        goodbye_text4.tStart = t  # local t and not account for scr refresh
        goodbye_text4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(goodbye_text4, 'tStartRefresh')  # time at next scr refresh
        # update status
        goodbye_text4.status = STARTED
        goodbye_text4.setAutoDraw(True)
    
    # if goodbye_text4 is active this frame...
    if goodbye_text4.status == STARTED:
        # update params
        pass
    
    # *goodbye_key* updates
    waitOnFlip = False
    
    # if goodbye_key is starting this frame...
    if goodbye_key.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
        # keep track of start time/frame for later
        goodbye_key.frameNStart = frameN  # exact frame index
        goodbye_key.tStart = t  # local t and not account for scr refresh
        goodbye_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(goodbye_key, 'tStartRefresh')  # time at next scr refresh
        # update status
        goodbye_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(goodbye_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(goodbye_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if goodbye_key.status == STARTED and not waitOnFlip:
        theseKeys = goodbye_key.getKeys(keyList=['space'], waitRelease=False)
        _goodbye_key_allKeys.extend(theseKeys)
        if len(_goodbye_key_allKeys):
            goodbye_key.keys = _goodbye_key_allKeys[-1].name  # just the last key pressed
            goodbye_key.rt = _goodbye_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in goodbyeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "goodbye" ---
for thisComponent in goodbyeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "goodbye" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
# Run 'End Experiment' code from code_6
thisExp.addData('Err1',myErr1)
thisExp.addData('Err2',myErr2)
thisExp.addData('Err3',myErr3)
thisExp.addData('Crit1',myCrit1)
thisExp.addData('Crit2',myCrit2)
thisExp.addData('Crit3',myCrit3)
thisExp.addData('PctErrTestOld',100*myOldErr/myOldTrials)
thisExp.addData('PctErrTestNew',100*myNewErr/myNewTrials)

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
