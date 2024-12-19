from PetriNet import *
#from PN_RAMS import *

def calculate_failure_events_monte_carlo(petri_net, n_simulations=1000):
    avg_failures, _ = petri_net.mc_simu(n_simulations=n_simulations)
    return avg_failures

petri_net = PetriNet()

# Add places
petri_net.add_place("W1", tokens=1)
petri_net.add_place("W2", tokens=0)
petri_net.add_place("F1", tokens=0)
petri_net.add_place("F2", tokens=0)
petri_net.add_place("S2", tokens=1)
petri_net.add_place("F", tokens=0)

petri_net.add_transition("f1(λ1)", inputs={"W1": 1}, outputs={"F1": 1, "S2": 1}, rate=0.1)
petri_net.add_transition("g1(µ1)", inputs={"S2": 1}, outputs={"W2": 1}, rate=0.05)
petri_net.add_transition("f2(λ2)", inputs={"W2": 1}, outputs={"F2": 1, "F": 1}, rate=0.1)


time_points = np.linspace(0, 100, 50)
reliability = petri_net.reliability(time_points, n_simulations=10000)

mttf = petri_net.mttf(n_simulations=10000)
print(f"Monte Carlo Estimated Mean Time to System Failure (MTTF): {mttf:.2f} time units")

avg_failures = calculate_failure_events_monte_carlo(petri_net, n_simulations=10000)
print(f"Average Number of Failure Events (Monte Carlo): {avg_failures:.2f}")

plt.figure(figsize=(10, 6))
plt.plot(time_points, reliability, label="System Reliability")
plt.xlabel("Time (time units)")
plt.ylabel("Reliability")
plt.title("System Reliability as a Function of Time (Monte Carlo)")
plt.grid(True)
plt.legend()
plt.show()

