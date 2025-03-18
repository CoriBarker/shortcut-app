# Stripe Analytics Dashboard

A full-stack web application that provides detailed analytics and visualizations for your Stripe payment data. Track your sales, analyze trends, and gain insights into your business performance through beautiful graphs and comprehensive statistics.

## Features

- **User Authentication**
  - Secure signup and login system
  - JWT-based authentication
  - Protected routes and API endpoints

- **Stripe Integration**
  - Connect your Stripe account securely
  - Real-time data synchronization
  - Historical data import

- **Analytics Dashboard**
  - Sales overview and trends
  - Revenue analytics
  - Customer insights
  - Payment success rates
  - Refund tracking
  - Custom date range filtering

- **Visualization**
  - Interactive charts and graphs
  - Daily/Weekly/Monthly/Yearly views
  - Revenue breakdown by product
  - Geographic sales distribution
  - Customer retention metrics

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- JWT Authentication
- Stripe API Integration

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Chart.js/D3.js for visualizations
- JWT Authentication

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL
- Stripe Account

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database and Stripe API credentials
   ```

5. Initialize the database:
   ```bash
   python init_db.py
   ```

6. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URLs and public keys
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## API Documentation

The API documentation is available at `/docs` or `/redoc` when running the backend server.

### Key Endpoints
- `/api/signup` - Create a new user account
- `/api/login` - Authenticate user and get JWT token
- `/api/me` - Get current user information
- `/api/stripe/connect` - Connect Stripe account
- `/api/stripe/analytics` - Get analytics data
- `/api/stripe/transactions` - Get transaction history

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Security

- All sensitive data is encrypted
- Stripe API keys are stored securely
- JWT tokens for authentication
- CORS protection
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Stripe API Documentation
- FastAPI Documentation
- Next.js Documentation 