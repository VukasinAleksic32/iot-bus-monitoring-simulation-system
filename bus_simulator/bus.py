import time
import random

USED_LINES = set()


class Bus:
    def __init__(self, bus_id):
        self.id = bus_id

        # Line info
        self.line_number = self._generate_unique_line()
        self.line_name = f"Line {self.line_number}"

        # Passenger counters
        self.entered = 0
        self.exited = 0

        # Real-time occupancy
        self.inside = 0

        # Capacity
        self.capacity = random.choice([30, 50, 70])

        # Demand profile
        self.demand_factor = random.uniform(0.6, 1.6)

        # State machine
        self.state = "TRAVEL"
        self.state_timer = time.time()

        # Route
        self.current_stop = 0
        self.stop_count = random.randint(8, 15)

        # Timing
        self.travel_time = random.uniform(12, 25)
        self.min_stop_time = random.uniform(6, 10)
        self.rest_time = random.uniform(30, 90)

        # Queues
        self.boarding_queue = 0
        self.exit_queue = 0
        self.terminal_waiting_queue = 0

        # Individual passenger delays
        self.next_board_time = time.time()
        self.next_exit_time = time.time()

    # Unique line generator
    def _generate_unique_line(self):
        while True:
            line = random.randint(1, 99)
            if line not in USED_LINES:
                USED_LINES.add(line)
                return line

    # Simulation step
    def step(self):
        now = time.time()

        # Travel
        if self.state == "TRAVEL":
            if now - self.state_timer >= self.travel_time:
                self.state = "STOP"
                self.state_timer = now
                self.current_stop += 1

                # Terminal stop
                if self.current_stop >= self.stop_count:
                    self.current_stop = self.stop_count

                    if self.inside > 0:
                        self.exit_queue += self.inside

                    self.boarding_queue = 0

                    # People waiting at terminal
                    terminal_demand = int(
                        random.randint(8, 20) * self.demand_factor
                    )
                    self.terminal_waiting_queue += terminal_demand

                # Normal stop
                else:
                    # Exit logic
                    if self.inside > 0:
                        occupancy_ratio = self.inside / self.capacity
                        base_exit = random.randint(1, 4)
                        crowd_exit = int(
                            occupancy_ratio * random.randint(6, 12)
                        )

                        if self.demand_factor > 1.2:
                            crowd_exit = int(crowd_exit * 0.6)

                        exit_group = random.randint(
                            base_exit,
                            base_exit + crowd_exit
                        )

                        self.exit_queue += min(exit_group, self.inside)

                    # Boarding logic
                    free_space = self.capacity - self.inside
                    if free_space > 0:
                        base_board = random.randint(3, 8)
                        demand_board = int(base_board * self.demand_factor)

                        if self.inside / self.capacity < 0.8:
                            demand_board += random.randint(0, 6)

                        self.boarding_queue += min(demand_board, free_space)

        # Stop
        elif self.state == "STOP":

            # Exit has priority
            if self.exit_queue > 0 and now >= self.next_exit_time:
                self.exited += 1
                self.exit_queue -= 1
                self.inside -= 1
                self.next_exit_time = now + random.uniform(0.4, 1.1)

            # Board only if no one is exiting
            elif (
                self.exit_queue == 0
                and self.boarding_queue > 0
                and self.inside < self.capacity
                and now >= self.next_board_time
            ):
                self.entered += 1
                self.boarding_queue -= 1
                self.inside += 1
                self.next_board_time = now + random.uniform(0.9, 2.2)

            stop_elapsed = now - self.state_timer

            # Terminal → Rest
            if self.current_stop == self.stop_count:
                if self.exit_queue == 0:
                    self.state = "REST"
                    self.state_timer = now
                    self.rest_time = random.uniform(30, 90)

            # Normal stop → Travel
            elif (
                stop_elapsed >= self.min_stop_time
                and self.exit_queue == 0
                and self.boarding_queue == 0
            ):
                self.state = "TRAVEL"
                self.state_timer = now
                self.travel_time = random.uniform(12, 25)
                self.min_stop_time = random.uniform(6, 10)

        # Rest
        elif self.state == "REST":
            if now - self.state_timer >= self.rest_time:
                # Reset statistics
                self.entered = 0
                self.exited = 0
                self.inside = 0

                self.boarding_queue = min(
                    self.terminal_waiting_queue,
                    self.capacity
                )
                self.terminal_waiting_queue -= self.boarding_queue
                self.exit_queue = 0

                self.current_stop = 0
                self.state = "TRAVEL"
                self.state_timer = now
                self.travel_time = random.uniform(12, 25)
                self.min_stop_time = random.uniform(6, 10)

        # ---------------- API RETURN ----------------
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
