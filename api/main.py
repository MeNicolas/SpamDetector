import flask
from flask import request, render_template

app = flask.Flask(__name__, static_url_path='')
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
def home():
	prediction = None
	mail = None
	
	if request.method == 'POST':
		mail = request.form['mail']
		prediction = predict(mail)
				
	return render_template('index.html', mail = mail, prediction = prediction)
	
@app.route('/api/predict', methods=['POST'])
def api():
	mail = request.form['mail']
	prediction = predict(mail)
				
	return {'spam': prediction}
		
import joblib
model = joblib.load('randomforest.pkl')
xgb = joblib.load('xgb.pkl')
	
def predict(mail):
	x = analyze_mail(mail)
	print(len(x))
	return bool(model.predict([x])[0])

def word_freq(mail, word):
	words = mail.split(' ')
	nb_words = len(words)
	if nb_words == 0: return 0
	
	nb_occ = 0
	for w in words:
		if w == word: nb_occ += 1

	return nb_occ/nb_words*100
	
def char_freq(mail, char):
	nb = len(mail)
	if nb == 0: return 0
	
	nb_occ = 0
	for c in mail:
		if c == char: nb_occ += 1

	return nb_occ/nb*100

def capital_sequences(mail):
	seq = []
	current = ''
	
	for c in mail:
		if c.isupper():
			current += c
		else:
			if len(current) > 0:
				seq.append(current)
				current = ''
	
	if len(current) > 0:
		seq.append(current)
					
	return seq

def analyze_mail(mail):
	words = 'make,address,all,3d,our,over,remove,internet,order,mail,receive,will,people,report,addresses,free,business,email,you,credit,your,font,000,money,hp,hpl,george,650,lab,labs,telnet,857,data,415,85,technology,1999,parts,pm,direct,cs,meeting,original,project,re,edu,table,conference'.split(',')
	chars = ';,(,[,!,$,#'.split(',')
	
	print(len(words), len(chars))
	
	words_freq = [word_freq(mail, word) for word in words]
	chars_freq = [word_freq(mail, char) for char in chars]
	print(words_freq)	
	print(chars_freq)	
	
	capitals = capital_sequences(mail)
	capital_run_lenghts = [len(seq) for seq in capitals]
	
	total = sum(capital_run_lenghts)
	average = total/(len(capitals)+1)
	longest = max(capital_run_lenghts) if total > 0 else 0
	
	return words_freq + chars_freq + [average, longest, total]
	
app.run()