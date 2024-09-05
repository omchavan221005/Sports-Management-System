from flask import Flask, render_template, request, redirect, url_for, session,send_file
from certificate_generator import generate_certificate  # Import the certificate generation function

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random string

# Mock data for users, tournaments, registrations, schedules, rules, and winners
users = {
    'admin': {'password': 'admin123', 'access_level': 'admin'},
    'user': {'password': 'user123', 'access_level': 'user'}
}

# Mock data for tournaments, registrations, schedules, rules, winners, and sport status
tournaments = [
    {
        'name': 'Spring Sports Fest',
        'date': '2024-09-10',
        'sports': [
            {'name': 'Football', 'status': 'completed'},
            {'name': 'Basketball', 'status': 'completed'},
            {'name': 'Tennis', 'status': 'completed'}
        ],
        'winners': {'Football': 'Team A', 'Basketball': 'Team E', 'Tennis': 'Player A'}
    },
    {
        'name': 'Winter Games',
        'date': '2024-12-05',
        'sports': [
            {'name': 'Cricket', 'status': 'ongoing'},
            {'name': 'Volleyball', 'status': 'ongoing'},
            {'name': 'Badminton', 'status': 'ongoing'}
        ],
        'winners': {}  # Winners not available yet
    }
]

registrations = {
    'Football': [],
    'Basketball': [],
    'Tennis': [],
    'Cricket': [],
    'Volleyball': [],
    'Badminton': []
}

# Mock data for schedules with venues
schedules = {
    'Football': [
        {'match': 'Team A vs Team B', 'date': '2024-09-11', 'time': '10:00 AM', 'venue': 'Stadium A'},
        {'match': 'Team C vs Team D', 'date': '2024-09-12', 'time': '02:00 PM', 'venue': 'Stadium B'}
    ],
    'Basketball': [
        {'match': 'Team E vs Team F', 'date': '2024-09-11', 'time': '12:00 PM', 'venue': 'Arena 1'},
        {'match': 'Team G vs Team H', 'date': '2024-09-12', 'time': '04:00 PM', 'venue': 'Arena 2'}
    ],
    'Tennis': [
        {'match': 'Player A vs Player B', 'date': '2024-09-11', 'time': '09:00 AM', 'venue': 'Court 1'},
        {'match': 'Player C vs Player D', 'date': '2024-09-12', 'time': '03:00 PM', 'venue': 'Court 2'}
    ],
    'Cricket': [
        {'match': 'Team X vs Team Y', 'date': '2024-12-06', 'time': '11:00 AM', 'venue': 'Cricket Ground A'},
        {'match': 'Team Z vs Team W', 'date': '2024-12-07', 'time': '01:00 PM', 'venue': 'Cricket Ground B'}
    ],
    'Volleyball': [
        {'match': 'Team 1 vs Team 2', 'date': '2024-12-06', 'time': '02:00 PM', 'venue': 'Volleyball Court 1'},
        {'match': 'Team 3 vs Team 4', 'date': '2024-12-07', 'time': '04:00 PM', 'venue': 'Volleyball Court 2'}
    ],
    'Badminton': [
        {'match': 'Player E vs Player F', 'date': '2024-12-06', 'time': '10:00 AM', 'venue': 'Badminton Hall 1'},
        {'match': 'Player G vs Player H', 'date': '2024-12-07', 'time': '12:00 PM', 'venue': 'Badminton Hall 2'}
    ]
}

rules_and_regulations = {
    'Football': '1. The game consists of two halves of 45 minutes each. 2. Each team consists of 11 players including the goalkeeper. 3. The offside rule applies.',
    'Basketball': '1. The game is played in four quarters of 12 minutes each. 2. Each team consists of 5 players. 3. The three-point line is 23.75 feet from the basket.',
    'Tennis': '1. Matches are played in best of 3 or 5 sets. 2. Players serve from behind the baseline. 3. The ball must land within the opponent’s service box.',
    'Cricket': '1. Each team consists of 11 players. 2. The game is played in innings, with each team batting once. 3. The bowler must deliver the ball with a straight arm.',
    'Volleyball': '1. Each team has 6 players on the court. 2. Matches are played in best of 5 sets. 3. The ball must be hit over the net and land in the opponent’s court.',
    'Badminton': '1. The game is played in 3 sets. 2. Players use a shuttlecock and rackets. 3. Points are scored by hitting the shuttlecock over the net and into the opponent’s court.'
}

# Example of winner data with additional fields for certificate generation
winners = {
    'Football': {'name': 'Team A', 'certificate_details': {'team_name': 'Team A', 'event': 'Football Championship'}},
    'Basketball': {'name': 'Team E', 'certificate_details': {'team_name': 'Team E', 'event': 'Basketball Tournament'}},
    'Tennis': {'name': 'Player A', 'certificate_details': {'player_name': 'Player A', 'event': 'Tennis Open'}}
}

# Home route
@app.route('/')
def home():
    return render_template('home.html', user=session.get('user'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['user'] = {'username': username, 'access_level': user['access_level']}
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials, please try again.'
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# Tournaments route
@app.route('/tournaments')
def view_tournaments():
    return render_template('tournaments.html', tournaments=tournaments)

@app.route('/tournament/<tournament_name>')
def tournament_details(tournament_name):
    tournament = next((t for t in tournaments if t['name'] == tournament_name), None)
    if tournament:
        return render_template('tournament_details.html', tournament=tournament, user=session.get('user'))
    return 'Tournament not found.', 404

@app.route('/sport/<sport>')
def sport_details(sport):
    sport_info = next((s for t in tournaments for s in t['sports'] if s['name'] == sport), None)
    if not sport_info:
        return 'Sport not found.', 404

    schedule = schedules.get(sport, [])
    rules = rules_and_regulations.get(sport, 'No rules available.')
    return render_template('sport_details.html', sport=sport, schedule=schedule, rules=rules, sport_status=sport_info['status'], user=session.get('user'))

@app.route('/register/<sport>', methods=['GET', 'POST'])
def register(sport):
    if request.method == 'POST':
        username = session.get('user', {}).get('username')
        if not username:
            return redirect(url_for('login'))
        
        player_name = request.form['player_name']
        if player_name:
            registrations[sport].append({'username': username, 'player_name': player_name})
        return redirect(url_for('view_schedule', sport=sport))

    return render_template('register.html', sport=sport)

@app.route('/schedule/<sport>')
def view_schedule(sport):
    user = session.get('user', {})
    schedule = schedules.get(sport, [])
    if user and user.get('access_level') == 'admin':
        return render_template('schedule.html', sport=sport, schedule=schedule, user=user)
    elif user:
        return render_template('schedule.html', sport=sport, schedule=schedule, user=user)
    else:
        return redirect(url_for('login'))

# Admin route to add/update schedule (for demonstration purposes)
@app.route('/admin/schedule/<sport>', methods=['GET', 'POST'])
def manage_schedule(sport):
    user = session.get('user', {})
    if user.get('access_level') != 'admin':
        return 'Access denied. Only admins can manage schedules.', 403

    if request.method == 'POST':
        match = request.form['match']
        date = request.form['date']
        time = request.form['time']
        if match and date and time:
            schedules.setdefault(sport, []).append({'match': match, 'date': date, 'time': time})
        return redirect(url_for('view_schedule', sport=sport))

    return render_template('manage_schedule.html', sport=sport)

@app.route('/generate_certificate/<sport>')
def generate_certificate_route(sport):
    winner = winners.get(sport)
    if not winner:
        return 'Winner not found.', 404
    
    file_name = generate_certificate(winner)
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
