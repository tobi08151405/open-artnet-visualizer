# Open source visualizer for ArtNet

First a short disclaimer: This project is still **EARLY ACCESS**!

### Final target of this project
In the end this project should be able to function as a replacement for expensive 3D-DMX-Visualizer.
In the current state it's far away of being able to do so.

### Install
1. Download Blender 2.8x from the [official site](https://builder.blender.org/download/).
2. clone this repository to your computer **OR** just download the `.blend` File.
3. Make sure you are opening the file with the blender version downloaded from above.

### Use this project
* Switch to the Scene called "Scripting"
* Run the script "create_lamps.py" (see table below for more info)
* Change options in "artnet_server.py" (if needed, see below for more info)
* Run the script "artnet_server.py"
* Switch back to Scene "Modeling"
* Switch Viewport shading to "Rendered"
* Enjoy
* Exit the script with `ESC` or `RMB`

<br>

Option | value | Notes
--- | --- | ---
Starting DMX Address | Starting Address of this lamp | Overlapping Address Spaces are possible, but not two lamps at the same starting position
Fixturetype | choice from below
- | `dimmer` | 1 Channel Dimmer
- | `rgb` | 3 Channels (Red, Green, Blue)
- | `rgbw` | 4 Channels (Red, Green, Blue, White)
- | `rgb_dimmer` | 4 Channels (Red, Green, Blue, Master)
- | `dimmer_rgb` | 4 Channels (Master, Red, Green, Blue)
- | `uv` | 1 Channel with violet colour preset
Watts | maximum output energy of the lamp | Tool is calibrated for values >= 100

<br>

Option | Explanation | Default Value
--- | --- | ---
address | the address the UDP Server binds to `""` will bind to all addresses | `""` (listen on all addresses)
port | the port the UDP Server binds to | `6454` (standard ArtNet port)
net | Artnet universe to listen to (currently only one Universe is supported) | `0`
update_interval | timeout for the UDP Server in seconds | `0.01`

<br>

### Background Info

* The script will create a csv-file in the same folder as the blend-file and store the fixture mapping in it. It will use the first spotlight parented to the object with the name of a DMX-channel, with the number displayed in three digits. So DMX-address `1` will be mapped to the object with the name `001`.


Copyright (C) 2020 Tobias Teichmann <tobias@teichmann.top>
