#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.2),
    on January 05, 2024, at 17:12
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
assets_path = os.path.join(os.getcwd(), "assets")
training_path =  os.path.join(assets_path, "training")
testing_path = os.path.join(assets_path, "testing")
exp_files_path = os.path.join(os.getcwd(), "experiment_files")
data_path = os.path.join(os.getcwd(), "data")
summaries_path = os.path.join(data_path, "summaries")

if(not os.path.exists(data_path)):
    os.mkdir(data_path)
if(not os.path.exists(summaries_path)):
    os.mkdir(summaries_path)
if(not os.path.exists(exp_files_path)):
    os.mkdir(exp_files_path)


exp_date_time = datetime.datetime.now()
# Weekday(full name), Month(full name) Day(dd), Year(yyyy)
date = "\"" + exp_date_time.strftime("%A, %B %d, %Y") + "\""
# Hour(00-12):Minute(00-59):Second(00-59) AM/PM
time = "\"" + exp_date_time.strftime("%I:%M:%S %p") + "\""

stims_field_names = ["Left_Stim", "Right_Stim"]

practice_pair = ["circle", "triangle"]

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
# Run 'Before Experiment' code from initialize_vars

# This dictionary tells which object has a smiley 
# it has the format {<object_name> : True/False}.
has_smiley = {}

# First practice answer is always wrong. So we assigned the smiley AFTER
# subject's response. We use this variable to determine if we have assigned 
# the smiley yet
first_choice = True

# We use this variable to determine what phase we are in and 
# update it accordingly
current_phase = "practice"

# Changes on trialLoop
consecutive_correct_responses = 0

# Initialized to avoid errors
Right_Stim = ""
Left_Stim = ""

eval_to_criterion = True

show_post_practice = True
# Run 'Before Experiment' code from data_summary_vars
train_accuracy = 0
train_avg_RT = 0.0
train_error = 0
train_trials = 0

