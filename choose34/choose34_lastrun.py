#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.2),
    on July 05, 2023, at 16:46
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

from collections import defaultdict
# Run 'Before Experiment' code from constants
pairsPath = "./assets/pairs/"
expFilesPath = "./experimentFiles/"
stimsFieldNames = ["Left_Stim", "Right_Stim"]
leftKey = 'z'
rightKey = 'm'
phases = ["practice", "training", "testing"]
# Run 'Before Experiment' code from initializeVars
def constantFactory(value):
    return lambda: value

# This dictionary tells which object has a smiley 
# it has the format {<object_name> : True/False}. If <object_name> is not in
# in the dictionary it will return False by default.
hasSmiley = defaultdict(constantFactory(False))

# First practice answer is always wrong. So we assigned the smiley AFTER
# subject's response. We use this variable to determine if we have assigned 
# the smiley yet
assignedSmiley = False

# We use this variable to determine what phase we are in and 
#update it accordingly
currentPhase = "practice"

# Number of consecutive correct responses needed to move to next phase
# this changes in the trialBlocks loop
criterion = 16 

# Changes on trialLoop
consecutiveCorrectResponses = 0

# Initialized to avoid errors
Right_Stim = ""
Left_Stim = ""
# Run 'Before Experiment' code from generatePhaseFiles
for phase in phases[1:]:
    with open(f"./experimentFiles/{phase}.csv", "w") as f:
        f.write("pair,Left_Stim,Right_Stim,Correct_Response\n")
        for i in range(1, 9):
            imgs = os.listdir(f"./assets/pairs/pair{i}/{phase}")
            correct = random.randint(0, 1)
            if correct == 0:
                img0 = imgs[0].split(".")[0]
                img1 = imgs[1].split(".")[0]
                f.write(f"pair{i},{img0},{img1},left\n")
                f.write(f"pair{i},{img1},{img0},right\n")
                hasSmiley[img0] = True
            else:
                img0 = imgs[0].split(".")[0]
                img1 = imgs[1].split(".")[0]
                f.write(f"pair{i},{img0},{img1},right\n")
                f.write(f"pair{i},{img1},{img0},left\n")
                hasSmiley[img1] = True


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.2'
expName = 'Choose34'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'experimenter': '',
    'condition': 'C',
    'number of pairs': '8',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s' % (expName, expInfo['participant'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\josel\\gluck_lab\\GluckLab\\choose34\\choose34_lastrun.py',
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
    size=[1536, 960], fullscr=False, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[1.0000, 1.0000, 1.0000], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = True
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

