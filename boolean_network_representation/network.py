from graphviz import Digraph
from itertools import product

from boolean_network_representation.rules import RuleLoader
from graphviz import Digraph


class BooleanNetwork:
    def __init__(self, entity_count, rule_source="manual"):
        """
        Initialize the Boolean Network.

        Args:
        - entity_count: Number of entities in the Boolean Network (fixed).
        - rule_source: Source of rules ('gui' or 'manual')
        """
        self.entity_count = entity_count
        self.nodes = [f"N{i + 1}" for i in range(entity_count)]
        self.states = [f"{i:0{entity_count}b}" for i in range(2 ** entity_count)]

        # Initialize RuleLoader as a blueprint for rules
        self._rule_loader = RuleLoader(entity_count)
        self.initial_rules = self._rule_loader.load_rules(rule_source)
        self.current_rules = self.initial_rules.copy()

        # Check that the number of rules matches the number of entities
        self._validate_rules()

    def _validate_rules(self):
        """
        Checks that the number of rules matches the number of entities.
        """
        if len(self.current_rules) != self.entity_count:
            raise ValueError("Number of rules must match the number of entities")

    def get_next_state(self, current_state):
        """
        Calculates the next state for each entity using current_rules.

        Args:
        - current_state: A list of integers representing the current state of each entity.

        Returns:
        - next_state: A list of integers representing the next state of each entity.
        """
        next_state = []
        for i, rule in enumerate(self.current_rules):
            if rule is not None:
                next_state.append(rule(current_state, i))
            else:
                next_state.append(current_state[i])  # If no rule, keep current state
        return next_state

    def get_state_transition(self):
        """
        Generates all state transitions for the Boolean Network.

        Returns:
        - transitions: A dictionary with current state as keys and next state as values.
        """
        transitions = {}
        for state in self.states:
            current_state = list(map(int, state))
            next_state = self.get_next_state(current_state)
            next_state_str = ''.join(map(str, next_state))
            transitions[state] = next_state_str
        return transitions

    def generate_state_graph(self, filename='state_graph'):
        """
        Generates the state graph for the Boolean Network.
        """
        dot = Digraph(comment=f'{self.entity_count}-Entity Boolean Network State Graph')
        dot.attr(rankdir='LR')

        for state, next_state in self.get_state_transition().items():
            dot.node(state, state)
            dot.edge(state, next_state, label=f"{state} → {next_state}")

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
            next_state = self.get_next_state(current_state)
            next_state_str = ''.join(map(str, next_state))

            transition_desc = ", ".join(
                [f"{self.nodes[i]}'={current_state[i]}->{next_state[i]}" for i in range(self.entity_count)]
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
                next_state_list = self.get_next_state(current_state_list)
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
