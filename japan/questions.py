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
		<input type="submit" class="b-pretty" value="Submit">
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
		<input type="hidden" name="q" value="{1}">
		<input type="radio" name="answer" value="a">{2}<br/>
		<input type="radio" name="answer" value="b">{3}<br/>
		<input type="radio" name="answer" value="c">{4}<br/>
		<input type="radio" name="answer" value="d">{5}<br/>
		<input type="submit" class="b-pretty" value="Submit">
		</form>""".format(self.question, self.id, *self.answers)
		
questions = (
	OpenEndedQuestion(0, "How might the geography of Japan relate to its early conflicts?"),
	OpenEndedQuestion(1, "Based on the map shown on the last page, what areas might the most populated? Why?"),
	OpenEndedQuestion(2, "Summarize Japan's geography in the best way possible using the previous passage.'"),
	OpenEndedQuestion(3, "Based on the passage, do you think it would be nice to live in Japan? Why or why not?"),
	OpenEndedQuestion(4, "Compare and contrast the geography where you live to the geography of Japan."),
	OpenEndedQuestion(5, "Based on the Wikipedia passage, what could have Japan's culture been like?"),
	OpenEndedQuestion(9999, "The top voted answers for each question, in order.")
	)

game_questions = (
	MultipleChoiceQuestion(0,
	"The four main islands were: Hokkaido, _______, Kyushu, and Shikoku",
	("Honshu", "Okinawa", "Nara", "Tokyo"),
	"a"),
	MultipleChoiceQuestion(1, 
	"How much of Japan’s land can be farmed?",
	("20%", "30%", "50%", "15%"),
	"a"),
	MultipleChoiceQuestion(2,
	"How did the Japanese get their food?",
	("Fishing", "Hunting", "Trading", "None of the Above"),
	"a"),
	MultipleChoiceQuestion(3,
	"Most of Japan is made up of__________",
	("Islands", "Mountains", "Farmland", "A and B"),
	"d"),
	MultipleChoiceQuestion(4,
	"Why has wildlife in Japan suffered?",
	("Mountains", "Its Population", "The Land", "None of the Above"),
	"d"),
	MultipleChoiceQuestion(5,
	"A lot of Japan’s mountains are volcanoes",
	("True", "False", "whats a volcano", "whats a Japan"),
	"a"),
	MultipleChoiceQuestion(6,
	"Mount Fuji is the highest peak in Japan",
	("True", "False", "aaaaaaaaa", "aaaaaaaa"),
	"a"),
	MultipleChoiceQuestion(7,
	"Japan is not an archipelago",
	("True", "False", "what", "A R C H I P E L A G O"),
	"b"),
	MultipleChoiceQuestion(8,
	"Early Japanese conflict was caused by a lack of water.",
	("True", "False", "A R C H I P E L A G O", "O G A L E P I H C R A"),
	"b")
)
