#! python3

name='Gravitational Slingshot Simulator'
version='v0.4'
author='Bill Ola Rasmussen'

from math import sin, cos, radians, hypot, pow, atan2, sqrt

class Position:
	def __init__(self,x,y):
		self.x=x
		self.y=y
	def dx(self,other):
		'distance to another position'
		return hypot(other.y-self.y,other.x-self.x)
	def angle(self,other):
		'angle to another position'
		return atan2(other.y-self.y,other.x-self.x)
	def add(self,other):
		'add to this position'
		self.x+=other.x
		self.y+=other.y

class Vector:
	def __init__(self,direction,magnitude):
		'direction in radians'
		self.direction=direction
		self.magnitude=magnitude
		# velocity units: distance / time
	def cartesian(self):
		'apply vector to 0,0'
		x=cos(self.direction)*self.magnitude
		y=sin(self.direction)*self.magnitude
		return Position(x,y)
	def add(self,other):
		'add other vector to this vector'
		dx=cos(self.direction)*self.magnitude+cos(other.direction)*other.magnitude
		dy=sin(self.direction)*self.magnitude+sin(other.direction)*other.magnitude
		self.magnitude=sqrt(pow(dx,2)+pow(dy,2))
		self.direction=atan2(dy,dx)

class Body:
	'body with mass, position, velocity'
	def __init__(self,mass,x,y,dir,mag):
		self.mass=mass
		self.pos=Position(float(x),float(y))
		self.vel=Vector(radians(dir),mag)
	def update(self, other, time):
		'update self with effect from other over duration time'

		# force is proportional to this calculation (ignores gravitational constant)
		# f = (m1 * m2) / r^2, see https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation#Modern_form
		force = self.mass*other.mass/pow(self.pos.dx(other.pos),2)
		# force units: mass * distance / time^2

		# force is also: f = m * a, thus a = f / m
		acceleration = force / self.mass
		# acceleration units: distance / time^2

		# s = 1/2 * a * t^2
		moveDistance = 0.5 * acceleration * pow(time,2) 
		moveAngle = self.pos.angle(other.pos);

		self.vel.add(Vector(moveAngle,moveDistance))
		self.pos.add(self.vel.cartesian())

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
		time=5
		for me in range(len(original)):
			# prior indices
			for other in range(0,me):
				cumulative+=self.buf[me].update(original[other],time)
			# subsequent indices
			for other in range(me+1,len(original)):
				cumulative+=self.buf[me].update(original[other],time)
		for me in self.buf:
			print(me.pos.x, me.pos.y, end="  ")
		print()
		return cumulative

def main():
	print(name, version)

	# setup
	cluster=Cluster()
	cluster.add(Body(.9,0,0,0,0))
	cluster.add(Body(.1,0,20,180,5))

	# run
	maxIteration=int(2e5)
	initialTotalAttraction=cluster.step()
	for iteration in range(maxIteration):
		if cluster.step() < initialTotalAttraction: break

	print("done.")

if __name__ == "__main__":
	main()
