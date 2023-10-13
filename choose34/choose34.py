#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.2),
    on October 13, 2023, at 14:11
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
prefs.hardware['audioLatencyMode'] = '3'
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

# Run 'Before Experiment' code from imports
import random
import csv
import datetime
# Run 'Before Experiment' code from constants
assetsPath = "./assets/"
trainingPath =  "./assets/training/"
testingPath = "./assets/testing/"
expFilesPath = "./experimentFiles/"
dataPath = "./data/"
summariesPath = dataPath + "summaries/"

expDateTime = datetime.datetime.now()
# Weekday(full name), Month(full name) Day(dd), Year(yyyy)
date = "\"" + expDateTime.strftime("%A, %B %d, %Y") + "\""
# Hour(00-12):Minute(00-59):Second(00-59) AM/PM
time = "\"" + expDateTime.strftime("%I:%M:%S %p") + "\""

stimsFieldNames = ["Left_Stim", "Right_Stim"]
leftKey = 'z'
rightKey = 'm'

practicePair = ["circle", "triangle"]

# Stores the testing phase equivalent of every pair ofobjects 
# from the training phase. Each entry is one pair:
# pairs[<(trainObj1, trainObj2)>] == (testObj1, testObj2)
pairs = {
    ("s3c1", "s3c2"): ("s3c1", "s3c2"),
    ("s1c3", "s2c3"): ("s1c96", "s2c96"),
    ("s10c8", "s10c98"): ("s13c8", "s13c98"),
    ("s8c11", "s9c11"): ("s8c26", "s9c26"),
    ("s18c15", "s18c16"): ("s21c15", "s21c16"),
    ("s15c17", "s16c17"): ("s15c5", "s16c5"),
    ("s24c22", "s24c23"): ("s25c22", "s25c23"),
    ("s22c24", "s23c24"): ("s22c25", "s23c25")
    }

# Run 'Before Experiment' code from initializeVars

# This dictionary tells which object has a smiley 
# it has the format {<object_name> : True/False}.
hasSmiley = {}

# First practice answer is always wrong. So we assigned the smiley AFTER
# subject's response. We use this variable to determine if we have assigned 
# the smiley yet
firstChoice = True

# We use this variable to determine what phase we are in and 
# update it accordingly
currentPhase = "practice"

# Changes on trialLoop
consecutiveCorrectResponses = 0

# Initialized to avoid errors
Right_Stim = ""
Left_Stim = ""

evalToCriterion = True

showPostPractice = True
# Run 'Before Experiment' code from dataSummaryVars
trainAccuracy = 0
trainAvgRT = 0.0
trainError = 0
trainTrials = 0

probeAccuracy = 0
probeAvgRT = 0.0
probeError = 0
probeTrials = 0


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.2'
expName = 'Choose34'  # from the Builder filename that created this script
expInfo = {
    'Participant': '',
    'Experimenter': '',
    'Language': 'english',
    'Condition': 'C',
    'Number of pairs': '8',
    'Evaluate to criterion or fixed number of trials?': 'criterion',
    'Training phase max blocks': '6',
    'Testing phase max blocks': '6',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s' % (expName, expInfo['Participant'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\josel\\gluck_lab\\GluckLab\\choose34\\choose34.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1920, 1200], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[1.0000, 1.0000, 1.0000], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True, 
    units='height')
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

# --- Initialize components for Routine "setup" ---
# Run 'Begin Experiment' code from validateExpInfo
if(expInfo["Condition"] != "C" and expInfo["Condition"] != "S"):
    print("Condition must be \"C\" or \"S\"", file=sys.stderr)
    exit()
if(not expInfo["Number of pairs"].isdigit()):
   print("Number of pairs must be a positive number in the range [1,8]", file=sys.stderr) 
   exit()
if(int(expInfo["Number of pairs"]) > 8 or int(expInfo["Number of pairs"]) < 1):
    print("Number of pairs must be in the range [1,8]", file=sys.stderr)
    exit()
    
critOrFixed = expInfo["Evaluate to criterion or fixed number of trials?"]
if(critOrFixed in set(["criterion", "Criterion"])):
    evalToCriterion = True
elif(critOrFixed in set(["fixed", "Fixed"])):
    evalToCriterion = False
else:
    print("Evaluate to criterion or fixed number of trials must set to either 'criterion' or 'fixed'", file=sys.stderr)
    exit()
    
if(not expInfo["Training phase max blocks"].isdigit() or not expInfo["Testing phase max blocks"].isdigit()):
    print("Max blocks must be a number", file=sys.stderr) 
    exit()
# Run 'Begin Experiment' code from constants

delPairs = 8 - int(expInfo["Number of pairs"])
if(delPairs > 0):
    pairsToDelete = random.sample(pairs.keys(), delPairs)
    for pair in pairsToDelete:
        pairs.pop(pair)
        

