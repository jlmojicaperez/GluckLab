# GluckLab

<div align="center">
  <a href="https://brainhealth.rutgers.edu/">
    <img src=./imgs/Rutgers-AgingAndBrainHealthAllianceLogo.png width=500/>
  </a>
</div>


<p align="center">
【 <a href="./documentation/fish15_documentation.md">Fish 15</a> | <a href="./documentation/choose34_documentation.md">Choose 34</a> | <a href="./documentation/choose_fmri_documentation.md">Choose fMRI</a> | <a href="./documentation/charts_documentation.md">Charts</a> | <a href="./documentation/utils_documentation.md">Utils</a> 】

</p>

---

GluckLab is a repository for the software created for the Aging and Brain Health
Alliance.

Current content:
- [Fish 15](./fish15/): Fish Acquired Equivalence task implemented as a PsychoPy experiment.
- [Choose 34](./choose34/): Choose Concurrent Discrimination Task implemented as a PsychoPy experiment.
- [Choose fMRI](./choose_fmri/): Modified Choose Concurrent Discrimination Task as an fMRI tas implemented as a PsychoPy experiment.
- [Charts](./charts/): Experiment designed to monitor a subject's progress in learning deterministic categorization and analyze their subsequent generalizations.
Implemented as a Psychopy exeperiment
- [Utils](./utils/): Useful scripts and tools.
  - [Autoscore](./utils/autoscore.py): a program which automatically scores Fish 8.1a and/or Choose 32.1 output files
  - [SubjectID to Seqid](./utils/subjectid_to_seqid.py): a program to convert Subject IDs to 
SeqIDs + REDCap instance number and viceversa.

## Get the repository

Clone this repository using git and the following command **(Recommeneded)**:

```text
git clone https://github.com/jlmojicaperez/GluckLab.git
```

- Alternatively you can download and decompress the zipped repository. [Click here to download.][GluckLabZippedRepo]

## Running the Generalization Tasks

The tasks are implemented as PsychoPy experiments. So you will need to 
first install the PsychoPy app. The following section explains how.

### Install PsychoPy

- Download and install [the latest version of the PsychoPy standalone app][PsychoPyDownloadInstructions].
All versions of the Standalone app can be found [here][PsychoPyReleases].
  
- MacOS users may have to give permission to PsychoPy to control their computer. To do this:
  - Go to System Settings -> Privacy & Security -> Accessibility
  - Unlock these settings using your password if necessary.
  - Click the add button.
  - Select the PsychoPy app in the list, then click Open.
  
### Fish 15

- Open the file named `fish15.psyexp` found in `GluckLab/fish15/`. If prompted,
select the PsyschoPy app to open this file. The experiment should open
in the PsychoPy app. 
- Select the "Run Experiment" button and follow the instructions on screen.
- The "LEFT" and "RIGHT" keys are `z` and `m` or the left and right arrow keys.
- To quit the experiment early press the ESC key.
#### Settings
- **Language**: Changes the language of the experiment on-screen instructions. The following languages are supported: `english` and `spanish`(`español`).

### Choose 34

