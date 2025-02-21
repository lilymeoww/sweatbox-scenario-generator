# sweatbox-scenario-generator
Generates .txt files to be used with EuroScope for training sessions at ADC level conducted in the sweatbox.

# Requirements
Should work out of the box.
If you wish to build the app yourself:
run 
`pip install -r requirements.txt`
`python3 -m PyInstaller App.spec`

# Limitations
- While single stands will not be populated with multiple aircraft, sometimes stands that are very close are both populated, leading to euroscope interpreting them as crashed. We are working on a fix for this, but a workaround is to delete one of the conflicting aircraft, then "uncrash" the other using the "ICD" button in the general management tab.
- Currently the program is only suitable for OBS>S1 training. S2 training is coming soon!
- The "Miles in trail" separation doesn't work for arrivals.

## Attributions

<a target="_blank" href="https://icons8.com/icon/59723/plane">Plane</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>

UI from [customtkinter](https://customtkinter.tomschimansky.com/)

