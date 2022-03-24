class dynamic_tor_path:
	def __init__(self, consensus):
		self.consensus = consensus

	def node_in_tree(self, new_node, tree):
		for node in tree:
			if node != None and new_node.id == node.id:
				return True
		return False

	def generate_trees(self, num_paths, use_guard_node):
		paths = []

		guard_node = None
		if use_guard_node:
			guard_node = self.consensus.get_guard_node()

		for i in range(num_paths):
			tree = [None for i in range(7)] # 7 nodes total in tree

			# choose entry node
			entry_node = None
			if use_guard_node:
				entry_node = guard_node
			else:
				entry_node = self.consensus.get_guard_node()

			tree[0] = entry_node

			# choose exit nodes
			for i in range(3, 7):
				exit_node = self.consensus.get_exit_node()
				while self.node_in_tree(exit_node, tree):
					exit_node = self.consensus.get_exit_node()
				tree[i] = exit_node

			# choose middle nodes
			for i in range(1, 3):
				middle_node = self.consensus.get_middle_node()
				while self.node_in_tree(middle_node, tree):
					middle_node = self.consensus.get_middle_node()
				tree[i] = middle_node

			paths.append(tree)

		return paths
