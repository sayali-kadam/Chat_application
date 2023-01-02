from flask import Flask, request, render_template, redirect, url_for
import pymongo

app = Flask(__name__)
count_cust = 1
count_agent = 1
CONNECTION_STRING = "mongodb+srv://Sayali:sayali@cluster0.d5uvhoq.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('internship_project')
colle = db["customerList"]

@app.route('/')
def flask_mongodb_atlas():
    return "flask mongodb atlas!"

@app.route('/admin/agent_dashboard')
def view_customers():
    all_todos = db["customerList"].find()
    results = list(all_todos)
    if len(results)==0:
        print("Empty Cursor")
    else:
        print("Cursor is Not Empty")
        print(results)
    return render_template('agent_dashboard.html', colle=results)

@app.route('/customer_dashboard', methods=['GET', 'POST'])
def customer_dashboard():
    customers = db["customerList"].find()
    customer = list(customers)

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        url = '/customer_conv/'+customer_id
        return redirect(url)

    return render_template('customer_dashboard.html', colle=customer)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    global count_cust
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        url = '/customer_conv/'+str(count_cust)
        db.customerList.insert_one({"customer_id": count_cust, 'Name': customer_name})
        count_cust = count_cust+1
        return redirect(url)

    return render_template('add_customer.html')

@app.route('/customer_conv/<id>', methods=['GET', 'POST'])
def customer_conv(id):
    customers = list(db["customerList"].find())
    agents = list(db["agentList"].find())
    messages = list(db["messsageList"].find({"customer_id": int(id)}))
    global count_cust

    if request.method == 'POST':
        msg_body = request.form['message']
        customer_id = int(request.form.get('customer_id', 0))
        customer_name = request.form.get('customer_name')
        
        if customer_id:
            print(customer_id)
        else:
            db.customerList.insert_one({"customer_id": count_cust, 'Name': customer_name})
            customer_id = count_cust
            count_cust = count_cust+1

        db.messsageList.insert_one({'customer_id': customer_id, 'customer_name': customer_name, 'Body': msg_body})
    
    if len(messages)==0:
        print("Empty Cursor")
    else:
        print("Cursor is Not Empty")
        print(messages)
    return render_template('customer_conv.html', messages=messages, agents=agents, customers=customers)

@app.route('/admin/agent_conv/<int:id>', methods=['GET', 'POST'])
def view_customer(id):
    customer = []
    for x in db["customerList"].find({"customer_id": id}):
        customer.append(x['customer_id'])
        customer.append(x['Name'])
    
    agents = list(db["agentList"].find())
    customers = list(db["customerList"].find())
    messages = list(db["messsageList"].find({"customer_id": id}))
    
    if request.method == 'POST':
        msg_body = request.form['message']
        agent_id = int(request.form.get('agent_id', 0))
        print(agent_id)
        agent = []
        for x in db["agentList"].find({"agent_id": str(agent_id)}):
            agent.append(x['agent_id'])
            agent.append(x['Name'])
            print(x)
        print(agent)
        db.messsageList.insert_one({'customer_id': customer[0], 'customer_name': customer[1], 'agent_id': agent[0], 'agent_name': agent[1], 'Body': msg_body})
    
    print(customer)
    return render_template('agent_conv.html', customers=customers, agents=agents, messages=messages)

if __name__ == '__main__':
    app.run(port=8000)