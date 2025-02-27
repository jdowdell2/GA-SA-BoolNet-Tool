from graphviz import Digraph
from itertools import product


class BooleanNetwork:
    def __init__(self, rules_function, node_count, rules):
        """
        Initialize the Boolean Network.

        Args:
        - rules_function: Function defining the state transition rules.
        - node_count: Number of nodes in the Boolean Network (default: 4).
        """
        self.rules_function = rules_function
        self.node_count = node_count
        self.nodes = [f"N{i + 1}" for i in range(node_count)]
        self.states = [f"{i:0{node_count}b}" for i in range(2 ** node_count)] # convert all 2^n states to binary strings of n bits
        self.states = rules

    def get_next_state(self, current_state):
        next_state = []
        for i, rule in enumerate(self.rules):
            next_state.append(rule(current_state, i))  # Pass index to rule for adaptability
        return next_state

    def generate_state_graph(self, filename='state_graph'):
        """
        Generates the state graph for the Boolean Network.
        """
        dot = Digraph(comment=f'{self.node_count}-Node Boolean Network State Graph')
        dot.attr(rankdir='LR')

        for state in self.states:
            current_state = list(map(int, state))
            next_state = self.rules_function(*current_state)
            next_state_str = ''.join(map(str, next_state))

            dot.node(state, state)
            dot.edge(state, next_state_str, label=f"{state} → {next_state_str}")

        dot.render(filename, format='png', view=True)

    def generate_truth_table(self):
        """
        Generates and prints the truth table for the Boolean Network.
        """
        print("\nTruth Table for Boolean Network")
        header = " | ".join(self.nodes) + " | " + " | ".join([f"{n}'" for n in self.nodes]) + " | Description"
        print(header)
        print("-" * len(header))

        for state in self.states:
            current_state = list(map(int, state))
            next_state = self.rules_function(*current_state)
            next_state_str = ''.join(map(str, next_state))

            transition_desc = ", ".join(
                [f"{self.nodes[i]}'={current_state[i]}->{next_state[i]}" for i in range(self.node_count)]
            )
            print(f"  {' '.join(state)} | {' '.join(map(str, next_state))} | {transition_desc}")

    def detect_attractors(self):
        """
        Detects attractors in the Boolean Network.
        """
        attractors = []

        for initial_state in self.states:
            visited = {}
            current_state = initial_state

            while current_state not in visited:
                visited[current_state] = len(visited)
                current_state_list = list(map(int, list(current_state)))
                next_state_list = self.rules_function(*current_state_list)
                next_state = ''.join(map(str, next_state_list))
                current_state = next_state

            start = visited[current_state]
            cycle = list(visited.keys())[start:]
            min_rotation = min([cycle[i:] + cycle[:i] for i in range(len(cycle))])
            attractors.append(min_rotation)

        unique_attractors = []
        for attractor in attractors:
            if attractor not in unique_attractors:
                unique_attractors.append(attractor)

        print("\nDetected Attractors:")
        for attractor in unique_attractors:
            print("Cycle:", " → ".join(attractor))