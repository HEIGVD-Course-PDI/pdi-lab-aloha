"""SimPy model to simulate a user that generates packets and send them to a Aloha channel"""



class User:
    """A user that sends packets to the channel."""


    def __init__(self, env, channel, packets_per_second, packet_duration):
        """Initialize the user."""
        self.env = env
        self.channel = channel
        self.packets_per_second = packets_per_second
        self.packet_duration = packet_duration


    def generate_packets(self):
        """Generate packets and send them to the channel."""
        while True:
            # 1. Compute the interarrival time based on the packet arrival rate.
            # 2. Wait for the interarrival time
            # 3. Send the packet to the channel and **wait** until it is processed.

            # ******** Add your code here ********
