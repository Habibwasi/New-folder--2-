from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# --- Portfolio Data ---
# We'll keep all the data here for simplicity.
portfolio_data = {
    "name": "Habib Wasi",
    "title": "Passionate Developer",
    "bio": "Explore my work and get to know me better.",
    "about": "Hello! I'm Habib Wasi, a developer with a passion for creating elegant and efficient solutions. I have experience in web development, leveraging modern technologies to build responsive and user-friendly applications. I'm a quick learner and always eager to take on new challenges.",
    "contact": {
        "email": "your.email@example.com",
        "linkedin": "https://linkedin.com/in/yourprofile",
        "github": "https://github.com/yourusername"
    },
    "skills": ["Python", "Flask", "JavaScript", "HTML", "CSS", "TailwindCSS", "Git"],
    "projects": [
        {
            "id": 0,
            "title": "Project One",
            "description": "A brief description of your first project. What problem does it solve?",
            "image": "https://placehold.co/600x400/1F2937/E5E7EB?text=Project+1",
            "link": "#",
            "ratings": [],
            "avg_rating": 0
        },
        {
            "id": 1,
            "title": "Project Two",
            "description": "A brief description of your second project. Highlight key features.",
            "image": "https://placehold.co/600x400/1F2937/E5E7EB?text=Project+2",
            "link": "#",
            "ratings": [],
            "avg_rating": 0
        },
        {
            "id": 2,
            "title": "Project Three",
            "description": "A brief description of your third project. What did you learn?",
            "image": "https://placehold.co/600x400/1F2937/E5E7EB?text=Project+3",
            "link": "#",
            "ratings": [],
            "avg_rating": 0
        }
    ]
}

# --- Routes for Each Page ---

@app.route('/')
def home():
    # This logic now runs on the server to generate the welcome message.
    # NOTE: On a server, this may show the server's location, not the user's.
    welcome_message = "Welcome!"
    try:
        ip_info = requests.get('https://ipapi.co/json/').json()
        city = ip_info.get('city', 'your area')
        welcome_message = f"Welcome from {city}!"
    except Exception as e:
        print(f"Could not fetch location: {e}")
        welcome_message = "Welcome!" # Fallback message

    return render_template('index.html', data=portfolio_data, welcome_message=welcome_message)

@app.route('/about')
def about():
    return render_template('about.html', data=portfolio_data)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=portfolio_data['projects'])

@app.route('/contact')
def contact():
    return render_template('contact.html', contact_info=portfolio_data['contact'])

@app.route('/rate_project/<int:project_id>', methods=['POST'])
def rate_project(project_id):
    rating_data = request.get_json()
    rating = rating_data.get('rating')

    project = next((p for p in portfolio_data['projects'] if p['id'] == project_id), None)

    if project and rating:
        try:
            numeric_rating = int(rating)
            project['ratings'].append(numeric_rating)
            project['avg_rating'] = sum(project['ratings']) / len(project['ratings'])
            return jsonify({
                'status': 'success',
                'new_avg_rating': round(project['avg_rating'], 2)
            })
        except (ValueError, ZeroDivisionError):
            return jsonify({'status': 'error', 'message': 'Invalid rating data.'}), 400
    
    return jsonify({'status': 'error', 'message': 'Project not found.'}), 404


if __name__ == '__main__':
    app.run(debug=True)

