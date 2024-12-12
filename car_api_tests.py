import unittest 
from car_api import app

class CarApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

        home = """
        <h1>CAR SERVICE SYSTEM</h1>
        <p>tables = ["customers", "mechanics", "cars", "bookings"] </p>
        """
        normalized_response = " ".join(response.data.decode().split())
        normalized_home = " ".join(home.split())
        self.assertEqual(normalized_response, normalized_home)

if __name__ == "__main__":
    unittest.main()