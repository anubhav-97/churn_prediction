from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the Random Forest CLassifier model
filename = 'churn.pkl'
regressor = pickle.load(open(filename, 'rb'))

# print(regressor)

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        
        CreditScore = int(request.form['CreditScore'])
        CreditScore = ((CreditScore - 650.5288) / 96.65329873613061)
        age = int(request.form['age'])
        tenure = int(request.form['tenure'])
        balance = int(request.form['balance'])
        balance = ((balance - 76485.88928799961) / 62397.40520238623)
        numofproducts = int(request.form['numofproducts'])

        temp_array = temp_array+[CreditScore, age, tenure, balance, numofproducts]
        
        crcard = request.form['crcard']
        if crcard == '1':
            temp_array = temp_array + [1]
        elif crcard == '0':
            temp_array = temp_array + [0]
        
        member = request.form['member']
        if member == '1':
            temp_array = temp_array + [1]
        elif member == '0':
            temp_array = temp_array + [0]

        estimatedsalary = int(request.form['estimatedsalary'])
        estimatedsalary = ((estimatedsalary - 100090.2398809998) / 57510.49281769822)
        temp_array = temp_array + [estimatedsalary]
        
        country = request.form['country']
        if country == 'France':
            temp_array = temp_array + [1,0,0]
        elif country == 'Germany':
            temp_array = temp_array + [0,1,0]
        elif country == 'Spain':
            temp_array = temp_array + [0,0,1]
            
        gender = request.form['gender']
        if gender == 'Female':
            temp_array.extend([1,0])
        elif gender == 'Male':
            temp_array.extend([0,1])
        
        # temp_array = temp_array + [CreditScore, age, tenure, balance, numofproducts, crcard, member, estimatedsalary]
        print(temp_array)
        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data))
        print(my_prediction)
        lst = []
        if my_prediction == 0:
            lst.append("Not Churn")
        elif my_prediction == 1:
            lst.append("Churn")
              
        return render_template('result.html', lower_limit = lst[0])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

	# app.run(debug=True)