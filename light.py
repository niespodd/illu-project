import signal, sys, os
import RPi.GPIO as GPIO
from light_modules import *

GPIO_PINS = []
GPIO_MODE = GPIO.BCM
LOADING_MODULE = Loading
WORKING_MODULE = Sequential

class LightController:
	# Default in-use pin count:
	pin_count = 4

	def __init__( self, pins = None ):
		if pins:
			self.pin_count = pins

		# Set proper mode
		GPIO.setmode( GPIO_MODE )

		# Put low on all pins and set on out mode
		for i in range( 1, self.pin_count ):
			GPIO.setup( i, GPIO.OUT )
			self.off( i )

		# Put pid into /tmp/illu_controller.pid
		try:
			pid = os.getpid()
			f = open( '/tmp/illu_controller.pid', 'w' )
			f.write( str( pid ) )
			f.close()
		except Exception, e:
			raise Exception, "Problem while creating pid. Propably process is already running or not used sudo running script."
		
		signal.signal( signal.SIGUSR1, self.handle )
                signal.pause()

	""" Handle signals - USR1 while playing beat """
	def handle( self, signal, frame ):
		
		signal.pause()

	""" Function setting HIGH on pinout """
	def on( self, n ):
		GPIO.output(n, GPIO.HIGH)

	""" Same, but turning off """
	def off( self, n ):
		GPIO.output(n, GPIO.LOW)

if __name__ == "__main__":
	c = LightController( sys.argv[1] if len(sys.argv) > 2 else None )
