import os

dag_file_dir = os.path.dirname(os.path.realpath(__file__))

validation_split = 0.95
model_location = os.path.join(dag_file_dir, 'models/GBC.pkl')
accuracy_location = os.path.join(dag_file_dir, 'models/accuracy.txt')
simulation_location = os.path.join(dag_file_dir, 'simulations')
feature_window = 60
data_loc = os.path.join(dag_file_dir, 'data/EUR-USD.csv')