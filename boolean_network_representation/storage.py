import json
import os
import pandas as pd
import random


class BooleanNetworkStorage:
    """Handles loading and saving Boolean Networks in CSV or JSON formats."""

    @staticmethod
    def load_network(filename):
        """Loads a Boolean Network from JSON."""
        filepath = os.path.join("saved_networks", filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Network file '{filename}' not found.")

        with open(filepath, "r") as f:
            return json.load(f)

    @staticmethod
    def save_network(filename, entities, rules, truth_table=None):
        """Saves a Boolean Network in JSON format."""
        data = {
            "entities": entities,
            "rules": rules,
            "truth_table": truth_table
        }
        with open(f"imported_networks/{filename}", "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_csv_as_truth_table(filename):
        """Loads a CSV truth table and returns entities + truth table dictionary."""
        df = pd.read_csv(f"imported_networks/{filename}")
        input_columns = df.columns[:len(df.columns) // 2]
        output_columns = df.columns[len(df.columns) // 2:]

        truth_table = {
            "".join(map(str, row[input_columns].astype(int))): list(row[output_columns])
            for _, row in df.iterrows()
        }
        return list(output_columns), truth_table

    @staticmethod
    def mutate_truth_table(self):
        """Mutates a random value in the truth table and saves as evolved version."""
        from boolean_network_representation.storage import BooleanNetworkStorage

        # Perform mutation
        BooleanNetworkStorage.mutate_truth_table(self.truth_table)

        # Determine the next evolved version number
        network_path = os.path.join("imported_networks", self.name)
        existing_versions = [f for f in os.listdir(network_path) if f.startswith("evolved_v")]
        next_version = len(existing_versions) + 1

        # Save evolved network
        BooleanNetworkStorage.save_network(self.name, self.entities, self.rules, self.truth_table,
                                           evolved_version=next_version)

        print(f"Saved evolved network version: evolved_v{next_version}.json")
