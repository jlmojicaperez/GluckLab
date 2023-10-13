# GluckLab

<div align="center">
  <a href="https://brainhealth.rutgers.edu/">
    <img src=./imgs/Rutgers-AgingAndBrainHealthAllianceLogo.png width=500/>
  </a>
</div>


<p align="center">
【 <a href="./documentation/fish15_documentation.md">Fish 15 Documentation</a> | <a href="./documentation/choose34_documentation.md">Choose 34 Documentation</a> | <a href="./documentation/utils_documentation.md">Utils Documentaton</a> 】
</p>

GluckLab is a repository for the software created for the Aging and Brain Health
Alliance. Developed at Rutgers University CMBN - Gluck Lab.

Current content:
- [Fish 15](./fish15/): Fish Acquired Equivalence task implemented as a PsychoPy experiment
- [Choose 34](./choose34/): Choose Concurrent Discrimination Task implemented as a PsychoPy experiment
- [Utils](./utils/): Useful scripts and tools.
  - [Autoscore](./utils/autoscore.py): a program which automatically scores Fish 8.1a and/or Choose 32.1 output files

## Get the repository

Clone this repository using git and the following command **(Recommeneded)**:

```text
git clone https://github.com/J-Mojica/GluckLab.git
```

- Alternatively you can download and decompress the zipped repository. [Click here to download.][GluckLabZippedRepo]

## Running the Generalization Tasks

The tasks are implemented as PsychoPy experiments. So you will need to 
first install the PsychoPy app. The following section explains how.

### Install PsychoPy

- Download and install [PsychoPy version 2023.1.2 standalone app][PyschoPy2023.1.2].
**Make sure to install this version as other versions may not be compatible**. 
All versions of the Standalone app can be found [here][PsychoPyReleases].
  - [PsychoPy 2023.1.2 standalone app for Windows][PyschoPy2023.1.2Windows]
  - [PsychoPy 2023.1.2 standalone app for MacOS][PyschoPy2023.1.2MacOS]
  
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
- The "LEFT" and "RIGHT" keys are `z` and `m`.
- To quit the experiment early press the ESC key.
#### Settings
- **Language**: Changes the language of the experiment on-screen instructions. The following languages are supported: `english` and `spanish`(`español`).
- **Condition**: Concurrent training or Shaping. Currently this setting does not do anything. Acceptable values: `C` or `S`.
- **Number of pairs**: How many pairs of objects to use during the experiment. Acceptable values: Any value on the range `[1,8]`.
- **Evaluate to criterion or fixed number of trials?**: Acceptable values: `criterion`, `Criterion`, `fixed`, `Fixed`
- **Training phase max blocks**: Each trial block consists of each pair of training objects. Among each pair each object
appears in both the left and right position. e.g. 1 block of 8 pairs -> 16 trials, 1 block of 6 pairs -> 12 trials.
Acceptable values: Any positive integer.
- **Testing phase max blocks**: Each trial block consists of each pair of testing objects. Among each pair each object
appears in both the left and right position. e.g. 1 block of 8 pairs -> 16 trials, 1 block of 6 pairs -> 12 trials.
Acceptable values: Any positive integer.

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
[GluckLabZippedRepo]: https://github.com/J-Mojica/GluckLab/archive/refs/heads/main.zip
[RutgersBrainLogo]: ./imgs/Rutgers-AgingAndBrainHealthAllianceLogo.png
[RutgersBrainHealthWebsite]: https://brainhealth.rutgers.edu/


