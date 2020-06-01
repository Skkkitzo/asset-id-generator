import sys
import time

from luaparser import get_string_contents
from tkinter import *
from tkinter.filedialog import askopenfilename

luaformat = """-- This is a generated file
-- Do not modify it, unless you know exactly what you are doing

ModId = "%s"

IdMap = {
    { %s }
}"""

# Global values
primaryFile = None
secondaryFile = None

def parseLua(file: str) -> tuple:
    """Parse a lua file and read modid and list of asset Ids

    Parameters:
        file : filepath of lua script
    """

    modid = None
    assetList = None

    with open(file, "r") as f:
        content = f.read().split('\n') # all the lines of the lua file

        for index, line in enumerate(content):
            if line.startswith("ModId"): modid = get_string_contents(line)[0]
            elif line.startswith("IdMap"):
                # parse the rest of the file
                lines = [line if '{' in line and '}' in line else '' for line in content[index+1:]] # get all asset ID lines
                lines = list(filter(None, lines)) # get rid of blank values

                assetList = [get_string_contents(line) for line in lines]
                break

    return (modid, assetList)

def joinGroup(group):
    """Parse a group of asset Ids to string

    Parameters:
        group : Group of asset Ids
    """

    a, b, c = group
    return "\"%s\", \"%s\", \"%s\"" % (a, b, c)

def combineFiles(primary: str, secondary: str) -> str:
    """Combine two generated_ids.lua scripts into one

    Parameters:
        primary : the main generated_ids.lua file
        secondary : the newly generated generated_ids.lua file
    """

    # Get modid and asset Ids from primary file
    modid, mainAssetList = parseLua(primary)
    #print(parseLua(primary))
    mainAssetIdList = [x[0] for x in mainAssetList]

    # Get asset Ids from secondary file
    secondaryAssetList = parseLua(secondary)[1]

    # Add new asset Ids to list
    for group in secondaryAssetList:
        if group[0] not in mainAssetIdList:
            mainAssetList.append(group)

    # Parse all items in list to string
    mainAssetListLines = [joinGroup(x) for x in mainAssetList]

    # Form the final script
    finalScript = luaformat % (modid, ' },\n    { '.join(mainAssetListLines))
    
    return finalScript

def writeScript(primary: str, secondary: str):
    """Write the combined file of primary and secondary to primary

    Parameters:
        primary : the main generated_ids.lua file
        secondary : the newly generated generated_ids.lua file
    """

    # Calculate data that needs to be written
    data = combineFiles(primary, secondary)

    # Write data
    with open(primary, 'w') as f:
        f.write(data)

def fileDialog() -> str:
    filepath = askopenfilename()

    if filepath != None:
        return filepath

def getShortFilepath(filepath) -> str:
    drive = filepath.split('/')[0]
    filename = filepath.split('/')[-1]

    return '%s/.../%s' % (drive, filename)

def writeToLog(text):
    """Write a string to log"""
    log.configure(state='normal')
    log.insert('end', text + "\n")
    log.configure(state='disabled')

def getMillis() -> int:
    return int(round(time.time() * 1000))

def setMainFile():
    global primaryFile
    primaryFile = fileDialog()

    btn1.configure(text = getShortFilepath(primaryFile))

def setSecondaryFile():
    global secondaryFile
    secondaryFile = fileDialog()

    btn2.configure(text = getShortFilepath(secondaryFile))

def main():
    global primaryFile, secondaryFile

    start = getMillis()

    writeToLog('Reading files')
    writeScript(primaryFile, secondaryFile)
    writeToLog('Writing file')
    
    end = getMillis()
    seconds = (end - start) / 1000

    writeToLog('Completed in %s seconds' % (seconds))


# Set basic properties of window
window = Tk()
window.geometry('300x500')
window.title('Generated IDs Packer')
window.resizable(False, False)

# Configure main window grid
Grid.rowconfigure(window, 0, weight = 1)
Grid.columnconfigure(window, 0, weight = 1)

# Create frame
frame = Frame(window)
frame.grid(row = 0, column = 0, sticky = N+E+S+W)

# Create the rows
Grid.rowconfigure(frame, 0, weight = 1)
Grid.rowconfigure(frame, 1, weight = 1)
Grid.rowconfigure(frame, 2, weight = 1)
Grid.rowconfigure(frame, 3, weight = 1)
Grid.rowconfigure(frame, 4, weight = 1)

# Create the columns
Grid.columnconfigure(frame, 0, weight = 1)
Grid.columnconfigure(frame, 1, weight = 2)

# Main lua file
lbl1 = Label(frame, text='Original file')
lbl1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N+E+S+W)

btn1 = Button(frame, text = 'Select a file', command = setMainFile)
btn1.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = N+E+S+W)

# Addition lua file
lbl2 = Label(frame, text = 'Combine with file')
lbl2.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = N+E+S+W)

btn2 = Button(frame, text = 'Select a file', command = setSecondaryFile)
btn2.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = N+E+S+W)

# Options
group = LabelFrame(frame, text = 'Options', padx = 5, pady = 5)
group.grid(row = 2, column = 0, columnspan = 2, padx = 5, sticky = N+E+S+W)

btn3 = Checkbutton(group, text = 'Sort alphabetically')
btn3.pack()

# Submit button
submit = Button(frame, text = 'Calculate', command = main)
submit.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = N+E+S+W)

# Log
log = Text(frame, height = 10, state = 'disabled')
log.grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = N+E+S+W)

window.mainloop()