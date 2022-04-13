# tor-stats-simulation
An emulation and statistical analysis of the default Tor path selection and dynamic paths. Created for CSC466: Overlay and Peer-to-Peer Networking final project.

## Running
`python3 main.py <consensus file> [options]`

### Options
| **Option** | **Default** | **Description** |
| ---------- | ----------- | --------------- |
| --num_tor_paths | 20 | The number of regular Tor paths to create. |
| --num_dynamic_path | 20 | The number of dynamic Tor paths to create. |
| --use_guard_node | 1 | Requires path generation to use a trusted guard node for all paths. |
| --adv_guards_start | 199 | The number of aversary guard nodes to start in the directory. |
| --adv_guards_end | 200 | The number of aversary guard nodes to end in the directory. |
| --adv_guard_bw_start | 10000 | The advertised bandwidth for adversary guard nodes. |
| --adv_exits_start | 199 | The number of aversary exit nodes to start in the directory. |
| --adv_exits_end | 200 | The number of aversary exit nodes to end in the directory. |
| --adv_exit_bw_start | 15000 | The advertised bandwidth for adversary exit nodes. |
| --output_mode | None | Use DEBUG output mode to print Tor paths, circuit trees and stats. |
| --output_file | output_file.csv | Specify the output file for stats. |