# Run 'Begin Experiment' code from initializeVars
# Number of consecutive correct responses needed to move to next phase
# this changes in the trialBlocks loop
criterion = int(expInfo["Number of pairs"]) * 2

trialNumReps = {"practice": 6,
                "training" : int(expInfo["Training phase max blocks"]),
                "testing" : int(expInfo["Testing phase max blocks"])
                }
# Run 'Begin Experiment' code from assignSmiley
practice0, practice1 = practicePair

# Initially both practice objects have no smiley. This changes based on the
# subject's first choice. 
hasSmiley[practice0] = False
hasSmiley[practice1] = False

for pair in pairs:
    train0, train1 = pair
    test0, test1 = pairs[pair]
    
    r = random.randint(0,1)
    
    if(r == 0):
        hasSmiley[train0] = True
        hasSmiley[train1] = False
        hasSmiley[test0] = True
        hasSmiley[test1] = False
    else:
        hasSmiley[train0] = False
        hasSmiley[train1] = True
        hasSmiley[test0] = False
        hasSmiley[test1] = True
        

# Run 'Begin Experiment' code from generateStimFiles
with open(expFilesPath + "training.csv", "w") as f1:
    with open(expFilesPath + "testing.csv", "w") as f2:
        f1.write("Left_Stim,Right_Stim,Correct_Response\n")
        f2.write("Left_Stim,Right_Stim,Correct_Response\n")
        for pair in pairs:
            train0, train1 = pair
            test0, test1 = pairs[pair]
            if(hasSmiley[train0] and hasSmiley[test0]):
                f1.write(f"{train0},{train1},left\n")
                f1.write(f"{train1},{train0},right\n")
                f2.write(f"{test0},{test1},left\n")
                f2.write(f"{test1},{test0},right\n")
            else:
                f1.write(f"{train0},{train1},right\n")
                f1.write(f"{train1},{train0},left\n")
                f2.write(f"{test0},{test1},right\n")
                f2.write(f"{test1},{test0},left\n")
                
with open(expFilesPath + "practice.csv", "w") as f:
    f.write("Left_Stim,Right_Stim\n")
    practice0, practice1 = practicePair
    f.write(f"{practice0},{practice1}\n")
    f.write(f"{practice1},{practice0}\n")
# Run 'Begin Experiment' code from language
language = expInfo["Language"].lower()
if(language == "spanish" or language == "español"):
    language = "spanish"
elif(language == "english"):
    language = "english"

texts = {}

