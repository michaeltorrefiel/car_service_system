import unittest 
from car_api import app
from datetime import datetime

class CarApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        # customer dummy data
        self.test_customer_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700"
        } 
        response = self.app.post("/customers", json=self.test_customer_dummy)
        self.assertEqual(response.status_code, 201)
        self.customer_id = response.get_json()["customer_id"]

        # mechanic dummy data
        self.test_mechanic_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700",
            "other_mechanic_details": "MECHANIC_DEETS_TEST"
        }
        response = self.app.post("/mechanics", json=self.test_mechanic_dummy)
        self.assertEqual(response.status_code, 201)
        self.mechanic_id = response.get_json()["mechanic_id"]

        # car dummy data
        self.test_car_dummy = {
            "plate_number": "PLT_TEST",
            "customer_id": self.customer_id,
            "manufacturer": "MAN_TEST",
            "model": "MOD_TEST",
            "known_issue": "KNOWN_ISS_TEST",
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

    def test_if_table_not_found(self):
        response = self.app.get(f"/motorcyles")
        self.assertEqual(response.status_code, 404)

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

    def test_post_customer(self):
        test_customer_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700"
        } 
        response = self.app.post("/customers", json=test_customer_dummy)
        self.assertEqual(response.status_code, 201)

        response_data = response.get_json()
        # print(response_data)
        self.assertIn("customer_id", response_data)
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "customer added successfully")
        self.assertEqual(response_data["rows_affected"], 1)

        customer_id = response_data["customer_id"]
        self.app.delete(f"/customers/{customer_id}")

    def test_post_mechanic(self):
        test_mechanic_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700",
            "other_mechanic_details": "MECHANIC_DEETS_TEST"
        } 
        response = self.app.post("/mechanics", json=test_mechanic_dummy)
        self.assertEqual(response.status_code, 201)

        response_data = response.get_json()
        # print(response_data)
        self.assertIn("mechanic_id", response_data)
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "mechanic added successfully")
        self.assertEqual(response_data["rows_affected"], 1)

        mechanic_id = response_data["mechanic_id"]
        self.app.delete(f"/mechanics/{mechanic_id}")

    def test_post_car(self):
        test_customer_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700"
        } 
        response = self.app.post("/customers", json=test_customer_dummy)
        self.assertEqual(response.status_code, 201)
        customer_id = response.get_json()["customer_id"]

        test_car_dummy = {
            "plate_number": "PLT_TEST1",
            "customer_id": customer_id,
            "manufacturer": "MAN_TEST",
            "model": "MOD_TEST",
            "known_issue": "KNOWN_ISS_TEST",
            "other_details": "CAR_DEETS_TEST",
        }
        response = self.app.post("/cars", json=test_car_dummy)
        self.assertEqual(response.status_code, 201)

        response_data = response.get_json()
        self.assertIn("plate_number", response_data)
        self.assertEqual(response_data["plate_number"], test_car_dummy["plate_number"])
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "car added successfully")
        self.assertEqual(response_data["rows_affected"], 1)

        plate_number = test_car_dummy["plate_number"]
        self.app.delete(f"/cars/{plate_number}")
        self.app.delete(f"/customers/{customer_id}")

    def test_post_booking(self):
        test_customer_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700"
        } 
        response = self.app.post("/customers", json=test_customer_dummy)
        self.assertEqual(response.status_code, 201)
        customer_id = response.get_json()["customer_id"]

        test_mechanic_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700",
            "other_mechanic_details": "MECHANIC_DEETS_TEST"
        } 
        response = self.app.post("/mechanics", json=test_mechanic_dummy)
        self.assertEqual(response.status_code, 201)
        mechanic_id = response.get_json()["mechanic_id"]

        test_car_dummy = {
            "plate_number": "PLT_TEST2",
            "customer_id": customer_id,
            "manufacturer": "MAN_TEST",
            "model": "MOD_TEST",
            "known_issue": "KNOWN_ISS_TEST",
            "other_details": "CAR_DEETS_TEST",
        }
        response = self.app.post("/cars", json=test_car_dummy)
        self.assertEqual(response.status_code, 201)
        plate_number = response.get_json()["plate_number"]

        test_booking_dummy = {
            "mechanic_id": mechanic_id,
            "customer_id": customer_id,
            "plate_number": plate_number,
            "date_time_of_service": "2024-12-12 12:12:12",
            "payment": "2024"
        }
        response = self.app.post("/bookings", json=test_booking_dummy)
        self.assertEqual(response.status_code, 201)

        response_data = response.get_json()        
        self.assertIn("booking_id", response_data)
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "booking added successfully")
        self.assertEqual(response_data["rows_affected"], 1)

        booking_id = response_data["booking_id"]
        self.app.delete(f"/bookings/{booking_id}")
        self.app.delete(f"/cars/{plate_number}")
        self.app.delete(f"/customers/{customer_id}")
        self.app.delete(f"/mechanics/{mechanic_id}")

    def test_put_customer(self):
        test_customer_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700"
        } 
        response = self.app.post("/customers", json=test_customer_dummy)
        self.assertEqual(response.status_code, 201)
        customer_id = response.get_json()["customer_id"]

        updated_customer_data = {
            "first_name": "UPDATED_FNAME",
            "last_name": "UPDATED_LNAME",
            "contact_number": "09111735811"
        }
        response = self.app.put(f"/customers/{customer_id}", json=updated_customer_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertEqual(response_data["message"], "record updated successfully")
        self.assertEqual(response_data["rows_affected"], 1)

        self.app.delete(f"/customers/{customer_id}")

    def test_put_mechanic(self):
        test_mechanic_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700",
            "other_mechanic_details": "MECHANIC_DEETS_TEST"
        } 
        response = self.app.post("/mechanics", json=test_mechanic_dummy)
        self.assertEqual(response.status_code, 201)
        mechanic_id = response.get_json()["mechanic_id"]

        updated_mechanic_data = {
            "first_name": "UPDATED_FNAME",
            "last_name": "UPDATED_LNAME",
            "contact_number": "09111735811",
            "other_mechanic_details": "UPDATED_MECHANIC_DEETS"
        }
        response = self.app.put(f"/mechanics/{mechanic_id}", json=updated_mechanic_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertEqual(response_data["message"], "record updated successfully")
        self.assertEqual(response_data["rows_affected"], 1)

        self.app.delete(f"/mechanics/{mechanic_id}")

    def test_put_car(self):
        test_customer_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700"
        } 
        response = self.app.post("/customers", json=test_customer_dummy)
        self.assertEqual(response.status_code, 201)
        customer_id = response.get_json()["customer_id"]

        test_car_dummy = {
            "plate_number": "PLT_TEST3",
            "customer_id": customer_id,
            "manufacturer": "MAN_TEST",
            "model": "MOD_TEST",
            "known_issue": "KNOWN_ISS_TEST",
            "other_details": "CAR_DEETS_TEST",
        }
        response = self.app.post("/cars", json=test_car_dummy)
        self.assertEqual(response.status_code, 201)
        plate_number = test_car_dummy["plate_number"]

        updated_car_data = {
            "plate_number": "UPD_PLT",
            "customer_id": customer_id,
            "manufacturer": "UPDATED_MAN",
            "model": "UPDATED_MOD",
            "known_issue": "UPDATED_KNOWN_ISS",
            "other_details": "UPDATED_CAR_DEETS",
        }
        response = self.app.put(f"/cars/{plate_number}", json=updated_car_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertEqual(response_data["message"], "record updated successfully")
        self.assertEqual(response_data["rows_affected"], 1)

        self.app.delete(f"/cars/{plate_number}")
        self.app.delete(f"/customers/{customer_id}")

    def test_put_booking(self):
        test_customer_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700"
        } 
        response = self.app.post("/customers", json=test_customer_dummy)
        self.assertEqual(response.status_code, 201)
        customer_id = response.get_json()["customer_id"]

        test_mechanic_dummy = {
            "first_name": "FNAME_TEST",
            "last_name": "LNAME_TEST",
            "contact_number": "09000735700",
            "other_mechanic_details": "MECHANIC_DEETS_TEST"
        } 
        response = self.app.post("/mechanics", json=test_mechanic_dummy)
        self.assertEqual(response.status_code, 201)
        mechanic_id = response.get_json()["mechanic_id"]

        test_car_dummy = {
            "plate_number": "PLT_TEST4",
            "customer_id": customer_id,
            "manufacturer": "MAN_TEST",
            "model": "MOD_TEST",
            "known_issue": "KNOWN_ISS_TEST",
            "other_details": "CAR_DEETS_TEST",
        }
        response = self.app.post("/cars", json=test_car_dummy)
        self.assertEqual(response.status_code, 201)
        plate_number = test_car_dummy["plate_number"]

        test_booking_dummy = {
            "mechanic_id": mechanic_id,
            "customer_id": customer_id,
            "plate_number": plate_number,
            "date_time_of_service": "2024-12-12 12:12:12",
            "payment": "2024"
        }
        response = self.app.post("/bookings", json=test_booking_dummy)
        self.assertEqual(response.status_code, 201)
        booking_id = response.get_json()["booking_id"]

        updated_booking_data = {
            "date_time_of_service": "2025-12-12 12:12:12",
            "payment": "2025"
        }
        response = self.app.put(f"/bookings/{booking_id}", json=updated_booking_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertEqual(response_data["message"], "record updated successfully")
        self.assertEqual(response_data["rows_affected"], 1)

        self.app.delete(f"/bookings/{booking_id}")
        self.app.delete(f"/cars/{plate_number}")
        self.app.delete(f"/mechanics/{plate_number}")
        self.app.delete(f"/customers/{customer_id}")

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