#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.2),
    on June 29, 2023, at 20:16
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
# Run 'Before Experiment' code from gen_practice
trainPath = "./assets/training/"
testPath = "./assets/testing/"
expFilesPath = "./experimentFiles/"
stimsFieldNames = ["Left_Stim", "Right_Stim"]

with open(expFilesPath + "practice.csv", "w") as file:

    practicePair = random.choice(os.listdir(trainPath))
    imgs = os.listdir(trainPath + practicePair)
    writer = csv.DictWriter(file, fieldnames=stimsFieldNames, 
            lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    writer.writerow({"Left_Stim": imgs[0], "Right_Stim": imgs[1]})
    writer.writerow({"Left_Stim": imgs[1], "Right_Stim": imgs[0]})



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.2'
expName = 'Choose 34'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'experimenter': '',
    'task': 'P',
    'condition': 'C',
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

# --- Initialize components for Routine "practice_choose" ---
leftStim = visual.ImageStim(
    win=win,
    name='leftStim', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(-0.25, 0), size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
rightStim = visual.ImageStim(
    win=win,
    name='rightStim', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0.25, 0), size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
key_resp = keyboard.Keyboard()

# --- Initialize components for Routine "practice_reveal" ---
practiceLeftStimReveal = visual.ImageStim(
    win=win,
    name='practiceLeftStimReveal', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(-0.25, 0), size=(0.125, 0.125),
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
    ori=0.0, pos=(0.25, 0), size=(0.0625, 0.0625),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)

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

# set up handler to look after randomisation of conditions etc
practice_loop = data.TrialHandler(nReps=2.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('experimentFiles/practice.csv'),
    seed=None, name='practice_loop')
thisExp.addLoop(practice_loop)  # add the loop to the experiment
thisPractice_loop = practice_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
if thisPractice_loop != None:
    for paramName in thisPractice_loop:
        exec('{} = thisPractice_loop[paramName]'.format(paramName))

for thisPractice_loop in practice_loop:
    currentLoop = practice_loop
    # abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
    if thisPractice_loop != None:
        for paramName in thisPractice_loop:
            exec('{} = thisPractice_loop[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "practice_choose" ---
    continueRoutine = True
    # update component parameters for each repeat
    leftStim.setImage((trainPath + practicePair + "/" + Left_Stim))
    rightStim.setImage((trainPath + practicePair + "/" + Right_Stim))
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # keep track of which components have finished
    practice_chooseComponents = [leftStim, rightStim, key_resp]
    for thisComponent in practice_chooseComponents:
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
    
    # --- Run Routine "practice_choose" ---
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
        
        # *key_resp* updates
        waitOnFlip = False
        
        # if key_resp is starting this frame...
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            # update status
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['y','n','left','right','space'], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
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
        for thisComponent in practice_chooseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "practice_choose" ---
    for thisComponent in practice_chooseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    practice_loop.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        practice_loop.addData('key_resp.rt', key_resp.rt)
    # the Routine "practice_choose" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "practice_reveal" ---
    continueRoutine = True
    # update component parameters for each repeat
    practiceLeftStimReveal.setImage((trainPath + practicePair + "/" + Left_Stim))
    practiceRightStimReveal.setImage((trainPath + practicePair + "/" + Right_Stim))
    # keep track of which components have finished
    practice_revealComponents = [practiceLeftStimReveal, practiceRightStimReveal, practiceSmiley]
    for thisComponent in practice_revealComponents:
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
    
    # --- Run Routine "practice_reveal" ---
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
            pass
        
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
            practiceRightStimReveal.setPos([0.25, min(0.1, frameN/100)], log=False)
        
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
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'practiceSmiley.started')
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
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'practiceSmiley.stopped')
                # update status
                practiceSmiley.status = FINISHED
                practiceSmiley.setAutoDraw(False)
        
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
        for thisComponent in practice_revealComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "practice_reveal" ---
    for thisComponent in practice_revealComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
# completed 2.0 repeats of 'practice_loop'


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
