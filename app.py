from flask import Flask, request, session, render_template
import json
import uuid


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "secret key"


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/university', methods=['GET'])
def university():
	print("something")
	return render_template('university.html')


@app.route('/login', methods=['GET'])
def login():
	role = request.args.get('role')
	id = request.args.get('id')
	response = dict()
	if role == 'student':
		session['sid'] = id
		if 'uid' in session:
			del session['uid']
		response['status'] = "OK"
		response['message'] = "Student logged in."
	elif role == 'university':
		session['uid'] = id
		if 'sid' in session:
			del session['sid']
		response['status'] = "OK"
		response['message'] = "University logged in."
	else:
		response['status'] = "ERROR"
		response['message'] = "Invalid role."
	return json.dumps(response)


@app.route('/logout', methods=['GET'])
def logout():
	id = request.args.get('id')
	response = dict()
	if 'uid' in session:
		del session['uid']
		response['status'] = "OK"
		response['message'] = "University logged out."
	elif 'sid' in session:
		del session['sid']
		response['status'] = "OK"
		response['message'] = "Student logged out."
	return json.dumps(response)


@app.route('/fetch_current_students', methods=['GET'])
def fetch_current_students():
	if 'uid' in session:
		with open(session['uid'] + '.json', "r", encoding='utf8') as file:
			data =json.load(file)
		return json.dumps(data['current_students'], indent=3)
	else:
		return None


@app.route('/fetch_prospective_students', methods=['GET'])
def fetch_prospective_students():
	if 'uid' in session:
		with open(session['uid'] + '.json', "r", encoding='utf8') as file:
			data = json.load(file)
		return json.dumps(data['prospective_students'], indent=3)
	else:
		return None


@app.route('/fetch_updates', methods=['GET'])
def fetch_updates():
	if 'sid' in session:
		with open('actions.json', "r", encoding='utf8') as file:
			data = json.load(file)
			actions = []
			for i in data:
				if 'sid' in i and i['sid'] == session['sid']:
					action = dict()
					action['title'] = i['title']
					action['uname'] = i['uname']
					action['uid'] = i['uid']
					action['tid'] = i['tid']
					action['action'] = i['action']
					actions.append(action)
		return json.dumps(actions, indent=3)
	elif 'uid' in session:
		with open('actions.json', "r", encoding='utf8') as file:
			data = json.load(file)
			actions = []
			for i in data:
				if 'uid' in i and i['uid'] == session['uid']:
					action = dict()
					action['title'] = i['title']
					action['sname'] = i['sname']
					action['sid'] = i['sid']
					action['tid'] = i['tid']
					action['action'] = i['action']
					action['data'] = i['data']
					actions.append(action)
		return json.dumps(actions, indent=3)
	else:
		return None


@app.route('/award_degree', methods=['GET'])
def award_degree():
	if 'uid' in session:
		sid = request.args.get('sid')
		last_transaction = request.args.get('last_transaction')
		action = dict()
		action['title'] = 'award_degree'
		action['tid'] = uuid.uuid4().hex
		action['data'] = uuid.uuid4().hex
		action['sid'] = sid
		action['sname'] = get_sname(sid)
		action['action'] = {"type": "buttons", "options": ['Accept', 'Decline']}
		action_data = dict()
		with open('actions.json',"r", encoding="utf8") as file:
			action_data = json.load(file)
		if last_transaction is not None and last_transaction in action_data:
			del action_data[last_transaction]
		action_data[action['tid']] = action
		with open("actions.json", "w", encoding="utf8") as file:
			json.dump(action_data, file, indent=3)
	else:
		return None


@app.route('/accept_degree', methods=['GET'])
def accept_degree():
	if 'sid' in session:
		uid = request.args.get('uid')
		last_transaction = request.args.get('last_transaction')
		degree = request.args.get('degree')
		action = dict()
		action['title'] = 'degree_accepted'
		action['tid'] = uuid.uuid4().hex
		action['data'] = degree
		action['uid'] = uid
		action['uname'] = get_uname(uid)
		action['action'] = {"type": "info"}
		with open("degree.json", "w", encoding="utf8") as file:
			degree_data = json.load(file)
			if session['sid'] in degree_data:
				degree_data[session['sid']].append(degree)
			else:
				degree_data[session['sid']] = [degree]
		action_data = dict()
		with open('actions.json', "r", encoding="utf8") as file:
			action_data = json.load(file)
		if last_transaction is not None and last_transaction in action_data:
			del action_data[last_transaction]
		action_data[action['tid']] = action
		with open("actions.json", "w", encoding="utf8") as file:
			json.dump(action_data, file, indent=3)
	else:
		return None


