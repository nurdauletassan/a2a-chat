# A2A Assistant Project

This project implements an Assistant-to-Assistant (A2A) interaction system using Google's Gemini and OpenAI's GPT models. It features a FastAPI backend, React frontend, and uses Celery with Redis for task scheduling.

## Project Structure

```
project/
├── backend/           # FastAPI backend
├── frontend/         # React frontend
├── docs/            # Documentation
└── scripts/         # Deployment scripts
```

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker and Docker Compose
- Google Gemini API key
- OpenAI API key

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create and configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. Start the development environment:
   ```bash
   docker compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Deployment to DigitalOcean Droplet

1. Create a new Droplet on DigitalOcean (Ubuntu 22.04 recommended)

2. SSH into your Droplet:
   ```bash
   ssh root@your-droplet-ip
   ```

3. Run the deployment script:
   ```bash
   curl -sSL https://raw.githubusercontent.com/your-repo/main/scripts/deploy.sh | bash
   ```

4. Configure your domain (optional):
   - Point your domain to the Droplet's IP address
   - Update the Nginx configuration with your domain
   - (Optional) Set up Let's Encrypt for HTTPS

## Features

- A2A Interaction: Combines responses from Gemini and OpenAI
- Daily Timestamp Task: Automatically logs timestamps at midnight
- Modern React Frontend: Clean and responsive UI
- Scalable Backend: FastAPI with Celery for async tasks
- Docker Support: Easy deployment and scaling

## API Endpoints

- `POST /api/a2a`: Send prompts for A2A interaction
  ```json
  {
    "prompt": "Your question or prompt here"
  }
  ```

## Development

### Backend Development

1. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Development

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 