import time
import random

USED_LINES = set()


class Bus:
    def __init__(self, bus_id):
        self.id = bus_id

        # Line info
        self.line_number = self._generate_unique_line()
        self.line_name = f"Line {self.line_number}"

        # Capacity & demand
        self.capacity = random.choice([30, 50, 70])
        self.demand_factor = random.uniform(0.6, 1.6)

        # State
        self.state = "TRAVEL"
        self.state_timer = time.time()

        # Route
        self.current_stop = 0
        self.stop_count = random.randint(8, 15)

        # Counters (per route)
        self.entered = 0
        self.exited = 0
        self.inside = 0

        # Queues
        self.boarding_queue = 0
        self.exit_queue = 0
        self.terminal_waiting_queue = 0

        # Timing
        self._reset_travel_params()
        self.rest_time = random.uniform(30, 90)

        # Passenger delays
        self.next_board_time = time.time()
        self.next_exit_time = time.time()

    # Utilities

    def _generate_unique_line(self):
        while True:
            line = random.randint(1, 99)
            if line not in USED_LINES:
                USED_LINES.add(line)
                return line

    def _reset_travel_params(self):
        self.travel_time = random.uniform(12, 25)
        self.min_stop_time = random.uniform(6, 10)

    def _reset_route_stats(self):
        self.entered = 0
        self.exited = 0
        self.current_stop = 0

    # Simulation step

    def step(self):
        now = time.time()

        # Travel
        if self.state == "TRAVEL":
            if now - self.state_timer >= self.travel_time:
                self.state = "STOP"
                self.state_timer = now
                self.current_stop += 1

                is_terminal = self.current_stop >= self.stop_count

                if is_terminal:
                    self.current_stop = self.stop_count

                    # Terminal: everyone exits, NO boarding
                    self.exit_queue = self.inside
                    self.boarding_queue = 0

                else:
                    # Normal stop exits
                    if self.inside > 0:
                        occupancy = self.inside / self.capacity
                        self.exit_queue = min(
                            random.randint(1, int(occupancy * 10) + 3),
                            self.inside
                        )

                    # Normal stop boarding
                    free_space = self.capacity - self.inside
                    if free_space > 0:
                        board = int(
                            random.randint(3, 8) * self.demand_factor
                        )
                        self.boarding_queue = min(board, free_space)

        # Stop
        elif self.state == "STOP":

            # Exit first
            if self.exit_queue > 0 and now >= self.next_exit_time:
                self.exit_queue -= 1
                self.exited += 1
                self.inside -= 1
                self.next_exit_time = now + random.uniform(0.4, 1.1)

            # Boarding (only non-terminal or post-rest terminal)
            elif (
                self.exit_queue == 0
                and self.boarding_queue > 0
                and self.inside < self.capacity
                and now >= self.next_board_time
            ):
                self.boarding_queue -= 1
                self.entered += 1
                self.inside += 1
                self.next_board_time = now + random.uniform(0.9, 2.2)

            is_terminal = self.current_stop == self.stop_count
            stop_elapsed = now - self.state_timer

            # Terminal → Rest
            if is_terminal and self.exit_queue == 0 and self.inside == 0:
                self.state = "REST"
                self.state_timer = now
                self.rest_time = random.uniform(30, 90)
                self.terminal_waiting_queue = 0

            # Normal stop → Travel
            elif (
                not is_terminal
                and stop_elapsed >= self.min_stop_time
                and self.exit_queue == 0
                and self.boarding_queue == 0
            ):
                self.state = "TRAVEL"
                self.state_timer = now
                self._reset_travel_params()

        # Rest
        elif self.state == "REST":
            if now - self.state_timer >= self.rest_time:

                # Generate terminal demand AFTER rest
                terminal_demand = int(
                    random.randint(10, 25) * self.demand_factor
                )
                self.terminal_waiting_queue += terminal_demand

                # Prepare boarding for NEW route
                self.boarding_queue = min(
                    self.capacity,
                    self.terminal_waiting_queue
                )
                self.terminal_waiting_queue -= self.boarding_queue

                self._reset_route_stats()
                self.state = "STOP"
                self.state_timer = now

        # API
        return {
            "bus_id": self.id,
            "line_name": self.line_name,
            "line_number": self.line_number,
            "state": self.state,
            "stop": self.current_stop,
            "inside": self.inside,
            "entered": self.entered,
            "exited": self.exited,
            "capacity": self.capacity,
            "boarding_queue": self.boarding_queue,
            "exit_queue": self.exit_queue,
            "terminal_waiting": self.terminal_waiting_queue,
            "timestamp": int(now),
        }