@app.route('/reject_degree', methods=['GET'])
def reject_degree():
	if 'sid' in session:
		uid = request.args.get('uid')
		last_transaction = request.args.get('last_transaction')
		degree = request.args.get('degree')
		action = dict()
		action['title'] = 'degree_rejected'
		action['tid'] = uuid.uuid4().hex
		action['data'] = "Degree rejected"
		action['uid'] = uid
		action['uname'] = get_uname(uid)
		action['action'] = {"type": "info"}
		action_data = dict()
		with open('actions.json', "r", encoding="utf8") as file:
			action_data = json.load(file)
		if last_transaction is not None and last_transaction in action_data:
			del action_data[last_transaction]
		action_data[action['tid']] = action
		with open("actions.json", "w", encoding="utf8") as file:
			json.dump(action_data, file, indent=3)
	else:
		return None


@app.route('/request_degree', methods=['GET'])
def request_degree():
	if 'uid' in session:
		sid = request.args.get('sid')
		last_transaction = request.args.get('last_transaction')
		action = dict()
		action['title'] = 'degree_requested'
		action['tid'] = uuid.uuid4().hex
		action['data'] = "Degree requested"
		action['sid'] = sid
		action['sname'] = get_sname(sid)
		action['action'] = {"type": "buttons", "option": ["Send", "Don't Send"]}
		action_data = dict()
		with open('actions.json', "r", encoding="utf8") as file:
			action_data = json.load(file)
		if last_transaction is not None and last_transaction in action_data:
			del action_data[last_transaction]
		action_data[action['tid']] = action
		with open("actions.json", "w", encoding="utf8") as file:
			json.dump(action_data, file, indent=3)
	else:
		return None


@app.route('/send_degree', methods=['GET'])
def send_degree():
	if 'sid' in session:
		uid = request.args.get('uid')
		last_transaction = request.args.get('last_transaction')
		degree = request.args.get('degree')
		action = dict()
		action['title'] = 'send_degree'
		action['tid'] = uuid.uuid4().hex
		action['uid'] = uid
		action['uname'] = get_uname(uid)
		action['action'] = {"type": "info"}
		action_data = dict()
		with open("degree.json", "r", encoding="utf8") as file:
			degree_data = json.load(file)
			if session['sid'] in degree_data:
				action['data'] = degree_data[session['sid']]
			else:
				action['data'] = []
		with open('actions.json', "r", encoding="utf8") as file:
			action_data = json.load(file)
		if last_transaction is not None and last_transaction in action_data:
			del action_data[last_transaction]
		action_data[action['tid']] = action
		with open("actions.json", "w", encoding="utf8") as file:
			json.dump(action_data, file, indent=3)
	else:
		return None


@app.route('/donot_send_degree', methods=['GET'])
def donot_send_degree():
	if 'sid' in session:
		uid = request.args.get('uid')
		last_transaction = request.args.get('last_transaction')
		degree = request.args.get('degree')
		action = dict()
		action['title'] = 'donot_send_degree'
		action['tid'] = uuid.uuid4().hex
		action['uid'] = uid
		action['uname'] = get_uname(uid)
		action['data'] = "Request Declined"
		action['action'] = {"type": "info"}
		action_data = dict()
		with open('actions.json', "r", encoding="utf8") as file:
			action_data = json.load(file)
		if last_transaction is not None and last_transaction in action_data:
			del action_data[last_transaction]
		action_data[action['tid']] = action
		with open("actions.json", "w", encoding="utf8") as file:
			json.dump(action_data, file, indent=3)
	else:
		return None


def get_sname(sid):
	with open('smap', "r", encoding='utf8') as smap:
		smap = json.load(smap)
		if sid in smap:
			return smap[sid]
		else:
			return None


def get_uname(uid):
	with open('umap', "r", encoding='utf8') as umap:
		umap = json.load(umap)
		if uid in umap:
			return umap[uid]
		else:
			return None


if __name__ == '__main__':
	app.debug = True
	app.run()
