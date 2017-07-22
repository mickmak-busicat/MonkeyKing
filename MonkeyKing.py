import sys
import os
import time
from datetime import datetime
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice


class MonkeyKing:

    DEFAULTS = {
        'skipParamChar': '.',
        'waitUntilScreenMaxAttempt': 40,
        'waitUntilScreenInterval': 3,
        'checkScreenThreshold': 0.9,

        'closeAppDragStart': (472, 1153),
        'closeAppDragEnd': (57, 1153),

        'screenCenter': (354, 670),

        'screenIdImagePath': 'screen/%s.png'
    }

    # All am function must return bool to indicate execution result
    ACTION_MAP = {
        'wait-screen': {
            'func': 'amWaitUntilScreen',
            'parameterKey': [
                ['screenId', None, 'str'],
                ['maxAttempt', DEFAULTS['waitUntilScreenMaxAttempt'], 'int'],
                ['interval', DEFAULTS['waitUntilScreenInterval'], 'int'],
                ['threshold', DEFAULTS['checkScreenThreshold'], 'float'],
                ['optional', False, 'bool']
            ],
            'log': '[INFO] Wait until screen appears'
        },
        'branch-screen': {
            # Check result saved to self.branchIf
            'func': 'amBranchIfScreen',
            'parameterKey': [
                ['screenId', None, 'str'],
                ['threshold', DEFAULTS['checkScreenThreshold'], 'float']
            ],
            'log': '[INFO] Branch if screen check'
        },
        'tap-until-screen': {
            'func': 'amTapUntilScreen',
            'parameterKey': [
                ['screenId', None, 'str'],
                ['maxTap', DEFAULTS['waitUntilScreenMaxAttempt'], 'int'],
                ['interval', DEFAULTS['waitUntilScreenInterval'], 'int'],
                ['threshold', DEFAULTS['checkScreenThreshold'], 'float'],
                ['position', None, 'pos'],
                ['optional', False, 'bool']
            ],
            'log': '[INFO] Trying to pass screen'
        },
        'pass-screen': {
            'func': 'amPassScreen',
            'parameterKey': [
                ['screenId', None, 'str'],
                ['maxAttempt', DEFAULTS['waitUntilScreenMaxAttempt'], 'int'],
                ['interval', DEFAULTS['waitUntilScreenInterval'], 'int'],
                ['threshold', DEFAULTS['checkScreenThreshold'], 'float'],
                ['position', None, 'pos'],
                ['optional', False, 'bool']
            ],
            'log': '[INFO] Trying to pass screen'
        },
        'sleep': {
            'func': 'amSleep',
            'parameterKey': [['duration', 0, 'float']],
            'log': '[INFO] MonkeyKing sleep event'
        },
        'shell': {
            'func': 'amRunShell',
            'parameterKey': [['cmd', '', 'str']],
            'log': '[INFO] Run adb shell'
        },

        'tap': {
            'func': 'amTap',
            'parameterKey': [['position', None, 'pos']],
            'log': '[INFO] Tap event'
        },
        'hold': {
            'func': 'amHold',
            'parameterKey': [['position', None, 'pos']],
            'log': '[INFO] Hold event'
        },
        'release': {
            'func': 'amRelease',
            'parameterKey': [],
            'log': '[INFO] Release event'
        },
        'drag': {
            'func': 'amDrag',
            'parameterKey': [['from', None, 'pos'], ['to', None, 'pos'], ['duration', 0, 'float']],
            'log': '[INFO] Drag event'
        },
        'press': {
            # String from https://developer.android.com/reference/android/view/KeyEvent.html#KEYCODE_MENU
            'func': 'amPress',
            'parameterKey': [['keyCode', None, 'str']],
            'log': '[INFO] Press a key'
        },
        'input-text': {
            'func': 'amInputText',
            'parameterKey': [['text', '', 'str']],
            'log': '[INFO] Input a string'
        },

        'bootup': {
            'func': 'amBootupGame',
            'parameterKey': [],
            'log': '[INFO] Booting up the game'
        },
        'shutdown': {
            'func': 'amShutdownGame',
            'parameterKey': [],
            'log': '[INFO] Shutting down the game'
        },
        'desktop': {
            'func': 'amShowDesktop',
            'parameterKey': [],
            'log': '[INFO] Show desktop'
        },
        'backup-game': {
            'func': 'amBackupGameAccount',
            'parameterKey': [],
            'log': '[INFO] Backup game account data'
        },
        'reset-game': {
            'func': 'amResetGameAccount',
            'parameterKey': [],
            'log': '[INFO] Reset the game to beginning'
        },

        'jump': {
            'func': 'amJump',
            'parameterKey': [['target', None, 'str']],
            'log': '[INFO] Jump to'
        },
        'jump-true': {
            'func': 'amJumpIfTrue',
            'parameterKey': [['target', None, 'str']],
            'log': '[INFO] Jump to if branchIf is True'
        },
        'jump-false': {
            'func': 'amJumpIfFalse',
            'parameterKey': [['target', None, 'str']],
            'log': '[INFO] Jump to if branchIf is False'
        },
        'checkpoint': {
            # checkpoint with id
            'func': '',
            'parameterKey': [['id', None, 'str']],
            'log': '-- [CHECKPOINT] --'
        },
        'exit': {
            'func': 'exitProgram',
            'parameterKey': [['message', 'No info', 'str']],
            'log': '[INFO] Urget exit program'
        },
        'save-snapshot': {
            'func': 'amSaveSnapshot',
            'parameterKey': [],
            'log': '[INFO] Save snapshot'
        },
        'save-result-screen': {
            'func': 'amSaveResultScreen',
            'parameterKey': [],
            'log': '[INFO] Save result screen'
        }
    }

    def __init__(self, device, config):
        self.device = device
        self.config = config
        self.done = False
        self.workingLog = []
        self.workPointer = 0
        self.branchIf = None

        if not os.path.exists(self.config.getProjectPath()):
            os.mkdir(self.config.getProjectPath())

        for path in self.config.getCoordinateFilesPath():
            fileName = self.config.getFileFullPath(path)
            try:
                cf = open(fileName, 'r')
                for line in cf:
                    if line[0] == '#':
                        continue
                    cmpt = line.splitlines()[0].split(' ')
                    try:
                        tmp = cmpt[1].split(',')
                        coord = self.makeCoordinateDict(cmpt[0], (int(tmp[0]), int(tmp[1])))
                    except:
                        print self.log('[MAKE COORD] Line exception: %s' % (str(cmpt)))

                    if not self.config.addCoordinate(coord):
                        print self.log('[MAKE COORD] Unable to add %s' % (line))
            except:
                print self.log('[INIT] Coordinate file read error: (%s)' % (fileName))

        for path in self.config.getScreenFilesPath():
            fileName = self.config.getFileFullPath(path)
            try:
                cf = open(fileName, 'r')
                for line in cf:
                    if line[0] == '#':
                        continue
                    cmpt = line.splitlines()[0].split(' ')
                    try:
                        tmp = cmpt[2].split(',')
                        screen = self.makeScreenDict(cmpt[0], cmpt[1], (int(tmp[0]), int(tmp[1]), int(tmp[2]), int(tmp[3])))
                    except:
                        print self.log('[MAKE SCREEN] Line exception: %s' % (str(cmpt)))

                    if not self.config.addScreen(screen):
                        print self.log('[MAKE SCREEN] Unable to add %s' % (line))
            except:
                print self.log('[INIT] Screen file read error: (%s)' % (fileName))

        for path in self.config.getScriptFilesPath():
            fileName = self.config.getFileFullPath(path)
            try:
                cf = open(fileName, 'r')
                for line in cf:
                    if line[0] == '#' or line == '\n':
                        continue
                    cmpt = line.splitlines()[0].split(' ')
                    action = {'action': cmpt[0]}
                    pidx = 1
                    try:
                        for param in MonkeyKing.ACTION_MAP[cmpt[0]]['parameterKey']:
                            original = self.smartcast(cmpt[pidx], param[2])
                            if not cmpt[pidx] == MonkeyKing.DEFAULTS['skipParamChar'] and original is not None:
                                action[param[0]] = original
                            elif original is None:
                                print self.log('[MAKE SCRIPT] Param (%s) cast failed. "%s" should be existing (%s).  #%s' % (param[0], cmpt[pidx], param[2], str(cmpt)))
                            pidx = pidx + 1
                    except:
                        print self.log('[MAKE SCRIPT] Line exception Takes %d param.  #%s' % (len(MonkeyKing.ACTION_MAP[cmpt[0]]['parameterKey']), str(cmpt)))

                    if not self.config.addScriptAction(action):
                        print self.log('[MAKE SCRIPT] Unable to add %s' % (line))
            except:
                print self.log('[INIT] Script file read error: (%s)' % (fileName))

    # Core
    def makeCoordinateDict(self, cid, position):
        return {'id': cid, 'position': position}

    def makeScreenDict(self, sid, filePath, rect):
        dictionary = {'id': sid, 'rect': rect}
        if not filePath == MonkeyKing.DEFAULTS['skipParamChar']:
            dictionary['file'] = filePath
        return dictionary

    def log(self, message):
        self.workingLog.append(message)
        return message

    def createFolder(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def saveLog(self):
        folder = 'logs'
        self.createFolder(self.config.getFileFullPath(folder))
        path = self.config.getFileFullPath("%s/work_%s.log" % (folder, datetime.now().strftime('%Y%m%d_%H%M%S')))
        f = open(path, 'w')
        result = f.write("\n".join(self.workingLog))
        f.close()
        return result

    def saveFailedScreenCheck(self, currentScreenImage, targetScreenImage, rect):
        folder = 'failed-screen'
        pairKey = "%s" % time.time()
        result = False
        self.createFolder(self.config.getFileFullPath(folder))

        crImagePath = self.config.getFileFullPath("%s/fpair_%s_current_rect.png" % (folder, pairKey))
        cImagePath = self.config.getFileFullPath("%s/fpair_%s_current.png" % (folder, pairKey))
        tImagePath = self.config.getFileFullPath("%s/fpair_%s_target.png" % (folder, pairKey))
        result = currentScreenImage.writeToFile(cImagePath, 'png')
        result = result and targetScreenImage.writeToFile(tImagePath, 'png')

        if rect[2] + rect[3] > 0:
            currentSubScreen = currentScreenImage.getSubImage(rect)
            result = result and currentSubScreen.writeToFile(crImagePath, 'png')

        return result

    def positionParse(self, position):
        if position.__class__ is tuple and len(position) == 2:
            return position
        elif position.__class__ is str:
            return self.config.getCoordinateById(position)['position']
        else:
            return None

    def jumpTargetParse(self, target):
        if target.__class__ is str:
            return self.config.getScriptStepIndexByCheckpoint(target)
        elif target.__class__ is int:
            return target
        else:
            return None

    def smartcast(self, string, theType):
        typeMap = {
            'int': int,
            'str': str,
            'float': float,
            'pos': 'pos',
            'bool': 'bool'
        }

        if string == MonkeyKing.DEFAULTS['skipParamChar']:
            return False

        try:
            targetType = typeMap[theType]
            if targetType.__class__ is type:
                return targetType(string)
            else:
                if targetType == 'bool':
                    return (string == 'true')
                elif targetType == 'pos':
                    p = string.split(',')
                    if len(p) == 2:
                        return tuple(map(lambda d: int(d), p))
                    else:
                        return self.positionParse(string)
        except:
            return None

        return None

    def exitProgram(self, message):
        sys.exit(message)

    def amJump(self, target):
        t = self.jumpTargetParse(target)
        if not t or t < 0 or t >= self.config.getScriptLength():
            return False

        self.workPointer = t
        return True

    def amJumpIfTrue(self, target):
        t = self.jumpTargetParse(target)
        if not t or t < 0 or t >= self.config.getScriptLength():
            return False

        print self.log('[TRUE BRANCH] branchIf state: (%s)' % (self.branchIf))

        if self.branchIf is True:
            self.workPointer = t
            self.branchIf = None
        return True

    def amJumpIfFalse(self, target):
        t = self.jumpTargetParse(target)
        if not t or t < 0 or t >= self.config.getScriptLength():
            return False

        print self.log('[FALSE BRANCH] branchIf state: (%s)' % (self.branchIf))

        if self.branchIf is False:
            self.workPointer = t
            self.branchIf = None
        return True

    def amBackupGameAccount(self):
        folder = 'backup'
        gameKey = "%s" % time.time()
        gameFolder = "%s/%s" % (folder, gameKey)
        self.createFolder(self.config.getFileFullPath(folder))
        self.createFolder(self.config.getFileFullPath(gameFolder))
        paths = self.config.getUserFilesPath()

        for p in paths:
            os.system('adb pull %s %s' % (p, self.config.getFileFullPath(gameFolder)))

        return True

    def amResetGameAccount(self):
        # TODO:
        # Remove a list of file here to make the game can start at beginning
        paths = self.config.getResetFilesPath()
        print paths
        # self.runShell()

    def amRunShell(self, cmd):
        return self.device.shell(cmd)

    def amSaveSnapshot(self, name=None):
        folder = 'cap'
        fileName = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.createFolder(self.config.getFileFullPath(folder))
        if name:
            fileName = name
        path = self.config.getFileFullPath("%s/cap_%s.png" % (folder, fileName))
        screen = self.device.takeSnapshot()
        return screen.writeToFile(path, 'png')

    # Emulator layout related
    def isAtScreen(self, screenId, threshold):
        screen = self.config.getScreenById(screenId)
        currentScreen = self.device.takeSnapshot()
        targetScreen = MonkeyRunner.loadImageFromFile(self.config.getFileFullPath(screen.get('file', self.DEFAULTS['screenIdImagePath'] % (screenId))))
        rect = screen.get('rect', (0, 0, 0, 0))
        return self.checkScreenByScreen(currentScreen, targetScreen, rect, threshold)

    def checkScreenByScreen(self, currentScreenImage, targetScreenImage, rect, threshold=0.9):
        isNeedToCut = False

        if rect[2] + rect[3] > 0:
            isNeedToCut = True

        if isNeedToCut:
            currentSubScreen = currentScreenImage.getSubImage(rect)
            return targetScreenImage.sameAs(currentSubScreen, threshold)
        else:
            return targetScreenImage.sameAs(currentScreenImage, threshold)

    def amBootupGame(self):
        return self.device.startActivity(component=self.config.getStartActivity())

    def amShutdownGame(self):
        # Open multitask menu and drag to close the game
        self.device.press('KEYCODE_APP_SWITCH', MonkeyDevice.DOWN_AND_UP)
        MonkeyRunner.sleep(1)
        self.amDrag(self.DEFAULTS['closeAppDragStart'], self.DEFAULTS['closeAppDragEnd'], 1)
        return True

    def amShowDesktop(self):
        self.device.press('KEYCODE_APP_SWITCH', MonkeyDevice.DOWN_AND_UP)
        MonkeyRunner.sleep(1)
        self.amTap((400, 400))
        return True

    def amWaitUntilScreen(self, screenId, maxAttempt, interval, threshold, optional):
        count = 0
        screen = self.config.getScreenById(screenId)
        targetScreen = MonkeyRunner.loadImageFromFile(self.config.getFileFullPath(screen.get('file', self.DEFAULTS['screenIdImagePath'] % (screenId))))
        rect = screen.get('rect', (0, 0, 0, 0))
        currentScreen = self.device.takeSnapshot()

        while not self.checkScreenByScreen(currentScreen, targetScreen, rect, threshold) and count < maxAttempt:
            count = count + 1
            MonkeyRunner.sleep(interval)
            currentScreen = self.device.takeSnapshot()
            print self.log("[WAIT] Attempt: %d of %d" % (count, maxAttempt))

        result = (count < maxAttempt)
        if not result:
            # Log compare image if failed more than max attempt and end the program.
            print self.log("[WAIT FAIL] Screen check failed: %s" % (screen))
            self.saveFailedScreenCheck(currentScreen, targetScreen, rect)
            if not optional:
                self.done = True

        return result

    def amTapUntilScreen(self, screenId, maxTap, interval, threshold, optional):
        count = 0
        screen = self.config.getScreenById(screenId)
        targetScreen = MonkeyRunner.loadImageFromFile(self.config.getFileFullPath(screen.get('file', self.DEFAULTS['screenIdImagePath'] % (screenId))))
        rect = screen.get('rect', (0, 0, 0, 0))
        currentScreen = self.device.takeSnapshot()

        while not self.checkScreenByScreen(currentScreen, targetScreen, rect, threshold) and count < maxTap:
            count = count + 1
            MonkeyRunner.sleep(interval)
            self.amTap(self.DEFAULTS['screenCenter'])
            currentScreen = self.device.takeSnapshot()
            print self.log("[TAP UNTIL] Tap: %d of %d" % (count, maxTap))

        result = (count < maxTap)
        if not result:
            # Log compare image if failed more than max attempt and end the program.
            print self.log("[TAP UNTIL FAIL] Screen check failed: %s" % (screen))
            self.saveFailedScreenCheck(currentScreen, targetScreen, rect)
            if not optional:
                self.done = True

        return result

    def amPassScreen(self, screenId, maxAttempt, interval, threshold, position, optional):
        if self.amWaitUntilScreen(self, screenId, maxAttempt, interval, threshold, optional):
            MonkeyRunner.sleep(0.5)
            return self.amTap(position or ("pass-%s" % screenId))
        return False

    def amBranchIfScreen(self, screenId, threshold):
        self.branchIf = self.isAtScreen(screenId, threshold)
        return True

    def amSleep(self, duration):
        return MonkeyRunner.sleep(duration)

    def amTap(self, position):
        p = self.positionParse(position)
        if not p:
            return False
        return self.device.touch(p[0], p[1], MonkeyDevice.DOWN_AND_UP)

    def amHold(self, position):
        p = self.positionParse(position)
        if not p:
            return False
        return self.device.touch(p[0], p[1], MonkeyDevice.DOWN)

    def amRelease(self):
        return self.device.touch(0, 0, MonkeyDevice.UP)

    def amDrag(self, fromPosition, toPosition, duration):
        f = self.positionParse(fromPosition)
        t = self.positionParse(toPosition)
        if not f or not t:
            return False
        return self.device.drag(f, t, duration)

    def amPress(self, keyCode):
        if not keyCode:
            return False
        return self.device.press(keyCode, MonkeyDevice.DOWN_AND_UP)

    def amInputText(self, text):
        return self.device.type(text)

    # Main work function
    def work(self):
        scripts = self.config.getScripts()
        scriptLen = self.config.getScriptLength()

        if scriptLen == 0:
            print self.log("[WARNING] No script setup.")
            return False

        self.amBootupGame()

        while not self.done:
            result = False
            s = scripts[self.workPointer]
            actionStr = s.get('action', 'unknown')

            try:
                action = MonkeyKing.ACTION_MAP[actionStr]
                params = map(lambda p: s.get(p[0], p[1]), action['parameterKey'])

                print self.log("%s: %s" % (action['log'], str(s)))
                if action['func'] != '':
                    result = getattr(self, action['func'])(*params)
                else:
                    # Skip non functional action.
                    result = True

                # TODO: result seems not work from device function return?
                # if not result:
                #     print self.log("[WARNING] Action not completed: %s. Please check parameter." % (str(s)))
            except:
                print self.log("[ERROR] Script exception: %s" % (str(s)))
                self.done = True

            # Global sleep time between script.
            MonkeyRunner.sleep(0.5)
            self.workPointer = self.workPointer + 1

            if self.workPointer >= scriptLen:
                print self.log("[END] Completed all scripts.")
                self.done = True