with open(os.path.join(expFilesPath, "texts.csv"), mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        texts[row["text_object"]] = row[language].replace("\\n","\n")

# --- Initialize components for Routine "copyrightInfo" ---
copyright = visual.TextStim(win=win, name='copyright',
    text='Choose 34, running on PsychoPy (v.2023.1.2)\n\nChoose 34 is a neuroscience experiment to test the generalization performance of individuals.\n   Copyright (C) 2023 Jose Mojica Perez\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU Affero General Public License as\n    published by the Free Software Foundation, either version 3 of the\n    License, or (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU Affero General Public License for more details.\n\n    You should have received a copy of the GNU Affero General Public License\n    along with this program.  If not, see <https://www.gnu.org/licenses/>.\n\nPress either the "LEFT" or "RIGHT" key to continue.',
    font='Open Sans',
    pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
copyrightResponse = keyboard.Keyboard()

# --- Initialize components for Routine "reference" ---
referenceText = visual.TextStim(win=win, name='referenceText',
    text='Design is adapted from the task originally described in: \nMyers, C. E., Kluger, A., Golomb, J., Ferris, S., de Leon, M., Schnirman, G. & Gluck, M. \n(2002). Hippocampal atrophy disrupts transfer generalization in non-demented elderly. \nJournal of Geriatric Psychiatry and Neurology, 15(2), 82-90. PMID: 12083598; \ndoi:10.1177/089198870201500206\n\nDesign is based on the description of Choose 33 written by Catherine E. Myers.\n\nPress either the "LEFT" or "RIGHT" key to continue.',
    font='Open Sans',
    pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
referenceResponse = keyboard.Keyboard()

# --- Initialize components for Routine "experimentInstructions" ---
instructions1 = visual.TextStim(win=win, name='instructions1',
    text='',
    font='Open Sans',
    pos=(0, 0.15), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
smileySample = visual.ImageStim(
    win=win,
    name='smileySample', 
    image='assets/smiley.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.0625, 0.0625),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
instructions2 = visual.TextStim(win=win, name='instructions2',
    text='',
    font='Open Sans',
    pos=(0, -0.15), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
expInstructionsResponse = keyboard.Keyboard()

# --- Initialize components for Routine "trialSetup" ---

# --- Initialize components for Routine "choose" ---
leftStim = visual.ImageStim(
    win=win,
    name='leftStim', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(-0.25, 0), size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
rightStim = visual.ImageStim(
    win=win,
    name='rightStim', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0.25, 0), size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
floorLine = visual.ImageStim(
    win=win,
    name='floorLine', 
    image='assets/line.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.08), size=(0.75, 0.0125),
    color='white', colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
textPrompt = visual.TextStim(win=win, name='textPrompt',
    text='',
    font='Open Sans',
    pos=(0, -0.25), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-4.0);
Subject_Response = keyboard.Keyboard()

# --- Initialize components for Routine "reveal" ---
leftStimReveal = visual.ImageStim(
    win=win,
    name='leftStimReveal', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
rightStimReveal = visual.ImageStim(
    win=win,
    name='rightStimReveal', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
smileyReveal = visual.ImageStim(
    win=win,
    name='smileyReveal', 
    image='assets/smiley.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.0625, 0.0625),
    color=[1,1,1], colorSpace='rgb', opacity=1.0,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
floorLineReveal = visual.ImageStim(
    win=win,
    name='floorLineReveal', 
    image='assets/line.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.08), size=(0.75, 0.0125),
    color='white', colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
textPrompt2 = visual.TextStim(win=win, name='textPrompt2',
    text='',
    font='Open Sans',
    pos=(0, -0.25), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-4.0);

# --- Initialize components for Routine "postPracticeInstructions" ---
postPracticeText = visual.TextStim(win=win, name='postPracticeText',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
postPracticeResp = keyboard.Keyboard()

# --- Initialize components for Routine "endExperiment" ---
endText = visual.TextStim(win=win, name='endText',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
endResp = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "setup" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
setupComponents = []
for thisComponent in setupComponents:
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

# --- Run Routine "setup" ---
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
    for thisComponent in setupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "setup" ---
for thisComponent in setupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "setup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "copyrightInfo" ---
continueRoutine = True
# update component parameters for each repeat
copyrightResponse.keys = []
copyrightResponse.rt = []
_copyrightResponse_allKeys = []
# keep track of which components have finished
copyrightInfoComponents = [copyright, copyrightResponse]
for thisComponent in copyrightInfoComponents:
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

# --- Run Routine "copyrightInfo" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *copyright* updates
    
    # if copyright is starting this frame...
    if copyright.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        copyright.frameNStart = frameN  # exact frame index
        copyright.tStart = t  # local t and not account for scr refresh
        copyright.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(copyright, 'tStartRefresh')  # time at next scr refresh
        # update status
        copyright.status = STARTED
        copyright.setAutoDraw(True)
    
    # if copyright is active this frame...
    if copyright.status == STARTED:
        # update params
        pass
    
    # *copyrightResponse* updates
    waitOnFlip = False
    
    # if copyrightResponse is starting this frame...
    if copyrightResponse.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        copyrightResponse.frameNStart = frameN  # exact frame index
        copyrightResponse.tStart = t  # local t and not account for scr refresh
        copyrightResponse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(copyrightResponse, 'tStartRefresh')  # time at next scr refresh
        # update status
        copyrightResponse.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(copyrightResponse.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(copyrightResponse.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if copyrightResponse.status == STARTED and not waitOnFlip:
        theseKeys = copyrightResponse.getKeys(keyList=[leftKey, rightKey], waitRelease=False)
        _copyrightResponse_allKeys.extend(theseKeys)
        if len(_copyrightResponse_allKeys):
            copyrightResponse.keys = _copyrightResponse_allKeys[-1].name  # just the last key pressed
            copyrightResponse.rt = _copyrightResponse_allKeys[-1].rt
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
    for thisComponent in copyrightInfoComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "copyrightInfo" ---
for thisComponent in copyrightInfoComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "copyrightInfo" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "reference" ---
continueRoutine = True
# update component parameters for each repeat
referenceResponse.keys = []
referenceResponse.rt = []
_referenceResponse_allKeys = []
# keep track of which components have finished
referenceComponents = [referenceText, referenceResponse]
for thisComponent in referenceComponents:
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

# --- Run Routine "reference" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *referenceText* updates
    
    # if referenceText is starting this frame...
    if referenceText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        referenceText.frameNStart = frameN  # exact frame index
        referenceText.tStart = t  # local t and not account for scr refresh
        referenceText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(referenceText, 'tStartRefresh')  # time at next scr refresh
        # update status
        referenceText.status = STARTED
        referenceText.setAutoDraw(True)
    
    # if referenceText is active this frame...
    if referenceText.status == STARTED:
        # update params
        pass
    
    # *referenceResponse* updates
    waitOnFlip = False
    
    # if referenceResponse is starting this frame...
    if referenceResponse.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        referenceResponse.frameNStart = frameN  # exact frame index
        referenceResponse.tStart = t  # local t and not account for scr refresh
        referenceResponse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(referenceResponse, 'tStartRefresh')  # time at next scr refresh
        # update status
        referenceResponse.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(referenceResponse.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(referenceResponse.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if referenceResponse.status == STARTED and not waitOnFlip:
        theseKeys = referenceResponse.getKeys(keyList=[leftKey, rightKey], waitRelease=False)
        _referenceResponse_allKeys.extend(theseKeys)
        if len(_referenceResponse_allKeys):
            referenceResponse.keys = _referenceResponse_allKeys[-1].name  # just the last key pressed
            referenceResponse.rt = _referenceResponse_allKeys[-1].rt
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
    for thisComponent in referenceComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "reference" ---
for thisComponent in referenceComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "reference" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "experimentInstructions" ---
continueRoutine = True
# update component parameters for each repeat
expInstructionsResponse.keys = []
expInstructionsResponse.rt = []
_expInstructionsResponse_allKeys = []
# keep track of which components have finished
experimentInstructionsComponents = [instructions1, smileySample, instructions2, expInstructionsResponse]
for thisComponent in experimentInstructionsComponents:
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

# --- Run Routine "experimentInstructions" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instructions1* updates
    
    # if instructions1 is starting this frame...
    if instructions1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instructions1.frameNStart = frameN  # exact frame index
        instructions1.tStart = t  # local t and not account for scr refresh
        instructions1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instructions1, 'tStartRefresh')  # time at next scr refresh
        # update status
        instructions1.status = STARTED
        instructions1.setAutoDraw(True)
    
    # if instructions1 is active this frame...
    if instructions1.status == STARTED:
        # update params
        instructions1.setText(texts["instructions1"], log=False)
    
    # *smileySample* updates
    
    # if smileySample is starting this frame...
    if smileySample.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        smileySample.frameNStart = frameN  # exact frame index
        smileySample.tStart = t  # local t and not account for scr refresh
        smileySample.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(smileySample, 'tStartRefresh')  # time at next scr refresh
        # update status
        smileySample.status = STARTED
        smileySample.setAutoDraw(True)
    
    # if smileySample is active this frame...
    if smileySample.status == STARTED:
        # update params
        pass
    
    # *instructions2* updates
    
    # if instructions2 is starting this frame...
    if instructions2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instructions2.frameNStart = frameN  # exact frame index
        instructions2.tStart = t  # local t and not account for scr refresh
        instructions2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instructions2, 'tStartRefresh')  # time at next scr refresh
        # update status
        instructions2.status = STARTED
        instructions2.setAutoDraw(True)
    
    # if instructions2 is active this frame...
    if instructions2.status == STARTED:
        # update params
        instructions2.setText(texts["instructions2"], log=False)
    
    # *expInstructionsResponse* updates
    waitOnFlip = False
    
    # if expInstructionsResponse is starting this frame...
    if expInstructionsResponse.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        expInstructionsResponse.frameNStart = frameN  # exact frame index
        expInstructionsResponse.tStart = t  # local t and not account for scr refresh
        expInstructionsResponse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(expInstructionsResponse, 'tStartRefresh')  # time at next scr refresh
        # update status
        expInstructionsResponse.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(expInstructionsResponse.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(expInstructionsResponse.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if expInstructionsResponse.status == STARTED and not waitOnFlip:
        theseKeys = expInstructionsResponse.getKeys(keyList=['z','m'], waitRelease=False)
        _expInstructionsResponse_allKeys.extend(theseKeys)
        if len(_expInstructionsResponse_allKeys):
            expInstructionsResponse.keys = _expInstructionsResponse_allKeys[-1].name  # just the last key pressed
            expInstructionsResponse.rt = _expInstructionsResponse_allKeys[-1].rt
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
    for thisComponent in experimentInstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "experimentInstructions" ---
for thisComponent in experimentInstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "experimentInstructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
phasesLoop = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('experimentFiles/phases.csv'),
    seed=None, name='phasesLoop')
thisExp.addLoop(phasesLoop)  # add the loop to the experiment
thisPhasesLoop = phasesLoop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPhasesLoop.rgb)
if thisPhasesLoop != None:
    for paramName in thisPhasesLoop:
        exec('{} = thisPhasesLoop[paramName]'.format(paramName))

for thisPhasesLoop in phasesLoop:
    currentLoop = phasesLoop
    # abbreviate parameter names if possible (e.g. rgb = thisPhasesLoop.rgb)
    if thisPhasesLoop != None:
        for paramName in thisPhasesLoop:
            exec('{} = thisPhasesLoop[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "trialSetup" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from trialSetupCode
    trialConditionsFile = "./experimentFiles/" + currentPhase + ".csv"
    
    consecutiveCorrectResponses = 0
    transitionedEarly = False
    
    if(currentPhase == "practice"):
        criterion = 3
    elif(evalToCriterion):
        criterion = int(expInfo["Number of pairs"]) * 2
    else:
        criterion = float("inf")
    # keep track of which components have finished
    trialSetupComponents = []
    for thisComponent in trialSetupComponents:
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
    
    # --- Run Routine "trialSetup" ---
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
        for thisComponent in trialSetupComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "trialSetup" ---
    for thisComponent in trialSetupComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "trialSetup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trialLoop = data.TrialHandler(nReps=trialNumReps[currentPhase], method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions((trialConditionsFile)),
        seed=None, name='trialLoop')
    thisExp.addLoop(trialLoop)  # add the loop to the experiment
    thisTrialLoop = trialLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrialLoop.rgb)
    if thisTrialLoop != None:
        for paramName in thisTrialLoop:
            exec('{} = thisTrialLoop[paramName]'.format(paramName))
    
    for thisTrialLoop in trialLoop:
        currentLoop = trialLoop
        # abbreviate parameter names if possible (e.g. rgb = thisTrialLoop.rgb)
        if thisTrialLoop != None:
            for paramName in thisTrialLoop:
                exec('{} = thisTrialLoop[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "choose" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from setImgsPaths
        leftImgPath = assetsPath + currentPhase + "/" + Left_Stim + ".png"
        rightImgPath = assetsPath + currentPhase + "/" + Right_Stim + ".png"
        
        
        leftStim.setImage(leftImgPath)
        rightStim.setImage(rightImgPath)
        Subject_Response.keys = []
        Subject_Response.rt = []
        _Subject_Response_allKeys = []
        # keep track of which components have finished
        chooseComponents = [leftStim, rightStim, floorLine, textPrompt, Subject_Response]
        for thisComponent in chooseComponents:
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
        
        # --- Run Routine "choose" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *leftStim* updates
            
            # if leftStim is starting this frame...
            if leftStim.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                leftStim.frameNStart = frameN  # exact frame index
                leftStim.tStart = t  # local t and not account for scr refresh
                leftStim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(leftStim, 'tStartRefresh')  # time at next scr refresh
                # update status
                leftStim.status = STARTED
                leftStim.setAutoDraw(True)
            
            # if leftStim is active this frame...
            if leftStim.status == STARTED:
                # update params
                pass
            
            # *rightStim* updates
            
            # if rightStim is starting this frame...
            if rightStim.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rightStim.frameNStart = frameN  # exact frame index
                rightStim.tStart = t  # local t and not account for scr refresh
                rightStim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rightStim, 'tStartRefresh')  # time at next scr refresh
                # update status
                rightStim.status = STARTED
                rightStim.setAutoDraw(True)
            
            # if rightStim is active this frame...
            if rightStim.status == STARTED:
                # update params
                pass
            
            # *floorLine* updates
            
            # if floorLine is starting this frame...
            if floorLine.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                floorLine.frameNStart = frameN  # exact frame index
                floorLine.tStart = t  # local t and not account for scr refresh
                floorLine.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(floorLine, 'tStartRefresh')  # time at next scr refresh
                # update status
                floorLine.status = STARTED
                floorLine.setAutoDraw(True)
            
            # if floorLine is active this frame...
            if floorLine.status == STARTED:
                # update params
                pass
            
            # *textPrompt* updates
            
            # if textPrompt is starting this frame...
            if textPrompt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                textPrompt.frameNStart = frameN  # exact frame index
                textPrompt.tStart = t  # local t and not account for scr refresh
                textPrompt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(textPrompt, 'tStartRefresh')  # time at next scr refresh
                # update status
                textPrompt.status = STARTED
                textPrompt.setAutoDraw(True)
            
            # if textPrompt is active this frame...
            if textPrompt.status == STARTED:
                # update params
                textPrompt.setText(texts["textPrompt"], log=False)
            
            # *Subject_Response* updates
            waitOnFlip = False
            
            # if Subject_Response is starting this frame...
            if Subject_Response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Subject_Response.frameNStart = frameN  # exact frame index
                Subject_Response.tStart = t  # local t and not account for scr refresh
                Subject_Response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Subject_Response, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Subject_Response.started')
                # update status
                Subject_Response.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(Subject_Response.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(Subject_Response.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if Subject_Response.status == STARTED and not waitOnFlip:
                theseKeys = Subject_Response.getKeys(keyList=[leftKey, rightKey], waitRelease=False)
                _Subject_Response_allKeys.extend(theseKeys)
                if len(_Subject_Response_allKeys):
                    Subject_Response.keys = _Subject_Response_allKeys[-1].name  # just the last key pressed
                    Subject_Response.rt = _Subject_Response_allKeys[-1].rt
                    # was this correct?
                    if (Subject_Response.keys == str((leftKey if hasSmiley[Left_Stim] else rightKey if hasSmiley[Right_Stim] else ''))) or (Subject_Response.keys == (leftKey if hasSmiley[Left_Stim] else rightKey if hasSmiley[Right_Stim] else '')):
                        Subject_Response.corr = 1
                    else:
                        Subject_Response.corr = 0
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
            for thisComponent in chooseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "choose" ---
        for thisComponent in chooseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if Subject_Response.keys in ['', [], None]:  # No response was made
            Subject_Response.keys = None
            # was no response the correct answer?!
            if str((leftKey if hasSmiley[Left_Stim] else rightKey if hasSmiley[Right_Stim] else '')).lower() == 'none':
               Subject_Response.corr = 1;  # correct non-response
            else:
               Subject_Response.corr = 0;  # failed to respond (incorrectly)
        # store data for trialLoop (TrialHandler)
        trialLoop.addData('Subject_Response.keys',Subject_Response.keys)
        trialLoop.addData('Subject_Response.corr', Subject_Response.corr)
        if Subject_Response.keys != None:  # we had a response
            trialLoop.addData('Subject_Response.rt', Subject_Response.rt)
        # Run 'End Routine' code from correctResponse
        correctResponse = False
            
        if(Subject_Response.keys == leftKey and hasSmiley[Left_Stim]):
            consecutiveCorrectResponses += 1
            correctResponse = True
        elif(Subject_Response.keys == rightKey and hasSmiley[Right_Stim]):
            consecutiveCorrectResponses += 1
            correctResponse = True
        else:
            consecutiveCorrectResponses = 0
        # Run 'End Routine' code from practiceAssignSmiley
        if(firstChoice and Subject_Response.keys == leftKey):
            hasSmiley[Right_Stim] = True
            hasSmiley[Left_Stim] = False
            firstChoice = False
        elif(firstChoice and Subject_Response.keys == rightKey):
            hasSmiley[Right_Stim] = False
            hasSmiley[Left_Stim] = True
            firstChoice = False
        # Run 'End Routine' code from updateSummaryVars
        if(currentPhase == "training"):
            trainTrials += 1
            trainAvgRT += Subject_Response.rt
            if(correctResponse):
                trainAccuracy += 1
            else:
                trainError += 1
        elif(currentPhase == "testing"):
            probeTrials += 1
            probeAvgRT += Subject_Response.rt
            if(correctResponse):
                probeAccuracy += 1
            else:
                probeError += 1
        # the Routine "choose" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "reveal" ---
        continueRoutine = True
        # update component parameters for each repeat
        leftStimReveal.setImage(leftImgPath)
        rightStimReveal.setImage(rightImgPath)
        smileyReveal.setOpacity(1 if correctResponse else 0 )
        smileyReveal.setPos((-0.25, 0) if hasSmiley[Left_Stim] else (0.25,0))
        # Run 'Begin Routine' code from earlyTransition
        if(consecutiveCorrectResponses >= criterion):
                trialLoop.finished = True
        # keep track of which components have finished
        revealComponents = [leftStimReveal, rightStimReveal, smileyReveal, floorLineReveal, textPrompt2]
        for thisComponent in revealComponents:
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
        
        # --- Run Routine "reveal" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *leftStimReveal* updates
            
            # if leftStimReveal is starting this frame...
            if leftStimReveal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                leftStimReveal.frameNStart = frameN  # exact frame index
                leftStimReveal.tStart = t  # local t and not account for scr refresh
                leftStimReveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(leftStimReveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                leftStimReveal.status = STARTED
                leftStimReveal.setAutoDraw(True)
            
            # if leftStimReveal is active this frame...
            if leftStimReveal.status == STARTED:
                # update params
                leftStimReveal.setPos([-0.25, min(0.1, frameN/100)] if (Subject_Response.keys == leftKey) else [-0.25, 0], log=False)
            
            # if leftStimReveal is stopping this frame...
            if leftStimReveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > leftStimReveal.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    leftStimReveal.tStop = t  # not accounting for scr refresh
                    leftStimReveal.frameNStop = frameN  # exact frame index
                    # update status
                    leftStimReveal.status = FINISHED
                    leftStimReveal.setAutoDraw(False)
            
            # *rightStimReveal* updates
            
            # if rightStimReveal is starting this frame...
            if rightStimReveal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rightStimReveal.frameNStart = frameN  # exact frame index
                rightStimReveal.tStart = t  # local t and not account for scr refresh
                rightStimReveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rightStimReveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                rightStimReveal.status = STARTED
                rightStimReveal.setAutoDraw(True)
            
            # if rightStimReveal is active this frame...
            if rightStimReveal.status == STARTED:
                # update params
                rightStimReveal.setPos([0.25, min(0.1, frameN/100)] if (Subject_Response.keys == rightKey) else [0.25, 0], log=False)
            
            # if rightStimReveal is stopping this frame...
            if rightStimReveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > rightStimReveal.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    rightStimReveal.tStop = t  # not accounting for scr refresh
                    rightStimReveal.frameNStop = frameN  # exact frame index
                    # update status
                    rightStimReveal.status = FINISHED
                    rightStimReveal.setAutoDraw(False)
            
            # *smileyReveal* updates
            
            # if smileyReveal is starting this frame...
            if smileyReveal.status == NOT_STARTED and tThisFlip >= 0.15-frameTolerance:
                # keep track of start time/frame for later
                smileyReveal.frameNStart = frameN  # exact frame index
                smileyReveal.tStart = t  # local t and not account for scr refresh
                smileyReveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(smileyReveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                smileyReveal.status = STARTED
                smileyReveal.setAutoDraw(True)
            
            # if smileyReveal is active this frame...
            if smileyReveal.status == STARTED:
                # update params
                pass
            
            # if smileyReveal is stopping this frame...
            if smileyReveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > smileyReveal.tStartRefresh + 0.85-frameTolerance:
                    # keep track of stop time/frame for later
                    smileyReveal.tStop = t  # not accounting for scr refresh
                    smileyReveal.frameNStop = frameN  # exact frame index
                    # update status
                    smileyReveal.status = FINISHED
                    smileyReveal.setAutoDraw(False)
            
            # *floorLineReveal* updates
            
            # if floorLineReveal is starting this frame...
            if floorLineReveal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                floorLineReveal.frameNStart = frameN  # exact frame index
                floorLineReveal.tStart = t  # local t and not account for scr refresh
                floorLineReveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(floorLineReveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                floorLineReveal.status = STARTED
                floorLineReveal.setAutoDraw(True)
            
            # if floorLineReveal is active this frame...
            if floorLineReveal.status == STARTED:
                # update params
                pass
            
            # if floorLineReveal is stopping this frame...
            if floorLineReveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > floorLineReveal.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    floorLineReveal.tStop = t  # not accounting for scr refresh
                    floorLineReveal.frameNStop = frameN  # exact frame index
                    # update status
                    floorLineReveal.status = FINISHED
                    floorLineReveal.setAutoDraw(False)
            
            # *textPrompt2* updates
            
            # if textPrompt2 is starting this frame...
            if textPrompt2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                textPrompt2.frameNStart = frameN  # exact frame index
                textPrompt2.tStart = t  # local t and not account for scr refresh
                textPrompt2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(textPrompt2, 'tStartRefresh')  # time at next scr refresh
                # update status
                textPrompt2.status = STARTED
                textPrompt2.setAutoDraw(True)
            
            # if textPrompt2 is active this frame...
            if textPrompt2.status == STARTED:
                # update params
                textPrompt2.setText(texts["textPrompt2"], log=False)
            
            # if textPrompt2 is stopping this frame...
            if textPrompt2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > textPrompt2.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    textPrompt2.tStop = t  # not accounting for scr refresh
                    textPrompt2.frameNStop = frameN  # exact frame index
                    # update status
                    textPrompt2.status = FINISHED
                    textPrompt2.setAutoDraw(False)
            
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
            for thisComponent in revealComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "reveal" ---
        for thisComponent in revealComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        thisExp.nextEntry()
        
    # completed trialNumReps[currentPhase] repeats of 'trialLoop'
    
    
    # set up handler to look after randomisation of conditions etc
    postPracticeScreenLoop = data.TrialHandler(nReps=1 if showPostPractice else 0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='postPracticeScreenLoop')
    thisExp.addLoop(postPracticeScreenLoop)  # add the loop to the experiment
    thisPostPracticeScreenLoop = postPracticeScreenLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPostPracticeScreenLoop.rgb)
    if thisPostPracticeScreenLoop != None:
        for paramName in thisPostPracticeScreenLoop:
            exec('{} = thisPostPracticeScreenLoop[paramName]'.format(paramName))
    
    for thisPostPracticeScreenLoop in postPracticeScreenLoop:
        currentLoop = postPracticeScreenLoop
        # abbreviate parameter names if possible (e.g. rgb = thisPostPracticeScreenLoop.rgb)
        if thisPostPracticeScreenLoop != None:
            for paramName in thisPostPracticeScreenLoop:
                exec('{} = thisPostPracticeScreenLoop[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "postPracticeInstructions" ---
        continueRoutine = True
        # update component parameters for each repeat
        postPracticeResp.keys = []
        postPracticeResp.rt = []
        _postPracticeResp_allKeys = []
        # Run 'Begin Routine' code from updateShowPostPractice
        showPostPractice = False
        # keep track of which components have finished
        postPracticeInstructionsComponents = [postPracticeText, postPracticeResp]
        for thisComponent in postPracticeInstructionsComponents:
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
        
        # --- Run Routine "postPracticeInstructions" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *postPracticeText* updates
            
            # if postPracticeText is starting this frame...
            if postPracticeText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                postPracticeText.frameNStart = frameN  # exact frame index
                postPracticeText.tStart = t  # local t and not account for scr refresh
                postPracticeText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(postPracticeText, 'tStartRefresh')  # time at next scr refresh
                # update status
                postPracticeText.status = STARTED
                postPracticeText.setAutoDraw(True)
            
            # if postPracticeText is active this frame...
            if postPracticeText.status == STARTED:
                # update params
                postPracticeText.setText(texts["postPracticeText"], log=False)
            
            # *postPracticeResp* updates
            waitOnFlip = False
            
            # if postPracticeResp is starting this frame...
            if postPracticeResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                postPracticeResp.frameNStart = frameN  # exact frame index
                postPracticeResp.tStart = t  # local t and not account for scr refresh
                postPracticeResp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(postPracticeResp, 'tStartRefresh')  # time at next scr refresh
                # update status
                postPracticeResp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(postPracticeResp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(postPracticeResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if postPracticeResp.status == STARTED and not waitOnFlip:
                theseKeys = postPracticeResp.getKeys(keyList=[leftKey, rightKey], waitRelease=False)
                _postPracticeResp_allKeys.extend(theseKeys)
                if len(_postPracticeResp_allKeys):
                    postPracticeResp.keys = _postPracticeResp_allKeys[-1].name  # just the last key pressed
                    postPracticeResp.rt = _postPracticeResp_allKeys[-1].rt
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
            for thisComponent in postPracticeInstructionsComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "postPracticeInstructions" ---
        for thisComponent in postPracticeInstructionsComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "postPracticeInstructions" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed 1 if showPostPractice else 0 repeats of 'postPracticeScreenLoop'
    
# completed 1.0 repeats of 'phasesLoop'


# --- Prepare to start Routine "endExperiment" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from writeSummary
trainAccuracy /= trainTrials
trainAvgRT /= trainTrials

probeAccuracy /= probeTrials
probeAvgRT /= probeTrials
info = {
        "subject": expInfo["Participant"],
        "experiment": expName,
        "experimenter": expInfo["Experimenter"],
        "date": date,
        "time": time,
        "condition": expInfo["Condition"],
        "task": "P",
        "train_accuracy": trainAccuracy,
        "train_errors": trainError,
        "train_avg_rt": trainAvgRT,
        "train_trials": trainTrials,
        "probe_accuracy": probeAccuracy,
        "probe_errors": probeError,
        "probe_rt_avg": probeAvgRT,
        "probe_trials": probeTrials
    }

summary_filename = f"{summariesPath}{expName}_{expInfo['Participant']}_summary.csv"
with open(summary_filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow([key for key in info])
    writer.writerow([val for val in info.values()]) 
endResp.keys = []
endResp.rt = []
_endResp_allKeys = []
# keep track of which components have finished
endExperimentComponents = [endText, endResp]
for thisComponent in endExperimentComponents:
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

# --- Run Routine "endExperiment" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endText* updates
    
    # if endText is starting this frame...
    if endText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        endText.frameNStart = frameN  # exact frame index
        endText.tStart = t  # local t and not account for scr refresh
        endText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(endText, 'tStartRefresh')  # time at next scr refresh
        # update status
        endText.status = STARTED
        endText.setAutoDraw(True)
    
    # if endText is active this frame...
    if endText.status == STARTED:
        # update params
        endText.setText(texts["endText"], log=False)
    
    # *endResp* updates
    waitOnFlip = False
    
    # if endResp is starting this frame...
    if endResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        endResp.frameNStart = frameN  # exact frame index
        endResp.tStart = t  # local t and not account for scr refresh
        endResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(endResp, 'tStartRefresh')  # time at next scr refresh
        # update status
        endResp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(endResp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(endResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if endResp.status == STARTED and not waitOnFlip:
        theseKeys = endResp.getKeys(keyList=[leftKey, rightKey], waitRelease=False)
        _endResp_allKeys.extend(theseKeys)
        if len(_endResp_allKeys):
            endResp.keys = _endResp_allKeys[-1].name  # just the last key pressed
            endResp.rt = _endResp_allKeys[-1].rt
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
    for thisComponent in endExperimentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "endExperiment" ---
for thisComponent in endExperimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "endExperiment" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='comma')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
