import random
import csv
import math
import time

num_particles = 2000
iterations = 100
max_vel = 1
global_best = {'a': 0, 'b': 0, 'c': 0, 'cost': float('inf')}
c1 = 0.4
c2 = 0.4
w = 0.4
num_over = 0

real_function = []
with open('data_points.csv', newline='') as data:
	reader = csv.DictReader(data)
	for row in reader:
		real_function.append({'x': float(row['x']), 'y': float(row['y']), 'z': float(row['z'])})

class Particle:
	def __init__(self, a, b, c):
		self.pos = {"a": a, "b": b, "c": c, cost: 0}
		cur_cost = cost(self)
		self.best_pos = {"a": a, "b": b, "c": c, 'cost': cur_cost}
		self.pos['cost'] = cur_cost

	def __str__(self):
		called = f'Current pos: {self.pos}, Best_pos: {self.best_pos}'
		return called

	def set_vel(self, vel_a, vel_b, vel_c):
		self.vel = {"a": vel_a, "b": vel_b, 'c': vel_c}

	def update_vel(self):
		global c1, c2, w, global_best, max_vel, num_over

		r1 = random.random()
		r2 = random.random()

		new_vel = w * self.vel['a'] + c1 * r1 * (self.best_pos['a'] - self.pos['a']) + c2 * r2 * (global_best['a'] - self.pos['a'])
		if abs(new_vel) > max_vel:
			num_over += 1
		self.vel['a'] = min(max_vel, new_vel) if new_vel >= 0 else max(-1 * max_vel, new_vel)
		new_vel = w * self.vel['b'] + c1 * r1 * (self.best_pos['b'] - self.pos['b']) + c2 * r2 * (global_best['b'] - self.pos['b'])
		if abs(new_vel) > max_vel:
			num_over += 1
		self.vel['b'] = min(max_vel, new_vel) if new_vel >= 0 else max(-1 * max_vel, new_vel)
		new_vel = w * self.vel['c'] + c1 * r1 * (self.best_pos['c'] - self.pos['c']) + c2 * r2 * (global_best['c'] - self.pos['c'])
		if abs(new_vel) > max_vel:
			num_over += 1
		self.vel['c'] = min(max_vel, new_vel) if new_vel >= 0 else max(-1 * max_vel, new_vel)

	def update_pos(self):
		self.pos['a'] += self.vel['a']
		self.pos['b'] += self.vel['b']
		self.pos['c'] += self.vel['c']
		cur_cost = cost(self)
		self.pos['cost'] = cur_cost
		if self.pos['cost'] < self.best_pos['cost']:
			self.best_pos['a'] = self.pos['a']
			self.best_pos['b'] = self.pos['b']
			self.best_pos['c'] = self.pos['c']
			self.best_pos['cost'] = self.pos['cost']


def main():
	global global_best, num_over
	start = time.time()
	particle_swarm()
	end = time.time()
	#print(f'Time: {end-start}')
	#print(global_best)
	#print(num_over)

def evaluate_function(a, b, c, x, y):
	z = (a * x ** 2 + y ** 2 + b) * math.sin(c * x + y)

	return z

def cost(particle):
	global real_function

	squared_error = 0
	for point in real_function:
		point_z = evaluate_function(particle.pos['a'], particle.pos['b'], particle.pos['c'], point['x'], point['y'])
		squared_error += (point_z - point['z']) ** 2

	return squared_error

def particle_swarm():
	global num_particles, iterations, global_best

	particles = []

	for i in range(num_particles):
		a = random.random() * 10 - 5
		b = random.random() * 100 - 50
		c = random.random() * (10-0.01) + 0.01

		new_particle = Particle(a, b, c)
		new_particle.set_vel(0, 0, 0)
		particles.append(new_particle)
		if new_particle.best_pos['cost'] < global_best['cost']:
			global_best['a'] = new_particle.best_pos['a']
			global_best['b'] = new_particle.best_pos['b']
			global_best['c'] = new_particle.best_pos['c']
			global_best['cost'] = new_particle.best_pos['cost']

	count = 0
	while count < iterations:
		for i in particles:
			i.update_vel()
			i.update_pos()
			if i.pos['cost'] < global_best['cost']:
				global_best['a'] = i.pos['a']
				global_best['b'] = i.pos['b']
				global_best['c'] = i.pos['c']
				global_best['cost'] = i.pos['cost']
		count += 1
		#print(f"a: {global_best['a']}, b: {global_best['b']}, c: {global_best['c']}, cost{global_best['cost']}")
		print(f"{count}, {global_best['cost']}")



if __name__ == '__main__':
	main()