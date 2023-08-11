# Forex Prediction Project

## Description

The Forex Prediction Project aims to predict currency exchange rates using historical data and machine learning techniques. It employs an orchestrated pipeline managed through Apache Airflow to collect and clean data from a Forex website. Feature engineering is conducted using the past 60 days' price values, and a predictive model is trained to forecast currency outcomes.

## Installation

- Clone the repository: `https://github.com/aameerhamza1801/forex_predictor_pipeline.git`
- Install required packages: `pip install -r Requirements.txt`

## Usage

- Configure your Forex website credentials in the provided configuration file.
- Ensure that Apache Airflow is properly set up and configured.
- Run the Airflow DAG to initiate the pipeline.

## Features

- Utilizes historical Forex data to enhance prediction accuracy.
- Adopts a sliding window technique, incorporating the last 60 days' price values as features.
- Predicts currency outcomes through a machine learning model.
- Orchestrates the complete process using Apache Airflow.

## Pipeline

The project's pipeline comprises the following stages:
- Data Collection: Retrieves historical currency exchange data from the Forex website.
- Data Cleaning: Preprocesses and scrubs the acquired data.
- Feature Engineering: Generates features based on the price values from the past 60 days.
- Model Training: Trains a machine learning model using the engineered features.
- Prediction: Makes predictions utilizing the trained model.
- Results: Assesses and visualizes the model's performance.

## FAQs

- **Q:** How frequently is the prediction model updated?
  - **A:** The model is updated as per the schedule defined in the Airflow DAG.

- **Q:** Can I apply this project to other financial instruments?
  - **A:** Although this project is customized for Forex prediction, you can adapt it for other financial instruments with appropriate adjustments.

## Support

If you encounter any difficulties or have inquiries, please don't hesitate to contact us at hamza91ghani@gmail.com.
