# tor-stats-simulation
An emulation and statistical analysis of the default Tor path selection and dynamic paths. Created for CSC466: Overlay and Peer-to-Peer Networking final project.

## Running
`python3 main.py <consensus file> [options]`

### Options
| **Option** | **Type** | **Default** | **Description** |
| ---------- | -------- | ----------- | --------------- |
| --num_tor_paths | number | 20 | The number of regular Tor paths to create. |
| --num_dynamic_paths | numer | 20 | The number of dynamic Tor paths to create. |
| --use_guard_node | number | 1 | Requires path generation to use a trusted guard node for all paths. |
| --adv_guards | number | 200 | The number of aversary guard nodes to include in the directory. |
| --adv_guard_bw | number | 10000 | The advertised bandwidth from adversary guard nodes. |
| --adv_exits | number | 200 | The number of aversary exit nodes to include in the directory. |
| --adv_exit_bw | number | 15000 | The advertised bandwidth from adversary exit nodes. |
| --hop_build_time | number,number,number | Will use current Tor metrics | The build time for the first, scond and thrid hop in the circuit in ms. |
| --output_mode | str | DISPLAY | Able to use DISPLAY and DEBUG output modes. |

## Example
`python3 main.py --use_guard_node=0 --adv_guards=200 --adv_guard_bw=15000 --adv_exits=200 --adv_exit_bw=10000`