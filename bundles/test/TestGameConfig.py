ENV_CONFIG = {
    'GAME_PACKAGE': 'tw.wonderplanet.CrashFever',
    'RUNNABLE_ACTITVITY': 'jp.wonderplanet.Yggdrasil.BULL',
    'GAME_PROJECT_PATH': '/Users/makkit/monkeyscript/test/',
    'APK_LOCATION': '/Users/makkit/monkeyscript/apk/cf_new.apk',
    'GAME_USER_FILES': [
        '/data/data/tw.wonderplanet.CrashFever/shared_prefs/SmartBeat.xml',
        '/data/data/tw.wonderplanet.CrashFever/shared_prefs/initPrefs.xml',
        '/data/data/tw.wonderplanet.CrashFever/shared_prefs/appsflyer-data.xml',
        '/data/data/tw.wonderplanet.CrashFever/shared_prefs/HSJsonData.xml',
    ],
    'COORDINATES': [
        {
            'id': 'close-news-button',
            'position': (360, 1204)
        },
        {
            'id': 'close-newbie-button',
            'position': (352, 1016)
        },
        {
            'id': 'close-crash-button',
            'position': (352, 716)
        },
        {
            'id': 'close-app-drag-start',
            'position': (472, 1153)
        },
        {
            'id': 'close-app-drag-end',
            'position': (57, 1153)
        },
    ],
    'SCREENS': [
        {
            'id': 'title-screen',
            'file': 'cap/title-text.png',
            'rect': (28, 547, 670, 103)
        },
        {
            'id': 'news-popup',
            'file': 'cap/news-popup.png',
            'rect': (282, 1154, 144, 107)
        },
        {
            'id': 'newbie-popup',
            'file': 'cap/newbie-popup.png',
            'rect': (108, 217, 488, 126)
        },
        {
            'id': 'switch-crash?',
            'file': 'cap/crash-dialog.png',
            'rect': (147, 575, 431, 171)
        },
    ],
    'SCRIPTS': [
        {
            'action': 'bootup'
        },
        {
            'action': 'sleep',
            'duration': 5
        },
        {
            'action': 'wait-screen',
            'screenId': 'title-screen'
        },
        {
            'action': 'backup-game'
        },
        {
            'action': 'shutdown'
        }
        # {
        #     'action': 'tap',
        #     'position': (400, 400)
        # },
        # {
        #     'action': 'wait-screen',
        #     'screenId': 'news-popup'
        # },
        # {
        #     'action': 'tap',
        #     'position': 'close-news-button'
        # },
        # {
        #     'action': 'wait-screen',
        #     'screenId': 'newbie-popup'
        # },
        # {
        #     'action': 'tap',
        #     'position': 'close-newbie-button'
        # },
        # {
        #     'action': 'sleep',
        #     'duration': 2
        # },
        # {
        #     'action': 'save-snapshot'
        # },
        # {
        #     'action': 'press',
        #     'keyCode': 'KEYCODE_APP_SWITCH'
        # },
        # {
        #     'action': 'sleep',
        #     'duration': 1
        # },
        # {
        #     'action': 'branch-screen',
        #     'screenId': 'switch-crash?'
        # },
        # {
        #     'action': 'jump-false',
        #     'target': 'drag-to-close-app'
        # },
        # {
        #     'action': 'tap',
        #     'position': 'close-crash-button'
        # },
        # {
        #     'action': 'checkpoint',
        #     'id': 'drag-to-close-app'
        # },
        # {
        #     'action': 'drag',
        #     'from': 'close-app-drag-start',
        #     'to': 'close-app-drag-end',
        #     'duration': 1
        # }
    ]
}
