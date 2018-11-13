To make the dist folder for res.volume.1943.lcragage

* run "pyinstaller res.volume.1943.lcragage.py" or "pyinstaller res.volume.1943.lcragage.spec" (if the .spec file was modified w/ hooks etc.)

* copy the following files into the dist/res.volume.1943.lcragage folder:
  - chromedriver.exe
  - travis.csv
  - Travis.08154500.1943-2018.csv
  - stage.vol.travis.2dec.csv
  - pandas._libs.skiplist.pyd
  - pandas._libs.tslibs.nattype.pyd
  - pandas._libs.tslibs.np_datetime.pyd
 
 * in the dist/res.volume.1943.lcragage folder, create a new subfolder "platforms"
 * into the new "platforms" folder, copy dist/res.volume.1943.lcragage/pyqt5/qt/plugins/platforms/qwindows.dll
