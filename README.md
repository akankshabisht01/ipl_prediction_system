﻿# IPL Match Prediction System

A modern web application that predicts IPL match outcomes using machine learning. The system provides real-time win probability predictions based on match conditions and historical data.

## Features

- 🎯 Real-time match predictions
- 📊 Interactive statistics and visualizations
- 🏏 Support for all IPL teams and venues
- 🌙 Dark/Light mode support
- 📱 Responsive design for all devices
- 🔄 Live match state updates

## Data Science Tools & Technologies Used
- **Python**: Core programming language for data processing and model development.
- **Pandas**: For data manipulation and analysis.
- **NumPy**: For numerical computations.
- **scikit-learn**: For building and evaluating machine learning models.
- **Jupyter Notebook**: For exploratory data analysis and prototyping.
- **Matplotlib & Seaborn**: For data visualization.
- **Flask**: For serving the trained model as a REST API backend.

## Project Workflow
1. **Data Collection & Cleaning**: Gathered IPL match data, cleaned and preprocessed it for analysis.
2. **Exploratory Data Analysis (EDA)**: Explored trends, team stats, and key features influencing match outcomes.
3. **Feature Engineering**: Created relevant features to improve model performance.
4. **Model Training**: Trained various machine learning models (e.g., Logistic Regression, Random Forest) and selected the best-performing one.
5. **Model Evaluation**: Evaluated model accuracy and performance using cross-validation and test data.
6. **Model Serialization**: Saved the final model as a `.pkl` file for deployment.
7. **API Development**: Built a Flask API to serve predictions from the trained model.

## Model Storage with Azure
The trained model file (`ipl_prediction_model.pkl`) is too large to be pushed to GitHub due to repository size limits. To address this, the model is securely stored on **Azure Blob Storage**. The backend fetches the model from Azure during deployment, ensuring efficient and scalable access without exceeding GitHub's file size restrictions.

## Deployment
- **Backend**: Deployed on [Render](https://render.com/) for reliable and scalable API hosting.
- **Frontend**: Deployed on [Vercel](https://vercel.com/).

## Live Demo
Check out the live IPL Match Prediction platform here: [https://ipl-prediction-system-two.vercel.app/](https://ipl-prediction-system-two.vercel.app/)

---
© 2025 IPL Match Prediction. All rights reserved.
