import numpy as np


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
            # Reset the Petri net to the initial state
            self.places = {"W1": 1, "W2": 0, "F1": 0, "F2": 0, "S2": 1, "F": 0}
            time_to_failure, _ = self.simulate()

            if time_to_failure > t:
                successes += 1

        reliability_at_t = successes / n_simulations
        reliability.append(reliability_at_t)

    return reliability


def calculate_mtbf(petri_net, n_simulations=1000):
    repair_times = []

    for _ in range(n_simulations):
        petri_net.places = {"W1": 1, "W2": 0, "F1": 0, "F2": 0, "S2": 1, "F": 0}
        failure_time, _ = petri_net.simulate()
        repair_time = np.random.exponential(1 / 0.05)  # Assume repair rate of 0.05 (example)
        repair_times.append(failure_time + repair_time)

    mtbf = np.mean(repair_times)
    return mtbf

def calculate_mdt(petri_net, n_simulations=1000):
    down_times = []

    for _ in range(n_simulations):
        repair_time = np.random.exponential(1 / 0.05)  # Assume repair rate of 0.05 (example)
        down_times.append(repair_time)

    mdt = np.mean(down_times)
    return mdt
