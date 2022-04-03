class statistics:
	def __init__(self, consensus, paths, trees, adv_guards, adv_guard_bw, adv_exits, adv_exit_bw):
		self.consensus = consensus
		self.paths = paths
		self.trees = trees
		self.adv_guards = adv_guards
		self.adv_guard_bw = adv_guard_bw
		self.adv_exits = adv_exits
		self.adv_exit_bw = adv_exit_bw

	def calculate(self):
		results = []
		headers = []

		headers.append("# of nodes")
		results.append(len(self.consensus.get_middle_nodes()))

		headers.append("# of paths")
		headers.append("# of trees")
		results.append(len(self.paths))
		results.append(len(self.trees))

		headers.append("% bandwidth of adversary exit nodes among other exit nodes")
		exit_nodes = self.consensus.get_exit_nodes()
		total_bw_exits = 0
		for node in exit_nodes:
			total_bw_exits += node.bandwidth
		results.append(100*self.adv_exits*self.adv_exit_bw/total_bw_exits)

		headers.append("% bandwidth of adversary entry nodes among other entry nodes")
		guard_nodes = self.consensus.get_guard_nodes()
		total_bw_guards = 0
		for node in guard_nodes:
			total_bw_guards += node.bandwidth
		results.append(100*self.adv_guards*self.adv_guard_bw/total_bw_guards)
		
		headers.append("% bandwidth of adversary nodes among all nodes")
		middle_nodes = self.consensus.get_middle_nodes()
		total_bw_middles = 0
		for node in middle_nodes:
			total_bw_middles += node.bandwidth
		results.append(100*(self.adv_guards*self.adv_guard_bw+self.adv_exits*self.adv_exit_bw)/total_bw_middles)

		headers.append("% of paths with an adversary exit node")
		headers.append("% of paths with an adversary entry node")
		headers.append("% of paths with both aversary exit and entry node")
		headers.append("% of paths with both aversary exit midle and entry node")

		total_exits_adv = 0
		total_entries_adv = 0
		total_entries_exits_adv = 0
		total_entries_middles_exits_adv = 0
		for path in self.paths:
			if path[2].is_adv():
				total_exits_adv += 1
			if path[0].is_adv():
				total_entries_adv += 1
			if path[0].is_adv() and path[2].is_adv():
				total_entries_exits_adv += 1
			if path[0].is_adv() and path[1].is_adv() and path[2].is_adv():
				total_entries_middles_exits_adv += 1
		results.append(100*total_exits_adv/len(self.paths))
		results.append(100*total_entries_adv/len(self.paths))
		results.append(100*total_entries_exits_adv/len(self.paths))
		results.append(100*total_entries_middles_exits_adv/len(self.paths))

		headers.append("% of trees with an adversary exit node")
		headers.append("% of trees with an adversary entry node")
		headers.append("% of trees with an adversary entry and exit node")
		headers.append("% of trees with an adversary entry middle and exit node")
		headers.append("average number of adversary middle nodes")
		headers.append("average number of adversary exit nodes")

		total_trees_exits_adv = 0
		total_trees_entries_adv = 0
		total_trees_entries_exits_adv = 0
		total_trees_entries_middles_exits_adv = 0
		total_midles_adv = 0;
		total_exits_adv = 0;

		for tree in self.trees:
			adv_entry = False
			if tree[0].is_adv():
				total_trees_entries_adv += 1
				adv_entry = True

			adv_middle = False
			for i in range(1, 3):
				if tree[i].is_adv():
					adv_middle = True
					total_midles_adv += 1

			adv_exit = False
			for i in range(3, 7):
				if tree[i].is_adv():
					adv_exit = True
					total_exits_adv += 1

			if adv_exit:
				total_trees_exits_adv += 1
			if adv_entry:
				total_trees_entries_adv += 1
			if adv_entry and adv_exit:
				total_trees_entries_exits_adv += 1
			if adv_entry and adv_middle and adv_exit:
				total_trees_entries_middles_exits_adv += 1
			
		results.append(100*total_trees_exits_adv/len(self.trees))
		results.append(100*total_trees_entries_adv/len(self.trees))
		results.append(100*total_trees_entries_exits_adv/len(self.trees))
		results.append(100*total_entries_middles_exits_adv/len(self.trees))
		results.append(total_midles_adv)
		results.append(total_exits_adv)

		return results, headers

	def output(self, results=None):
		if resuls == None:
			results = self.calculate()

		# # of nodes
		print("# of nodes: {}".format(results[0]))

		# # of paths
		# # of trees
		print("# of paths: {}".format(results[1]))
		print("# of trees: {}".format(results[2]))

		# % bandwidth of adversary exit nodes among other exit nodes
		print("% bandwidth of adversary exit nodes among all exit nodes: {:.2f}%".format(results[3]))

		# % bandwidth of adversary entry nodes among other entry nodes
		print("% bandwidth of adversary guard nodes among all guard nodes: {:.2f}%".format(results[4]))
		
		# % bandwidth of adversary nodes among all nodes
		print("% bandwidth of all adversary nodes among all nodes: {:.2f}%".format(results[5]))

		# % of paths with an adversary exit node
		# % of paths with an adversary entry node
		# % of paths with both aversary exit and entry node
		print("% of paths with adversary exit node: {:.2f}%".format(results[6]))
		print("% of paths with adversary entry node: {:.2f}%".format(results[7]))
		print("% of paths with adversary entry and exit node: {:.2f}%".format(results[8]))
		print("% of paths with adversary entry, middle, and exit node: {:.2f}%".format(results[9]))

		# % of trees with an adversary exit node
		# % of trees with an adversary entry node
		# % of trees with an adversary entry and exit node
		# % of trees with an adversary entry, middle and exit node
		# mode number of adversary middle nodes
		# mode number of adversary exit nodes
		print("% of trees with an adversary exit node: {:.2f}%".format(results[10]))
		print("% of trees with an adversary entry node: {:.2f}%".format(results[11]))
		print("% of trees with an adversary entry and exit node: {:.2f}%".format(results[12]))
		print("% of trees with an adversary entry, middle and exit node: {:.2f}%".format(results[13]))
		print("mode number of adversary middle nodes: {}".format(results[14]))
		print("mode number of adversary exit nodes: {}".format(results[15]))