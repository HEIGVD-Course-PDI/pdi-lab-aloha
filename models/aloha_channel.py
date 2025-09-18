"""SimPy model to simulate the Aloha protocol"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
@dataclass
class Transmission:
    """Data structure to represent a packet transmission."""
    start_time: float
    end_time: float
    collision: bool = False


# ---------------------------------------------------------------------------
class AlohaChannel:
    """An Aloha channel that can transport packets.

    A user can send packets on the channel using the method `send_packet`.
    If two or more transmissions occur at the same time, a collision occurs.
    The channel processes the packet and records if it was successful or if a collision occurred.

    The channel keeps track of statistics such as number of transmissions, collisions, etc.
    """

    def __init__(self, env, packet_duration):
        """Initialize the Aloha channel."""
        self.env = env
        self.packet_duration = packet_duration
        self.active_transmissions = [] # List of currently active transmissions

        # Statistics
        self.num_all_transmissions = 0 # Total number of transmissions attempted
        self.num_successful_transmissions = 0 # Total number of successful transmissions
        self.num_collisions = 0 # Total number of collisions
        self.time_successful_transmission = 0.0 # Total time spent in successful transmissions
        self.time_channel_idle = 0.0 # Total time the channel is idle
        self.last_transmission_end_time = 0.0 # Helper to calculate idle time


    def send_packet(self):
        """Attempt sending a packet of a given duration.
        
        If there are any other active transmissions, a collision occurs.
        """
        # IMPORTANT: if a new transmission starts exactly when another one ends, let the old one finish processing first
        yield self.env.timeout(0) # Let the other transmissions finish processing

        duration = self.packet_duration
        new_transmission = Transmission(start_time=self.env.now, end_time=self.env.now+duration, collision=False)
        self.active_transmissions.append(new_transmission)

        if len(self.active_transmissions) == 1:
            # There is no other active transmission, i.e., the channel is idle.
            # Record the time since the last transmission as idle time
            self.time_channel_idle += self.env.now - self.last_transmission_end_time
        else:
            # There are other active transmissions. Mark all transmissions as collisions.
            for transmission in self.active_transmissions:
                transmission.collision = True

        # Wait until the transmission is complete and remove it from the active list
        yield self.env.timeout(duration)
        self.active_transmissions.remove(new_transmission)

        # Update the statistics
        self.num_all_transmissions += 1
        if new_transmission.collision:
            self.num_collisions += 1
        else:
            self.time_successful_transmission += duration
            self.num_successful_transmissions += 1
        self.last_transmission_end_time = self.env.now
