# Homework 2 - CS4300/CS5300
## Student Information
**Name:** Mehak Hagemann  
**Course:** CS4300/CS5300
**GitHub Username:** mikki613  




# Movie Theater Booking System  
 Homework 2 using Django + Django REST Framework + Bootstrap

---

## Project Overview

This project is a full-stack Movie Theater Booking System built using Django and Django REST Framework (DRF).

The application provides:

- A RESTful API
- A Bootstrap-based web interface
- Authentication-protected booking
- Unit and integration tests
- BDD testing using Behave

Users can:
- View available movies
- View available seats
- Book seats for a movie
- View their booking history

---

## Repository Structure

This project is located inside the `homework2` directory of the main repository:

cs4300/
└── homework2/
├── manage.py
├── requirements.txt
├── behave.ini
├── bookings/
├── movie_theater_booking/
└── features/


---

##  Database Models

###  Movie
- title
- description
- release_date
- duration (minutes)

###  Seat
- seat_number
- is_booked (boolean)

###  Booking
- movie (ForeignKey)
- seat (OneToOneField)
- user (ForeignKey)
- booking_date

Seats cannot be double-booked.

---

##  API Endpoints

Base URL (local development):

```bash

http://127.0.0.1:3000

```
### Movies
- `GET /api/movies/`
- `POST /api/movies/`
- `GET /api/movies/<id>/`
- `PUT/PATCH/DELETE /api/movies/<id>/`

### Seats
- `GET /api/seats/`
- `POST /api/seats/<id>/book/` *(Authentication required)*

### Bookings
- `GET /api/bookings/` *(Authentication required)*

Booking history only returns the logged-in user's bookings.

---

##  Web Interface Routes

- `/` → Movie list
- `/movies/<id>/book/` → Seat booking
- `/history/` → Booking history
- `/login/`
- `/logout/`

Features:
- Disabled seats once booked
- Success/error alerts
- Authentication required to book seats
- Bootstrap 5 styling

---

## Setup Instructions

### Clone the Repository

```bash

git clone https://github.com/mikki613/cs4300.git

cd cs4300/homework2

```
---

###  Create Virtual Environment

```bash

python3 -m venv hw2_env --system-site-packages
source hw2_env/bin/activate
```

---

###  Install Dependencies

```bash 
pip install -r requirements.txt
```

---

###  Apply Database Migrations

```bash
python3 manage.py migrate

```
---

###  Create Superuser

```bash
python3 manage.py createsuperuser

```
---

###  Run Development Server

```bash 
python3 manage.py runserver 0.0.0.0:3000

```

### Open in browser:

```bash

http://127.0.0.1:3000

``` 

---

##  Testing

### Django Unit & Integration Tests

```bash
python3 manage.py test

``` 

These tests verify:
- API endpoints return correct status codes
- Booking requires authentication
- Seats cannot be double-booked
- Booking history is filtered per user

---

### BDD Testing with Behave

```bash

behave
```

BDD scenario verifies:
- Unauthenticated users cannot access booking history endpoint

---

## Deployment (Render Configuration)

Build Command:

```bash
pip install -r requirements.txt && python manage.py migrate

```

Ensure `ALLOWED_HOSTS` includes:
- DevEdu domain
- localhost
- 127.0.0.1
- testserver

---

##  Security Considerations

- Authentication required for booking
- Booking history restricted per user
- Seat double-booking prevented
- CSRF protection enabled
- Proper ALLOWED_HOSTS configuration

---

##  AI Usage Disclosure

AI tools (ChatGPT) were used to assist with:

- Django project scaffolding
- Debugging configuration issues
- Structuring documentation/Grammar correction

All code was reviewed, tested, and modified to meet assignment requirements.

---

##  Assignment Requirements Covered

- Django project created
- Models implemented
- DRF ViewSets implemented
- REST API endpoints functional
- Bootstrap UI implemented
- Booking logic enforced
- Unit & integration tests implemented
- BDD tests implemented
- Ready for deployment

