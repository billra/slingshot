#! python3

name='Gravitational Slingshot Simulator'
version='v0.3'
author='Bill Ola Rasmussen'

from math import sin, cos, radians, hypot, pow

class Position:
	def __init__(self,x,y):
		self.x=x
		self.y=y
	def dx(self,other):
		'distance to another position'
		return hypot(other.x-self.x,other.y-self.y)

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
	def update(self, other):
		'update self with effect from other'
		# f = (m1 * m2) / r^2, see https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation#Modern_form
		# force is proportional to this calculation (ignores gravitational constant)
		force = self.mass*other.mass/pow(self.pos.dx(other.pos),2)
		# todo update position based on force
		return force

class Cluster:
	def __init__(self):
		self.buf=[]
	def add(self,body):
		self.buf.append(body)
	def step(self):
		'one step in body interaction, returns sum of attraction between bodies'
		original=list(self.buf) # work on unchanged values
		cumulative=0
		for me in range(len(original)):
			# prior indices
			for other in range(0,me):
				cumulative+=self.buf[me].update(original[other])
			# subsequent indices
			for other in range(me+1,len(original)):
				cumulative+=self.buf[me].update(original[other])
		return cumulative

def main():
	print(name, version)

	# setup
	cluster=Cluster()
	cluster.add(Body(10,100,100,90,20))
	cluster.add(Body(20,110,200,270,5))

	# run
	maxIteration=int(2e5)
	initialTotalAttraction=cluster.step()
	for iteration in range(maxIteration):
		if cluster.step() < initialTotalAttraction: break

	print("done.")

if __name__ == "__main__":
	main()
