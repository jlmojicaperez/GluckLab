# Choose 34

## Description

The discrimination-and-transfer (“Choose”) task is a concurrent visual
discrimination task, followed by a generalization (probe) phase in which
irrelevant stimulus features are altered. In the training phase, subjects
learn a number of discriminations between pairs of colored shapes; in each
pair, one feature is relevant and one is redundant and therefore
irrelevant. For example, in the training phase, subjects might learn to
choose one object (green mushroom) in preference to another (brown
mushroom); in this example,color is predictive but shape is redundant and
therefore irrelevant.  Other pairs differ in shape (relevant) but not color
(irrelevant).  Later, in the probe phase, irrelevant features are altered.
Thus, subjects might be presented with a green frame and a brown frame;
color is still predictive (green still beats brown) but the irrelevant
shape feature has been altered.  Healthy controls typically generalize
well, but amnesic patients with bilateral hippocampal damage (Myers, DeLuca
et al., 2008) and non-demented elderly with bilateral hippocampal atrophy
(Myers, Kluger et al., 2002) both show impaired generalization.

The task design was described in Myers, Kluger et al. (2002) and was
subsequently modified to allow the user to specify various details of the
training and probe phases. This version of the software was used in several
recent papers including Anastasides et al. (2015), in which veterans with
more severe symptoms of post-traumatic stress disorder (PTSD) symptoms
showed an increased tendency to generalize, compared to peers with few/no
PTSD symptoms.

## PsychoPy Implementation

The implementation of the main parts of this task are broken down into the following routines:

![Choose 34 Routine Diagram](../imgs/Choose34Diagram.png)

- Setup:
  
  - Before experiment:

    - Imports libraries that are used in the experiment.
    - Defines constants that are used throughout the experiment or for
    records purposes.
    - Initializes variables that are used throughout the experiment

  - Beginning of experiment (after settings are entered):

    - Validates and applies experiment's user-entered settings.
    - Initializes variables that are used throughout the experiment,
    for different purposes.
    - Assigns which objects have a smiley face at random.
    - Generates the `trialsLoop` condition files found in
    `GluckLab/choose34/experimentFiles`. These files contain all the
    image stimulus that will be shown to the subject. By setting the
    the `loopType` parameter in `trialsLoop` to `random` we make sure
    the stimulus are shown in a random order without repetition within each
    block of trials.
    - Initializes data summary variables which are updated every trial
    depending on the subject's responses.

- Experiment Instructions:
  
  - Begin Routine:

    - Simple screen with text instructions and a sample of the smiley face:

      ![Choose 34 Instructions Screen](../imgs/Choose34InstructionsScreen.png)

    - Routine terminates once the subject gives any valid keyboard response.

- Trials Setup:

  - Begin Routine:

    - Sets the path to the `trialsLoop` condition file according to the
    current phase.
    - Sets the `criterion` variable to one of the following:

      - Three, if the current phase is the practice phase.
      - Twice the number of pairs, if the current phase is not the practice
      phase and evaluating to criterion.
      - Infinity, if the current phase is not the practice
      phase and evaluating for a fixed number of trials.

- Choose:

  - Begin routine:

    - Shows the pair of objects to the subject and prompts a keyboard
    response:
      ![Choose 34 Choose Screen](../imgs/Choose34TrainingChooseScreen.png)

  - End routine:

    - Update number of consecutive correct responses based on subject's
    response.
    - If in the practice phase, and if it's the first time the subject
    chose an object, then we assign the smiley face to the object which
    the subject **did not** choose.
    - Updates the data summary variables based on subject's response.

- Reveal:

  - Begin Routine:

    - "Lifts" the object chosen by the subject to reveal whether the smiley
    face is under them or not. This is done by updating the position of the
    image stimulus every frame conditioned on the subject response:
      ![Choose 34 Reveal Screen](../imgs/Choose34TrainingRevealScreen.png)

  - End routine:

    - If the subject's consecutive correct responses reached the
    `criterion`, we update the `currentPhase` to the next phase and we
    terminate trials loop early by setting `trialsLoop.finished = True`.
    In the case that we are evaluating to a fixed number of trials
    `criterion` is set to infinity, so early transition will never happen.

- Post-Practice Instructions:

  - This routine occurs only after the practice phase. This is achieved
  by enclosing the routine in a loop (`Post-Practice Screen Loop`)
  which has 1 repetition if `currentPhase` is the practice phase or
  0 repetitions otherwise.

  - Begin routine:

    - Simple screen with text instructions:
      ![Choose 34 Post Practice Screen](../imgs/Choose34PostPracticeScreen.png)
    - Routine terminates once the subject gives any valid keyboard response.

- Transtion

  - Begin Routine:

    - In case there was no early transition, this updates `currentPhase`
    to the next phase after the trials loop is finished.

- End Experiment:

  - Begin routine:

    - Creates a summary csv file where we can find the following fields:
  
    - Shows a simple screen with text instructions:

      "The End.

      Thanks for playing.

      Please inform the experimenter that you are done."

    - Routine and experiment terminate once the subject gives any valid
      keyboard response.

### Generating stimulus files

### Mapping training objects to testing objects

Things such as the date and time at which the
experiment begun, the left and right keys to be used, the paths to
the assets and data directories, etc. Here is where we define the
pairs of objects. For this we create a dictionary (`pairs`) in which
each key is a pair of training objects, and it's value is the
corresponding pair of testing objects.

### Evaluation to criterion

Sets the `criterion` to twice the `Number of pairs` parameter. This
is because when evaluating to criterion we terminate the phase early
if the subject completes a full block of trials with consecutive
correct answers.

### Different numbers of pairs

- Depending on the `Number of pairs` parameter from the settings,
  it eliminates some or none of the object pairs available in the experiment.

### Data  

      - Experiment
      - Subject ID
      - Experimenter
      - Date
      - Time
      - Training Accuracy Average
      - Training RT Average
      - Training Errors
      - Probe Accuracy Average
      - Probe RT Average
      - Probe Errors
