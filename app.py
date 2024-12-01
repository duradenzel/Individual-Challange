from flask import Flask, render_template, request
import joblib
import datetime
import csv

app = Flask(__name__)
model = joblib.load('model.pkl')

DATA_FILE = 'user_inputs.csv'

def initialize_csv(file_path):
    try:
        with open(file_path, mode='x', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow(['timestamp', 'hp', 'ac', 'size', 'can_fly', 'can_swim', 'legendary',
                             'str', 'dex', 'con', 'int', 'wis', 'cha', 'predicted_cr'])
    except FileExistsError:
        pass  

initialize_csv(DATA_FILE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
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

        input_data = [[hp, ac, size, can_fly, can_swim, legendary, strength,
                       dexterity, constitution, intelligence, wisdom, charisma]]

        predicted_cr = round(model.predict(input_data)[0],2)

        timestamp = datetime.datetime.now().isoformat()

        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, hp, ac, size, can_fly, can_swim, legendary,
                             strength, dexterity, constitution, intelligence, wisdom, charisma, predicted_cr])

        return render_template('index.html', predicted_cr=predicted_cr)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
