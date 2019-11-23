# Open source visualizer for ArtNet

First a short disclaimer: This project is still **EARLY ACCESS**!

### Final target of this project
In the end this project should be able to function as a replacement for expensive 3D-DMX-Visualizer.
In the current state it's far away of being able to do so.

### Install
1. Download Blender 2.8x from the [official site](https://builder.blender.org/download/).
**Note: **this version is still experimental, but the real-time-render-engine is only available in this version.
2. clone this repository to your computer **OR** just download the `.blend` File.
3. Make sure you are opening the file with the blender version downloaded from above.

### Use this project
* First call run the script named create_lamps.py.
* At this stage the program only allows only **one** type of fixtures. You have to replace the marked line with the correct line(s) shown below.

Fixture type | Code
------------ | -------------
Dimmer | `obj.data.energy = watt * 10 * (values[i] / 255)`
RGB LED | `obj.data.energy = watt * 10` <br> `obj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))`
RGB-Dimmer LED | `obj.data.energy = watt * 10 * (values[i+3] / 255)` <br> `obj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))`

* The script will use the first spotlight parented to the object with the name of a DMX-channel, with the number displayed in three letters. So DMX-address `1` will be mapped to the object with the name `001`.

* Then switch to the Modelling Tab, switch to "Rendered"-View and click `Run Script` in the bottom right corner.

* Then the script should pick up all ArtNet traffic on the current network and will render it to the display.

Copyright (C) 2018 Tobias Teichmann <tobias.teichmann@gmx.at>
