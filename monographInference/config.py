import os

# Define paths
ROOT_PROJETS_PATH = 'C:\\Users\\jorge.morales\\Documents\\Personales\\UdeA\\ml2MLOPSMonograph'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(ROOT_PROJETS_PATH,'storage', 'data', 'raw')
FEAUTURE_DATA_PATH = os.path.join(ROOT_PROJETS_PATH,'storage', 'data', 'feauture-store')
MODELS_ARTIFACTS_PATH = os.path.join(ROOT_PROJETS_PATH,'storage', 'models')
LOG_PATH = os.path.join(ROOT_PROJETS_PATH,'storage','logs')

MODEL_CURRENT_VERSION = 'C:\\Users\\jorge.morales\\Documents\\Personales\\UdeA\\ml2MLOPSMonograph\\storage\\models\\0.1\\model.joblib'

# Define database connection details
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'my_database'
DB_USER = 'my_username'
DB_PASSWORD = 'my_password'

# Define email notification settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'my_email@gmail.com'
EMAIL_PASSWORD = 'my_email_password'
EMAIL_RECIPIENTS = ['recipient1@example.com', 'recipient2@example.com']
