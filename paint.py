import PySimpleGUI as sg
from tkinter import Tk, font
from PIL import ImageGrab
import os


#/** Get Font Families from tkinter **/
root = Tk()
font_tuple = font.families()
root.destroy()
#/** Get Font Families from tkinter **/

# History variable
history_changes = []
history_deletes = []

# Color picker list loop up
positionColor = []

# isFileSaved variable
isFileSaved = False
fileName = ''

# isLoading variable
isLoading = False

# load mode
mode = 'draw'

# Mode
loadMode = 'draw'

def addDataToHistory(ID, xy, size, color, element):
    history_changes.append([ID, xy, size, color, element])   
    
def clearBoard():
    window['-graph-'].draw_rectangle((0, 0), (600, 400), fill_color='white')
    window['-graph-'].update()

def save_element_as_file(element, filename):
    widget = element.Widget
    box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height())
    grab = ImageGrab.grab(bbox=box)
    grab.save(filename)

def fixStrTuple(pos):
    # Str tuple to tuple (pos)
    pos = pos.replace("(", "")
    pos = pos.replace(")", "")
    pos = pos.replace(",", " ")
    posList = pos.split()
    posList = list(map(float, posList))
    pos = tuple(posList)

    return pos

def setupLoadFile():
    file_types = [("TEXT (*.TXT)", "*.TXT"), ("All files (*.*)", "*.*")]
    filename = sg.popup_get_file('Will not see this message', no_window=True, file_types=file_types)
    if filename:
        clearBoard()
        
        # Setup progress bar
        window['-load_imageProgress-'].update(visible=True)
        window['-load_imageText-'].update(visible=True)

        # Read ALL data and load it on the graph
        loaded_data=[]
        isLoading=True

        with open(filename, 'r') as fp:
            for data_line in fp:
                # Convert data_line (str) to list
                fixed_data = data_line[:-1]

                # Append to temp list
                loaded_data.append(fixed_data)

        # Change max in progress bar
        window['-load_imageProgress-'].update(max = len(loaded_data))
        watchFile(loaded_data)
        # Update window
        window['-graph-'].update()
        # Update isLoading
        isLoading=False

        window['-load_imageProgress-'].update(visible=False)
        window['-load_imageText-'].update(visible=False)
    return filename   
    
def watchFile(loaded_data):
    for i in range(len(loaded_data)):
        pos=loaded_data[0].split('¤')[0]
        size=int(loaded_data[0].split('¤')[1])
        c=loaded_data[0].split('¤')[2]
        typ=loaded_data[0].split('¤')[3]

        # Str tuple to tuple (pos)
        pos = fixStrTuple(pos)

        # Update progress bar
        window['-load_imageProgress-'].update_bar(i, len(loaded_data)*3)
        if(typ == 'circle'):
            window['-graph-'].draw_circle(pos, size, fill_color=c, line_color=c, line_width=1)
        elif(typ.split(':')[0] == 'text'):
            font_temp = (typ.split(':')[2], size)
            window['-graph-'].draw_text(typ.split(':')[1], pos, color = c, font = font_temp)


        del loaded_data[0]

def openFile():
    file_types = [("PNG (*.PNG)", "*.PNG"), ("All files (*.*)", "*.*")]
    filename = sg.popup_get_file('Will not see this message', no_window=True, file_types=file_types)
    window['-graph-'].draw_image(filename=filename, location=(0, 400))
    window['-graph-'].update()
    return filename

def find_files(filename, search_path):
   result = []

# Wlaking top-down from the root
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

menu_def=['&File', ['&New File', '&Open...', '&Watch Drawing','---', '&Export','&Close']],['&Save',['&Save File'  ]], ['&Edit', ['&Undo', '&Redo']]

