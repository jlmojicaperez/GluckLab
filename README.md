# GluckLab

Repository for the development of the Fish v.15 and Choose v.34 experiments for the Center for Molecular and Behavioural Neuroscience -- Gluck Lab

# Fish 15
## How to run the experiment
### Method 1 (recommnended): Psychopy Standalone App

- Download and install the PyschoPy standalone app according to [these instructions.][PsychoPyDownloadInstructions]
MacOS and other versions of the Standalone app can be found [here.][PsychoPyReleases]
- Clone this repository using the following command:
```
git clone https://github.com/J-Mojica/GluckLab.git
```
- Alternatively you can download and decompress the zipped repository. [Click here to download.][GluckLabZippedRepo]
- Open the PsychoPy app.
- Select File -> Open and then select the file named `fish15.psyexp` found in `GluckLab/fish15/`.
- Select the "Run Experiment" button and follow the instructions on screen.
- To quit early press the ESC key. 

### Method 2: Running the experiment script
- Install PsychoPy **manually** following [these instructions.][PsychoPyDownloadInstructions] **Using Python 3.8 is strongly recommended** for this.
- Clone this repository using the following command:
```
git clone https://github.com/J-Mojica/GluckLab.git
```
- Navigate to `GluckLab/fish15/`:
```
cd GluckLab/fish15/
```
- Run the experiment script using the python interpreter with the PyschoPy package installed:
```
python3 fish15.py
```
- Alternatively you can simply open the psychopy app with the following command and follow the last 4 steps of Method 1:
```
psychopy
```
The following is an example of installing PsychoPy using anaconda/miniconda. For this you will need to download [PyschoPy's environment file][PsychoPyEnvFile].
```
# Creating a virtual environment with the psychopy package and specifications
conda env create -n psychopy -f psychopy-env.yml
conda activate psychopy
# Running the experiment script
python3 fish15.py
# Or alternatively opening the PsychoPy app
psychopy
```


[PsychoPyDownloadInstructions]: https://www.psychopy.org/download.html
[PsychoPyReleases]: https://github.com/psychopy/psychopy/releases
[PsychoPyEnvFile]: https://raw.githubusercontent.com/psychopy/psychopy/master/conda/psychopy-env.yml
[GluckLabZippedRepo]: https://github.com/J-Mojica/GluckLab/archive/refs/heads/main.zip

