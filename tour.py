from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tours.db'
db = SQLAlchemy(app)


class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    tour_title = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(10), nullable=False)

    tour = db.relationship('Tour', backref=db.backref('orders', lazy=True))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    tours = Tour.query.all()
    return render_template('main.html', tours=tours)


@app.route('/my_tours')
def booked_tours():
    orders = Order.query.all()
    return render_template('my_tours.html', booked_tours=orders)


@app.route('/add_tour', methods=['GET', 'POST'])
def add_tour():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image = request.form.get('image')

        new_tour = Tour(title=title, description=description, image=image)
        db.session.add(new_tour)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_tour.html')


@app.route('/book_tour/<int:tour_id>', methods=['POST'])
def book_tour(tour_id):
    surname = request.form.get('surname')
    name = request.form.get('name')
    date = request.form.get('date')

    order = Order(tour_id=tour_id, surname=surname, name=name, date=date)
    db.session.add(order)
    db.session.commit()

    return redirect(url_for('view_tour', tour_id=tour_id))


@app.route('/tour/<int:tour_id>', methods=['GET', 'POST'])
def view_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)

    if request.method == 'POST':
        surname = request.form.get('surname')
        name = request.form.get('name')
        date = request.form.get('date')

        order = Order(tour_id=tour_id, surname=surname, name=name, date=date)
        db.session.add(order)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('view_tour.html', tour=tour)


if __name__ == '__main__':
    app.run(debug=True)
