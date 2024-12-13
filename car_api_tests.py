import unittest 
from car_api import app
from datetime import datetime

class CarApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        # customer dummy data
        self.test_customer_dummy = {
            "first_name": "CUSTOMER_TEST",
            "last_name": "CUSTOMER_TESTER",
            "contact_number": "09000735700"
        } 
        response = self.app.post("/customers", json=self.test_customer_dummy)
        self.assertEqual(response.status_code, 201)
        self.customer_id = response.get_json()["customer_id"]

        # mechanic dummy data
        self.test_mechanic_dummy = {
            "first_name": "MECHANIC_TEST",
            "last_name": "MECHANIC_TESTER",
            "contact_number": "09110735701",
            "other_mechanic_details": "TEST TEST TEST"
        }
        response = self.app.post("/mechanics", json=self.test_mechanic_dummy)
        self.assertEqual(response.status_code, 201)
        self.mechanic_id = response.get_json()["mechanic_id"]

        # car dummy data
        self.test_car_dummy = {
            "plate_number": "CAR_TEST",
            "customer_id": self.customer_id,
            "manufacturer": "CAR_MAN_TEST",
            "model": "CAR_MOD_TEST",
            "known_issue": "CAR_KNOW_ISS_TEST",
            "other_details": "CAR_DEETS_TEST",
        }
        response = self.app.post("/cars", json=self.test_car_dummy)
        self.assertEqual(response.status_code, 201)
        self.plate_number = response.get_json()["plate_number"]

        # booking dummy data
        self.test_booking_dummy = {
            "mechanic_id": self.mechanic_id,
            "customer_id": self.customer_id,
            "plate_number": self.plate_number,
            "date_time_of_service": "2024-12-12 12:12:12",
            "payment": "2024"
        }
        response = self.app.post("/bookings", json=self.test_booking_dummy)
        self.assertEqual(response.status_code, 201)
        self.booking_id = response.get_json()["booking_id"]

    def tearDown(self):
        self.app.delete(f"/bookings/{self.booking_id}")
        self.app.delete(f"/cars/{self.plate_number}")
        self.app.delete(f"/customers/{self.customer_id}")
        self.app.delete(f"/mechanics/{self.mechanic_id}")

    def test_1_get_customer(self):
        response = self.app.get(f"/customers/{self.customer_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        # print(data)
        self.assertEqual(data[0]["first_name"], self.test_customer_dummy["first_name"])
        self.assertEqual(data[0]["last_name"], self.test_customer_dummy["last_name"])
        self.assertEqual(data[0]["contact_number"], self.test_customer_dummy["contact_number"])

    def test_1_get_mechanic(self):
        response = self.app.get(f"/mechanics/{self.mechanic_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        # print(data)
        self.assertEqual(data[0]["first_name"], self.test_mechanic_dummy["first_name"])
        self.assertEqual(data[0]["last_name"], self.test_mechanic_dummy["last_name"])
        self.assertEqual(data[0]["contact_number"], self.test_mechanic_dummy["contact_number"])
        self.assertEqual(data[0]["other_mechanic_details"], self.test_mechanic_dummy["other_mechanic_details"])

    def test_1_get_car(self):
        response = self.app.get(f"/cars/{self.plate_number}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        # print(data)
        self.assertEqual(data[0]["customer_id"], self.test_car_dummy["customer_id"])
        self.assertEqual(data[0]["manufacturer"], self.test_car_dummy["manufacturer"])
        self.assertEqual(data[0]["model"], self.test_car_dummy["model"])
        self.assertEqual(data[0]["known_issue"], self.test_car_dummy["known_issue"])
        self.assertEqual(data[0]["other_details"], self.test_car_dummy["other_details"])
    
    def test_1_get_booking(self):
        response = self.app.get(f"/bookings/{self.booking_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        # print(data)
        self.assertEqual(data[0]["mechanic_id"], self.test_booking_dummy["mechanic_id"])
        self.assertEqual(data[0]["customer_id"], self.test_booking_dummy["customer_id"])
        self.assertEqual(data[0]["plate_number"], self.test_booking_dummy["plate_number"])

        # revert jsonify datetime format to sql datetime format
        date_obj = datetime.strptime(data[0]["date_time_of_service"], "%a, %d %b %Y %H:%M:%S GMT")
        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(formatted_date, self.test_booking_dummy["date_time_of_service"])

        self.assertEqual(data[0]["payment"], self.test_booking_dummy["payment"])

    def test_2_delete_record(self):
        # delete test for bookings
        response = self.app.delete(f"/bookings/{self.booking_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("record deleted successfully", response.get_json()["message"])

        get_response = self.app.get(f"/bookings/{self.booking_id}")
        self.assertEqual(get_response.status_code, 404)

        # delete test for cars 
        response = self.app.delete(f"/cars/{self.plate_number}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("record deleted successfully", response.get_json()["message"])

        get_response = self.app.get(f"/cars/{self.plate_number}")
        self.assertEqual(get_response.status_code, 404)

        # delete test for customers
        response = self.app.delete(f"/customers/{self.customer_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("record deleted successfully", response.get_json()["message"])

        get_response = self.app.get(f"/customers/{self.customer_id}")
        self.assertEqual(get_response.status_code, 404)

        # delete test for mechanics
        response = self.app.delete(f"/mechanics/{self.mechanic_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("record deleted successfully", response.get_json()["message"])

        get_response = self.app.get(f"/mechanics/{self.mechanic_id}")
        self.assertEqual(get_response.status_code, 404)

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