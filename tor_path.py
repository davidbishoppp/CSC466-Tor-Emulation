class tor_path:
	def __init__(self, consensus):
		self.consensus = consensus

	def node_in_path(self, new_node, path):
		for node in path:
			if node != None and new_node.id == node.id:
				return True
		return False

	def generate_paths(self, num_paths, use_guard_node):
		paths = []
		
		guard_node = None
		if use_guard_node:
			guard_node = self.consensus.get_guard_node()

		for i in range(num_paths):
			# choose entry node
			entry_node = None
			if use_guard_node:
				entry_node = guard_node
			else:
				entry_node = self.consensus.get_guard_node()

			# choose exit node
			exit_node = self.consensus.get_exit_node()
			while exit_node.id == entry_node.id:
				exit_node = self.consensus.get_exit_node()

			# choose middle node
			middle_node = self.consensus.get_middle_node()
			while middle_node.id == entry_node.id or middle_node.id == exit_node.id:
					middle_node = self.consensus.get_middle_node()

			paths.append((entry_node, middle_node, exit_node))

		return paths
