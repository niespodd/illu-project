import random

class Random:
	pin_count = None
	last_pin = None
	controller = None

	def __init__( self, controller ):
		self.pin_count = controller.pin_count
		self.controller = controller

	def work( self ):
		""" Put random channels on/off, clearly random """
		for i in range(0, self.pin_count):
			if random.randint(0, 1) == 0:
				self.controller.on( i )
			else:
				self.controller.off( i )


