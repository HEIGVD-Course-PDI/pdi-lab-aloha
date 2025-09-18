Aloha simulation lab solution
=============================

The learning goals of this lab are:

- to understand how to write simulation models with SimPy,
- to learn how to use Python's random number generator to draw numbers from a given distribution,
- to learn how to create traffic sources that generate packets according to a given distribution,
- to understand the performance characteristics of the Aloha protocol.


0 - Introduction
----------------

Aloha is a simple random access protocol for wireless networks. A user can transmit a packet at any time. But if the transmission overlaps with another user's transmission, a collision occurs and both packets are lost. See the Wikipedia article on [Aloha protocol](https://en.wikipedia.org/wiki/Aloha_protocol) for more details.

This protocol is very simple. But as we will see, it has some serious performance issues.


1 - Understand the simulation model
-----------------------------------

File `./models/aloha_user.py`
  : This file contains an (incomplete) implementation of a  `Class User` class that generates packets and sends them to the channel. For each packet, it sends it to the channel and waits for the transmission to complete before sending the next packet. 
  : You will need to complete this method later.

File `./models/aloha_channel.py`
  : This file contains the `Class Channel` that represents the Aloha transmission channel. A user can send packets to the channel using its `send_packet` method. The channel keeps statistics about successful transmissions and collisions. It also measures when the channel is occupied or idle.
  : You do not need to modify this class.

File `/main_aloha.py`
  : The `main` function in this file sets up the simulation environment, creates the channel, and starts all user processes. It runs the simulation for a given duration and prints the statistics at the end.
  : You do not need to modify this function.

#### Todo

- [ ] Read the code in `models/aloha.py` and understand how the simulation works. Try to understand the `Channel.send_packet` method.
- [ ] Answer the questions in the `Questions.md` file.


2 - Implement the packet generation
-----------------------------------

The `User.generate_packets` method should generate packets at a given rate, but it is currently incomplete. You need to implement the simulation model to generate packets.

#### Todo

- [ ] The Python function `numpy.random.exponential` from the Numpy package generates values from an exponential distribution. Test this function with different values of $\lambda$. Do the generated values match your expectations?
- [ ] Implement the packet generation in the `User.generate_packets` method in the file `./models/user.py`. Generate packets with exponential interarrival times. The mean is given by the `packets_per_second` parameter.
- [ ] Run the simulation for different number of users and observe the printed statistics. Do the statistics match your expectations? In particular, check the number of generated packets and the total utilization of the channel.
- [ ] Answer the question in the `Questions.md` file.


3 - Analyze the Aloha protocol
------------------------------

After a simulation, observe the channel utilization, number of collisions and the time in successful transmissions. The time in successful transmissions is the ratio between the time spent transmitting packets without collisions and the total simulation time. It is equivalent to the achieved throughput.

#### Todo

- [ ] Run the simulation for different values of `NUM_USERS`. For which utilization does the throughput (i.e., time in successful transmissions) reach its maximum? What is the maximum throughput?
- [ ] Plot the throughput as a function of the utilization: the script `./optimize_aloha.py` runs the simulation for different values of `NUM_USERS` and collects the statistics. It then plots the throughput as well as the channel utilization. Examine the plot files (`./aloha_throughput.png` and `./aloha_channel_occupation.png`).
- [ ] Answer the question in the `Questions.md` file.


4 - Implement slotted Aloha
---------------------------

As you've seen, the Aloha protocol has a very low throughput, because there are many collisions. There is a variant of Aloha called *slotted Aloha* that improves the throughput. The idea that the time is divided into slots of a fixed duration equal to the packet transmission time. A transmission can only start at the beginning of a slot at and it will fill the entire slot. This reduces the chance of collisions: in normal Aloha, a collision occurs even if two transmissions overlap by a single bit. In slotted Aloha, they overlap completely or not at all. This reduces the chance of collisions and increases the throughput. See the Wikipedia article on [Slotted Aloha](https://en.wikipedia.org/wiki/Slotted_Aloha) for more details.

#### Todo

- [ ] Make a copy of the `./models/aloha_user.py` file and rename it to `./models/slotted_aloha_user.py`. Use the new file for your implementation.
- [ ] Implement slotted Aloha in the `generate_packets` method. The change is very simple: only a single line of code needs to be changed. Instead of generating exponential interarrival times, can you generate a discrete number of time slots to wait before sending the next packet? Each time slot has a duration equal to the packet duration.
- [ ] Make a copy of the `./main_aloha.py` file and rename it to `./main_slotted_aloha.py`. Modify the new file to use the slotted Aloha user class instead of the normal Aloha user class.
- [ ] Run several simulations using the `./main_slotted_aloha.py` script with different numbers of users. Are the number of generated packets correct?
- [ ] Make a copy of the `./optimize_aloha.py` file and rename it to `./optimize_slotted_aloha.py`. Modify the new file to use the `./main_slotted_aloha.py` script instead of the normal Aloha script and plot the results to different files.
- [ ] Answer the question in the `Questions.md` file.


4 - Analyze the slotted Aloha protocol
--------------------------------------

#### Todo

- [ ] Modify the `optimize_aloha.py` script to run the simulation for slotted Aloha and save the plots to different files.
- [ ] Using the `optimize_aloha.py` script, run the simulation for slotted Aloha and observe the throughput. How does it compare to the normal Aloha protocol? Does it reach a higher maximum throughput? At which utilization does it reach this maximum throughput?
- [ ] Answer the question in the `Questions.md` file.

Final checklist
---------------

The last commit before the deadline will be considered as your solution. Make sure that you've completed the following tasks:

- [ ] Answer all questions in the `Questions.md` file.
- [ ] The Aloha model in `models/aloha.py` is complete and runs without errors.
- [ ] You provide a file `models/slotted_aloha.py` that implements the slotted Aloha model. It runs without errors.
- [ ] You have the following plot files: 
  - `throughput.png`,
  - `channel_occupation.png`,
  - `slotted_aloha_throughput.png`, and 
  - `slotted_aloha_channel_occupation.png`.
