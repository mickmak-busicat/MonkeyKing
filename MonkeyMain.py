from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import commands
import sys
import os
from pprint import *

MONKEY_PROJECT_PATH = '/Users/makkit/monkeyscript'
sys.path.append(MONKEY_PROJECT_PATH)

# Game modules
# from MainConfig import *
from MonkeyKing import MonkeyKing
from GameAutomateConfig import GameAutomateConfig

if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.exit("Missing config.")

    # Load config file
    config = __import__(sys.argv[-1])

    if 'ENV_CONFIG' not in dir(config):
        sys.exit("Configuration not found.")

    # Create config object for Monkey King
    gaConfig = GameAutomateConfig.loadConfig(config.ENV_CONFIG)

    print "[MAIN] Loaded config file."

    if not gaConfig:
        sys.ext("Missing configuration items. Please check config file.")

    # Get emulator for Monkey King
    device = MonkeyRunner.waitForConnection()

    if not device:
        print "[MAIN] No device available."
    else:
        print "[MAIN] Check package exist."

        # Install apk if package not exist.
        apk_path = device.shell('pm path %s' % gaConfig.getGamePackage())
        if apk_path.startswith('package:'):
            print "[MAIN] App already installed."
        else:
            print "[MAIN] App not installed, installing APKs..."
            device.installPackage(gaConfig.getAPKLocation())

        print "[MAIN] Work start."

        # Start working.
        king = MonkeyKing(device, gaConfig)
        king.work()
        king.saveLog()

        print "[MAIN] Work done."

    # connection to the current device, and return a MonkeyDevice object
    # device = MonkeyRunner.waitForConnection()

    # apk_path = device.shell('pm path com.myapp')
    # if apk_path.startswith('package:'):
    #     print "myapp already installed."
    # else:
    #     print "myapp not installed, installing APKs..."
    #     device.installPackage('/Users/makkit/monkeyscript/apk/granblue.apk')

    # print "launching myapp..."
    # device.startActivity(component='jp.mbga.a12016007.lite/jp.dena.shellappclient.ShellAppProxyActivity')

    # #screenshot
    # MonkeyRunner.sleep(1)
    # result = device.takeSnapshot()
    # result.writeToFile('/Users/makkit/monkeyscript/splash.png','png')
    # print "screen 1 taken"

    # #sending an event which simulate a click on the menu button
    # device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)

    # print "end of script"
    #('unzip /data/app/tw.wonderplanet.CrashFever-1.apk -d /sdcard/extracted/cf')
    #KEYCODE_BACK