# specs followed from https://gitweb.torproject.org/torspec.git/tree/path-spec.txt
# and https://gitweb.torproject.org/torspec.git/tree/dir-spec.txt
# also inspired by functions from https://github.com/torps/torps for path selection

import sys
import copy
import consensus
import tor_path
import dynamic_tor_path
import statistics


def main():
	consensus_file = sys.argv[1]

	num_tor_paths = 20
	num_dynamic_paths = 20
	use_guard_node = 1
	adv_guards_start = 200
	adv_guards_end = 200
	adv_guard_bw_start = 10000
	adv_guard_bw_end = 10000
	adv_exits_start = 200
	adv_exits_end = 200
	adv_exit_bw_start = 15000
	adv_exit_bw_end = 15000
	output_mode = None
	output_file = "output_file.csv"

	# parse options
	for option in sys.argv:
		tokens = option.split('=')
		if tokens[0].startswith("--num_tor_paths"):
			num_tor_paths = int(tokens[1])
		if tokens[0].startswith("--num_dynamic_paths"):
			num_dynamic_paths = int(tokens[1])
		if tokens[0].startswith("--use_guard_node"):
			use_guard_node = int(tokens[1])
		if tokens[0].startswith("--adv_guards_start"):
			adv_guards_start = int(tokens[1])
		if tokens[0].startswith("--adv_guards_end"):
			adv_guards_end = int(tokens[1])
		if tokens[0].startswith("--adv_guard_bw_start"):
			adv_guard_bw_start = int(tokens[1])
		if tokens[0].startswith("--adv_guard_bw_end"):
			adv_guard_bw_end = int(tokens[1])
		if tokens[0].startswith("--adv_exits_start"):
			adv_exits_start = int(tokens[1])
		if tokens[0].startswith("--adv_exits_end"):
			adv_exits_end = int(tokens[1])
		if tokens[0].startswith("--adv_exit_bw_start"):
			adv_exit_bw_start = int(tokens[1])
		if tokens[0].startswith("--adv_exit_bw_end"):
			adv_exit_bw_end = int(tokens[1])
		if tokens[0].startswith("--output_mode"):
			output_mode = tokens[1]
		if tokens[0].startswith("--output_file"):
			output_file = tokens[1]

	wrote_header = False

	# create and parse the consensus file
	original_consensus = consensus.consensus(consensus_file)
	original_consensus.parse_consensus()
	num_guards = 0
	num_exits = 0

	# add starting number of guard nodes
	for num_guards in range(adv_guards_start):
		name = "adv_guard_{}".format(num_guards)
		original_consensus.add_node(name, name, ['Guard', 'Valid', 'Fast', 'Running', 'Stable', 'Adv'], adv_guard_bw_start)
	
	# add starting number of exit nodes
	for num_exits in range(adv_exits_start):
		name = "adv_exit_{}".format(num_exits)
		original_consensus.add_node(name, name, ['Exit', 'Valid', 'Fast', 'Running', 'Stable', 'Adv'], adv_exit_bw_start)

	for num_guards in range(adv_guards_start, adv_guards_end):
		# add another guard node
		name = "adv_guard_{}".format(num_guards)
		original_consensus.add_node(name, name, ['Guard', 'Valid', 'Fast', 'Running', 'Stable', 'Adv'], adv_guard_bw_start)

		cons = copy.deepcopy(original_consensus)

		for num_exits in range(adv_exits_start, adv_exits_end):
			# add another exit node
			name = "adv_exit_{}".format(num_exits)
			cons.add_node(name, name, ['Exit', 'Valid', 'Fast', 'Running', 'Stable', 'Adv'], adv_exit_bw_start)

			cons.compute_scale_weight_nodes()

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
					for k in range(1, 3):
						print("middle: {}".format(tree[k].name))
					for k in range(3, 7):
						print("exit: {}".format(tree[k].name))
					print()
				
			stats = statistics.statistics(cons, paths, trees, num_guards, adv_guard_bw_start, num_exits, adv_exit_bw_start)
			results, headers = stats.calculate()

			if output_mode == "DEBUG":
				stats.output(results=results);

			# output results to file
			with open(output_file, 'a') as f:
				if not wrote_header:
					f.write("# of adv guards,adv guard bw,# of adv exits,adv exit bw,")
					for header in headers:
						f.write(header+",")
					f.write("\n")
					wrote_header = True
				f.write("{},{},{},{},".format(num_guards, adv_guard_bw_start, num_exits, adv_exit_bw_start))
				for result in results:
					f.write(str(result)+",")
				f.write("\n")

if __name__ == "__main__":
	main()