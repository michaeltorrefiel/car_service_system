# Car Service System

## Description
A simple implementation of a Car Service System. Here, users can see the interaction between the different elements that make up this business. The relationships of mechanics, customers, cars, and bookings are will be demonstrated here.

## Installation
```bash
pip install -r requirements.txt
```
## Configuration
Environment variables needed:

- **FLASK_APP**: `app.py`
- **DATABASE_URL**: `michaeltorrefiel.mysql.pythonanywhere-services.com`
- **USER**: `michaeltorrefiel`
- **PASSWORD**: `root1234`
- **DATABASE**: `michaeltorrefiel$car_service`
- **SECRET_KEY**: `secret_key`

## API Endpoints (markdown table)


| Endpoint                       | Method | Description                |
|--------------------------------|--------|----------------------------|
| `/login`                       | POST   | Get token                  |
| `/protected`                   | GET    | Verify token               |
| `/`                            | GET    | Home page                  |
| `/<table>`                     | GET    | Get records for `<table>`  |
| `/<table>/<int:id>`            | GET    | Get a specific record      |
| `/cars/<plate_number>`         | GET    | Get a specific car record  |
| `/<table>`                     | POST   | Add record for `<table>`   |
| `/<table>/<int:id>`            | PUT    | Edit a record              |
| `/cars/<plate_number>`         | PUT    | Edit a car record          |
| `/<table>/<int:id>`            | DELETE | Delete a record            |
| `/cars/<plate_number>`         | DELETE | Delete a car record        |
| `/mechanics/schedule/<int:id>` | GET    | List mechanic schedule     |
| `/cars/details/<plate_number>` | GET    | List car details           |
| `/customers/bills/<int:id>`    | GET    | List customer bills        |

## Testing
```bash
 Run "python car_api_tests.py"
```
 Make sure that app.py and car_api_tests.py are on the same directory

## Note
- `local_app.py` is the file I originally used for local testing.
- `car_api_tests.py` tests the `local_app.py`.
- `app.py` is the deployed app with a few changes in the code.

