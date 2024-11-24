from flask import Flask, request, render_template
import joblib
import numpy as np

model = joblib.load('model.pkl')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        size_mapping = {
            "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5
        }

        hp = float(request.form['hp'])
        ac = float(request.form['ac'])
        if hp <= 0 or ac <= 0:
            raise ValueError("HP and AC must be positive values.")
        
        ability_scores = [
            float(request.form['str']),
            float(request.form['dex']),
            float(request.form['con']),
            float(request.form['int']),
            float(request.form['wis']),
            float(request.form['cha']),
        ]
        if any(score < 1 or score > 30 for score in ability_scores):
            raise ValueError("Ability scores must be between 1 and 30.")

        input_data = [
            hp,
            ac,
            size_mapping[request.form['size']],
            int(request.form['can_fly']),
            int(request.form['can_swim']),
            int(request.form['legendary']),
            *ability_scores,
        ]

        input_array = np.array([input_data])

        prediction = model.predict(input_array)[0]
        return render_template('index.html', prediction=f'{prediction:.2f}')

    except ValueError as e:
        return render_template('index.html', prediction=f"Error: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
