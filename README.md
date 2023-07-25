# GluckLab

Repository for the development of the Fish v.15 and Choose v.34 experiments for the Center for Molecular and Behavioural Neuroscience -- Gluck Lab

## How to run the experiments

- Download and install the PyschoPy standalone app according to [these instructions][PsychoPyDownloadInstructions].
**These experiments were developed on PsychoPy version 2023.1.2** other versions may not be compatible.
  MacOS and other versions of the Standalone app can be found [here][PsychoPyReleases].
- Clone this repository using the following command:

```text
git clone https://github.com/J-Mojica/GluckLab.git
```

- Alternatively you can download and decompress the zipped repository. [Click here to download.][GluckLabZippedRepo]

### Fish 15

- Open the PsychoPy app.
- Select File -> Open and then select the file named `fish15.psyexp` found in `GluckLab/fish15/`.
- Select the "Run Experiment" button and follow the instructions on screen.
- The "LEFT" and "RIGHT" keys are `z` and `m` or the left and right arrow keys.
- To quit the experiment early press the ESC key.

### Choose 34

- Open the PsychoPy app.
- Select File -> Open and then select the file named `choose34.psyexp` found in `GluckLab/choose34/`.
- Select the "Run Experiment" button and follow the instructions on screen.
- The "LEFT" and "RIGHT" keys are `z` and `m`.
- To quit the experiment early press the ESC key.
#### Settings
- **Condition**: Concurrent training or Shaping. Currently this setting does not do anything. Acceptable values: `C` or `S`.
- **Number of pairs**: How many pairs of objects to use during the experiment. Acceptable values: Any value on the range `[1,8]`.
- **Evaluate to criterion or fixed number of trials?**: Acceptable values: `criterion`, `Criterion`, `fixed`, `Fixed`
- **Training phase max blocks**: Each trial block consists of each pair of training objects. Among each pair each object
appears in both the left and right position. e.g. 1 block of 8 pairs -> 16 trials, 1 block of 6 pairs -> 12 trials.
Acceptable values: Any positive integer.
- **Testing phase max blocks**: Each trial block consists of each pair of testing objects. Among each pair each object
appears in both the left and right position. e.g. 1 block of 8 pairs -> 16 trials, 1 block of 6 pairs -> 12 trials.
Acceptable values: Any positive integer.

[PsychoPyDownloadInstructions]: https://www.psychopy.org/download.html
[PsychoPyReleases]: https://github.com/psychopy/psychopy/releases
[GluckLabZippedRepo]: https://github.com/J-Mojica/GluckLab/archive/refs/heads/main.zip
