# Mergington High School Activities Project

This project is a small FastAPI application plus a static frontend for managing extracurricular activity registration at Mergington High School.

## Project Overview

The application helps students browse activities, register for open spots, and review who is already participating. The backend exposes a simple in-memory API, while the frontend renders activity cards and signup details in the browser.

## Core Capabilities

- List available extracurricular activities
- Show current participants for each activity
- Register students for activities
- Unregister participants from an activity
- Validate registration flows with automated tests

## Architecture Summary

- Backend: FastAPI application in [src/app.py](../src/app.py)
- Frontend: Static assets in [src/static/index.html](../src/static/index.html), [src/static/app.js](../src/static/app.js), and [src/static/styles.css](../src/static/styles.css)
- Tests: Pytest-based backend coverage in [tests/test_app.py](../tests/test_app.py)

## Running the Project

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the app:

   ```bash
   python src/app.py
   ```

3. Open the API documentation:

   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## OctoAcme Project Management Process Overview

OctoAcme uses a lightweight delivery process centered on short feedback loops. Work starts from a clearly scoped issue, moves through implementation in a feature branch, and is validated with focused tests before review.

Planning happens before larger changes so requirements, testing approach, and constraints are explicit early. Implementation is then handled incrementally, with fast checks to confirm each change works as intended.

Before merging, changes are summarized in a pull request, linked back to the originating issue, and reviewed by a teammate. This keeps execution traceable from request to validation to approval while still allowing the team to move quickly.