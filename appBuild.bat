pyinstaller --onefile --add-data="rsc/*:rsc/" --add-data="icons8-plane-50.png:." --log-level WARN App.py App.spec
pyinstaller --onefile  --noconsole --log-level WARN StandLister.py