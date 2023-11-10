class Car:
    def __init__(self, name, x, y, direction, commands):
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.commands = commands
        self.collided = False
        self.step = 0
        self.collided_with = ""

    def change_direction(self, turn):
        directions = ["N", "E", "S", "W"]
        current_index = directions.index(self.direction)

        if turn == "R":
            new_index = (current_index + 1) % len(directions)
        elif turn == "L":
            new_index = (current_index - 1) % len(directions)
        else:
            return

        self.direction = directions[new_index]

    def move(self, field):
        new_x, new_y = self.x, self.y

        if self.direction == "N":
            new_y += 1
        elif self.direction == "S":
            new_y -= 1
        elif self.direction == "E":
            new_x += 1
        elif self.direction == "W":
            new_x -= 1

        # Check for collisions with field bounds
        if not field.is_within_field(new_x, new_y):
            # print(f"Out of bounds! {self.name} cannot move to ({new_x}, {new_y}).")
            return

        self.x, self.y = new_x, new_y
    
    def collid(self, step, collided_with):
        self.collided = True
        self.step = step
        self.collided_with = collided_with
    
    def execute_commands(self, field):
        if not self.commands:
            return
    
        command = self.commands[0]
        if command == "F":
            self.move(field)
        elif command in ["R", "L"]:
            self.change_direction(command)
        self.commands = self.commands[1:]

    def get_status(self):
        status = f"{self.name}, ({self.x}, {self.y}) {self.direction}"
        if self.commands:
            status += f", {self.commands}"
        if self.collided:
            status = f"{self.name}, collides with {self.collided_with} at ({self.x}, {self.y}) at step {self.step}"
        return status

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cars = []

    def add_car(self, car):
        if self.is_within_field(car.x, car.y):
            for other_car in self.cars:
                if other_car.x == car.x and other_car.y == car.y:
                    # print(f"Cannot add {car.name} to the field. Position is taken by another car.")
                    return
            self.cars.append(car)

    def is_within_field(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def simulation(self):
        max_steps = max(len(car.commands) for car in self.cars)

        for step in range(max_steps):
            car_positions = {}
            for car in self.cars:
                if car.commands and not car.collided:
                    car.execute_commands(self)
                position = (car.x, car.y)
                if position in car_positions:
                    car_positions[position].append(car)
                else:
                    car_positions[position] = [car]

            for position in car_positions:
                cars = car_positions[position]
                if len(cars) > 1:
                    for car in cars:
                        if car.collided:
                            continue
                        car.collid(step + 1, ",".join(other_car.name for other_car in cars if car != other_car))
                

    def get_car_status(self):
        car_statuses = ["- " + car.get_status() for car in self.cars]
        return "\n".join(car_statuses)

def main():
    print("Welcome to Auto Driving Car Simulation!\n")

    stage = "Initial field"

    while stage is not None:
        match stage:
            case "Initial field":
                try:
                    width_height = input("Please enter the width and height of the simulation field in x y format: ")
                    width, height = map(int, width_height.split())
                    field = Field(width, height)
                    print(f"You have created a field of {width} x {height}.")
                    stage = "Field options"
                except ValueError:
                    print("Invalid input. Please enter valid integers for width and height.")
            
            case "Field options":
                print("Please choose from the following options: ")
                print("[1] Add a car to field")
                print("[2] Run simulation")
                choice = input("")
                
                if choice == "1":
                    stage = "Add car"
                elif choice == "2":
                    stage = "Simulation"
                else:
                    print("Invalid input.")
            
            case "Add car":
                try:
                    name = input("Please enter the name of the car: ")
                    initial_position = input(f"Please enter the initial position of car {name} in x y Direction format: ")
                    commands = input(f"Please enter the commands for car {name}: ")
                    x, y, direction = initial_position.split()
                    car = Car(name, int(x), int(y), direction, commands)
                    field.add_car(car)
                    if len(field.cars):
                        print("Your current list of cars are: ")
                        print(field.get_car_status())
                    stage = "Field options"
                except ValueError:
                    print("Invalid input. Please enter valid integers for initial position.")
                    stage = "Field options"

            case "Simulation":
                field.simulation()
                if len(field.cars):
                    print("After simulation, the result is: ")
                    print(field.get_car_status())
                stage = "Simulation finished"

            case "Simulation finished":
                print("Please choose from the following options: ")
                print("[1] Start over")
                print("[2] Exit")
                choice = input("")
                
                if choice == "1":
                    stage = "Initial field"
                elif choice == "2":
                    stage = None
                else:
                    print("Invalid input.")

            case _:
                stage = None
    
    print("Thank you for running the simulation. Goodbye!")

if __name__ == "__main__":
    main()
