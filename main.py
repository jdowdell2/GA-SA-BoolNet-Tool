from graphviz import Digraph


# === 1. MAIN FUNCTION TO GENERATE STATE GRAPH ===
def generate_boolean_network_graph(rules_function, filename='4_node_state_graph'):
    """
    Generates a state graph for a 4-node Boolean network.

    Args:
    - rules_function: Function that takes (A, B, C, D) as input and returns (A', B', C', D')
    - filename: Name of the output file (default: '4_node_state_graph')
    """
    # Initialise Graphviz Digraph
    dot = Digraph(comment='4-Node Boolean Network State Graph')
    dot.attr(rankdir='TB')

    # Generate state transitions for all 16 states (0000 to 1111)
    states = [f"{i:04b}" for i in range(16)]
    for state in states:
        A, B, C, D = map(int, list(state))

        # Get the next state using the rules function
        A_next, B_next, C_next, D_next = rules_function(A, B, C, D)
        next_state_str = f"{A_next}{B_next}{C_next}{D_next}"

        # Create nodes and edges for the state graph
        dot.node(state, state)
        dot.edge(state, next_state_str, label=f"{state} → {next_state_str}")

    # Render and view Graphviz state graph
    dot.render(filename, format='png', view=True)


# === 2. MAIN FUNCTION TO GENERATE TRUTH TABLE ===
def generate_truth_table(rules_function):
    print("\nTruth Table for Boolean Network")
    print("Current State | Next State | Transition")
    print(" A B C D  | A' B' C' D' | Description")
    print("-" * 40)

    # Generate state transitions for all 16 states (0000 to 1111)
    states = [f"{i:04b}" for i in range(16)]
    for state in states:
        A, B, C, D = map(int, list(state))

        # Get the next state using the rules function
        A_next, B_next, C_next, D_next = rules_function(A, B, C, D)
        next_state_str = f"{A_next}{B_next}{C_next}{D_next}"

        # Generate Transition Description
        transition_desc = (
            f"A'={A}->{A_next}, "
            f"B'={B}->{B_next}, "
            f"C'={C}->{C_next}, "
            f"D'={D}->{D_next}"
        )

        # Display the Truth Table row
        print(f"  {A} {B} {C} {D}   | {A_next} {B_next} {C_next} {D_next}  | {transition_desc}")


# === 3. IMPROVED FUNCTION TO GENERATE WIRING DIAGRAM ===
def generate_wiring_diagram(rules_function, filename='wiring_diagram'):
    # Initialise Graphviz Digraph
    dot = Digraph(comment='4-Node Boolean Network Wiring Diagram')
    dot.attr(rankdir='LR')

    # Add nodes
    nodes = ['A', 'B', 'C', 'D']
    for node in nodes:
        dot.node(node, node)

    # Analyse rules to find logical dependencies
    # Test all possible inputs to identify dependencies
    inputs = [f"{i:04b}" for i in range(16)]
    dependencies = {'A': set(), 'B': set(), 'C': set(), 'D': set()}

    for state in inputs:
        A, B, C, D = map(int, list(state))
        A_next, B_next, C_next, D_next = rules_function(A, B, C, D)

        # Check which inputs affect each next state
        # By flipping each input and checking the effect on the next state
        for i, node in enumerate(nodes):
            original = list(state)
            original[i] = '1' if original[i] == '0' else '0'  # Flip the input
            flipped_state = "".join(original)
            A_flip, B_flip, C_flip, D_flip = map(int, list(flipped_state))
            A_flip_next, B_flip_next, C_flip_next, D_flip_next = rules_function(A_flip, B_flip, C_flip, D_flip)

            # Check dependencies by comparing next states
            if A_next != A_flip_next:
                dependencies['A'].add(node)
            if B_next != B_flip_next:
                dependencies['B'].add(node)
            if C_next != C_flip_next:
                dependencies['C'].add(node)
            if D_next != D_flip_next:
                dependencies['D'].add(node)

    # Create wiring connections from logical dependencies
    for target, sources in dependencies.items():
        for source in sources:
            if source != target:  # Avoid self-loops
                dot.edge(source, target)

    # Render and view Graphviz wiring diagram
    dot.render(filename, format='png', view=True)

