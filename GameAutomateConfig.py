class GameAutomateConfig:

    @classmethod
    def loadConfig(cls, config):
        # Check required keys exist. Create object if all exist.
        requiredKeys = [
            'GAME_PACKAGE',
            'RUNNABLE_ACTITVITY',
            'SCREENS',
            'GAME_USER_FILES',
            'COORDINATE_FILES',
            'SCREEN_FILES',
            'SCRIPT_FILES',
            'COORDINATES',
            'APK_LOCATION',
            'SCRIPTS',
            'GAME_PROJECT_PATH']
        for k in requiredKeys:
            if k not in config.keys():
                return None
        return cls(config)

    def __init__(self, config):
        self.GAME_PACKAGE = config['GAME_PACKAGE']
        self.RUNNABLE_ACTITVITY = config['RUNNABLE_ACTITVITY']
        self.SCREENS = config['SCREENS']
        self.GAME_USER_FILES = config['GAME_USER_FILES']
        self.COORDINATES = config['COORDINATES']
        self.APK_LOCATION = config['APK_LOCATION']
        self.SCRIPTS = config['SCRIPTS']
        self.GAME_PROJECT_PATH = config['GAME_PROJECT_PATH']
        self.SCRIPT_FILES = config['SCRIPT_FILES']
        self.COORDINATE_FILES = config['COORDINATE_FILES']
        self.SCREEN_FILES = config['SCREEN_FILES']

    def addCoordinate(self, dictionary):
        if dictionary.get('id', None) and dictionary.get('position', None):
            self.COORDINATES.append(dictionary)
            return True
        return False

    def addScreen(self, dictionary):
        if dictionary.get('id', None) and dictionary.get('rect', None):
            self.SCREENS.append(dictionary)
            return True
        return False

    def addScriptAction(self, dictionary):
        if dictionary.get('action', None):
            self.SCRIPTS.append(dictionary)
            return True
        return False

    def getGamePackage(self):
        return self.GAME_PACKAGE

    def getRunnableActivity(self):
        return self.RUNNABLE_ACTITVITY

    def getStartActivity(self):
        return "%s/%s" % (self.GAME_PACKAGE, self.RUNNABLE_ACTITVITY)

    def getScreenById(self, sid):
        try:
            return filter(lambda x: x.get('id', '') == sid, self.SCREENS)[0]
        except:
            return None

    def getScriptFilesPath(self):
        return self.SCRIPT_FILES

    def getCoordinateFilesPath(self):
        return self.COORDINATE_FILES

    def getScreenFilesPath(self):
        return self.SCREEN_FILES

    def getUserFilesPath(self):
        return self.GAME_USER_FILES

    def getCoordinateById(self, cid):
        try:
            return filter(lambda x: x.get('id', '') == cid, self.COORDINATES)[0]
        except:
            return None

    def getAPKLocation(self):
        return self.APK_LOCATION

    def getProjectPath(self):
        return self.GAME_PROJECT_PATH

    def getFileFullPath(self, name):
        return "%s/%s" % (self.GAME_PROJECT_PATH, name)

    def getScripts(self):
        return self.SCRIPTS

    def getScriptStepIndexByCheckpoint(self, name):
        for idx, s in enumerate(self.SCRIPTS):
            if (s.get('action', '') == 'checkpoint' and s.get('id', '') == name):
                return idx
        return None

    def getScriptLength(self):
        return len(self.SCRIPTS)
