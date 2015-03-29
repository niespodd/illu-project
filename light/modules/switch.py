import random

class Switch:
	pin_count = None
	phrase = 0
	controller = None

	def __init__( self, controller ):
		self.pin_count = controller.pin_count
		self.controller = controller

	def work( self ):
		
		if self.phrase == 0:
			self.phrase = 1
			for i in range(0, self.pin_count):
				if i % 2 == 0:
					self.controller.on ( i )
				else:
					self.controller.off( i )

		else:
			self.phrase = 0 
			for i in range(0, self.pin_count):
				if i % 2 == 1:
					self.controller.on( i )
				else:
					self.controller.off( i )

