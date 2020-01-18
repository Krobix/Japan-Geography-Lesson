class OpenEndedQuestion:
	def __init__(self, pg, prompt):
		self.prompt = prompt
		self.pg = pg
		
	@property
	def html(self):
		return """<link rel="stylesheet" href="/styles.css">
		<h1>Question: {0}</h1>
		<form action="/qsubmit/openended" method="post">
		<input type="text" class="answer-box" name="answer">
		<input type="hidden" name="pg" value="{1}">
		<input type="submit" value="Submit">
		</form>
		""".format(self.prompt, self.pg)
		
class MultipleChoiceQuestion:
	def __init__(self, id, question, answers, correct):
		self.id = id
		self.question = question
		self.answers = answers
		self.correct = correct
		
	@property
	def html(self):
		return """
		<link rel="stylesheet" href="/styles.css">
		<h1>{0}</h1><br/><br/>
		<form action="/qsubmit/choice" method="get">
		<input type="radio" name="answer" value="a">{0}<br/>
		<input type="radio" name="answer" value="b">{1}<br/>
		<input type="radio" name="answer" value="c">{2}<br/>
		<input type="radio" name="answer" value="d">{3}<br/>
		<input type="submit" class="b-pretty" value="Submit">
		</form>""".format(*self.answers)
		
questions = (
	OpenEndedQuestion(0, "How might the geography of Japan relate to its early conflicts?"),
	OpenEndedQuestion(1, "Based on the map shown on the last page, what areas might the most populated? Why?"),
	OpenEndedQuestion(2, "Summarize Japan's geography in the best way possible using the previous passage.'"),
	OpenEndedQuestion(3, "Based on the passage, do you think it would be nice to live in Japan? Why or why not?"),
	OpenEndedQuestion(4, "Compare and contrast the geography where you live to the geography of Japan."),
	OpenEndedQuestion(5, "Based on the Wikipedia passage, what could have Japan's culture been like?"),
	OpenEndedQuestion(9999, "The top voted answers for each question, in order.")
	)
