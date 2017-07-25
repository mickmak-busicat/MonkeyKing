# Monkey King Library
Monkey King Library is a simple Jython tool that make use of `monkeyrunner` in Android Developer Tools to run customized automation scripts(.mks). You can write your own mks script to automate a task on your Android environment such as doing some repetitive tasks or doing App test automations. **This library is mainly designed for rerolling first summons(or GACHA)(aka 刷首抽 in Chinese) in a modern mobile game**. It provided some useful methods to help achieve the reroll process in a more convenient way.

## How to contribute:
Basically, I will non-regularly upload some script bundles of a few most recent&famous mobile game to `bundle` folder. Feel free to get it and try. It is soooo welcome for anyone who is also interested in writing script bundle, there is a quick guide in WIKI page. Just read it and follow the instruction. :D

## Environment setup:
1. Major setup:
  - `adb` command available
  - `monkeyrunner` available

2. Other setup:
  - `aapt` build-tools available
  - Android emulator(NOX player is tested.)

## Usage:

1. **Get your Android Environment ready:**
---
Get emulator connected using adb:

https://www.bignox.com/blog/how-to-connect-android-studio-with-nox-app-player-for-android-development-and-debug/

or Get your device connected using adb:

https://developer.android.com/studio/command-line/adb.html#Enabling

2. **Run the tool:**
---
Go to Android tools directory(or add it to system path), run:

```./monkeyrunner {PATH TO MonkeyKing}/MonkeyMain.py {Config name}```

Config name is the filename of mks config without file extension. For example, a full command:

```./monkeyrunner ~/MonkeyScript/MonkeyMain.py MonsterStrikeBundle```

## Configurations:

## Available Methods:
WIKI

## Bundle structures:
WIKI

## Pending items:
- [x] Library contents
- [ ] Readme
- [ ] Wiki for contributing
- [ ] Example bundle for test

### Support:
Welcome to leave me comment or idea in this repo.
