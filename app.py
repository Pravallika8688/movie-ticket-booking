from flask import Flask, render_template, request, redirect, url_for, session
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "bookmyshow123"

# Cities list - idi nee all_theatres.html lo top-bar kosam
CITIES = ["Vizag", "Rajahmundry", "Kakinada", "Peddapuram"]

THEATRES_BY_CITY = {
    'Vizag': ['PVR Phoenix Mall', 'INOX Varun Beach', 'Jagadamba Theatre'],
    'Rajahmundry': ['Anand Theatre', 'Sri Kanya Complex', 'Apsara Theatre'],
    'Kakinada': ['Devi Multiplex', 'Anand Theatre Kkd', 'Surya Theatre'],
    'Peddapuram': ['Urvashi Theatre', 'Lakshmi Theatre', 'Sri Balaji Theatre']
}

movies = [
    {"id": "1", "title": "Devara"},
    {"id": "2", "title": "Kalki 2898 AD"},
    {"id": "3", "title": "OG"},
]

SHOW_TIMES = ["10:00 AM", "01:30 PM", "06:00 PM", "09:30 PM"]
ALL_SEATS = [f"{r}{c}" for r in "ABCDEFG" for c in range(1, 11)]

@app.route('/')
def index():
    return redirect(url_for('select_city'))

@app.route('/select-city')
def select_city():
    return render_template('region.html', cities=CITIES)

@app.route('/set-city/<city>')
def set_city(city):
    # lower case kuda work avvali ani
    for c in CITIES:
        if c.lower() == city.lower():
            session['city'] = c
            break
    return redirect(url_for('all_theatres'))

@app.route('/theatres')
def all_theatres():
    if 'city' not in session:
        return redirect(url_for('select_city'))
    city = session['city']
    theatres = THEATRES_BY_CITY.get(city, [])
    # IKKADA cities=CITIES add chesa - nee error ki fix idi
    return render_template('all_theatres.html', city=city, theatres=theatres, cities=CITIES)

@app.route('/theatre/<theatre_name>')
def theatre_shows(theatre_name):
    if 'city' not in session:
        return redirect(url_for('select_city'))
    dates = [(datetime.now() + timedelta(days=i)).strftime("%d %b - %a") for i in range(4)]
    return render_template('theatre_shows.html', city=session['city'], theatre=theatre_name, movies=movies, dates=dates, show_times=SHOW_TIMES)
@app.route('/book')
def book_page():
    theatre = request.args.get('theatre')
    movie_id = request.args.get('movie_id')
    date = request.args.get('date')
    show = request.args.get('show')
    movie = next((m for m in movies if str(m['id']) == str(movie_id)), movies[0])

    # 70 seats generate
    ALL_SEATS = [f"{chr(65+i//10)}{i%10+1}" for i in range(70)] # A1 to G10

    return render_template('book.html', theatre=theatre, movie=movie, date=date, show=show, seats=ALL_SEATS)

@app.route('/success', methods=['POST'])
def success():
    theatre = request.form.get('theatre')
    movie = request.form.get('movie_title')
    date_only = request.form.get('date_only')
    show_time = request.form.get('show_time')
    seats = request.form.getlist('seats')

    if not seats:
        seats = ['No seats selected']
        total = 0
    else:
        total = len(seats) * 150

    booking_id = "BMS" + str(random.randint(400000, 499999))

    return render_template('success.html',
                           theatre=theatre,
                           movie=movie,
                           date=date_only,
                           show_time=show_time,
                           seats=seats,
                           total=total,
                           booking_id=booking_id)

if __name__ == '__main__':
    app.run(debug=True)

