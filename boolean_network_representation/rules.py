class RuleLoader:
    def __init__(self, entity_count):
        """
        Blueprint for rule management.
        """
        self.entity_count = entity_count
        self.rules = [None] * self.entity_count  # Initialise empty rules list

    def load_rules(self, rule_source="gui"):
        """
        Loads rules from a specified source.
        """
        if rule_source == "gui":
            return self.load_from_gui()
        elif rule_source == "manual":
            return self.rules
        else:
            raise ValueError("Unsupported rule source")

    def set_rule(self, entity_index, rule_function):
        """
        Sets the rule for a specific entity.
        """
        if not (0 <= entity_index < self.entity_count):
            raise IndexError("Entity index out of range")

        self.rules[entity_index] = rule_function

    def load_from_gui(self):
        print("Not implemented")
        return self.rules

    def clear_rules(self):
        """
        Clears all current rules, resetting to None.
        """
        self.rules = [None] * self.entity_count


class TruthTableToRules:
    """Converts a truth table to Boolean rule expressions (Sum of Products form)."""

    @staticmethod
    def convert(truth_table, entities):
        rules = {}
        for i, entity in enumerate(entities):
            terms = []
            for input_state, output_state in truth_table.items():
                if output_state[i] == 1:  # If the entity's next state is 1
                    term = []
                    for j, val in enumerate(input_state):
                        if val == "0":
                            term.append(f"NOT {entities[j]}")
                        else:
                            term.append(entities[j])
                    terms.append(f"({' AND '.join(term)})")
            rules[entity] = " OR ".join(terms) if terms else "0"
        return rules
