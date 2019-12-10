#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a trial loop Step 2
Use this template to turn Step 1 into a loop
@author: katherineduncan
"""
#%% Required set up 
# this imports everything you might need and opens a full screen window
# when you are developing your script you might want to make a smaller window 
# so that you can still see your console 
import numpy as np
import pandas as pd
import os, sys
from psychopy import visual, core, event, gui, logging

# Escape method
event.globalKeys.add(key='q', func=core.quit)

# Demographic info
expInfo = {"SubjectNumber":'',"Age":'',"Gender":''}
subgui = gui.DlgFromDict(expInfo)

# Save the data
subNum = expInfo["SubjectNumber"]
age = expInfo["Age"]
gend = expInfo["Gender"]


# Open a white full screen window
win = visual.Window(fullscr=True, allowGUI=False, color='white', unit='height') 


# Setting up instructions
Instructions = visual.TextStim(win=win, name='Instructions', 
    text="""Welcome to the experiment. 
    
    In this experiment, you will be reading several stories that happens at school setting. 
    
    After reading each story, you will be evaluating the behaviour described in the story. 
    
    Your task is to move the triangle to the number on the scale. 
    
    Remember that there is no right or wrong answer. 
    
    When you are ready, press any key to start.""",
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0)

Instructions.draw()

win.flip()

keys = event.waitKeys()

core.wait(1)

# Initializing rating scale
myScale = visual.RatingScale(win=win, name='Rating', marker='triangle', size=1.0, pos=[0.0, -0.4], low=1, high=5, labels=['not okay at all', ' a little not okay', ' neutral', ' a little okay', ' very okay'], scale='How okay or not okay is this behaviour described?')

# Setting up feedback

aboveMidpoint = visual.TextStim(win=win,
    text='You made a positive evaluation',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='green', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

belowMidpoint = visual.TextStim(win=win,
    text='You made a negative evaluation',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='yellow', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
                                
atMidpoint = visual.TextStim(win=win,
    text='You made a neutral evaluation',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='blue', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
                             

#%% your loop here
# Stimulus list
scenario1 = visual.TextStim(win, text='Here is Tommy. This morning Tommy brought a cupcake and he was going to eat this cupcake at snack time. Tommy put it on the table. Then, Tommy went out to play. Next, Dave came \nin and found that there was this cupcake on the table. Dave was hungry. Dave knew that \nthis cupcake is Tommy’s, but he took away the cupcake and ate it without asking Tommy.')
scenario2 = visual.TextStim(win, text='Now let’s suppose that it was not the first time for Dave to take away and eat Tommy’s food. Dave kept doing this over and over. In this case, Tommy thought Dave should be treated in the same way. He thought next day he would take away Dave’s muffin from his lunch box as return.')
scenario3 = visual.TextStim(win, text='Here is another story, and this is about Mike and Danny. This morning Mike brought a cupcake and he was going to eat this cupcake at snack time. He usually leaves his cupcake in the lunchbox but this time he just put this cupcake on the table. Then, Mike went out to play. Next, Danny came in and found that there was the cupcake on the table. Danny thought this is the surprise cupcake given by the teacher because the teacher sometimes gives surprise cupcake to the class. Danny thought it is his turn to take the surprise cupcake. Therefore, Danny took away the cupcake and ate it.')

scenarios = [scenario1, scenario2, scenario3]
scenarios = pd.Dataframe(scenarios)

# Trial info output
outputFileName = 'data/sub1_output.csv'
out = pd.DataFrame(columns=['trial','response'])
out.to_csv(outputFileName,index=False)

# Trial loop
for scenario in scenarios:
    myStimulus = visual.TextStim(win=win,
    text=scenario,
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0)
    
    myStimulus.draw()
    win.flip()
    
    myScale.draw()
    
    # Record response and RT
    trialRating = myScale.getRating()
    
    # Display appropriate feedback
    if trialRating < 3:
            belowMidpoint.draw()
    elif trialRating > 3:
            aboveMidpoint.draw()
    else:
            atMidpoint.draw()
            
    win.flip()
        
    core.wait(1)
       
    # Store trial info
    out.loc[scenario,'trial'] = scenario
    out.loc[scenario,'response'] = trialRating
    
    # Append trial info to file, to_csv must be in append mode
    out.loc[[scenario]].to_csv(outputFileName,mode='a',header=False,index=False)

# End of the experiment
close = visual.TextStim(win, color = 'black', height=.05, 
        text="""You have finished this experiment, thank you again for your time. 
        
        Please press any key to quit.""")

event.clearEvents()
close.draw()
win.flip()

# closes properly

core.wait(2)
win.close()