layout = [
    [sg.Menu(menu_def, background_color='white',text_color='black', disabled_text_color='black', font='Arial', pad=(10,10))],
    [sg.Text('File is not saved!*',key='-saved-')],
    [
        sg.Button('Layout(s)',key='-layout-', expand_x=True, expand_y=True),
        sg.Graph(
            canvas_size=(600, 400),
            graph_bottom_left=(0, 0),
            graph_top_right=(600, 400),
            key="-graph-",
            enable_events=True,
            float_values=True,
            drag_submits=True
        ),
        sg.Column([
        [sg.Button('       ',key='-color_blue-', button_color='blue', mouseover_colors='blue')],
        [sg.Button('       ',key='-color_black-', button_color='black', mouseover_colors='black')],
        [sg.Button('       ',key='-color_white-', button_color='white', mouseover_colors='white')],
        [sg.Button('       ',key='-color_yellow-', button_color='yellow', mouseover_colors='yellow')],
        [sg.Button('       ',key='-color_red-', button_color='red', mouseover_colors='red')],
        [sg.Button('       ',key='-color_green-', button_color='green', mouseover_colors='green')],
        [sg.Button('       ',key='-color_pink-', button_color='pink', mouseover_colors='pink')],
        [sg.Button('       ',key='-color_purple-', button_color='purple', mouseover_colors='purple')],
        [sg.Button('       ',key='-color_gray-', button_color='gray', mouseover_colors='gray')],
        [sg.Button('       ',key='-color_orange-', button_color='orange', mouseover_colors='orange')],
        [sg.Button('       ',key='-color_brown-', button_color='brown', mouseover_colors='brown')],
        [sg.Button('       ',key='-color_pink-', button_color='pink', mouseover_colors='pink')]
        ], key='-colorCol-')
    ], 
    [sg.Button('Draw', key='-draw-', button_color='black'), 
    sg.Slider(range=(1, 20), default_value=2, orientation='h', key='-draw_slider-', visible=True,disable_number_display=True), 

    sg.Button('Erase', key='-erase-', button_color='gray'), 
    sg.Slider(range=(1, 20), default_value=12, orientation='h', key='-erase_slider-', visible=False,disable_number_display=True),

    sg.Button('Color Picker', key='-cpicker-', button_color='gray'), 

    sg.Button('Text', key='-text-', button_color='gray'), 
    sg.Slider(range=(11, 32), resolution=3, default_value=11, orientation='h', key='-text_slider-', visible=False,disable_number_display=False),
    sg.Column([    
        [
    sg.Button('', key='-text_color_white-', button_color='white', mouseover_colors='white', size=(1, 1), visible=False),
    sg.Button('', key='-text_color_red-', button_color='red', mouseover_colors='red', size=(1, 1), visible=False),
    sg.Button('', key='-text_color_black-', button_color='black', mouseover_colors='black', size=(1, 1), visible=False)
        ]
    ], key='-textcolorCol-'),
    sg.Combo(font_tuple, default_value=sg.DEFAULT_FONT, size=(10, 5), auto_size_text=True, readonly=True, key='-font_combo-', visible=False)
    ],
    [sg.Text('Loading buffer data:', key='-load_imageText-', visible=False)],
    [sg.ProgressBar(max_value=100, orientation='h', size=(20, 20), key='-load_imageProgress-', visible=False)]
]

# Create the Window
window = sg.Window('Paint', layout, element_justification='center', size=(800, 600), return_keyboard_events=True).Finalize()

# Create paint field
window['-graph-'].draw_rectangle((0, 0), (600, 400), fill_color='white')

def setDrawBtnActive():
    window['-draw-'].update(button_color=c)
    window['-erase-'].update(button_color='gray')
    window['-text-'].update(button_color='gray')
    window['-cpicker-'].update(button_color='gray')
    window['-erase_slider-'].update(visible=False)
    window['-draw_slider-'].update(visible=True)
    window['-text_slider-'].update(visible=False)
    window['-text_color_white-'].update(visible=False)
    window['-text_color_red-'].update(visible=False)
    window['-text_color_black-'].update(visible=False)
    window['-font_combo-'].update(visible=False)
def setEraseBtnActive():
    window['-draw-'].update(button_color='gray')
    window['-erase-'].update(button_color=('#FFFFFF', '#283b5b'))
    window['-text-'].update(button_color='gray')
    window['-cpicker-'].update(button_color='gray')
    window['-erase_slider-'].update(visible=True)
    window['-draw_slider-'].update(visible=False)
    window['-text_slider-'].update(visible=False)
    window['-text_color_white-'].update(visible=False)
    window['-text_color_red-'].update(visible=False)
    window['-text_color_black-'].update(visible=False)
    window['-font_combo-'].update(visible=False)
def setTextBtnActive():
    window['-draw-'].update(button_color='gray')
    window['-erase-'].update(button_color='gray')
    window['-text-'].update(button_color=('#FFFFFF', '#283b5b'))
    window['-cpicker-'].update(button_color='gray')
    window['-erase_slider-'].update(visible=False)
    window['-draw_slider-'].update(visible=False)
    window['-text_slider-'].update(visible=True)
    window['-text_color_white-'].update(visible=True)
    window['-text_color_red-'].update(visible=True)
    window['-text_color_black-'].update(visible=True)
    window['-font_combo-'].update(visible=True)
