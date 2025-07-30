"""Script to run the ALOHA simulation for different loads and plot the throughput vs. utilization."""

from models.aloha import main as aloha
from matplotlib import pyplot as plt

ARRIVAL_RATE_PER_USER = 0.001 # Packets per second per user
PACKET_DURATION = 1.0 # Duration of a packet in seconds
SIMULATION_DURATION = 50_000 # Total simulation time in seconds

utilization = []
throughput = []
ratio_in_successful_transmissions = []
ratio_in_collisions = []
ratio_channel_idle = []

for num_users in range(50, 2001, 50):
    print(f"Running simulation with {num_users} users...")
    result = aloha(
        num_users=num_users,
        arrival_rate_per_user=ARRIVAL_RATE_PER_USER,
        packet_duration=PACKET_DURATION,
        simulation_duration=SIMULATION_DURATION,
        print_stats=False
    )

    utilization.append(result["total_utilization"])
    throughput.append(result["ratio_in_successful_transmissions"])
    ratio_in_successful_transmissions.append(result["ratio_in_successful_transmissions"])
    ratio_in_collisions.append(result["ratio_in_collisions"])
    ratio_channel_idle.append(result["ratio_channel_idle"])

# Plotting the results: Utilization vs. Throughput
plt.figure()
plt.plot(utilization, throughput, marker='o', linestyle='-')
plt.xlabel("Utilization")
plt.ylabel("Throughput")
plt.title("Aloha Protocol: Throughput vs. Utilization")
plt.grid()
plt.savefig("aloha_throughput.png")

# Plotting the ratios in a stacked line chart
plt.figure()
plt.stackplot(utilization,
               ratio_in_successful_transmissions,
               ratio_in_collisions,
               ratio_channel_idle,
               labels=['Successful Transmissions', 'Collisions', 'Channel Idle'],
               colors=['#76c7c0', '#ff6f61', '#d3d3d3'])
plt.xlabel("Utilization")
plt.ylabel("Ratio")
plt.title("Aloha Protocol: Ratios of Successful Transmissions, Collisions, and Idle Time")
plt.legend(loc='upper left')
plt.grid()
plt.savefig("aloha_channel_occupation.png")
