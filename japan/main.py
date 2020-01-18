import bottle, sqlite3, uuid, questions, secrets

ADMIN_KEY = "ADD MIN. KEY" #Enter this as name to unlock admin privs

ADMIN_SECRET = secrets.token_urlsafe(25)

RESET_DB = True

game_started = False

db = sqlite3.connect("japan_geo.db")
if RESET_DB:
	db.execute("DROP TABLE IF EXISTS users")
	db.execute("DROP TABLE IF EXISTS answers")
	db.execute("CREATE TABLE users (id text, name text, on_pg int, score int)")
	db.execute("CREATE TABLE answers (q_num int, user_id text, answer_text longtext, votes int)")
	db.commit()

@bottle.route("/")
def index():
	return bottle.static_file("index.html", root="./static/")
	
@bottle.route("/styles.css")
def stylesheet():
	return bottle.static_file("styles.css", root="./static/")
	
@bottle.route("/img/<iname>")
def fetch_img(iname):
	return bottle.static_file(iname, "./static/img/")

@bottle.route("/pg/<num>")
def static_page(num):
	id = bottle.request.get_cookie("id")
	if int(num) < 6:
		return bottle.static_file(f"pg{num}.html", root="./static/")
	else:
		bottle.redirect(f"/review/{ADMIN_SECRET}/{id}/0")	
	
@bottle.route("/login", method="GET")
def login_processing_page():
	name = bottle.request.query.name
	new_id = uuid.uuid4().int
	print(name, " ", new_id)
	db.execute("INSERT INTO users VALUES(?, ?, 0, 0)", (str(new_id), name))
	db.commit()
	bottle.response.set_cookie("id", str(new_id), max_age=60*60)
	if name == ADMIN_KEY:
		return f'<meta http-equiv="Refresh" content="0; url=/{ADMIN_SECRET}/main" />'
	return '<meta http-equiv="Refresh" content="0; url=/pg/0" />'
	
@bottle.route("/question")
def question_pg():
	qpg = bottle.request.query.pg
	return questions.questions[int(qpg)].html
	
@bottle.route("/qsubmit/openended", method="POST")
def submit_openended():
	pg = int(bottle.request.forms.get("pg"))
	answer = bottle.request.forms.get("answer")
	user_id = bottle.request.get_cookie("id")
	if user_id == None:
		bottle.abort(401, "not logged in!")
	db.execute("UPDATE users SET on_pg=? WHERE id=?", (pg + 1, user_id))
	db.execute("INSERT INTO answers VALUES(?, ?, ?, 0)", (pg, user_id, answer))
	db.commit()
	bottle.redirect(f"/pg/{pg+1}")
	
@bottle.route(f"/{ADMIN_SECRET}/<action>")
def admin_page(action):
	if action == "main":
		return generate_status_page()
		
@bottle.route(f"/game/{ADMIN_SECRET}/<user_id>", method="POST")
def game_staring_pg(user_id):
	real_id = bottle.request.get_cookie("id")
	if real_id == None or user_id != real_id:
		bottle.abort(401, "not logged in!")
	c = db.cursor()
	c.execute("UPDATE users SET on_pg=-1 WHERE id=?", (user_id,))
	db.commit()
	if game_started:
		pass
	else:
		return bottle.static_file("game_not_started.html", root="./static/")
		
@bottle.route(f"/review/{ADMIN_SECRET}/<user_id>/<question>")
def review_pg(user_id, question):
	c = db.cursor()
	real_id = bottle.request.get_cookie("id")
	if str(real_id) != str(user_id):
		bottle.abort(401, "Access denied")
	if question == 6:
		return get_best_answers(user_id)
	c.execute("SELECT * FROM answers WHERE q_num=? AND NOT user_id=?", (int(question), user_id))
	answers = c.fetchall()
	return generate_answer_page(answers, c, int(question), user_id, vote=(int(question) != len(questions.questions)-1))
	
@bottle.route("/vote")
def vote_pg():
	user_id = bottle.request.get_cookie("id")
	voted_for_id = bottle.request.query.chosen
	question = bottle.request.query.question
	c = db.cursor()
	c.execute("SELECT * FROM answers WHERE user_id=? AND q_num=?", (voted_for_id, question))
	current_votes = c.fetchone()[3]
	c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
	score = int(c.fetchone()[3])
	c.execute("UPDATE answers SET votes=? WHERE user_id=? AND q_num=?", (int(current_votes)+1, voted_for_id, question))
	c.execute("UPDATE users SET score=? WHERE user_id=?", (score += 2, user_id))
	bottle.redirect(f"/review/{ADMIN_SECRET}/{user_id}/{int(question)+1}")
	
def get_best_answers(user_id):
	c = db.cursor()
	q = 0
	qlist = []
	while q < 6:
		c.execute("SELECT MAX(votes) FROM answers WHERE q_num=?", (q,))
		qlist.append(c.fetchone())
		q += 1
	return generate_answer_page(qlist, db.cursor(), 6, user_id)
		
def generate_status_page():
	c = db.cursor()
	c.execute("SELECT * FROM users WHERE name=?", (ADMIN_KEY,))
	admin_id = c.fetchone()[0]
	ret_html = f"<link rel='stylesheet' href='/styles.css'>Review link: /review/{ADMIN_SECRET}/{admin_id}/0<br/><br/>"
	c = db.cursor()
	c.execute("SELECT * FROM users")
	all_users = c.fetchall()
	for x in all_users:
		ret_html += f"<h1>{x[1]}</h1><br/><br/>"
		ret_html += f"ID: {x[0]}<br/>"
		ret_html += f"On page: {x[2]}<br/>"
		ret_html += f"Score: {x[3]}<br/><br/>"
	return ret_html
	
def generate_answer_page(answers, c, q_num, user_id, vote=False):
	content = f"<link rel='stylesheet' href='/styles.css'><h1>Review: {questions.questions[q_num].prompt}</h1><br/><br/>"
	for x in answers:
		c.execute("SELECT * FROM users WHERE id=?", (x[1],))
		name = c.fetchone()[1]
		content += f"<div class='answer-review-box'><h2>Name:{name}<br/>ID:{x[1]}</h2><br/><p class='textbook-sect'>Answer:{x[2]}</p></div></br></br>"
	if vote:
		content += """
		<br/><form action="/vote" method="get">
		<p class="textbook-sect">Copy and paste the long number of the answer that you think is best here.</p>
		<br/><input type="hidden" name="question" value="{0}">
		<input type="text" name="chosen"><br/>
		<input type="submit" value="Submit" class="b-pretty">
		</form>
		""".format(q_num)
	else:
		content += """
		<form action="/game/{0}/{1}" method="post">
		<input type="submit" class="b-pretty" value="Continue">
		</form>
		""".format(ADMIN_SECRET, user_id)
	return content
	
bottle.run(host="localhost", port=80, debug=True)
