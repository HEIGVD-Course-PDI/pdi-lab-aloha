"""Run a simulation of the Aloha protocol using SimPy."""

import simpy
from models.aloha_channel import AlohaChannel
from models.aloha_user import User

# ---------------------------------------------------------------------------
# CONSTANTS -- adjust as needed
NUM_USERS = 100
ARRIVAL_RATE_PER_USER = 0.001 # Packets per second per user
PACKET_DURATION = 1.0 # Mean duration of a packet in seconds
SIMULATION_DURATION = 500_000 # Total simulation time in seconds

# ============================================================================
def main(num_users, arrival_rate_per_user, packet_duration, simulation_duration, print_stats):
    """Main function to run the Aloha simulation."""

    # Create the SimPy environment, the Aloha channel, and the users
    env = simpy.Environment()
    channel = AlohaChannel(env, packet_duration)
    for _ in range(num_users):
        user = User(env, channel, arrival_rate_per_user, packet_duration)
        env.process(user.generate_packets())

    env.run(until=simulation_duration)

    # Compute the statistics
    simulation_end_time = channel.last_transmission_end_time
    total_packets = channel.num_all_transmissions
    total_utilization = num_users * arrival_rate_per_user * packet_duration
    successful_transmissions = channel.num_successful_transmissions
    collisions = channel.num_collisions
    ratio_in_successful_transmissions = channel.time_successful_transmission / simulation_end_time
    ratio_channel_idle = channel.time_channel_idle / simulation_end_time
    ratio_in_collisions = ((simulation_end_time - channel.time_channel_idle - channel.time_successful_transmission)
                            / simulation_end_time)

    if print_stats:
        print("-----------------------------------------------------")
        print("Packet transmission statistics:")
        print(f"  Total packets:\t\t\t {total_packets}")
        print("-----------------------------------------------------")
        print("Channel statistics:")
        print(f"  Total time:\t\t\t\t {simulation_end_time:.0f} seconds")
        print(f"  Time in successful transmissions:\t {ratio_in_successful_transmissions:.1%}")
        print(f"  Time in collisions:\t\t\t {ratio_in_collisions:.1%}")
        print(f"  Time idle:\t\t\t\t {ratio_channel_idle:.1%}")

    return {
        "total_packets": total_packets,
        "total_utilization": total_utilization,
        "successful_transmissions": successful_transmissions,
        "collisions": collisions,
        "ratio_in_successful_transmissions": ratio_in_successful_transmissions,
        "ratio_channel_idle": ratio_channel_idle,
        "ratio_in_collisions": ratio_in_collisions,
        "simulation_end_time": simulation_end_time,
    }

if __name__ == "__main__":
    main(NUM_USERS, ARRIVAL_RATE_PER_USER, PACKET_DURATION, SIMULATION_DURATION, True)
