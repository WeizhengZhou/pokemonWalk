import applescript


cmd = """

delay 0.01
activate application "Xcode"
tell application "System Events"
	tell process "Xcode"
		click menu item "pokemonData" of menu 1 of menu item "Simulate Location" of menu 1 of menu bar item "Debug" of menu bar 1
	end tell
end tell
tell application "Xcode"
	set miniaturized of window 1 to true
end tell
activate application "Google Chrome"

"""

def RunXcode():
	applescript.AppleScript(cmd).run()


if __name__ == '__main__':
	RunXcode()