def setColorPickerBtnActive():
    window['-draw-'].update(button_color='gray')
    window['-erase-'].update(button_color='gray')
    window['-text-'].update(button_color='gray')
    window['-cpicker-'].update(button_color=('#FFFFFF', '#283b5b'))
    window['-erase_slider-'].update(visible=False)
    window['-draw_slider-'].update(visible=False)
    window['-text_slider-'].update(visible=False)
    window['-text_color_white-'].update(visible=False)
    window['-text_color_red-'].update(visible=False)
    window['-text_color_black-'].update(visible=False)
    window['-font_combo-'].update(visible=False)
def resetAll():
    window['-draw-'].update(button_color='gray')
    window['-erase-'].update(button_color='gray')
    window['-text-'].update(button_color='gray')
    window['-cpicker-'].update(button_color='gray')
    window['-erase_slider-'].update(visible=False)
    window['-draw_slider-'].update(visible=False)
    window['-text_slider-'].update(visible=False)
    window['-text_color_white-'].update(visible=False)
    window['-text_color_red-'].update(visible=False)
    window['-text_color_black-'].update(visible=False)
    window['-font_combo-'].update(visible=False)

c = 'black'
font_size = 11
font_name = sg.DEFAULT_FONT
font = (font_name, font_size)
textColor = 'black'

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(event)
    if not isLoading:
        # Check graph event mouse pressed
        if event == '-graph-':
            history_deletes = []

            # Mode is draw? Do draw stuff then
            if mode == 'draw':
                addDataToHistory(window[event].draw_circle(values.get(event), (int(values['-draw_slider-'])), fill_color=c, line_color=c, line_width=1), values.get(event), int(values['-draw_slider-']), c, 'circle')
                window[event].update()
                positionColor.append([values.get(event), c])
                isFileSaved = False # New updates to file!
                window['-saved-'].update(value ='File is not saved!* ' + fileName)

            # Mode is erase? Do erase stuff then
            elif mode == 'erase':
                addDataToHistory(window[event].draw_circle(values.get(event), (int(values['-erase_slider-'])), fill_color='white', line_color='white', line_width=1), values.get(event), int(values['-draw_slider-']), 'white', 'circle')
                window[event].update()
                isFileSaved = False # New updates to file!
                window['-saved-'].update(value ='File is not saved!* ' + fileName)

            # Mode is text? Do text stuff then
            elif mode == 'text':
                # Get text/font size
                font_size = (int(values['-text_slider-']))
                font_name = (str(values['-font_combo-']))
                font = (font_name, font_size)
                # Append to undo history with keyword "text_element" and text elemnt to graph at mouse position
                addDataToHistory(window['-graph-'].draw_text(textValue, values.get(event), color = textColor, font=font), values.get(event), font_size, textColor, f'text:{textValue}:{font_name}')

                # Reset all elements
                resetAll()
                # Reset mode
                mode=0

            # Mode is color picker? Do color picker stuff then
            elif mode == 'cpicker':
                # Get the position of the figure related to positionColor values
                for i in range(len(positionColor)):
                    if values.get(event) == positionColor[i][0]:
                        c = positionColor[i][-1]
                        window['-draw-'].update(button_color=c)


        # Check if draw button is pressed 
        if event == '-draw-':
            mode = 'draw'
            setDrawBtnActive()

        # Check if erase button is pressed
        if event == '-erase-':
            mode = 'erase'
            setEraseBtnActive()

        # Check if text button is pressed
        if event == '-text-':
            mode = 'text'

            # Ask user for text value
            textValue = sg.popup_get_text(f'What do u want to write? ')
            setTextBtnActive()

        # Check if color picker is pressed
        if event == '-cpicker-':
            mode = 'cpicker'
            setColorPickerBtnActive()
            
        # Check if a color has been selected in draw/erase
        if event.startswith('-color_'):
            # Split color string
            c = event.split('_', 1)[1].split('-', 1)[0]
            if mode == 'draw':
                setDrawBtnActive()
        # Check if a color has been selected in text
        if event.startswith('-text_color_'):
            # Split color string
            textColor = event.split('_', 1)[1].split('-', 1)[0].split('_', 1)[1]

        # Undo pressed or CTRL+Z (z:90)
        if event == 'Undo' or event == 'z:90':
            for i in range(30):
                # Is there anything in the buffer
                if len(history_changes) > 0:

                    # Append undo data to redo data "history_deletes"
                    history_deletes.append(history_changes[-1])
                    
                    # Delete figure from window
                    window['-graph-'].delete_figure(history_changes[-1][0])

                    # Now delete the data from undo "history_changes"
                    history_changes = history_changes[:-1]
            window['-graph-'].update()
            isFileSaved = False # New updates to file!
            window['-saved-'].update(value ='File is not saved!* ' + fileName)
        
        # Redo pressed or CTRL+Y (y:89)
        if event == 'Redo' or event == 'y:89':
            for i in range(30):
                # Is there anything in the buffer
                if len(history_deletes) > 0:

                    # Recreate a duplicate version of the drawn history & append data to undo history
                    addDataToHistory(window['-graph-'].draw_circle(history_deletes[-1][1], (history_deletes[-1][2]), fill_color=history_deletes[-1][3], line_color=history_deletes[-1][3], line_width=1), history_deletes[-1][1], history_deletes[-1][2], history_deletes[-1][3], history_deletes[-1][4])

                    # Now delete the data from redo "history_deletes"
                    history_deletes = history_deletes[:-1]
        
        # New file pressed
        if event == 'New File':
            # Are u sure u want to create a new file?
            if not isFileSaved:
                # Are u sure you want to exit?
                result = sg.PopupYesNo("Your current file is not saved! Do you want to continue?")
                if result == 'Yes':
                    clearBoard()
                    fileName = ''
                    window['-saved-'].update(value ='File is not saved!* ' + fileName)
                    history_changes = []
            else:
                clearBoard()
                fileName = ''
                window['-saved-'].update(value ='File is not saved!* ' + fileName)
                history_changes = []

        # Watch Drawing pressed
        if event == 'Watch Drawing':
            loadMode = "watch"
            # Are u sure u want to create a new file?
            if not isFileSaved:
                # Are u sure you want to exit?
                result = sg.PopupYesNo("Your current file is not saved! Do you want to continue?")
                if result == 'Yes':
                    history_changes = []
                    filepath=setupLoadFile()
                    fileName = filepath.split('/')[-1]
                    window['-saved-'].update(value ='Your file is saved! ' + fileName)
                    sg.PopupOK(f'{filepath} buffer data has been loaded successfully')
            else:
                history_changes = []
                filepath=setupLoadFile()
                fileName = filepath.split('/')[-1]
                window['-saved-'].update(value ='Your file is saved! ' + fileName)
                sg.PopupOK(f'{filepath} buffer data has been loaded successfully')

        if event == 'Open...':
            loadMode = "open"
            # Are u sure u want to create a new file?
            if not isFileSaved:
                # Are u sure you want to exit?
                result = sg.PopupYesNo("Your current file is not saved! Do you want to continue?")
                if result == 'Yes':
                    history_changes = []
                    filepath=openFile()
                    fileName = filepath.split('/')[-1]
                    window['-saved-'].update(value ='Your file is saved! ' + fileName)
                    sg.PopupOK(f'{filepath} has been loaded successfully')
            else:
                history_changes = []
                filepath=openFile()
                fileName = filepath.split('/')[-1]
                window['-saved-'].update(value ='Your file is saved! ' + fileName)
                sg.PopupOK(f'{filepath} has been loaded successfully')


        if event == 'Export':
            filename = sg.popup_get_text('File Name Here: ')
            
            if filename != None:
                save_element_as_file(window['-graph-'], f'{filename}.png')
                isFileSaved = True
                window['-saved-'].update(value ='Your file is saved! ' + fileName)
                with open(f'{filename}_buffer.txt', 'w') as fp:
                    for data in history_changes:
                        fp.write(f'{data[1]}¤{data[2]}¤{data[3]}¤{data[4]}\n')
                fp.close()
                sg.PopupOK(f'{filename}.png has been exported! To "Watch Drawing" use {filename}_buffer.txt or to "Open..." user {filename}.png')

        # CTRL+S pressed, only update text
        if event == 'Save File' or event == 's:83':
            isFileSaved = True
            window['-saved-'].update(value ='Your file is saved! ' + fileName)

        if event == sg.WIN_CLOSED: # if user closes window
            if not isFileSaved:
            # Are u sure you want to exit?
                result = sg.PopupYesNo("Are you sure you want to exit? Your current file is not saved!")
                if result == 'Yes':
                    break


window.close()