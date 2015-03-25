import os, sys, hashlib, time
from mplayer import Player
from signal import SIGUSR1

VERBOSE = True
""" BEAT_DELTA - the difference between played music position and beat position """
BEAT_DELTA = 0.3

class Play:
	player = None
	player_status = False
	hash = None
	beats = [ 1, 1.1, 1.2, 1.3, 1.9, 2, 5, 10, 10.1, 10.2, 20]
	controller_pid = None

	def __init__( self, filepath ):
		# Calculate file hash
		self.hash = hashlib.md5( open( filepath, 'r' ).read() ).hexdigest()
		if VERBOSE:
			print "Calculated %s hash is %s." % ( filepath, self.hash )

		""" Retrieve light daemon pid """
		self.controller_pid = self.get_controller()
		if not self.controller_pid:
			print "There's no certainty light controller is running."
		else:
			print "Found controller (pid=%d)" % self.controller_pid

		""" Load modules """
		self.load_player( filepath )
		self.load_beats( filepath )

		self.play()
	
	""" get_controller() - used to retreive light controller pid """			
	def get_controller( self ):
		f = open('/tmp/illu_controller.pid', 'r')
		pid = int(f.read())
		try:
			os.kill( pid, 0 )
		except:
			pid = None
		return pid

	""" send_controller() - to send beat signal via kill to controller """
	def send_controller( self ):
		try:
			os.kill( pid, SIGUSR1 )
		except:
			print "Beat found! Nothing happens, becouse propably no light controller is active."


	def load_beats( self, filepath ):
		if os.path.isfile( filepath + ".beats" ):
			""" Not implemented yet. """
			return None
		else:
			""" Should convert file into .wav and progress its beats """
			return None
		
		return None 

	def load_player( self, filepath ):
		""" Load Player and pause it """
		print filepath
		self.player = Player( filepath )
		#self.player.loadfile( filepath )
		self.player_status = True
		self.turn_player()

	def turn_player( self ):
		self.player.pause()
		self.player_status = ( True if self.player_status == False else False )

	def play( self ):
		""" Start the music... """
		self.turn_player()

		""" ...and send beat-signals in background. """
		current_beat = 0
		while True:
			current_time = self.player.time_pos
			if current_beat >= len( self.beats ):
				print "No more beats to play. Gonna make a powernap for 5s :)."
				time.sleep( 5 )
				break
			if current_time + BEAT_DELTA > self.beats[ current_beat ]:
				self.send_controller()
				current_beat = current_beat + 1 


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: %s <filename>" % sys.argv[0]
		sys.exit(1)

	play = Play( sys.argv[1] )