# --- Initialize components for Routine "experimentInstructions" ---
instructions1 = visual.TextStim(win=win, name='instructions1',
    text='Welcome to the experiment.\n\nYou will see pairs of objects. Each time there is a smiley face hidden under one of the objects. It looks like this:',
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
    text='Each time, use the \'\'LEFT" or "RIGHT" key to choose the object you think the smiley face is under. In the beginning you will have to guess.\n\nPress the button to see an example of the first kind of pair.',
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
textPrompt = visual.TextStim(win=win, name='textPrompt',
    text='Which object is the smiley face under?',
    font='Open Sans',
    pos=(0, -0.5), height=0.035, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
Subject_Response = keyboard.Keyboard()

# --- Initialize components for Routine "reveal" ---
practiceLeftStimReveal = visual.ImageStim(
    win=win,
    name='practiceLeftStimReveal', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
practiceRightStimReveal = visual.ImageStim(
    win=win,
    name='practiceRightStimReveal', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
practiceSmiley = visual.ImageStim(
    win=win,
    name='practiceSmiley', 
    image='assets/smiley.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.0625, 0.0625),
    color=[1,1,1], colorSpace='rgb', opacity=1.0,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
textPrompt2 = visual.TextStim(win=win, name='textPrompt2',
    text='Which object is the smiley face under?',
    font='Open Sans',
    pos=(0, -0.5), height=0.035, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

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
        pass
    
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
        pass
    
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
trialBlocks = data.TrialHandler(nReps=3.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='trialBlocks')
thisExp.addLoop(trialBlocks)  # add the loop to the experiment
thisTrialBlock = trialBlocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrialBlock.rgb)
if thisTrialBlock != None:
    for paramName in thisTrialBlock:
        exec('{} = thisTrialBlock[paramName]'.format(paramName))

for thisTrialBlock in trialBlocks:
    currentLoop = trialBlocks
    # abbreviate parameter names if possible (e.g. rgb = thisTrialBlock.rgb)
    if thisTrialBlock != None:
        for paramName in thisTrialBlock:
            exec('{} = thisTrialBlock[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "trialSetup" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from trialSetupCode
    trialConditionsFile = "./experimentFiles/" + currentPhase + ".csv"
    
    consecutiveCorrectResponses = 0
    
    if(currentPhase == "practice"):
        criterion = 3
    else:
        criterion = int(expInfo["number of pairs"]) * 2
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
    trialLoop = data.TrialHandler(nReps=6.0, method='random', 
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
        leftImgPath = pairsPath + pair + "/" + currentPhase + "/" + Left_Stim + ".png"
        rightImgPath = pairsPath + pair + "/" + currentPhase + "/" + Right_Stim + ".png"
        
        print(f"COOOOOOOOONNOOOOOOO {trialConditionsFile}")
        
        if(currentPhase == "practice"):
            leftImgPath = pairsPath + currentPhase + "/" + Left_Stim + ".png"
            rightImgPath = pairsPath + currentPhase + "/" + Right_Stim + ".png"
        leftStim.setImage(leftImgPath)
        rightStim.setImage(rightImgPath)
        Subject_Response.keys = []
        Subject_Response.rt = []
        _Subject_Response_allKeys = []
        # keep track of which components have finished
        chooseComponents = [leftStim, rightStim, textPrompt, Subject_Response]
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
                pass
            
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
                theseKeys = Subject_Response.getKeys(keyList=['z', 'm', 'space',], waitRelease=False)
                _Subject_Response_allKeys.extend(theseKeys)
                if len(_Subject_Response_allKeys):
                    Subject_Response.keys = _Subject_Response_allKeys[-1].name  # just the last key pressed
                    Subject_Response.rt = _Subject_Response_allKeys[-1].rt
                    # was this correct?
                    if (Subject_Response.keys == str(('z' if hasSmiley[Left_Stim] else 'm' if hasSmiley[Right_Stim] else ''))) or (Subject_Response.keys == ('z' if hasSmiley[Left_Stim] else 'm' if hasSmiley[Right_Stim] else '')):
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
            if str(('z' if hasSmiley[Left_Stim] else 'm' if hasSmiley[Right_Stim] else '')).lower() == 'none':
               Subject_Response.corr = 1;  # correct non-response
            else:
               Subject_Response.corr = 0;  # failed to respond (incorrectly)
        # store data for trialLoop (TrialHandler)
        trialLoop.addData('Subject_Response.keys',Subject_Response.keys)
        trialLoop.addData('Subject_Response.corr', Subject_Response.corr)
        if Subject_Response.keys != None:  # we had a response
            trialLoop.addData('Subject_Response.rt', Subject_Response.rt)
        # Run 'End Routine' code from assignSmiley
        if(not assignedSmiley and Subject_Response.keys == leftKey):
            # assign smiley to right stim
            hasSmiley[Left_Stim] = False
            hasSmiley[Right_Stim] = True
            assignedSmiley = True
        elif(not assignedSmiley):
            #assign smiley to left stim
            hasSmiley[Left_Stim] = True
            hasSmiley[Right_Stim] = False
            assignedSmiley = True
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
        # the Routine "choose" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "reveal" ---
        continueRoutine = True
        # update component parameters for each repeat
        practiceLeftStimReveal.setImage(leftImgPath)
        practiceRightStimReveal.setImage(rightImgPath)
        practiceSmiley.setOpacity(1 if correctResponse else 0 )
        practiceSmiley.setPos((-0.25, 0) if hasSmiley[Left_Stim] else (0.25,0))
        # keep track of which components have finished
        revealComponents = [practiceLeftStimReveal, practiceRightStimReveal, practiceSmiley, textPrompt2]
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
            
            # *practiceLeftStimReveal* updates
            
            # if practiceLeftStimReveal is starting this frame...
            if practiceLeftStimReveal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                practiceLeftStimReveal.frameNStart = frameN  # exact frame index
                practiceLeftStimReveal.tStart = t  # local t and not account for scr refresh
                practiceLeftStimReveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(practiceLeftStimReveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                practiceLeftStimReveal.status = STARTED
                practiceLeftStimReveal.setAutoDraw(True)
            
            # if practiceLeftStimReveal is active this frame...
            if practiceLeftStimReveal.status == STARTED:
                # update params
                practiceLeftStimReveal.setPos([-0.25, min(0.1, frameN/100)] if (Subject_Response.keys == leftKey) else [-0.25, 0], log=False)
            
            # if practiceLeftStimReveal is stopping this frame...
            if practiceLeftStimReveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > practiceLeftStimReveal.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    practiceLeftStimReveal.tStop = t  # not accounting for scr refresh
                    practiceLeftStimReveal.frameNStop = frameN  # exact frame index
                    # update status
                    practiceLeftStimReveal.status = FINISHED
                    practiceLeftStimReveal.setAutoDraw(False)
            
            # *practiceRightStimReveal* updates
            
            # if practiceRightStimReveal is starting this frame...
            if practiceRightStimReveal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                practiceRightStimReveal.frameNStart = frameN  # exact frame index
                practiceRightStimReveal.tStart = t  # local t and not account for scr refresh
                practiceRightStimReveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(practiceRightStimReveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                practiceRightStimReveal.status = STARTED
                practiceRightStimReveal.setAutoDraw(True)
            
            # if practiceRightStimReveal is active this frame...
            if practiceRightStimReveal.status == STARTED:
                # update params
                practiceRightStimReveal.setPos([0.25, min(0.1, frameN/100)] if (Subject_Response.keys == rightKey) else [0.25, 0], log=False)
            
            # if practiceRightStimReveal is stopping this frame...
            if practiceRightStimReveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > practiceRightStimReveal.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    practiceRightStimReveal.tStop = t  # not accounting for scr refresh
                    practiceRightStimReveal.frameNStop = frameN  # exact frame index
                    # update status
                    practiceRightStimReveal.status = FINISHED
                    practiceRightStimReveal.setAutoDraw(False)
            
            # *practiceSmiley* updates
            
            # if practiceSmiley is starting this frame...
            if practiceSmiley.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                practiceSmiley.frameNStart = frameN  # exact frame index
                practiceSmiley.tStart = t  # local t and not account for scr refresh
                practiceSmiley.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(practiceSmiley, 'tStartRefresh')  # time at next scr refresh
                # update status
                practiceSmiley.status = STARTED
                practiceSmiley.setAutoDraw(True)
            
            # if practiceSmiley is active this frame...
            if practiceSmiley.status == STARTED:
                # update params
                pass
            
            # if practiceSmiley is stopping this frame...
            if practiceSmiley.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > practiceSmiley.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    practiceSmiley.tStop = t  # not accounting for scr refresh
                    practiceSmiley.frameNStop = frameN  # exact frame index
                    # update status
                    practiceSmiley.status = FINISHED
                    practiceSmiley.setAutoDraw(False)
            
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
                pass
            
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
        # Run 'End Routine' code from phaseTransition
        if(consecutiveCorrectResponses >= criterion):
            if(currentPhase == "practice"):
                currentPhase = "training"
            elif(currentPhase == "training"):
                currentPhase = "testing"
            else:
                trialBlocks.finished = True
            trialLoop.finished = True
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        thisExp.nextEntry()
        
    # completed 6.0 repeats of 'trialLoop'
    
# completed 3.0 repeats of 'trialBlocks'


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
