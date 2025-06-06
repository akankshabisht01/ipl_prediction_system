# IPL Match Prediction System

A modern web application that predicts IPL match outcomes using machine learning. The system provides real-time win probability predictions based on match conditions and historical data.

## Features

- 🎯 Real-time match predictions
- 📊 Interactive statistics and visualizations
- 🏏 Support for all IPL teams and venues
- 🌙 Dark/Light mode support
- 📱 Responsive design for all devices
- 🔄 Live match state updates

## Tech Stack

### Frontend
- Next.js 14
- React
- Tailwind CSS
- TypeScript
- Chart.js for visualizations

### Backend
- FastAPI
- Python
- Scikit-learn
- Pandas
- NumPy

## Prerequisites

- Node.js 18+ 
- Python 3.8+
- npm or yarn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/ipl-prediction.git
cd ipl-prediction
```

2. Install frontend dependencies:
```bash
npm install
# or
yarn install
```

3. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

## Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. In a new terminal, start the frontend development server:
```bash
npm run dev
# or
yarn dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
ipl_prediction/
├── backend/
│   ├── main.py
│   └── ipl_prediction_model.pkl
├── src/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── predict/
│   │   ├── stats/
│   │   ├── about/
│   │   └── contact/
│   └── components/
│       ├── layout/
│       ├── home/
│       └── predict/
├── public/
│   └── images/
└── package.json
```

## API Endpoints

- `POST /predict`: Get match prediction probabilities
  - Input: Match state (teams, venue, runs, wickets, etc.)
  - Output: Win probabilities for both teams

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- IPL data sources
- Machine learning model contributors
- Open source community
