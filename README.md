# Illu-Project - lights controlled with beats
Illu is a project written in Python containing proper modules to control Raspberry PI GPIO channels connected to high-voltage lights (regular 220/230 volts).
  Project contains both schemas and software needed to run your own Illu.

## Requirements
_Raspberry PI_ with Raspberrian or similar OS installed and some electronic stuff. Major software requirements are GGC compiler, MPlayer, Aubio library, Python 2.7+ and other related libraries (will update this later) installed.
  Future releases will propably require some database software to store beat informations, but at this stage you can ommit it.

### Python dependencies
1. python-automodinit
2. python-rpi (python interface for GPIO)
3. python-aubio (provided with Aubio package)
4. python-mplayer (MPlayer wrapper for Python)

## How does it work?
Project is made of two modules. The first is __Light Controller__ which is listening to something called beat-signal from the second module __Player__. The _beat signal_ is just a standard POSIX signal USR1 which tells light controller to flash the lights in proper user-defined way.

### Light Controller
It's located in ```/light/``` folder. There is a ```modules``` folder inside. These modules tells controller how it should react to the beat - e.g. flash all lights on and then off, flash one of them, flash them sequentialy etc. - as you wish. Take a look at default example scripts.

__Usage__: ``` sudo python light.py ```

### Player
Responsible for extracting beats from given audio file, playing it and sending _beat-signal_ to Light Controller.

__Usage__: ``` sudo python play.py <filename> ```

## Questions? Support?
Any questions may be send at ```niespodd@ee.pw.edu.pl```.
