class statistics:
	def __init__(self, consensus, paths, trees, adv_guards, adv_guard_bw, adv_exits, adv_exit_bw, hop_build_time):
		self.consensus = consensus
		self.paths = paths
		self.trees = trees
		self.adv_guards = adv_guards
		self.adv_guard_bw = adv_guard_bw
		self.adv_exits = adv_exits
		self.adv_exit_bw = adv_exit_bw
		self.hop_build_time = hop_build_time

	def output(self):
		# # of nodes
		print("# of nodes: {}".format(len(self.consensus.get_middle_nodes())))
		
		# # of paths
		# # of trees
		print("# of paths: {}".format(len(self.paths)))
		print("# of trees: {}".format(len(self.trees)))

		# % bandwidth of adversary exit nodes among other exit nodes
		exit_nodes = self.consensus.get_exit_nodes()
		total_bw_exits = 0
		for node in exit_nodes:
			total_bw_exits += node.bandwidth
		print("% bandwidth of adversary exit nodes among all exit nodes: {:.2f}%".format(100*self.adv_exits*self.adv_exit_bw/total_bw_exits))

		# % bandwidth of adversary entry nodes among other entry nodes
		guard_nodes = self.consensus.get_guard_nodes()
		total_bw_guards = 0
		for node in guard_nodes:
			total_bw_guards += node.bandwidth
		print("% bandwidth of adversary guard nodes among all guard nodes: {:.2f}%".format(100*self.adv_guards*self.adv_guard_bw/total_bw_guards))
		
		# % bandwidth of adversary nodes among all nodes
		middle_nodes = self.consensus.get_middle_nodes()
		total_bw_middles = 0
		for node in middle_nodes:
			total_bw_middles += node.bandwidth
		print("% bandwidth of all adversary nodes among all nodes: {:.2f}%".format(100*(self.adv_guards*self.adv_guard_bw+self.adv_exits*self.adv_exit_bw)/total_bw_middles))

		# % of paths with an adversary exit node
		# % of paths with an adversary entry node
		# % of paths with both aversary exit and entry node

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
		print("% of paths with adversary exit node: {:.2f}%".format(100*total_exits_adv/len(self.paths)))
		print("% of paths with adversary entry node: {:.2f}%".format(100*total_entries_adv/len(self.paths)))
		print("% of paths with adversary entry and exit node: {:.2f}%".format(100*total_entries_exits_adv/len(self.paths)))
		print("% of paths with adversary entry, middle, and exit node: {:.2f}%".format(100*total_entries_middles_exits_adv/len(self.paths)))

		# % of trees with an adversary exit node
		# % of trees with an adversary entry node
		# % of trees with an adversary entry and exit node
		# % of trees with an adversary entry, middle and exit node
		# mode number of adversary middle nodes
		# mode number of adversary exit nodes

		total_trees_exits_adv = 0
		total_trees_entries_adv = 0
		total_trees_entries_exits_adv = 0
		total_trees_entries_middles_exits_adv = 0
		mode_adv_middle = {0:0, 1:0, 2:0}
		mode_adv_exit = {0:0, 1:0, 2:0, 3:0, 4:0}

		for tree in self.trees:
			adv_entry = False
			if tree[0].is_adv():
				total_trees_entries_adv += 1
				adv_entry = True

			adv_middle = False
			num_adv_middle = 0
			for i in range(1, 3):
				if tree[i].is_adv():
					adv_middle = True
					num_adv_middle += 1
			mode_adv_middle[num_adv_middle] += 1

			adv_exit = False
			num_adv_exit = 0
			for i in range(3, 7):
				if tree[i].is_adv():
					adv_exit = True
					num_adv_exit += 1
			mode_adv_exit[num_adv_exit] += 1

			if adv_exit:
				total_trees_exits_adv += 1
			if adv_entry:
				total_trees_entries_adv += 1
			if adv_entry and adv_exit:
				total_trees_entries_exits_adv += 1
			if adv_entry and adv_middle and adv_exit:
				total_trees_entries_middles_exits_adv += 1
			
		print("% of trees with an adversary exit node: {:.2f}%".format(100*total_trees_exits_adv/len(self.trees)))
		print("% of trees with an adversary entry node: {:.2f}%".format(100*total_trees_entries_adv/len(self.trees)))
		print("% of trees with an adversary entry and exit node: {:.2f}%".format(100*total_trees_entries_exits_adv/len(self.trees)))
		print("% of trees with an adversary entry, middle and exit node: {:.2f}%".format(100*total_entries_middles_exits_adv/len(self.trees)))
		key_middle = 0
		for key in mode_adv_middle.keys():
			if mode_adv_middle[key] > mode_adv_middle[key_middle]:
				key_exit = key
		print("mode number of adversary middle nodes: {}".format(key_middle))
		key_exit = 0
		for key in mode_adv_exit.keys():
			if mode_adv_exit[key] > mode_adv_exit[key_exit]:
				key_exit = key
		print("mode number of adversary exit nodes: {}".format(key_exit))
		
		# % increase in circuit build time from current data
		# 
		pass