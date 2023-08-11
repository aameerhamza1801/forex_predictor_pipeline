Forex Prediction Project README

Description

This project focuses on predicting currency exchange rates using historical data and machine learning techniques. By leveraging a pipeline orchestrated through Apache Airflow, the project collects and cleans data from a Forex website, performs feature engineering using the past 60 days' price values, and trains a predictive model to forecast currency outcomes.

Installation

•	https://github.com/aameerhamza1801/forex_predictor_pipeline.git
•	pip install -r Requirements.txt

Usage

•	Configure your Forex website credentials in the configuration file.
•	Ensure that Apache Airflow is set up and configured properly.
•	Run the Airflow DAG to trigger the pipeline.
Features

•	Utilizes historical Forex data for accurate prediction.
•	Uses a sliding window approach, considering the last 60 days' price values as features.
•	Predicts currency outcomes using a machine learning model.
•	Orchestrates the entire process using Apache Airflow.

Pipeline

•	The project's pipeline includes the following steps:
•	Data Collection: Retrieve historical currency exchange data from the Forex website.
•	Data Cleaning: Preprocess and clean the collected data.
•	Feature Engineering: Create features based on the past 60 days' price values.
•	Model Training: Train a machine learning model on the engineered features.
•	Prediction: Make predictions using the trained model.
•	Results: Evaluate and visualize the model's performance.





FAQs

•	Q: How often is the prediction model updated? A: The model is updated based on the defined schedule in the Airflow DAG.
•	Q: Can I use this project for other financial instruments? A: While this project is tailored for Forex prediction, you can modify it for other financial instruments with suitable adjustments.

Support

•	If you encounter any issues or have questions, feel free to contact us at hamza91ghani@gmail.com


