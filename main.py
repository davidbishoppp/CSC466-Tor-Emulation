import sys
import math

class node:
	def __init__(self, name, flags, bandwidth):
		self.name = name
		self.flags = flags
		self.bandwidth = bandwidth

	def is_guard(self):
		return "Guard" in self.flags

	def is_valid(self):
		return "Valid" in self.flags

	def is_exit(self):
		return "Exit" in self.flags

	def is_bad_exit(self):
		return "BadExit" in self.flags

class consensus:
	def __init__(self, consensus_file):
		self.consensus_file = consensus_file
		self.guard_nodes = []
		self.exit_nodes = []
		self.relay_nodes = []

	def parse_consensus(self):
		with open(self.consensus_file, "r") as cf:
			# read lines and create nodes
			name = None
			flags = None
			bandwidth = None

			first_node = True

			line = cf.readline()
			while line:
				prefix = line[:2]

				if prefix == "r ": # came to new node
					if not first_node:
						if name == None or flags == None or bandwidth == None: # if we didnt fill any of the parameters
							print("ERROR")
							print("name = ", name)
							print("fags = ", flags)
							print("bandwitdh = ", bandwidth)
							exit(1)

						# make new node from values we have
						new_node = node(name, flags, bandwidth)
						if new_node.is_exit():
							self.exit_nodes.append(new_node)
						if new_node.is_guard():
							self.guard_nodes.append(new_node)
						self.relay_nodes.append(new_node)

						name = None
						flags = None
						bandwidth = None
					first_node = False

					tokens = line.split() # prefix, name, hash, hash, date, time, ip, port, ?
					name = tokens[1]
				elif prefix == "s ": # flags for node
					tokens = line.split()
					flags = tokens[1:] # want all but the prfix
				elif prefix == "w ": # bandwidth
					tokens = line.split()
					bandwidth_tokens = tokens[1].split(sep="=") # get bandwidth and value tokens
					bandwidth = int(bandwidth_tokens[1]) # convert to int
				else: # dont care about the others. TODO: include accept and reject ports for path selection?
					pass

				line = cf.readline()
	
	def average_bandwidth(self):
		total = 0
		for node in self.relay_nodes:
			total += node.bandwidth
		return math.floor(total/len(self.relay_nodes))

class normal_tor_path:
	pass

class dynamic_tor_path:
	pass

def main():
	adv_guards = int(sys.argv[1])
	adv_exits = int(sys.argv[2])

	# create and parse the consensus file
	cons = consensus("consensus")
	cons.parse_consensus()

	average_bandwidth = cons.average_bandwidth()

	# create adversary guard nodes
	for i in range(adv_guards):
		name = "adv_guard_{}".format(i)
		flags = ['Guard', 'Valid', 'Fast', 'Running', 'Stable']
		bandwidth = average_bandwidth
		new_node = node(name, flags, bandwidth)
		cons.guard_nodes.append(new_node)
		cons.relay_nodes.append(new_node)

	# create adversary exit nodes
	for i in range(adv_exits):
		name = "adv_exit_{}".format(i)
		flags = ['Exit', 'Valid', 'Fast', 'Running', 'Stable']
		bandwidth = average_bandwidth
		new_node = node(name, flags, bandwidth)
		cons.exit_nodes.append(new_node)
		cons.relay_nodes.append(new_node)

	print("number of adversary guards = {}".format(adv_guards))
	print("number of adversary Exits = {}".format(adv_exits))
	print("number of total guards = {}".format(len(cons.guard_nodes)))
	print("number of total exits = {}".format(len(cons.exit_nodes)))
	print("number of total relays = {}".format(len(cons.relay_nodes)))

if __name__ == "__main__":
	main()