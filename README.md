# OBS text from file with math

This repository includes a python script which allows running an equation over text read from a file (periodically in intervals).

## Installation
To add this to OBS go to Tools > Scripts > add a script via the plus and then select the python file downloaded from this repository.

**NOTE**: Ensure Python is installed and the python path is set in OBS in the scripts window.
This should be Python version 3.6.x 64-bit, I recommend 3.6.8 since it has an installer build for windows for ease.
You can find this installer [here](https://www.python.org/downloads/release/python-368/).
For example as to what should be in it should be alike `C:/Users/(User)/AppData/Local/Programs/Python/Python36`.

## Setup

These are the following settings to set up, these are found in the Scripts window in OBS when selecting this script;

- Update Interval: An update interval in seconds, how often it reads the text file for updates
- Text File Path: The path to the text file which should be used for this script (a text file with a number, presumably updated by something else).
- Equation: Equation that can be provided to be done over the number (represented by `x` in the equation) read from the text file, the script always rounds the number. An example equation could be `x/10` to remove the last number.
- Text Destination: A text source which the result of this script will update to. All styling can be done as normal in there, the text value will be overwritten by the script.

There's also a refresh button in case you want to manually refresh (rerun) the script, this triggers the same as the interval.