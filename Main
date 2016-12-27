from WindGuru import WindGuru
import firebase as fb
from FirebaseDetails import FirebaseDetails
from datetime import datetime

class Main:

	def __init__(self):
		print "Executing ..."
		firebaseDetails = FirebaseDetails()
		self.firebase = fb.FirebaseApplication(firebaseDetails.getURL(), firebaseDetails.getAuth())
		self.URL = "http://www.weatherlink.com/user/constantwind/"
		# self.test()
		self.startLoop()

	def test(self):
		print self.firebase.get('/')
		# self.firebase.put("/","testing","hi")

	def startLoop(self):
		counter = 20
		while counter >= 0:
			counter -= 1
			windGuru = WindGuru(self.URL)
			windData = windGuru.getWindData()

			currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			self.firebase.put("/",currentTime,windData)
		

Main()