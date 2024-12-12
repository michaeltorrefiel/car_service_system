import unittest 
from car_api import app

class CarApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        self.test_customer_dummy = {
            "first_name": "CUSTOMER_TEST",
            "last_name": "CUSTOMER_TESTER",
            "contact_number": "09000735700"
        } 
        response = self.app.post("/customers", json=self.test_customer_dummy)
        # print(response.get_json())
        self.assertEqual(response.status_code, 201)
        self.customer_id = response.get_json()["customer_id"]

        self.test_mechanic_dummy = {
            "first_name": "MECHANIC_TEST",
            "last_name": "MECHANIC_TESTER",
            "contact_number": "09110735701",
            "other_mechanic_details": "TEST TEST TEST"
        }
        response = self.app.post("/mechanics", json=self.test_mechanic_dummy)
        # print(response.get_json())
        self.assertEqual(response.status_code, 201)
        self.mechanic_id = response.get_json()["mechanic_id"]

    def tearDown(self):
        self.app.delete(f"/customers/{self.customer_id}")
        self.app.delete(f"/mechanics/{self.mechanic_id}")

    def test_get_customer(self):
        response = self.app.get(f"/customers/{self.customer_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        # print(data)
        self.assertEqual(data[0]["first_name"], self.test_customer_dummy["first_name"])
        self.assertEqual(data[0]["last_name"], self.test_customer_dummy["last_name"])
        self.assertEqual(data[0]["contact_number"], self.test_customer_dummy["contact_number"])

    def test_get_mechanic(self):
        response = self.app.get(f"/mechanics/{self.mechanic_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        # print(data)
        self.assertEqual(data[0]["first_name"], self.test_mechanic_dummy["first_name"])
        self.assertEqual(data[0]["last_name"], self.test_mechanic_dummy["last_name"])
        self.assertEqual(data[0]["contact_number"], self.test_mechanic_dummy["contact_number"])
        self.assertEqual(data[0]["other_mechanic_details"], self.test_mechanic_dummy["other_mechanic_details"])

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