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
