from flask import Flask, render_template, request
import joblib
import datetime
import csv

app = Flask(__name__)
model = joblib.load('model.pkl')

# Define CSV file path
DATA_FILE = 'user_inputs.csv'

# Function to ensure the CSV file exists
def initialize_csv(file_path):
    try:
        with open(file_path, mode='x', newline='') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(['timestamp', 'hp', 'ac', 'size', 'can_fly', 'can_swim', 'legendary',
                             'str', 'dex', 'con', 'int', 'wis', 'cha', 'predicted_cr'])
    except FileExistsError:
        pass  # File already exists, no need to do anything

# Initialize the CSV file
initialize_csv(DATA_FILE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve form inputs
        hp = int(request.form['hp'])
        ac = int(request.form['ac'])
        size = int(request.form['size'])
        can_fly = int(request.form['can_fly'])
        can_swim = int(request.form['can_swim'])
        legendary = int(request.form['legendary'])
        strength = int(request.form['str'])
        dexterity = int(request.form['dex'])
        constitution = int(request.form['con'])
        intelligence = int(request.form['int'])
        wisdom = int(request.form['wis'])
        charisma = int(request.form['cha'])

        # Prepare input for the model
        input_data = [[hp, ac, size, can_fly, can_swim, legendary, strength,
                       dexterity, constitution, intelligence, wisdom, charisma]]

        # Predict CR
        predicted_cr = round(model.predict(input_data)[0],2)

        # Get the current timestamp
        timestamp = datetime.datetime.now().isoformat()

        # Save the input and prediction to the CSV file
        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, hp, ac, size, can_fly, can_swim, legendary,
                             strength, dexterity, constitution, intelligence, wisdom, charisma, predicted_cr])

        # Display result on the same page
        return render_template('index.html', predicted_cr=predicted_cr)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
