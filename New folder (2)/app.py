from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

projects_data = [
    {
        'id': 0,
        'title': 'Project One',
        'description': 'A brief description of Project One.',
        'image': 'project1.png',
        'live_demo': '#',
        'ratings': [],
        'avg_rating': 0
    },
    {
        'id': 1,
        'title': 'Project Two',
        'description': 'A brief description of Project Two.',
        'image': 'project2.png',
        'live_demo': '#',
        'ratings': [],
        'avg_rating': 0
    }
]

def get_location_message():
    try:
        ip_info = requests.get('https://ipinfo.io/json').json()
        city = ip_info.get('city', 'your city')
        return f"Welcome from {city}!"
    except Exception:
        return "Welcome!"

@app.route('/')
def home():
    welcome_message = get_location_message()
    return render_template('index.html', welcome_message=welcome_message)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects_data)

@app.route('/rate_project/<int:project_id>', methods=['POST'])
def rate_project(project_id):
    rating = request.json.get('rating')
    if rating and 0 < rating <= 5:
        project = projects_data[project_id]
        project['ratings'].append(rating)
        project['avg_rating'] = sum(project['ratings']) / len(project['ratings'])
        return jsonify({'success': True, 'avg_rating': project['avg_rating']})
    return jsonify({'success': False})

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
