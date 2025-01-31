# sweatbox-scenario-generator
Generates .txt files to be used with EuroScope for training sessions at ADC level conducted in the sweatbox.

# Requirements
SSG requires [Python 3.13+](https://www.python.org/downloads/), and the "custom-tkinter" package, version 5.2.2

# How to use
Run App.py, specify the percentage of aircraft with the given qualities, enter the total number of aircraft and click "Generate Sweatbox File".

# Limitations
- While single stands will not be populated with multiple aircraft, sometimes stands that are very close are both populated, leading to euroscope interpreting them as crashed. We are working on a fix for this, but a workaround is to delete one of the conflicting aircraft, then "uncrash" the other using the "ICD" button in the general management tab.
- Once the directory for the generated sweatbox file is set, it cannot be changed. The workaround for this is to clear the "sweatbox_generator.config" file.
- Currently the program is only suitable for OBS>S1 training. S2 training is coming soon!


## Attributions

<a target="_blank" href="https://icons8.com/icon/59723/plane">Plane</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
UI from [customtkinter](https://customtkinter.tomschimansky.com/)

