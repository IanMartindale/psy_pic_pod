import csv
from psychopy import visual, core, event, sound, monitors
import time 
from psychopy.hardware import keyboard
#import serial
#port = serial.Serial("COM3", baudrate=115200)

#load audio
#audio_file_path = 'podcast_clip_1.wav'

csv_files = ["clip_1_input.csv", "clip_2_input.csv", "clip_3_input.csv"]
wav_files = ["podcast_clip_1.wav", "podcast_clip_2.wav", "podcast_clip_3.wav"]

#sound_stim = sound.Sound(audio_file_path, stereo=True, hamming=True)
#sound_stim = sound.Sound(sound.AudioClip.load (audio_file_path))

# Load data from CSV file
#data = []
#with open('clip_1_input.csv', 'r', encoding="utf-8-sig") as csvfile:
#    reader = csv.DictReader(csvfile)
#    for row in reader:
#        data.append(row)

# Initialize PsychoPy window
win = visual.Window(size=(1920, 1080), fullscr=True, color='black', waitBlanking=False,units='height')

# Create text stimulus for the start screen
start_text = visual.TextStim(
    win=win, name='start_text',
    text='Press Enter to Start',
    font='Open Sans',
    pos=(0, 0), height=0.05,
    color='white'
)
# Initialize keyboard
#defaultKeyboard = event.BuilderKeyResponse()

# Display the start screen
start_text.draw()
win.flip()

event.waitKeys(keyList=['return', 'escape'])

# Create text stimulus
text_stim = visual.TextStim(win=win, name='test_word_hmm',
        text='',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
        
fixation_cross = visual.TextStim(win=win, name='fixation_cross',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
        
#rectangle
PS_word = visual.Rect(
    win=win, name='PS_word',
    width=(0.05, 0.05)[0], height=(0.05, 0.05)[1],
    ori=0.0, pos=(+0.86, -0.47),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-6.0, interpolate=True)

# Wait for Enter key press to start the experiment
while True:
    keys = event.getKeys(keyList=['return', 'escape'])
    if 'return' in keys:
        fixation_cross.draw()
        win.flip()
        break
    if 'escape' in keys:
        core.quit()

for i in range(0, len(csv_files)):
    # load sound stim
    sound_stim = sound.Sound(sound.AudioClip.load(wav_files[i]))

    data = []
    with open(csv_files[i], 'r', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    
    sound_stim.play()

    #time sleep likely problematic for timing
    time.sleep(float(data[0]['Start']))

    # Main experiment loop
    for index in range(len(data)):
        trial = data[index]
        stim_word = trial['Word']
        start_time = float(trial['Start'])
        end_time = float(trial['End'])
        event_code = int(trial['Code'])
        # Display word from start_time to end_time
        text_stim.text = stim_word
        text_stim.draw()
        PS_word.draw()
        #port.write(str.encode(chr(event_code)))
        #port.flush
        
        win.flip() 
        
        fixation_cross.draw()
        time.sleep(end_time - start_time)
        
        win.flip()
        
        if index < len(data)-1:  
            sleep_time = float(data[index+1]['Start']) - end_time
            time.sleep(sleep_time)
        if 'escape' in event.getKeys():
            core.quit()
            
        win.flip()


# Close PsychoPy window at the end of the experiment
win.close()