probe_accuracy = 0
probe_avg_RT = 0.0
probe_error = 0
probe_trials = 0


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.2'
expName = 'Choose_34'  # from the Builder filename that created this script
expInfo = {
    'Participant': '',
    'Experimenter': '',
    'Language': 'english',
    'Number of pairs': '8',
    'Evaluate to criterion or fixed number of trials?': 'criterion',
    'Training phase max blocks': '6',
    'Testing phase max blocks': '6',
    'Left Key': 'z',
    'Right Key': 'm',
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
# Run 'Begin Experiment' code from validate_exp_info
# number of pairs
if(not expInfo["Number of pairs"].isdigit()):
   print("Number of pairs must be a positive number in the range [1,4]", file=sys.stderr) 
   exit()
if(int(expInfo["Number of pairs"]) > 8 or int(expInfo["Number of pairs"]) < 1):
    print("Number of pairs must be in the range [1,8]", file=sys.stderr)
    exit()

# Left and right keys
if(len(expInfo["Left Key"]) < 1):
    print("The Left Key parameter is empty. You must specify a vaild key.", file=sys.stderr)
    exit()
if(len(expInfo["Right Key"]) < 1):
    print("The Right Key parameter is empty. You must specify a vaild key.", file=sys.stderr)
    exit()

# Criterion or fixed
crit_or_fixed = expInfo["Evaluate to criterion or fixed number of trials?"]
if(crit_or_fixed.lower() == "criterion"):
    eval_to_criterion = True
elif(crit_or_fixed.lower() == "fixed"):
    eval_to_criterion = False
else:
    print("Evaluate to criterion or fixed number of trials must set to either 'criterion' or 'fixed'", file=sys.stderr)
    exit()
    
# Max trial blocks
if(not expInfo["Training phase max blocks"].isdigit() or not expInfo["Testing phase max blocks"].isdigit()):
    print("Max blocks must be a number", file=sys.stderr) 
    exit()
# Run 'Begin Experiment' code from constants

del_pairs = 8 - int(expInfo["Number of pairs"])
if(del_pairs > 0):
    pairs_to_delete = random.sample(pairs.keys(), del_pairs)
    for pair in pairs_to_delete:
        pairs.pop(pair)
        
left_key = expInfo["Left Key"]
right_key = expInfo["Right Key"]
# Run 'Begin Experiment' code from initialize_vars
# Number of consecutive correct responses needed to move to next phase
# this changes in the trialBlocks loop
criterion = int(expInfo["Number of pairs"]) * 2

trial_num_reps = {"practice": 6,
                "training" : int(expInfo["Training phase max blocks"]),
                "testing" : int(expInfo["Testing phase max blocks"])
                }
# Run 'Begin Experiment' code from assign_smiley
practice0, practice1 = practice_pair

# Initially both practice objects have no smiley. This changes based on the
# subject's first choice. 
has_smiley[practice0] = False
has_smiley[practice1] = False

for pair in pairs:
    train0, train1 = pair
    test0, test1 = pairs[pair]
    
    r = random.randint(0,1)
    
    if(r == 0):
        has_smiley[train0] = True
        has_smiley[train1] = False
        has_smiley[test0] = True
        has_smiley[test1] = False
    else:
        has_smiley[train0] = False
        has_smiley[train1] = True
        has_smiley[test0] = False
        has_smiley[test1] = True
        

# Run 'Begin Experiment' code from generate_stim_files
with open(os.path.join(exp_files_path, "training.csv"), "w") as f1:
    with open(os.path.join(exp_files_path, "testing.csv"), "w") as f2:
        f1.write("Left_Stim,Right_Stim,Correct_Response\n")
        f2.write("Left_Stim,Right_Stim,Correct_Response\n")
        for pair in pairs:
            train0, train1 = pair
            test0, test1 = pairs[pair]
            if(has_smiley[train0] and has_smiley[test0]):
                f1.write(f"{train0},{train1},left\n")
                f1.write(f"{train1},{train0},right\n")
                f2.write(f"{test0},{test1},left\n")
                f2.write(f"{test1},{test0},right\n")
            else:
                f1.write(f"{train0},{train1},right\n")
                f1.write(f"{train1},{train0},left\n")
                f2.write(f"{test0},{test1},right\n")
                f2.write(f"{test1},{test0},left\n")
                
with open(os.path.join(exp_files_path, "practice.csv"), "w") as f:
    f.write("Left_Stim,Right_Stim\n")
    practice0, practice1 = practice_pair
    f.write(f"{practice0},{practice1}\n")
    f.write(f"{practice1},{practice0}\n")
# Run 'Begin Experiment' code from language
supported_languages = ["english", "español"]

language = expInfo["Language"].lower()
if(language == "spanish" or language == "español"):
    language = "spanish"
elif(language == "english"):
    language = "english"
else:
    print("Language not supported. The supported languages are:", file=sys.stderr)
    for lang in supported_languages:
        print(lang, file=sys.stderr)

texts = {}

with open(os.path.join(exp_files_path, "texts.csv"), mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        texts[row["text_object"]] = row[language].replace("\\n","\n")

# --- Initialize components for Routine "copyright_info" ---
copyright = visual.TextStim(win=win, name='copyright',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
copyright_response = keyboard.Keyboard()

# --- Initialize components for Routine "reference" ---
reference_text = visual.TextStim(win=win, name='reference_text',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
reference_response = keyboard.Keyboard()

# --- Initialize components for Routine "experiment_instructions" ---
instructions1 = visual.TextStim(win=win, name='instructions1',
    text='',
    font='Open Sans',
    pos=(0, 0.15), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
smiley_sample = visual.ImageStim(
    win=win,
    name='smiley_sample', 
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
exp_instructions_response = keyboard.Keyboard()

# --- Initialize components for Routine "trial_setup" ---

# --- Initialize components for Routine "choose" ---
left_stim = visual.ImageStim(
    win=win,
    name='left_stim', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(-0.25, 0), size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
right_stim = visual.ImageStim(
    win=win,
    name='right_stim', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0.25, 0), size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
floor_line = visual.ImageStim(
    win=win,
    name='floor_line', 
    image='assets/line.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.08), size=(0.75, 0.0125),
    color='white', colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
text_prompt = visual.TextStim(win=win, name='text_prompt',
    text='',
    font='Open Sans',
    pos=(0, -0.25), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-4.0);
subject_response = keyboard.Keyboard()

# --- Initialize components for Routine "reveal" ---
left_stim_reveal = visual.ImageStim(
    win=win,
    name='left_stim_reveal', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
right_stim_reveal = visual.ImageStim(
    win=win,
    name='right_stim_reveal', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.125, 0.125),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
smiley_reveal = visual.ImageStim(
    win=win,
    name='smiley_reveal', 
    image='assets/smiley.png', mask=None, anchor='center',
    ori=0.0, pos=[0,0], size=(0.0625, 0.0625),
    color=[1,1,1], colorSpace='rgb', opacity=1.0,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
floor_line_reveal = visual.ImageStim(
    win=win,
    name='floor_line_reveal', 
    image='assets/line.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.08), size=(0.75, 0.0125),
    color='white', colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
text_prompt2 = visual.TextStim(win=win, name='text_prompt2',
    text='',
    font='Open Sans',
    pos=(0, -0.25), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=1.0, 
    languageStyle='LTR',
    depth=-4.0);

# --- Initialize components for Routine "post_practice_instructions" ---
post_practice_text = visual.TextStim(win=win, name='post_practice_text',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
post_practice_resp = keyboard.Keyboard()

# --- Initialize components for Routine "end_experiment" ---
end_text = visual.TextStim(win=win, name='end_text',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
end_resp = keyboard.Keyboard()

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

# --- Prepare to start Routine "copyright_info" ---
continueRoutine = True
# update component parameters for each repeat
copyright_response.keys = []
copyright_response.rt = []
_copyright_response_allKeys = []
# keep track of which components have finished
copyright_infoComponents = [copyright, copyright_response]
for thisComponent in copyright_infoComponents:
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

# --- Run Routine "copyright_info" ---
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
        copyright.setText(texts["copyright"], log=False)
    
    # *copyright_response* updates
    waitOnFlip = False
    
    # if copyright_response is starting this frame...
    if copyright_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        copyright_response.frameNStart = frameN  # exact frame index
        copyright_response.tStart = t  # local t and not account for scr refresh
        copyright_response.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(copyright_response, 'tStartRefresh')  # time at next scr refresh
        # update status
        copyright_response.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(copyright_response.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(copyright_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if copyright_response.status == STARTED and not waitOnFlip:
        theseKeys = copyright_response.getKeys(keyList=[left_key, right_key], waitRelease=False)
        _copyright_response_allKeys.extend(theseKeys)
        if len(_copyright_response_allKeys):
            copyright_response.keys = _copyright_response_allKeys[-1].name  # just the last key pressed
            copyright_response.rt = _copyright_response_allKeys[-1].rt
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
    for thisComponent in copyright_infoComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "copyright_info" ---
for thisComponent in copyright_infoComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "copyright_info" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "reference" ---
continueRoutine = True
# update component parameters for each repeat
reference_response.keys = []
reference_response.rt = []
_reference_response_allKeys = []
# keep track of which components have finished
referenceComponents = [reference_text, reference_response]
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
    
    # *reference_text* updates
    
    # if reference_text is starting this frame...
    if reference_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        reference_text.frameNStart = frameN  # exact frame index
        reference_text.tStart = t  # local t and not account for scr refresh
        reference_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(reference_text, 'tStartRefresh')  # time at next scr refresh
        # update status
        reference_text.status = STARTED
        reference_text.setAutoDraw(True)
    
    # if reference_text is active this frame...
    if reference_text.status == STARTED:
        # update params
        reference_text.setText(texts["reference_text"], log=False)
    
    # *reference_response* updates
    waitOnFlip = False
    
    # if reference_response is starting this frame...
    if reference_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        reference_response.frameNStart = frameN  # exact frame index
        reference_response.tStart = t  # local t and not account for scr refresh
        reference_response.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(reference_response, 'tStartRefresh')  # time at next scr refresh
        # update status
        reference_response.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(reference_response.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(reference_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if reference_response.status == STARTED and not waitOnFlip:
        theseKeys = reference_response.getKeys(keyList=[left_key, right_key], waitRelease=False)
        _reference_response_allKeys.extend(theseKeys)
        if len(_reference_response_allKeys):
            reference_response.keys = _reference_response_allKeys[-1].name  # just the last key pressed
            reference_response.rt = _reference_response_allKeys[-1].rt
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

# --- Prepare to start Routine "experiment_instructions" ---
continueRoutine = True
# update component parameters for each repeat
exp_instructions_response.keys = []
exp_instructions_response.rt = []
_exp_instructions_response_allKeys = []
# keep track of which components have finished
experiment_instructionsComponents = [instructions1, smiley_sample, instructions2, exp_instructions_response]
for thisComponent in experiment_instructionsComponents:
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

# --- Run Routine "experiment_instructions" ---
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
    
    # *smiley_sample* updates
    
    # if smiley_sample is starting this frame...
    if smiley_sample.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        smiley_sample.frameNStart = frameN  # exact frame index
        smiley_sample.tStart = t  # local t and not account for scr refresh
        smiley_sample.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(smiley_sample, 'tStartRefresh')  # time at next scr refresh
        # update status
        smiley_sample.status = STARTED
        smiley_sample.setAutoDraw(True)
    
    # if smiley_sample is active this frame...
    if smiley_sample.status == STARTED:
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
    
    # *exp_instructions_response* updates
    waitOnFlip = False
    
    # if exp_instructions_response is starting this frame...
    if exp_instructions_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        exp_instructions_response.frameNStart = frameN  # exact frame index
        exp_instructions_response.tStart = t  # local t and not account for scr refresh
        exp_instructions_response.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(exp_instructions_response, 'tStartRefresh')  # time at next scr refresh
        # update status
        exp_instructions_response.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(exp_instructions_response.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(exp_instructions_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if exp_instructions_response.status == STARTED and not waitOnFlip:
        theseKeys = exp_instructions_response.getKeys(keyList=[left_key, right_key], waitRelease=False)
        _exp_instructions_response_allKeys.extend(theseKeys)
        if len(_exp_instructions_response_allKeys):
            exp_instructions_response.keys = _exp_instructions_response_allKeys[-1].name  # just the last key pressed
            exp_instructions_response.rt = _exp_instructions_response_allKeys[-1].rt
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
    for thisComponent in experiment_instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "experiment_instructions" ---
for thisComponent in experiment_instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "experiment_instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
phases_loop = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('experiment_files/phases.csv'),
    seed=None, name='phases_loop')
thisExp.addLoop(phases_loop)  # add the loop to the experiment
thisPhases_loop = phases_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPhases_loop.rgb)
if thisPhases_loop != None:
    for paramName in thisPhases_loop:
        exec('{} = thisPhases_loop[paramName]'.format(paramName))

for thisPhases_loop in phases_loop:
    currentLoop = phases_loop
    # abbreviate parameter names if possible (e.g. rgb = thisPhases_loop.rgb)
    if thisPhases_loop != None:
        for paramName in thisPhases_loop:
            exec('{} = thisPhases_loop[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "trial_setup" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from trial_setup_code
    trial_conditions_file = "./experiment_files/" + current_phase + ".csv"
    
    consecutive_correct_responses = 0
    transitioned_early = False
    
    if(current_phase == "practice"):
        criterion = 3
    elif(eval_to_criterion):
        criterion = int(expInfo["Number of pairs"]) * 2
    else:
        criterion = float("inf")
    # keep track of which components have finished
    trial_setupComponents = []
    for thisComponent in trial_setupComponents:
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
    
    # --- Run Routine "trial_setup" ---
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
        for thisComponent in trial_setupComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "trial_setup" ---
    for thisComponent in trial_setupComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "trial_setup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trial_loop = data.TrialHandler(nReps=trial_num_reps[current_phase], method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions((trial_conditions_file)),
        seed=None, name='trial_loop')
    thisExp.addLoop(trial_loop)  # add the loop to the experiment
    thisTrial_loop = trial_loop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_loop.rgb)
    if thisTrial_loop != None:
        for paramName in thisTrial_loop:
            exec('{} = thisTrial_loop[paramName]'.format(paramName))
    
    for thisTrial_loop in trial_loop:
        currentLoop = trial_loop
        # abbreviate parameter names if possible (e.g. rgb = thisTrial_loop.rgb)
        if thisTrial_loop != None:
            for paramName in thisTrial_loop:
                exec('{} = thisTrial_loop[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "choose" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from set_imgs_paths
        left_img_path = os.path.join(assets_path, current_phase, Left_Stim + ".png")
        right_img_path = os.path.join(assets_path, current_phase, Right_Stim + ".png")
        
        
        left_stim.setImage(left_img_path)
        right_stim.setImage(right_img_path)
        subject_response.keys = []
        subject_response.rt = []
        _subject_response_allKeys = []
        # keep track of which components have finished
        chooseComponents = [left_stim, right_stim, floor_line, text_prompt, subject_response]
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
            
            # *left_stim* updates
            
            # if left_stim is starting this frame...
            if left_stim.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                left_stim.frameNStart = frameN  # exact frame index
                left_stim.tStart = t  # local t and not account for scr refresh
                left_stim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(left_stim, 'tStartRefresh')  # time at next scr refresh
                # update status
                left_stim.status = STARTED
                left_stim.setAutoDraw(True)
            
            # if left_stim is active this frame...
            if left_stim.status == STARTED:
                # update params
                pass
            
            # *right_stim* updates
            
            # if right_stim is starting this frame...
            if right_stim.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                right_stim.frameNStart = frameN  # exact frame index
                right_stim.tStart = t  # local t and not account for scr refresh
                right_stim.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(right_stim, 'tStartRefresh')  # time at next scr refresh
                # update status
                right_stim.status = STARTED
                right_stim.setAutoDraw(True)
            
            # if right_stim is active this frame...
            if right_stim.status == STARTED:
                # update params
                pass
            
            # *floor_line* updates
            
            # if floor_line is starting this frame...
            if floor_line.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                floor_line.frameNStart = frameN  # exact frame index
                floor_line.tStart = t  # local t and not account for scr refresh
                floor_line.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(floor_line, 'tStartRefresh')  # time at next scr refresh
                # update status
                floor_line.status = STARTED
                floor_line.setAutoDraw(True)
            
            # if floor_line is active this frame...
            if floor_line.status == STARTED:
                # update params
                pass
            
            # *text_prompt* updates
            
            # if text_prompt is starting this frame...
            if text_prompt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_prompt.frameNStart = frameN  # exact frame index
                text_prompt.tStart = t  # local t and not account for scr refresh
                text_prompt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_prompt, 'tStartRefresh')  # time at next scr refresh
                # update status
                text_prompt.status = STARTED
                text_prompt.setAutoDraw(True)
            
            # if text_prompt is active this frame...
            if text_prompt.status == STARTED:
                # update params
                text_prompt.setText(texts["text_prompt"], log=False)
            
            # *subject_response* updates
            waitOnFlip = False
            
            # if subject_response is starting this frame...
            if subject_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                subject_response.frameNStart = frameN  # exact frame index
                subject_response.tStart = t  # local t and not account for scr refresh
                subject_response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(subject_response, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'subject_response.started')
                # update status
                subject_response.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(subject_response.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(subject_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if subject_response.status == STARTED and not waitOnFlip:
                theseKeys = subject_response.getKeys(keyList=[left_key, right_key], waitRelease=False)
                _subject_response_allKeys.extend(theseKeys)
                if len(_subject_response_allKeys):
                    subject_response.keys = _subject_response_allKeys[-1].name  # just the last key pressed
                    subject_response.rt = _subject_response_allKeys[-1].rt
                    # was this correct?
                    if (subject_response.keys == str((left_key if has_smiley[Left_Stim] else right_key if has_smiley[Right_Stim] else ''))) or (subject_response.keys == (left_key if has_smiley[Left_Stim] else right_key if has_smiley[Right_Stim] else '')):
                        subject_response.corr = 1
                    else:
                        subject_response.corr = 0
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
        if subject_response.keys in ['', [], None]:  # No response was made
            subject_response.keys = None
            # was no response the correct answer?!
            if str((left_key if has_smiley[Left_Stim] else right_key if has_smiley[Right_Stim] else '')).lower() == 'none':
               subject_response.corr = 1;  # correct non-response
            else:
               subject_response.corr = 0;  # failed to respond (incorrectly)
        # store data for trial_loop (TrialHandler)
        trial_loop.addData('subject_response.keys',subject_response.keys)
        trial_loop.addData('subject_response.corr', subject_response.corr)
        if subject_response.keys != None:  # we had a response
            trial_loop.addData('subject_response.rt', subject_response.rt)
        # Run 'End Routine' code from correct_response
        correct_response = False
            
        if(subject_response.keys == left_key and has_smiley[Left_Stim]):
            consecutive_correct_responses += 1
            correct_response = True
        elif(subject_response.keys == right_key and has_smiley[Right_Stim]):
            consecutive_correct_responses += 1
            correct_response = True
        # Only wrong answers reset the consecutive correct responses
        # if the subject doesn't respond on time then we just 
        # ignore that it happened
        elif(subject_response.keys):
            consecutive_correct_responses = 0
        
        # Run 'End Routine' code from practice_assign_smiley
        if(first_choice and subject_response.keys == left_key):
            has_smiley[Right_Stim] = True
            has_smiley[Left_Stim] = False
            first_choice = False
        elif(first_choice and subject_response.keys == right_key):
            has_smiley[Right_Stim] = False
            has_smiley[Left_Stim] = True
            first_choice = False
        # Run 'End Routine' code from update_summary_vars
        
        # type(subject_response.rt) == float is True 
        # if the subject responded within the alloted time (3 secs)
        if(current_phase == "training" and type(subject_response.rt) == float):
            train_trials += 1
            train_avg_RT += subject_response.rt
            if(correct_response):
                train_accuracy += 1
            else:
                train_error += 1   
        elif(current_phase == "testing" and type(subject_response.rt) == float):
            probe_trials += 1
            probe_avg_RT += subject_response.rt
            if(correct_response):
                probe_accuracy += 1
            else:
                probe_error += 1
        # the Routine "choose" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "reveal" ---
        continueRoutine = True
        # update component parameters for each repeat
        left_stim_reveal.setImage(left_img_path)
        right_stim_reveal.setImage(right_img_path)
        smiley_reveal.setOpacity(1 if correct_response else 0 )
        smiley_reveal.setPos((-0.25, 0) if has_smiley[Left_Stim] else (0.25,0))
        # Run 'Begin Routine' code from early_transition
        if(consecutive_correct_responses >= criterion):
                trial_loop.finished = True
        # keep track of which components have finished
        revealComponents = [left_stim_reveal, right_stim_reveal, smiley_reveal, floor_line_reveal, text_prompt2]
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
            
            # *left_stim_reveal* updates
            
            # if left_stim_reveal is starting this frame...
            if left_stim_reveal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                left_stim_reveal.frameNStart = frameN  # exact frame index
                left_stim_reveal.tStart = t  # local t and not account for scr refresh
                left_stim_reveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(left_stim_reveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                left_stim_reveal.status = STARTED
                left_stim_reveal.setAutoDraw(True)
            
            # if left_stim_reveal is active this frame...
            if left_stim_reveal.status == STARTED:
                # update params
                left_stim_reveal.setPos([-0.25, min(0.1, frameN/100)] if (subject_response.keys == left_key) else [-0.25, 0], log=False)
            
            # if left_stim_reveal is stopping this frame...
            if left_stim_reveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > left_stim_reveal.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    left_stim_reveal.tStop = t  # not accounting for scr refresh
                    left_stim_reveal.frameNStop = frameN  # exact frame index
                    # update status
                    left_stim_reveal.status = FINISHED
                    left_stim_reveal.setAutoDraw(False)
            
            # *right_stim_reveal* updates
            
            # if right_stim_reveal is starting this frame...
            if right_stim_reveal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                right_stim_reveal.frameNStart = frameN  # exact frame index
                right_stim_reveal.tStart = t  # local t and not account for scr refresh
                right_stim_reveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(right_stim_reveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                right_stim_reveal.status = STARTED
                right_stim_reveal.setAutoDraw(True)
            
            # if right_stim_reveal is active this frame...
            if right_stim_reveal.status == STARTED:
                # update params
                right_stim_reveal.setPos([0.25, min(0.1, frameN/100)] if (subject_response.keys == right_key) else [0.25, 0], log=False)
            
            # if right_stim_reveal is stopping this frame...
            if right_stim_reveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > right_stim_reveal.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    right_stim_reveal.tStop = t  # not accounting for scr refresh
                    right_stim_reveal.frameNStop = frameN  # exact frame index
                    # update status
                    right_stim_reveal.status = FINISHED
                    right_stim_reveal.setAutoDraw(False)
            
            # *smiley_reveal* updates
            
            # if smiley_reveal is starting this frame...
            if smiley_reveal.status == NOT_STARTED and tThisFlip >= 0.15-frameTolerance:
                # keep track of start time/frame for later
                smiley_reveal.frameNStart = frameN  # exact frame index
                smiley_reveal.tStart = t  # local t and not account for scr refresh
                smiley_reveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(smiley_reveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                smiley_reveal.status = STARTED
                smiley_reveal.setAutoDraw(True)
            
            # if smiley_reveal is active this frame...
            if smiley_reveal.status == STARTED:
                # update params
                pass
            
            # if smiley_reveal is stopping this frame...
            if smiley_reveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > smiley_reveal.tStartRefresh + 0.85-frameTolerance:
                    # keep track of stop time/frame for later
                    smiley_reveal.tStop = t  # not accounting for scr refresh
                    smiley_reveal.frameNStop = frameN  # exact frame index
                    # update status
                    smiley_reveal.status = FINISHED
                    smiley_reveal.setAutoDraw(False)
            
            # *floor_line_reveal* updates
            
            # if floor_line_reveal is starting this frame...
            if floor_line_reveal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                floor_line_reveal.frameNStart = frameN  # exact frame index
                floor_line_reveal.tStart = t  # local t and not account for scr refresh
                floor_line_reveal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(floor_line_reveal, 'tStartRefresh')  # time at next scr refresh
                # update status
                floor_line_reveal.status = STARTED
                floor_line_reveal.setAutoDraw(True)
            
            # if floor_line_reveal is active this frame...
            if floor_line_reveal.status == STARTED:
                # update params
                pass
            
            # if floor_line_reveal is stopping this frame...
            if floor_line_reveal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > floor_line_reveal.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    floor_line_reveal.tStop = t  # not accounting for scr refresh
                    floor_line_reveal.frameNStop = frameN  # exact frame index
                    # update status
                    floor_line_reveal.status = FINISHED
                    floor_line_reveal.setAutoDraw(False)
            
            # *text_prompt2* updates
            
            # if text_prompt2 is starting this frame...
            if text_prompt2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_prompt2.frameNStart = frameN  # exact frame index
                text_prompt2.tStart = t  # local t and not account for scr refresh
                text_prompt2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_prompt2, 'tStartRefresh')  # time at next scr refresh
                # update status
                text_prompt2.status = STARTED
                text_prompt2.setAutoDraw(True)
            
            # if text_prompt2 is active this frame...
            if text_prompt2.status == STARTED:
                # update params
                text_prompt2.setText(texts["text_prompt2"], log=False)
            
            # if text_prompt2 is stopping this frame...
            if text_prompt2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text_prompt2.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    text_prompt2.tStop = t  # not accounting for scr refresh
                    text_prompt2.frameNStop = frameN  # exact frame index
                    # update status
                    text_prompt2.status = FINISHED
                    text_prompt2.setAutoDraw(False)
            
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
        
    # completed trial_num_reps[current_phase] repeats of 'trial_loop'
    
    
    # set up handler to look after randomisation of conditions etc
    post_practice_screen_loop = data.TrialHandler(nReps=1 if show_post_practice else 0, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='post_practice_screen_loop')
    thisExp.addLoop(post_practice_screen_loop)  # add the loop to the experiment
    thisPost_practice_screen_loop = post_practice_screen_loop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPost_practice_screen_loop.rgb)
    if thisPost_practice_screen_loop != None:
        for paramName in thisPost_practice_screen_loop:
            exec('{} = thisPost_practice_screen_loop[paramName]'.format(paramName))
    
    for thisPost_practice_screen_loop in post_practice_screen_loop:
        currentLoop = post_practice_screen_loop
        # abbreviate parameter names if possible (e.g. rgb = thisPost_practice_screen_loop.rgb)
        if thisPost_practice_screen_loop != None:
            for paramName in thisPost_practice_screen_loop:
                exec('{} = thisPost_practice_screen_loop[paramName]'.format(paramName))
        
        # --- Prepare to start Routine "post_practice_instructions" ---
        continueRoutine = True
        # update component parameters for each repeat
        post_practice_resp.keys = []
        post_practice_resp.rt = []
        _post_practice_resp_allKeys = []
        # Run 'Begin Routine' code from update_show_post_practice
        show_post_practice = False
        # keep track of which components have finished
        post_practice_instructionsComponents = [post_practice_text, post_practice_resp]
        for thisComponent in post_practice_instructionsComponents:
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
        
        # --- Run Routine "post_practice_instructions" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *post_practice_text* updates
            
            # if post_practice_text is starting this frame...
            if post_practice_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                post_practice_text.frameNStart = frameN  # exact frame index
                post_practice_text.tStart = t  # local t and not account for scr refresh
                post_practice_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(post_practice_text, 'tStartRefresh')  # time at next scr refresh
                # update status
                post_practice_text.status = STARTED
                post_practice_text.setAutoDraw(True)
            
            # if post_practice_text is active this frame...
            if post_practice_text.status == STARTED:
                # update params
                post_practice_text.setText(texts["post_practice_text"], log=False)
            
            # *post_practice_resp* updates
            waitOnFlip = False
            
            # if post_practice_resp is starting this frame...
            if post_practice_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                post_practice_resp.frameNStart = frameN  # exact frame index
                post_practice_resp.tStart = t  # local t and not account for scr refresh
                post_practice_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(post_practice_resp, 'tStartRefresh')  # time at next scr refresh
                # update status
                post_practice_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(post_practice_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(post_practice_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if post_practice_resp.status == STARTED and not waitOnFlip:
                theseKeys = post_practice_resp.getKeys(keyList=[left_key, right_key], waitRelease=False)
                _post_practice_resp_allKeys.extend(theseKeys)
                if len(_post_practice_resp_allKeys):
                    post_practice_resp.keys = _post_practice_resp_allKeys[-1].name  # just the last key pressed
                    post_practice_resp.rt = _post_practice_resp_allKeys[-1].rt
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
            for thisComponent in post_practice_instructionsComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "post_practice_instructions" ---
        for thisComponent in post_practice_instructionsComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "post_practice_instructions" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed 1 if show_post_practice else 0 repeats of 'post_practice_screen_loop'
    
# completed 1.0 repeats of 'phases_loop'


# --- Prepare to start Routine "end_experiment" ---
continueRoutine = True
# update component parameters for each repeat
# Run 'Begin Routine' code from write_summary
train_accuracy /= train_trials
train_avg_RT /= train_trials

probe_accuracy /= probe_trials
probe_avg_RT /= probe_trials
info = {
        "subject": expInfo["Participant"],
        "experiment": expName,
        "experimenter": expInfo["Experimenter"],
        "date": date,
        "time": time,
        "train_accuracy": train_accuracy,
        "train_errors": train_error,
        "train_avg_rt": train_avg_RT,
        "train_trials": train_trials,
        "probe_accuracy": probe_accuracy,
        "probe_errors": probe_error,
        "probe_rt_avg": probe_avg_RT,
        "probe_trials": probe_trials
    }

summary_file = os.path.join(summaries_path, f"{expName}_{expInfo['Participant']}_summary.csv")
with open(summary_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow([key for key in info])
    writer.writerow([val for val in info.values()]) 
end_resp.keys = []
end_resp.rt = []
_end_resp_allKeys = []
# keep track of which components have finished
end_experimentComponents = [end_text, end_resp]
for thisComponent in end_experimentComponents:
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

# --- Run Routine "end_experiment" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_text* updates
    
    # if end_text is starting this frame...
    if end_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_text.frameNStart = frameN  # exact frame index
        end_text.tStart = t  # local t and not account for scr refresh
        end_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_text, 'tStartRefresh')  # time at next scr refresh
        # update status
        end_text.status = STARTED
        end_text.setAutoDraw(True)
    
    # if end_text is active this frame...
    if end_text.status == STARTED:
        # update params
        end_text.setText(texts["end_text"], log=False)
    
    # *end_resp* updates
    waitOnFlip = False
    
    # if end_resp is starting this frame...
    if end_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_resp.frameNStart = frameN  # exact frame index
        end_resp.tStart = t  # local t and not account for scr refresh
        end_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_resp, 'tStartRefresh')  # time at next scr refresh
        # update status
        end_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(end_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(end_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if end_resp.status == STARTED and not waitOnFlip:
        theseKeys = end_resp.getKeys(keyList=[left_key, right_key], waitRelease=False)
        _end_resp_allKeys.extend(theseKeys)
        if len(_end_resp_allKeys):
            end_resp.keys = _end_resp_allKeys[-1].name  # just the last key pressed
            end_resp.rt = _end_resp_allKeys[-1].rt
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
    for thisComponent in end_experimentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "end_experiment" ---
for thisComponent in end_experimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "end_experiment" was not non-slip safe, so reset the non-slip timer
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
