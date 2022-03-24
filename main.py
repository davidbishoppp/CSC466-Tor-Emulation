# specs followed from https://gitweb.torproject.org/torspec.git/tree/path-spec.txt
# and https://gitweb.torproject.org/torspec.git/tree/dir-spec.txt
# also inspired by functions from https://github.com/torps/torps for path selection

import sys
import consensus
import tor_path
import dynamic_tor_path
import statistics

def main():
	consensus_file = sys.argv[1]

	num_tor_paths = 20
	num_dynamic_paths = 20
	use_guard_node = 1
	adv_guards = 200
	adv_guard_bw = 10000
	adv_exits = 200
	adv_exit_bw = 15000
	hop_build_time = None
	output_mode = "DISPLAY"

	# parse options
	for option in sys.argv:
		tokens = option.split('=')
		if tokens[0].startswith("--num_tor_paths"):
			use_guard_node = int(tokens[1])
		if tokens[0].startswith("--num_dynamic_paths"):
			use_guard_node = int(tokens[1])
		if tokens[0].startswith("--use_guard_node"):
			use_guard_node = int(tokens[1])
		if tokens[0].startswith("--adv_guards"):
			adv_guards = int(tokens[1])
		if tokens[0].startswith("--adv_guard_bw"):
			adv_guard_bw = int(tokens[1])
		if tokens[0].startswith("--adv_exits"):
			adv_exits = int(tokens[1])
		if tokens[0].startswith("--adv_exit_bw"):
			adv_exit_bw = int(tokens[1])
		if tokens[0].startswith("--hop_build_time"):
			timings = tokens[1].split(',')
			hop_build_time = [int(timings[0]), int(timings[1]), int(timings[2])]
		if tokens[0].startswith("--output_mode"):
			output_mode = tokens[1]
		
	# create and parse the consensus file
	cons = consensus.consensus(consensus_file)
	cons.parse_consensus()

	# create adversary guard nodes
	for i in range(adv_guards):
		name = "adv_guard_{}".format(i)
		flags = ['Guard', 'Valid', 'Fast', 'Running', 'Stable', 'Adv']
		bandwidth = 9000
		cons.add_node(name, name, flags, bandwidth)

	# create adversary exit nodes
	for i in range(adv_exits):
		name = "adv_exit_{}".format(i)
		flags = ['Exit', 'Valid', 'Fast', 'Running', 'Stable', 'Adv']
		bandwidth = 9000
		cons.add_node(name, name, flags, bandwidth)

	paths = tor_path.tor_path(cons).generate_paths(num_tor_paths, use_guard_node)
	if output_mode == "DEBUG":
		print("Tor paths:")
		for path in paths:
			print("guard: {}, middle: {}, exit: {}".format(path[0].name, path[1].name, path[2].name))

	trees = dynamic_tor_path.dynamic_tor_path(cons).generate_trees(num_dynamic_paths, use_guard_node)
	if output_mode == "DEBUG":
		print("Tor dynamic trees:")
		for tree in trees:
			print("guard: {}".format(tree[0].name))
			for i in range(1, 3):
				print("middle: {}".format(tree[i].name))
			for i in range(3, 7):
				print("exit: {}".format(tree[i].name))
			print()

	stats = statistics.statistics(cons, paths, trees, adv_guards, adv_guard_bw, adv_exits, adv_exit_bw, hop_build_time)
	stats.output()

if __name__ == "__main__":
	main()