import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class PetriNet:
    def __init__(self):
        self.places = {}
        self.transitions = {}

    def add_place(self, place_id, tokens=0):
        self.places[place_id] = tokens

    def add_transition(self, transition_id, inputs, outputs, rate):
        self.transitions[transition_id] = {'inputs': inputs, 'outputs': outputs, 'rate': rate}

    def is_enabled(self, transition_id):
        transition = self.transitions[transition_id]
        for place, weight in transition['inputs'].items():
            if self.places.get(place, 0) < weight:
                return False
        return True

    def fire_transition(self, transition_id):
        if not self.is_enabled(transition_id):
            return False

        for place, weight in self.transitions[transition_id]['inputs'].items():
            self.places[place] -= weight

        for place, weight in self.transitions[transition_id]['outputs'].items():
            self.places[place] += weight

        return True

    def get_marking(self):
        return self.places

    def plot_petri_net(self):
        G = nx.DiGraph()

        # Ajout des places (cercles)
        for place in self.places:
            G.add_node(place, type="place")

        # Ajout ds transitions (rectangles)
        for transition in self.transitions:
            G.add_node(transition, type="transition")

        # Ajouts des arcs (flèches)
        for transition_id, arcs in self.transitions.items():
            for place, weight in arcs['inputs'].items():
                G.add_edge(place, transition_id)
            for place, weight in arcs['outputs'].items():
                G.add_edge(transition_id, place)

        node_colors = []
        for node, attr in G.nodes(data=True):
            if attr["type"] == "place":
                node_colors.append("lightblue")
            else:
                node_colors.append("lightgreen")

        # Plot le graphe
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G, seed=42)  # Positioning nodes for visualization
        nx.draw(
            G, pos, with_labels=True, node_size=3000, node_color=node_colors,
            font_size=10, font_color="black", edge_color="gray"
        )

        # Legende
        legend_labels = {
            "Place (state)": "lightblue",
            "Transition": "lightgreen"
        }
        for label, color in legend_labels.items():
            plt.plot([], [], marker='o', color=color, label=label, markersize=10, linestyle='')
        plt.legend(loc='best')

        plt.title("Petri Net Visualization")
        plt.show()

    def simulate(self, max_steps=100):
        time = 0
        failure_count = 0
        while max_steps > 0:
            enabled_transitions = [(t_id, t['rate']) for t_id, t in self.transitions.items() if self.is_enabled(t_id)]

            if not enabled_transitions:
                break

            # Select the next transition to fire based on rates
            rates = [rate for _, rate in enabled_transitions]
            total_rate = sum(rates)
            if total_rate == 0:
                break

            # Compute the time to the next event
            time_to_next_event = np.random.exponential(1 / total_rate)
            time += time_to_next_event

            # Select which transition fires
            probabilities = [rate / total_rate for rate in rates]
            selected_transition = np.random.choice([t_id for t_id, _ in enabled_transitions], p=probabilities)

            # Fire the selected transition
            self.fire_transition(selected_transition)

            # Increment failure count if system failure occurs
            if selected_transition.startswith("f"):
                failure_count += 1

            # Check if system failure is reached
            if self.places.get("F", 0) > 0:
                return time, failure_count

            max_steps -= 1

        return time, failure_count  # Returns time until failure and failure count

    def mc_simu(self, n_simulations=1000, max_steps=100):
        total_failures = 0
        total_time = 0

        for _ in range(n_simulations):
            self.places = {"W1": 1, "W2": 0, "F1": 0, "F2": 0, "S2": 1, "F": 0}
            time, failure_count = self.simulate(max_steps=max_steps)
            total_failures += failure_count
            total_time += time

        avg_failures = total_failures / n_simulations
        avg_time = total_time / n_simulations
        return avg_failures, avg_time

    def mttf(self, n_simulations=1000):
        total_time_to_failure = 0

        for _ in range(n_simulations):
            self.places = {"W1": 1, "W2": 0, "F1": 0, "F2": 0, "S2": 1, "F": 0}
            time_to_failure, _ = self.simulate()
            total_time_to_failure += time_to_failure

        return total_time_to_failure / n_simulations

    def reliability(self, time_points, n_simulations=1000):
        reliability = []

        for t in time_points:
            successes = 0

            for _ in range(n_simulations):
                self.places = {"W1": 1, "W2": 0, "F1": 0, "F2": 0, "S2": 1, "F": 0}
                time_to_failure, _ = self.simulate()

                if time_to_failure > t:
                    successes += 1

            reliability_at_t = successes / n_simulations
            reliability.append(reliability_at_t)

        return reliability


