import signal, sys, os, time
import RPi.GPIO as GPIO
from modules import *

""" GPIO Pins put from official docs - feel free to modifiy """
GPIO_PINS = [ 18, 4, 17, 27 ]
GPIO_MODE = GPIO.BCM

IDLE = 10
IDLE_MODULE = Loading
WORKING_MODULE = Random
""" Printing anything on stdout? Not necessary, just for debugging purposes. """
VERBOSE = True

class LightController:
	""" Default in-use pin count: """
	pin_count = 4
	last_activity = None

	""" Modules used to work on """
	work_module = None
	loading_module = None

	def __init__( self, pins = None ):
		if pins:
			self.pin_count = pins

		if pins > len( GPIO_PINS ):
			raise Exception, "Want to use more channels then available ones."

		# Waring purposes
		GPIO.cleanup()
		
		# Set proper mode
		GPIO.setmode( GPIO_MODE )
	
		if not VERBOSE:
			GPIO.setwarnings(False)

		# Put low on all pins and set on out mode
		for i in range( 0, self.pin_count ):
			if VERBOSE:
				print "Setting GPIO-%d as output." % GPIO_PINS[ i ]
			GPIO.setup( GPIO_PINS[ i ], GPIO.OUT )
			self.on( i )

		# Put pid into /tmp/illu_controller.pid
		try:
			pid = os.getpid()
			f = open( '/tmp/illu_controller.pid', 'w' )
			f.write( str( pid ) )
			f.close()
		except Exception, e:
			raise Exception, "Problem while creating pid. Propably process is already running or not used sudo running script."
		
		self.work_module = WORKING_MODULE( self )
		self.idle_module = IDLE_MODULE( self )
		self.last_activity = time.time()

		signal.signal( signal.SIGUSR1, self.handle )
	
		print "\n\n"

		""" IDLE implemented below :) """
		while True:
			time.sleep( 0.5 ) # Count every second of idle and loading work every second; This should be fixed value (0.5-15).
			time_delta = time.time() - self.last_activity

			if time.time() - self.last_activity >= IDLE:
				if VERBOSE:
					print "\n\nLight module is IDLE. Not receiving any beat signal (since %d seconds)." % ( time_delta )

				self.idle_module.work()

		""" Return None for instance :P """
		return None

	""" Handle signals - USR1 while playing beat """
	def handle( self, signal, frame ):
		self.last_activity = time.time()
		self.work_module.work()

	""" Function setting HIGH on pinout """
	def on( self, n ):
		if VERBOSE:
			print "Setting on channel %d." % n

		if n >= self.pin_count:
			return None

		GPIO.setup( GPIO_PINS[ n ], GPIO.OUT )
		GPIO.output( GPIO_PINS[ n ], GPIO.HIGH)

	""" Same, but turning off """
	def off( self, n ):
		if VERBOSE:
			print "Setting off channel %d." % n

		if n >= self.pin_count:
			return None

		GPIO.setup( GPIO_PINS[ n ], GPIO.OUT )
		GPIO.output( GPIO_PINS[ n ], GPIO.LOW)

if __name__ == "__main__":
	c = LightController( sys.argv[1] if len(sys.argv) > 2 else None )
