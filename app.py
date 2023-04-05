import numpy as np
from flask import Flask, request, jsonify, render_template
from joblib import load
from collections import OrderedDict 
import pandas as pd


term_dict =OrderedDict()
years_dict =OrderedDict()
purpose_dict =OrderedDict()
home_dict = OrderedDict()

result = OrderedDict()


app = Flask(__name__)
model = load('rfc.joblib')

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict', methods=['GET','POST'])

def predict():
    
    features =[]
    term_dict = {"long term":0,"short term":0}
    
    years_dict = {'1 year':0,'10+ years':0,'2 years':0,'3 years':0,
                  '4 years':0,'5 years':0,'6 years':0,'7 years':0,'8 years':0,'9 years':0,'< 1 year':0}
    
    purpose_dict={"business loan":0,"buy house":0,"buy a car":0, "debt consolidation":0, 
                  "educational expenses":0,  "home improvements":0, "medical bills":0, 
                  "take a trip":0,"major purchase":0, "moving":0, "other":0,
                  "renewable energy":0, "small business":0, "vacation":0, "wedding":0 }
    
    
    home_dict={"home mortgage":0, "own home":0, "rent":0}
    
    
   
    full_name = request.form.get("full name")
    expected_loan_amount = request.form.get("expected loan amount")
    credit_score =request.form.get("credit score")
    annual_income = request.form.get("annual income")
    monthly_debt = request.form.get("monthly debt")
    years_of_credit_history = request.form.get("years of credit history")
    number_of_open_accounts = request.form.get("number of open accounts")
    number_of_credit_problems = request.form.get("number of credit problems")
    current_credit_balance = request.form.get("current credit balance")
    maximum_open_credit = request.form.get("maximum open credit")
    bankruptcies = request.form.get("bankruptcies")
    tax_liens = request.form.get("tax liens")
    
    features.extend([expected_loan_amount,credit_score,annual_income,monthly_debt,years_of_credit_history,
                    number_of_open_accounts,number_of_credit_problems,current_credit_balance,
                    maximum_open_credit,bankruptcies,tax_liens])
    
    result ={'Full Name':full_name,"Expected Loan Amount":expected_loan_amount,
            "Annual Income":annual_income,"Credit Score":credit_score,"Years of credit history": years_of_credit_history,
             "Monthly Debt": monthly_debt,
             "Number of open accounts":number_of_open_accounts,
             "Number of credit problems": number_of_credit_problems,"Current credit balance": current_credit_balance,
              "Maximum open credit": maximum_open_credit,"Bankruptcies": bankruptcies,
             "Tax liens":tax_liens}
    
    
    term = request.form.get("term")
    term_dict[term]=1
    result['Term'] = term
    term_list = list(term_dict.values())
    term_list=term_list[1:]
    print(len(term_list))
    
    years_in_current_in_job = request.form.get("years in current in job")
    years_dict[years_in_current_in_job] =1
    result['Years in current in job']=years_in_current_in_job
    years_list = list(years_dict.values())
    years_list= years_list[1:]
    print(len(years_list))
    
    purpose_of_loan = request.form.get("purpose of loan")
    purpose_dict[purpose_of_loan] = 1
    print(purpose_dict)
    result['Purpose of Loan']=purpose_of_loan
    purpose_list = list(purpose_dict.values())
    purpose_list= purpose_list[1:]
    print(len(purpose_list))
    
    home_ownership = request.form.get("home ownership")
    home_dict[home_ownership] = 1
    print(home_dict)
    result['Home_Ownership']=home_ownership
    home_list = list(home_dict.values())
    home_list = home_list[1:]
    print(len(home_list))
    
    features = features + term_list + home_list + years_list + purpose_list 
    
    print(features)
    print(len(features))
  
    features = [np.array(features)]
    prediction = model.predict(features)
    
    output = prediction[0]
    if output == 1:
            result['Loan status'] = "CAN BE APPROVED"
    else:
           result['Loan status'] = "CAN NOT BE APPROVED"
    
    
    results = pd.DataFrame(result.items())
    print(results)
    
    code ='''   
 <html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style> h3{{text-align:center;}}
 tr:nth-child(even){{background-color: #f2f2f2;}}
    td[value='Y']{{color:green; font-weight:bold;}}
    td[value='N']{{color:red;font-weight:bold;}}
  table, th, td {{margin-left: auto;border-collapse: collapse;
  margin-right: auto;font-size:10pt; border:2px solid black; border-collapse:collapse; text-align:left;}}
  th, td {{padding: 5px;}}
</style>
</head>
<body>
<h3>Loan Approval Status</h3>
{0}
</body>

</html>
'''.format(results.to_html(header=False,index=False))
    
    
    code = code.replace("<td>CAN BE APPROVED</td>", "<td value='Y'>CAN BE APPROVED</td>")
    code = code.replace("<td>CAN NOT BE APPROVED</td>", "<td value='N'>CAN NOT BE APPROVED</td>")   
        
        

    
    return code

    
    
if __name__=="__main__":
    app.run(debug=True)
