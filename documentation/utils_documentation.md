# Utils

## Autoscore

Autoscore is a program which automatically scores Fish 8.1a 
and/or Choose 32.1 output files. The program takes in a directory with
Fish 8.1a and Choose 32.1 output files and outputs two summaries of the
data, one for the fish files, and the other for the choose files, as CSV
files.

### Usage

```
python autoscore.py <DATA PATH>
```

Where `<DATA PATH>` is the path to a directory containing Fish 8.1a and
Choose 32.1 output files in either their raw format (plain text) or as
excel files.

### Design
The program is composed by two python files:

- [autoscore.py](../utils/autoscore.py): Contains the main
routine of the program. It converts all the data files to csv files
then uses the scoring funcitons to score the converted csv files.
- [scoring.py](../utils/scoring.py): Contains the functions
that read and score Fish 8.1a and Choose 32.1 output files.

The functions that score the files were separated to their own file
so that the program may be easily modifiable to accomodate other
types of files. To do this one can simply add new scoring functions
(say, `new_score_fish`, and `new_score_choose`) to the `scoring.py` file, 
and change the imports on lines 39 and 40 of `autoscore.py` from:

```python
from scoring import score_fish_81a as score_fish
from scoring import score_choose_321 as score_choose
```

to:

```python
from scoring import new_score_fish as score_fish
from scoring import new_score_choose as score_choose
```
