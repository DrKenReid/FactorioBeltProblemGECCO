import factorio_rcon # pip3 install factorio-rcon-py Library to use RCON for Factorio
from datetime import datetime
import numpy as np
import _thread
import time
import random
import configparser
import sys
import argparse
import time
from os import listdir
from os.path import isfile, join
import math

# constants are defined here
from constants import *

global debug

class Interface:
	# class constructor
	def __init__(self, ip, port, password, inputs, defaults):
		self.client = None
		self.ip = ip 
		self.port = port 
		self.password = password
		self.inputs = {}
		self.outputs = {}
		self.fitness = -1
		self.initialinputs = inputs
		self.default = defaults

	# connects to the Factorio Console. Needs a running multiplayer server.
	def connect(self):
		self.client = factorio_rcon.RCONClient(self.ip, self.port, self.password) # IP, Port, Password

	# removes all the entities in the surface
	def reset_surface(self):
		command = "/c game.surfaces[1].clear()"
		command += "; game.surfaces[1].daytime=0"
		self.send(command)

	# builds a solution matrix in game 
	def build(self, matrix, filename, index=0):
		filename = filename.split("/")
		filename = filename[len(filename)-1]

		# going through the matrix
		for x, a in enumerate(matrix):
			for y, b in enumerate(a):
				if b == 0:
					continue
				else:
					entity = MAP[b]
					entity = entity.split("_")
					
					n = 10 # groups of 3

					# calculate the factorio world position for each entities of the matrix (e.g transport belts / underground belts / spliters etc)
					yprime = x+2  + index * (len(matrix) + 6) - n * (len(matrix) + 6) * math.floor(index/n)
					xprime = y+2 + math.floor(index/n)*(len(matrix[0]) + 6)

					# create the entities
					if len(entity) == 2:
						self.create_entity(name=entity[0], position=(xprime, yprime), filename=filename, direction=entity[1])
					else:
						self.create_entity(name=entity[0], position=(xprime, yprime), filename=filename)

    # sends a message to rcon
	def send(self, message):
		return self.client.send_command("{}".format(message))

	# builds a given problem matrix for each solution that needs to be tested 
	def make_problem(self, matrix, files):
		# for each solution file
		for index, filename in enumerate(files):
			filename = filename.split("/")
			filename = filename[len(filename)-1]
			xl = len(matrix) 
			yl = len(matrix[0])
			if not filename in self.outputs.keys():
				self.outputs[filename] = [] 
			if not filename in self.inputs.keys():
				self.inputs[filename] = [] 
			
			# uses same principle as the build function
			for x, a in enumerate(matrix):
				for y, b in enumerate(a):
					n = 10 # groups of 3	
					xprime = x + index * (xl + 2) - n * (xl + 2) * math.floor(index/n)
					yprime = y + math.floor(index/n)*(yl + 2)

					if b == 0:
						continue
					else:
						entity = MAP[b]
						entity = entity.split("_")

						if entity[0] == "steel-chest":
							if (x-1 >= 0 and matrix[x-1][y] == -4) or (y-1 >= 0 and matrix[x][y-1] == -3) or (x+1 < xl and matrix[x+1][y] == -2) or (y+1 < yl and matrix[x][y+1] == -5):
								self.inputs[filename].append((yprime, xprime))
							else:
								self.outputs[filename].append((yprime, xprime))
						# at this point we have x and y
				
						# check whether or not the entity has direction
						if len(entity) == 2:
							self.create_entity(name=entity[0], position=(yprime, xprime), filename=filename, direction=entity[1])
						else:
							# no direction like a box for example or a steel-chest
							self.create_entity(name=entity[0], position=(yprime, xprime), filename=filename)

	# creates a box. can be full or empty
	def create_box(self, position, fill):
		x = position[0]
		y = position[1]
		command = "/c box = game.surfaces[1].create_entity{{name=\"steel-chest\", position={{{}, {}}}, force=game.forces.player}}".format(x, y)
		if fill:
			command += "; box.insert{name=\"iron-ore\", count=2000}"
		self.send(command)

	# creates an entity facing an arbitrary direction on a given position
	def create_entity(self, name, position, filename, direction=None):

		x = position[0]
		y = position[1]

		if name == "steel-chest" and position in self.inputs[filename]:
			
			command = "/c box = game.surfaces[1].create_entity{{name=\"steel-chest\", position={{{}, {}}}, force=game.forces.player}}".format(x, y)
			command += "; box.insert{name=\"iron-ore\", count=2000}"
			return self.client.send_command("{}".format(command))

		if direction:
			command = "/c entity = game.surfaces[1].create_entity{{name=\"{}\", position={{{}, {}}}, direction=defines.direction.{}, force=game.forces.player}}".format(name, x, y, direction)
		else:
			command = "/c entity = game.surfaces[1].create_entity{{name=\"{}\", position={{{}, {}}}, force=game.forces.player}}".format(name, x, y)
		
		return self.client.send_command("{}".format(command))

	# sets the game speed
	def set_game_speed(self, speed):
		self.send("/c game.speed={}".format(speed))

	# Returns the number of materials in the input/output box whenever the function is called for all the output/input boxes. Evaluation is done in the optimizer
	def evaluate(self):
		output = ""
		for filename in self.outputs:
			for i, pos in enumerate(self.outputs[filename]):
				x = pos[0]
				y = pos[1]
				command = "/c output = game.surfaces[1].find_entities_filtered{{name='steel-chest', position={{{}, {}}}, radius=1}}[1]".format(x, y)
				command += "; inventory = output.get_output_inventory()"
				command += "; count = inventory.get_item_count()"
				command += "; rcon.print(count)"
				response = self.send(command)
				
				output += "{}_output_{}: {}\n".format(filename, i, response)
				if debug:
					print("evaluate()::response = " + response + "\n")

		for filename in self.inputs:
			for i, pos in enumerate(self.inputs[filename]):
				x = pos[0]
				y = pos[1]
				command = "/c input = game.surfaces[1].find_entities_filtered{{name='steel-chest', position={{{}, {}}}, radius=1}}[1]".format(x, y)
				command += "; inventory = input.get_output_inventory()"
				command += "; count = inventory.get_item_count()"
				command += "; rcon.print(count)"
				response = self.send(command)
				# print("response", response)

				response = 2000 - int(response) 
				output += "{}_input_{}: {}\n".format(filename, i, response)
				if debug:
					print("evaluate()::response = " + repr(response) + "\n")

		self.fitness = output
		print(output)

	# saves the return value of evaluate (indirectly) in a given path (creates/truncates the file)
	def save_fitness(self, path):
		flag_save = True
		while flag_save:
			flag_save = False
			try:
				file = open(path, "w")
				file.write(str(self.fitness))
				file.close()
			except:
				flag_save = True
				# print("Interface Save Error: Retrying")
				time.sleep(0.0001)