def detect_attractors(rules_function):
    states = [f"{i:04b}" for i in range(16)]
    attractors = []

    for initial_state in states:
        visited = {}
        current_state = initial_state

        while current_state not in visited:
            visited[current_state] = len(visited)
            A, B, C, D = map(int, list(current_state))
            next_state = ''.join(map(str, rules_function(A, B, C, D)))
            current_state = next_state

        # Identify Attractor Cycle
        start = visited[current_state]
        cycle = list(visited.keys())[start:]

        # Normalise Cycle by finding minimal rotation
        min_rotation = min([cycle[i:] + cycle[:i] for i in range(len(cycle))])
        attractors.append(min_rotation)

    # Remove duplicate (rotationally equivalent) attractors
    unique_attractors = []
    for attractor in attractors:
        if attractor not in unique_attractors:
            unique_attractors.append(attractor)

    # Output Unique Attractors
    print("\nDetected Attractors:")
    for attractor in unique_attractors:
        print("Cycle:", " → ".join(attractor))





# === 4. ORIGINAL RULE SET ===
def original_rules(A, B, C, D):
    A_next = B  # A' = B
    B_next = C  # B' = C
    C_next = A and D  # C' = A AND D
    D_next = A and (not B)  # D' = A AND NOT B
    return int(A_next), int(B_next), int(C_next), int(D_next)


# === 5. EXAMPLE RULE SET 1: Feedback Loop Network ===
def example_rules_1(A, B, C, D):
    A_next = B
    B_next = C
    C_next = D
    D_next = A
    return int(A_next), int(B_next), int(C_next), int(D_next)


# === 6. EXAMPLE RULE SET 2: Majority Vote Network ===
def example_rules_2(A, B, C, D):
    """
    Majority Vote Network:
    - Each node takes the majority of its neighbors.
    """
    A_next = (B and C) or (B and D) or (C and D)
    B_next = (A and C) or (A and D) or (C and D)
    C_next = (A and B) or (A and D) or (B and D)
    D_next = (A and B) or (A and C) or (B and C)
    return int(A_next), int(B_next), int(C_next), int(D_next)


# === 7. EXAMPLE RULE SET 3: Random Boolean Network ===
def example_rules_3(A, B, C, D):
    A_next = (A and (not C)) or C
    B_next = (not C) or (C and D)
    C_next = B or (not D)
    D_next = A and B
    return int(A_next), int(B_next), int(C_next), int(D_next)

def poster_rules(A, B, C, D):
    A_next = B
    B_next = C
    C_next = D
    D_next = A or C
    return int(A_next), int(B_next), int(C_next), int(D_next)


# === 8. RUNNING THE SIMULATIONS ===
#print("\n=== Original Boolean Network ===")
#generate_truth_table(original_rules)
#detect_attractors(original_rules)
#generate_boolean_network_graph(original_rules, filename='Wiring Verifications/original_network_graph')
#generate_wiring_diagram(original_rules, filename='Wiring Verifications/original_wiring_diagram')

# --- Feedback Loop Network ---
#print("\n=== Feedback Loop Network ===")
#generate_truth_table(example_rules_1)
#detect_attractors(example_rules_1)
#generate_boolean_network_graph(example_rules_1, filename='Wiring Verifications/feedback_loop_graph')
#generate_wiring_diagram(example_rules_1, filename='Wiring Verifications/feedback_loop_wiring')

# --- Feedback Loop Network ---
#print("\n=== Majority Vote Netowrk ===")
#detect_attractors(example_rules_2)
#generate_boolean_network_graph(example_rules_2, filename='Wiring Verifications/majority_vote_graph')
#generate_wiring_diagram(example_rules_2, filename='Wiring Verifications/majority_vote_wiring')

# --- Feedback Loop Network ---
# print("\n=== Random Boolean Netowrk ===")
# generate_truth_table(example_rules_3)
# detect_attractors(example_rules_3)
# generate_boolean_network_graph(example_rules_3, filename='Wiring Verifications/random_network_graph')
# generate_wiring_diagram(example_rules_3, filename='Wiring Verifications/random_network_wiring')

print("\n=== Poster ===")
generate_truth_table(poster_rules)
detect_attractors(poster_rules)
generate_boolean_network_graph(poster_rules, filename='Wiring Verifications/poster_graph')
generate_wiring_diagram(poster_rules, filename='Wiring Verifications/poster_wiring')
