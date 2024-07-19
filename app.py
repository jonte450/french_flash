from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FlashCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    french_word = db.Column(db.String(100), nullable=False)
    english_translation = db.Column(db.String(100),nullable=False)

@app.route('/')
def index():
    cards = FlashCard.query.all()
    return render_template('index.html', cards=cards)


@app.route('/add',methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        french_word = request.form['french_word']
        english_translation = request.form['english_translation']
        new_card = FlashCard(french_word=french_word, english_translation= english_translation)
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_card.html')


@app.route('/delete/<int:id>',methods=['POST'])
def delete_card(id):
    card = FlashCard.query.get(id)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>',methods=['GET','POST'])
def update_card(id):
    card = FlashCard.query.get(id)
    if request.method == 'POST':
        card.french_word = request.form['french_word']
        card.english_translation = request.form['english_translation']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_card.html', card=card)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

