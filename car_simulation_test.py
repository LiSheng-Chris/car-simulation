import unittest
from car_simulation import Car, Field, main
from unittest.mock import patch
from io import StringIO

class TestCar(unittest.TestCase):
    def test_change_direction(self):
        car = Car("TestCar", 0, 0, "N", "F")
        car.change_direction("R")
        self.assertEqual(car.direction, "E")

    def test_move_within_field(self):
        field = Field(5, 5)
        car = Car("TestCar", 2, 2, "N", "F")
        car.move(field)
        self.assertEqual((car.x, car.y), (2, 3))

    def test_move_out_of_bounds(self):
        field = Field(5, 5)
        car = Car("TestCar", 4, 4, "E", "F")
        car.move(field)
        self.assertEqual((car.x, car.y), (4, 4))  # Should not move out of bounds

    def test_execute_commands(self):
        field = Field(5, 5)
        car = Car("TestCar", 0, 0, "N", "F")
        car.execute_commands(field)
        self.assertEqual(car.direction, "N")
        self.assertEqual((car.x, car.y), (0, 1))

    def test_execute_empty_commands(self):
        field = Field(5, 5)
        car = Car("TestCar", 0, 0, "N", "")
        car.execute_commands(field)
        self.assertEqual((car.x, car.y), (0, 0))  # Should not move with empty commands

    def test_get_status(self):
        car = Car("TestCar", 3, 3, "W", "FFL")
        status = car.get_status()
        self.assertEqual(status, "TestCar, (3, 3) W, FFL")

    def test_collide(self):
        car = Car("TestCar", 2, 2, "S", "F")
        car.collid(1, "AnotherCar")
        self.assertTrue(car.collided)
        self.assertEqual(car.step, 1)
        self.assertEqual(car.collided_with, "AnotherCar")

class TestField(unittest.TestCase):
    def test_add_car_within_field(self):
        field = Field(5, 5)
        car = Car("TestCar", 1, 1, "N", "F")
        field.add_car(car)
        self.assertIn(car, field.cars)

    def test_add_car_out_of_bounds(self):
        field = Field(5, 5)
        car = Car("TestCar", 6, 6, "N", "F")
        field.add_car(car)
        self.assertNotIn(car, field.cars)

    def test_add_car_collision(self):
        field = Field(5, 5)
        car1 = Car("Car1", 2, 2, "N", "F")
        car2 = Car("Car2", 2, 2, "S", "F")
        field.add_car(car1)
        field.add_car(car2)
        self.assertNotIn(car2, field.cars)  # Car2 should not be added due to collision

    def test_is_within_field(self):
        field = Field(5, 5)
        self.assertTrue(field.is_within_field(2, 3))
        self.assertFalse(field.is_within_field(6, 6))

class TestCarSimulation(unittest.TestCase):
    @patch("builtins.input", side_effect=["10 10", "1", "A", "1 2 N", "FFRFFFFRRL", "2", "2"])
    def test_simulation_with_single_car(self, mock_input):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()

        output = mock_stdout.getvalue().strip()

        self.assertIn("Your current list of cars are:", output)
        self.assertIn("- A, (1, 2) N, FFRFFFFRRL", output)
        self.assertIn("After simulation, the result is:", output)
        self.assertIn("- A, (5, 4) S", output)

    @patch("builtins.input", side_effect=["10 10", "1", "A", "1 2 N", "FFRFFFFRRL", "1", "B", "7 8 W", "FFLFFFFFFF", "2", "2"])
    def test_simulation_with_multiple_car(self, mock_input):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()

        output = mock_stdout.getvalue().strip()

        self.assertIn("Your current list of cars are:", output)
        self.assertIn("- A, (1, 2) N, FFRFFFFRRL", output)
        self.assertIn("- B, (7, 8) W, FFLFFFFFFF", output)
        self.assertIn("After simulation, the result is:", output)
        self.assertIn("- A, collides with B at (5, 4) at step 7", output)
        self.assertIn("- B, collides with A at (5, 4) at step 7", output)

if __name__ == "__main__":
    unittest.main()