# converts string to boolean
def s2b(str):
  return str.lower() in ("yes", "true", "y", "1")

# The main function
def main():
	# globals
	global debug

	# arg parser
	parser = argparse.ArgumentParser()
	parser.add_argument("-problem", help="path to the problem matrix file")
	parser.add_argument("-input", help="path to the input matrix file")
	parser.add_argument("-output", help="path to the output/fitness file")
	parser.add_argument("-config", help="path to the config file")
	parser.add_argument("-idir", help="path to the inputs directory")
	args = parser.parse_args()

	config_path = "config.ini"

	if args.config:
		config_path = args.config

	# connect to the config file
	config = configparser.ConfigParser()

	config.read(config_path)

	# start of configuration from config.ini
	debug = s2b(config['DEFAULT']['debug'])
	input_file = config['DEFAULT']['inputfile']
	problem_file = config['DEFAULT']['problemfile']
	output_file = config['DEFAULT']['outputfile']
	ip = config['DEFAULT']['ip']
	port = int(config['DEFAULT']['port'])
	password = config['DEFAULT']['password']
	speed = config['DEFAULT']['gamespeed']
	seed = config['DEFAULT']['seed']
	wait_time = float(config['DEFAULT']['waittime'])
	inputsdefaults = config['DEFAULT']['inputsdefaults']
	inputs = config['DEFAULT']['inputs']

	# end of configuration from config.ini

	# begin configuration from terminal
	if args.input:
		input_file = args.input
	if args.output:
		output_file = args.output
	if args.problem:
		problem_file = args.problem

	inputDir = ""
	flag_multiInput = False
	if args.idir:
		inputDir = args.idir
		flag_multiInput = True

	random.seed(seed)

	# randomly generating a numpy matrix
	# input_matrix = np.random.randint(size, size=(n, n))

	# how to save a numpy matrix
	# np.savetxt("input/matrix.txt", input_matrix)
	
	# loading a numpy matrix
	# print("\n\n\n\n {} \n\n\n\n".format(input_file))

	if not flag_multiInput: 
		# We only get one input. Go according to the previous single input single output approach
		input_matrix = np.loadtxt(input_file)
		problem_matrix = np.loadtxt(problem_file)

		xi = len(input_matrix)
		yi = len(input_matrix[0])
		xp = len(problem_matrix)
		yp = len(problem_matrix[0])
		if xi + 4 != xp or yi + 4 != yp:
			raise "ERROR: incompatible input/problem. input matrix size: {}x{} problem matrix size: {}x{}".format(xi, yi, xp, yp)

		if debug:
			print("\nmain()::input_matrix = \n" + str(input_matrix) + "\n")

		intf = Interface(ip=ip, port=port, password=password, inputs=inputs, defaults=inputsdefaults)
		intf.connect()
		time.sleep(0.0001)
		intf.set_game_speed(speed=speed)
		intf.reset_surface()
		intf.make_problem(matrix=problem_matrix, files=[input_file])
		intf.build(matrix=input_matrix, filename=input_file)
		time.sleep(wait_time)
		intf.evaluate()   
		intf.save_fitness(path=output_file)

	elif flag_multiInput:
		# We have multiple input files and therefore all should be tested concurrently 

		problem_matrix = np.loadtxt(problem_file)

		# inputDir =  r"C:\Users\iliya\OneDrive\Desktop\Work\Codes\QuickGP\factorio\inputs\\"

		onlyfiles = [f for f in listdir(inputDir) if isfile(join(inputDir, f))]

		intf = Interface(ip=ip, port=port, password=password, inputs=inputs, defaults=inputsdefaults)
		intf.connect()
		intf.set_game_speed(speed=speed)
		intf.reset_surface()
		intf.make_problem(matrix=problem_matrix, files=onlyfiles)
		for index, filename in enumerate(onlyfiles):

			flag_save = True
			while flag_save:
				flag_save = False
				try:
					input_matrix = np.loadtxt(inputDir + filename)
				except:
					# ToDo:: fix this for mac files.
					flag_save = True
					time.sleep(0.0001)
			
			xi = len(input_matrix)
			yi = len(input_matrix[0])
			xp = len(problem_matrix)
			yp = len(problem_matrix[0])
			if xi + 4 != xp or yi + 4 != yp:
				raise "ERROR: incompatible input/problem. input matrix size: {}x{} problem matrix size: {}x{}".format(xi, yi, xp, yp)
			
			if debug:
				print("\nmain()::input_matrix = \n" + str(input_matrix) + "\n")

			intf.build(matrix=input_matrix, filename=filename, index=index)

		time.sleep(wait_time)
		intf.evaluate()   

		exit()

# calls the main function
if __name__ == '__main__':
	main()