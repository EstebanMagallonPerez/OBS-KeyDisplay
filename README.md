# OBS-KeyDisplay
This is a browser based keypress tracer. It is fully customizable and allows for custom CSS to be applied on a per key basis with css through a json or with standard class addressing

## Selecting Keyboard
To select your keyboard just navigate to http://localhost:8888/?keyboard=keyboardName
I have 2 keyboards packaged 
- gamingKeyboard.json
- keyboard.json

which can be accessed by going to

- http://localhost:8888/?keyboard=gamingKeyboard
- http://localhost:8888/?keyboard=keyboard

## Generate Keybaord
This tool is packaged with its own keyboard generator. Navagate to http://localhost:8888/generateKeyboard.html to generate your own layout.

1. Click Add Row
2. Press the keys in that row
3. Repeat until you have the number of rows and keys you want
4. Click export json
5. Place json file in /keyboards/myKeyboard.json
6. Restart the exe/python script
7. Navagate to http://localhost:8888/?keyboard=myKeyboard

## Custom Style
There is a custom.css file included in the folder with an example of some custom css, but really just add whatever you want here.
The important classes to target are:
- .key
  - this is what you will see when nothing is happening, and this can be targetted in the json to apply inline css
- .key.active
  - this is what you will see when you press a button
- .keyOverlay
  - You will also see this when you press a button, but this can be targeted by using the json to apply inline css

## Custom Script
There is a custom.js file which is included after all the other setup is done, so if you want to target keys using javascript to apply some styles or do some cool stuff just add it here 
