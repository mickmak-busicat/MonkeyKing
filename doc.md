-
# Auto getcha project
-
Due to different version of python(2.7) and jypthon(2.5) are using. The whole process can be separated into two parts:

1. A Monkeyrunner script to automate the game to getcha
2. A python script to process the result generated from Monkeyrunner.

### View APK start activity:
```
./aapt d badging ~/monkeyscript/apk/cf.apk 
```
Example:

```
launchable-activity: name='jp.wonderplanet.Yggdrasil.BULL'  label='Crash Fever' icon=''
```

### Get sub image in terminal
```
convert info.png -crop $wx$h+$x+$y converted.png
```

### Run MonkeyKing Main program
```
./monkeyrunner ~/monkeyscript/MonkeyMain.py ${Config name}
```

***: Target config file must be in the same directory sa MonkeyMain.py**

## Automate script

### Objective:
Auto-control the game to pass tutorials and get the first getcha. And able to start the process from beginning without downloading the game data again.

### Preconfig:
Add custom project path to monkeyrunner:

```
import sys
sys.path.append('/Users/makkit/monkeyscript')
# Start import.
import MonkeyKing...
```

### Result:
The script of this part should able to generate:

1. **Getcha result screen**
2. User profile data (if possible)
2. Recovery code screen(Optional)
1. Other information like getcha character identity(Optional)

### Presetup:

- Boot nox player.
- `adb connect 127.0.0.1:62001` # use `adb disconnect` to disconnect.
- then `waitForConnection()` can get access to nox player.
- Use `MonkeyDevice` to control the simulator.

### APK install location in NOX:
`/data/app/`


## Working with automated result

### Objective:
Another script should be able to read information from screenshots generated in simulator.

Advanced:

1. Write result and upload screenshot to server db.

### Tesseract OCR:
OCR tips:

1. Crop the image smaller that contains the significant text.
2. Use REGEXP to get final result from text.

```
from PIL import Image
import pytesseract
Image.open('/Users/makkit/monkeyscript/dummy/cap.png')
pytesseract.image_to_string(image, lang='eng')
```

--
	### Task 1: (nice)
	1. Run a game
	2. Go to target screen(Preset)
	3. Take snapshot
	4. Output log
	5. Shut down game

	### Task 2: (nice)
	1. Create files in a game package
	2. Use script to remove these files
	3. backup some files

### Task 3
1. Run a game
2. Get first getcha
3. Take snapshot
4. Output log
5. Reset game
6. Check if reset ok

### Task 4
1. Run repeat first getcha of a game for one day
2. Check performance

--
# [Concept] Config Tool draft:

function needed:

- Load many images(screen cap image)
- Easy switch images(show/hide)
- add tap point on image(export to x,y point id)

--
# MonkeyKingScript(.mks)

Script can be transformed into config like programmable code.

Format example:
`wait-screen gacha-screen 50 5 . . .`

Description:

- First param: command inside ACTION_MAP dict
- Second and so on: params of the action
- `.` can be used if no param needed

Usage:

- Define list of MonkeyKingScript instead of define list of action dict in config. Script file will be transformed and appended into config object one by one in array order.
- example:

```
'COORDINATE_FILES': ['script/coord.mks', 'script/main-flow.mks'],
'SCRIPT_FILES': ['script/part1.mks', 'script/part2.mks'],
'SCREEN_FILES': ['script/main-flow-screen.mks', 'script/flow-2.mks'],
```

- ? All script file name will also be a `checkpoint` variable. So script can use jump to jump to content of a mks.
- `checkpoint` defined are shared among all scripts.

-
# Website interface

- Gacha function
	- Every member can only do one gacha every n minutes.
	- One gacha have 5~10 accounts
	- Stat showing the gacha pool (~100 account left, 1% SR, 99% R)
	