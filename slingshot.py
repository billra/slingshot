#! python3

name='Gravitational Slingshot Simulator'
version='v0.2'
author='Bill Ola Rasmussen'

from math import sin, cos, radians

class Position:
	def __init__(self,x,y):
		self.x=x
		self.y=y

class Vector:
	def __init__(self,direction,magnitude):
		'direction in radians'
		self.direction=direction
		self.magnitude=magnitude

class Body:
	'body with mass, position, velocity'
	def __init__(self,mass,x,y,dir,mag):
		self.mass=mass
		self.pos=Position(x,y)
		self.vel=Vector(radians(dir),mag)

class Cluster:
	def __init__(self):
		self.list=[]
	def add(self,body):
		self.list.append(body)
	def step(self):
		'one step in body interaction, returns sum of attraction between bodies'
		return 1

def main():
	print(name, version)

	# setup
	cluster=Cluster()
	cluster.add(Body(10,100,100,90,20))
	cluster.add(Body(20,110,200,270,5))

	# run
	iteration=0
	maxIteration=2e5
	initialTotalAttraction=cluster.step()
	while cluster.step() > initialTotalAttraction and ++iteration < maxIteration:
		pass

	print("done.")

if __name__ == "__main__":
	main()
