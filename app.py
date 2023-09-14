import csv
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Initialize variables to track the presence of Rouge and Jaune
has_rouge = False
has_jaune = False

# Read the CSV file
data = []

with open('database.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# Initialize index to keep track of the current question
question_index = 0

@app.route('/')
def index():
    global question_index, has_rouge, has_jaune
    # Check if the user wants to start a new assessment
    start_new_assessment = request.args.get('new_assessment')
    if start_new_assessment:
        # Reset variables
        has_rouge = False
        has_jaune = False
        question_index = 0
    
    if question_index < len(data):
        question = data[question_index]
        return render_template('index.html', question=question)
    else:
        return render_template('result.html', has_rouge=has_rouge, has_jaune=has_jaune)

@app.route('/answer', methods=['POST'])
def answer():
    global question_index, has_rouge, has_jaune
    user_choice = request.form.get('choice')

    if user_choice in ['a', 'b', 'c', 'non']:
        question = data[question_index]
        if 'Rouge' in question[user_choice]:
            has_rouge = True
        if 'Jaune' in question[user_choice]:
            has_jaune = True
        question_index += 1

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