- Open the file named `choose34.psyexp` found in `GluckLab/choose34/`. If prompted,
select the PsyschoPy app to open this file. The experiment should open
in the PsychoPy app.
- Select the "Run Experiment" button and follow the instructions on screen.
- The "LEFT" and "RIGHT" keys are `z` and `m` by default, but it can be changed in the experiment settings.
- To quit the experiment early press the ESC key.
#### Settings
- **Language**: Changes the language of the experiment on-screen instructions. The following languages are supported: `english` and `spanish`(`español`).
- **Number of pairs**: How many pairs of objects to use during the experiment. Acceptable values: Any value on the range `[1,8]`.
- **Evaluate to criterion or fixed number of trials?**: Acceptable values: `criterion`, `fixed`.
- **Training phase max blocks**: Each trial block consists of each pair of training objects. Among each pair each object
appears in both the left and right position. e.g. 1 block of 8 pairs -> 16 trials, 1 block of 6 pairs -> 12 trials.
Acceptable values: Any positive integer.
- **Testing phase max blocks**: Each trial block consists of each pair of testing objects. Among each pair each object
appears in both the left and right position. e.g. 1 block of 8 pairs -> 16 trials, 1 block of 6 pairs -> 12 trials.
Acceptable values: Any positive integer.
- **Left Key**/**Right Key**: Acceptable values: The name of any key recognized by PsychoPy. To find the name of a key:
  - Open the PyschoPy app
  - In the "Coder" window click on Demos -> Input -> keyNameFinder.py
  - Select run and follow the instructions on screen.

### Choose fMRI

- Open the file named `choose_fmri.psyexp` found in `GluckLab/choose_fmri/`. If prompted,
select the PsyschoPy app to open this file. The experiment should open
in the PsychoPy app.
- Select the "Run Experiment" button and follow the instructions on screen.
- The "LEFT" and "RIGHT" keys are `z` and `m` by default, but it can be changed in the experiment settings.
- To quit the experiment early press the ESC key.
#### Settings
- **Language**: Changes the language of the experiment on-screen instructions. The following languages are supported: `english` and `spanish`(`español`).
- **Number of pairs**: How many pairs of objects to use during the experiment. Acceptable values: Any value on the range `[1,4]`.
- **Evaluate to criterion or fixed number of trials?**: Acceptable values: `criterion`, `fixed`.
- **Training phase max blocks**: Each trial block consists of each pair of training objects. Among each pair each object
appears in both the left and right position. e.g. 1 block of 4 pairs -> 8 trials, 1 block of 2 pairs -> 4 trials.
Acceptable values: Any positive integer.
- **Testing phase max blocks**: Each trial block consists of each pair of testing objects. Among each pair each object
appears in both the left and right position. e.g. 1 block of 4 pairs -> 8 trials, 1 block of 2 pairs -> 4 trials.
Acceptable values: Any positive integer.
- **Left Key**/**Right Key**: Acceptable values: The name of any key recognized by PsychoPy. To find the name of a key:
  - Open the PyschoPy app
  - In the "Coder" window click on Demos -> Input -> keyNameFinder.py
  - Select run and follow the instructions on screen.
  
### Charts
- Open the file named `charts.psyexp` found in `GluckLab/charts/`. If prompted,
select the PsyschoPy app to open this file. The experiment should open
in the PsychoPy app.
- Select the "Run Experiment" button and follow the instructions on screen.
- The "LEFT" and "RIGHT" keys are `z` and `m` by default, but it can be changed in the experiment settings.
- To quit the experiment early press the ESC key.
#### Settings
- **Left Key**/**Right Key**: Acceptable values: The name of any key recognized by PsychoPy. To find the name of a key:
  - Open the PyschoPy app
  - In the "Coder" window click on Demos -> Input -> keyNameFinder.py
  - Select run and follow the instructions on screen.


## Autoscoring Fish 8.1a and Choose 32.1 Output files

The [utils directory](./utils/) contains an auto-scoring program
for the output files of Fish 8.1a and Choose 32.1. To use it:

- Copy all the Fish 8.1a and Choose 32.1 you wish to score on a single
directory and copy its path (`<DATA PATH>`).
- Navigate to the `GluckLab` repository on a terminal.
- Use the following command:

```python
python utils/autoscore.py <DATA PATH>
```

[PsychoPyDownloadInstructions]: https://www.psychopy.org/download.html
[PsychoPyReleases]: https://github.com/psychopy/psychopy/releases
[PyschoPy2023.1.2]: https://github.com/psychopy/psychopy/releases/tag/2023.1.2
[PyschoPy2023.1.2Windows]: https://github.com/psychopy/psychopy/releases/download/2023.1.2/StandalonePsychoPy-2023.1.2-win64.exe
[PyschoPy2023.1.2MacOS]:https://github.com/psychopy/psychopy/releases/download/2023.1.2/StandalonePsychoPy-2023.1.2-macOS.dmg
[GluckLabZippedRepo]: https://github.com/jlmojicaperez/GluckLab/archive/refs/heads/main.zip
[RutgersBrainLogo]: ./imgs/Rutgers-AgingAndBrainHealthAllianceLogo.png
[RutgersBrainHealthWebsite]: https://brainhealth.rutgers.edu/


