# Shortcut App

A modern web application for managing shortcuts and quick access to frequently used resources.

## Project Structure

```
shortcut-app/
├── backend/           # FastAPI backend
│   ├── main.py       # Main application file
│   ├── models.py     # Database models
│   ├── database.py   # Database configuration
│   ├── test_main.py  # Backend tests
│   └── requirements.txt
└── frontend/         # Next.js frontend
    ├── app/         # App Router pages
    ├── __tests__/   # Frontend tests
    └── package.json
```

## Setup

### Backend Setup

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

4. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

## Testing

### Backend Tests
```bash
cd backend
pytest test_main.py -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Development

- Backend runs on http://localhost:8000
- Frontend runs on http://localhost:3000
- API documentation available at http://localhost:8000/docs

## Features

- User authentication (signup/login)
- Modern, responsive UI
- Secure password handling
- SQLite database for data persistence 