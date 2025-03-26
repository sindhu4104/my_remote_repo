from flask import Flask, render_template_string, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "mysecretkey"  # Needed for session management

# Our list of questions
questions = [
    {"question": "1. Who was the first President of the United States?",
     "options": ["A) Thomas Jefferson", "B) Abraham Lincoln", "C) George Washington", "D) John Adams"],
     "answer": "c"},

    {"question": "2. Which ancient civilization built the pyramids?",
     "options": ["A) Romans", "B) Greeks", "C) Egyptians", "D) Mesopotamians"],
     "answer": "c"},

    {"question": "3. During which war was the Battle of Gettysburg fought?",
     "options": ["A) World War I", "B) World War II", "C) American Revolutionary War", "D) American Civil War"],
     "answer": "d"},

    {"question": "4. Who was the British Prime Minister during World War II?",
     "options": ["A) Neville Chamberlain", "B) Winston Churchill", "C) Margaret Thatcher", "D) Tony Blair"],
     "answer": "b"},

    {"question": "5. What year did the Berlin Wall fall?",
     "options": ["A) 1985", "B) 1987", "C) 1989", "D) 1991"],
     "answer": "c"},

    {"question": "6. Who was the first Emperor of Rome?",
     "options": ["A) Julius Caesar", "B) Augustus", "C) Nero", "D) Caligula"],
     "answer": "b"},

    {"question": "7. Which treaty ended World War I?",
     "options": ["A) Treaty of Versailles", "B) Treaty of Tordesillas", "C) Treaty of Paris", "D) Treaty of Westphalia"],
     "answer": "a"},

    {"question": """8. Which revolution is known for the slogan "Liberty, Equality, Fraternity"?""",
     "options": ["A) American Revolution", "B) French Revolution", "C) Russian Revolution", "D) Chinese Revolution"],
     "answer": "b"},

    {"question": "9. Who discovered the sea route to India in 1498?",
     "options": ["A) Christopher Columbus", "B) Ferdinand Magellan", "C) Vasco da Gama", "D) Hernán Cortés"],
     "answer": "c"},

    {"question": "10. Which empire was ruled by Genghis Khan?",
     "options": ["A) Ottoman Empire", "B) Mongol Empire", "C) Byzantine Empire", "D) Persian Empire"],
     "answer": "b"}
]

# Home page: a simple welcome screen with a Start button.
@app.route("/")
def index():
    return render_template_string("""
    <html>
    <head>
      <title>Quiz Game</title>
    </head>
    <body style="font-family: sans-serif;">
      <h1>Welcome to the Quiz!</h1>
      <form action="{{ url_for('start_quiz') }}" method="post">
        <button type="submit">Start Quiz</button>
      </form>
    </body>
    </html>
    """)

# This route initializes the quiz session variables and then redirects to the first question.
@app.route("/start", methods=["POST"])
def start_quiz():
    session["score"] = 0
    session["current"] = 0
    session["correct_attempts"] = 0
    session["wrong_attempts"] = 0
    return redirect(url_for("question"))

# Display the current question.
@app.route("/question", methods=["GET"])
def question():
    current = session.get("current", 0)
    if current >= len(questions):
        return redirect(url_for("result"))
    q = questions[current]
    return render_template_string("""
    <html>
    <head>
      <title>Question {{ current + 1 }}</title>
    </head>
    <body style="font-family: sans-serif;">
      {% with messages = get_flashed_messages() %}
        {% if messages %}
          <ul style="color: green;">
          {% for msg in messages %}
            <li>{{ msg }}</li>
          {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}
      <h3>{{ q.question }}</h3>
      <form method="post" action="{{ url_for('submit') }}">
        {% for opt in q.options %}
          <!-- The radio value is the first character (e.g., "A") in lower-case -->
          <input type="radio" name="answer" value="{{ opt[0]|lower }}" required> {{ opt }}<br><br>
        {% endfor %}
        <button type="submit">Submit Answer</button>
      </form>
    </body>
    </html>
    """, q=q, current=current)

# Process the submitted answer, update the score, and move to the next question.
@app.route("/submit", methods=["POST"])
def submit():
    current = session.get("current", 0)
    if current >= len(questions):
        return redirect(url_for("result"))

    selected_answer = request.form.get("answer")
    q = questions[current]
    correct_answer = q["answer"]
    
    if selected_answer and selected_answer.lower() == correct_answer.lower():
        flash("Hurrahhh!!!! It's a correct answer.")
        session["score"] = session.get("score", 0) + 10
        session["correct_attempts"] = session.get("correct_attempts", 0) + 1
    else:
        flash("Ho no ...... It's a wrong answer.")
        flash(f"The correct answer is {correct_answer.upper()}.")
        session["wrong_attempts"] = session.get("wrong_attempts", 0) + 1

    session["current"] = current + 1
    return redirect(url_for("question"))

# Results page: shows final score and attempts.
@app.route("/result")
def result():
    score = session.get("score", 0)
    correct_attempts = session.get("correct_attempts", 0)
    wrong_attempts = session.get("wrong_attempts", 0)
    total = len(questions)
    return render_template_string("""
    <html>
    <head>
      <title>Quiz Results</title>
    </head>
    <body style="font-family: sans-serif;">
      <h1>Your Final Score: {{ score }}</h1>
      <p>Correct Attempts: {{ correct_attempts }} / {{ total }}</p>
      <p>Wrong Attempts: {{ wrong_attempts }} / {{ total }}</p>
      {% if score == total * 10 %}
        <h2>Applause !!!!! That's great!</h2>
      {% endif %}
      <br>
      <a href="{{ url_for('index') }}">Restart Quiz</a>
    </body>
    </html>
    """, score=score, correct_attempts=correct_attempts, wrong_attempts=wrong_attempts, total=total)

if __name__ == "__main__":
    app.run(debug=True)
