# NOVA API

A small FastAPI service with MongoDB-backed user registration and login.

## Setup

1. Install Python 3.10 or newer and MongoDB.
2. From the project root, install the app and test dependencies:

   ```powershell
   python -m pip install -e ".[test]"
   ```

3. Start MongoDB locally, then run the API:

   ```powershell
   uvicorn app.main:app --app-dir src --reload
   ```

   Set `MONGODB_URI` if MongoDB is running at a different address. The default is
   `mongodb://localhost:27017/`.

4. Open <http://127.0.0.1:8000/docs> to try the API. Both `/register` and
   `/login` accept `username` and `password` as form fields.

## Run tests

```powershell
python -m pytest
```
