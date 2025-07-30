"""SimPy model to simulate the Aloha protocol"""

from dataclasses import dataclass
import simpy

# ---------------------------------------------------------------------------
# CONSTANTS -- adjust as needed
NUM_USERS = 500
ARRIVAL_RATE_PER_USER = 0.001 # Packets per second per user
PACKET_DURATION = 1.0 # Mean duration of a packet in seconds
SIMULATION_DURATION = 500_000 # Total simulation time in seconds


# ---------------------------------------------------------------------------
def user(env, channel, packets_per_second, packet_duration):
    """A user that sends packets to the channel."""
    while True:
        # 1. Compute the interarrival time based on the packet arrival rate.
        # 2. Wait for the interarrival time
        # 3. Send the packet to the channel and wait until it is processed.
        #    Use a constant packet duration for each packet.

        # ******** Add your code here ********



# ---------------------------------------------------------------------------
@dataclass
class Transmission:
    """Data structure to represent a packet transmission."""
    start_time: float
    end_time: float
    collision: bool = False


# ---------------------------------------------------------------------------
class Channel:
    """An Aloha channel that can transport packets.

    A user can send packets on the channel using the method `send_packet`.
    If two or more transmissions occur at the same time, a collision occurs.
    The channel processes the packet and records if it was successful or if a collision occurred.

    The channel keeps track of statistics such as number of transmissions, collisions, etc.
    """

    def __init__(self, env, ):
        self._env = env
        self._active_transmissions = [] # List of currently active transmissions

        # Statistics
        self.num_all_transmissions = 0 # Total number of transmissions attempted
        self.num_successful_transmissions = 0 # Total number of successful transmissions
        self.num_collisions = 0 # Total number of collisions
        self.time_successful_transmission = 0.0 # Total time spent in successful transmissions
        self.time_channel_idle = 0.0 # Total time the channel is idle
        self.last_transmission_end_time = 0.0 # Helper to calculate idle time

    def send_packet(self, duration):
        """Attempt sending a packet of a given duration.
        
        If there are any other active transmissions, a collision occurs.
        """
        # IMPORTANT: if a new transmission starts exactly when another one ends, let the old one finish processing first
        yield self._env.timeout(0) # Let the other transmissions finish processing

        new_transmission = Transmission(start_time=self._env.now, end_time=self._env.now+duration, collision=False)
        self._active_transmissions.append(new_transmission)

        if len(self._active_transmissions) == 1:
            # There is no other active transmission, i.e., the channel is idle.
            # Record the time since the last transmission as idle time
            self.time_channel_idle += self._env.now - self.last_transmission_end_time
        else:
            # There are other active transmissions. Mark all transmissions as collisions.
            for transmission in self._active_transmissions:
                transmission.collision = True

        # Wait until the transmission is complete and remove it from the active list
        yield self._env.timeout(duration)
        self._active_transmissions.remove(new_transmission)

        # Update the statistics
        self.num_all_transmissions += 1
        if new_transmission.collision:
            self.num_collisions += 1
        else:
            self.time_successful_transmission += duration
            self.num_successful_transmissions += 1
        self.last_transmission_end_time = self._env.now


# ============================================================================
def main(num_users, arrival_rate_per_user, packet_duration, simulation_duration, print_stats):
    """Main function to run the Aloha simulation."""

    # Create and run the simulation
    env = simpy.Environment()
    channel = Channel(env) # Aloha transmission channel

    for _ in range(num_users):
        env.process(user(env, channel, arrival_rate_per_user, packet_duration))

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
        print(f"  Total utilization:\t\t\t {total_utilization:.1%}")
        print(f"  Successful transmission:\t\t {successful_transmissions / total_packets:.1%}")
        print(f"  Collisions:\t\t\t\t {collisions / total_packets:.1%}")
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
