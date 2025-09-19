from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Your portfolio data, now with an enhanced rating system
portfolio_data = {
    "name": "Habib Wasi",
    "title": "Passionate Developer",
    "bio": "Explore my work and get to know me better.",
    "contact": {
        "email": "your.email@example.com",
        "linkedin": "https://linkedin.com/in/yourprofile",
        "github": "https://github.com/yourusername"
    },
    "skills": ["Python", "Flask", "JavaScript", "HTML", "CSS", "TailwindCSS", "Git"],
    "projects": [
        {
            "title": "Project One",
            "description": "A brief description of your first project. What problem does it solve? What technologies were used?",
            "image": "https://placehold.co/600x400/1F2937/E5E7EB?text=Project+1",
            "link": "#",
            "ratings": [],
            "avg_rating": 0
        },
        {
            "title": "Project Two",
            "description": "A brief description of your second project. Highlight the key features and your role in the project.",
            "image": "https://placehold.co/600x400/1F2937/E5E7EB?text=Project+2",
            "link": "#",
            "ratings": [],
            "avg_rating": 0
        },
        {
            "title": "Project Three",
            "description": "A brief description of your third project. What did you learn? What are you most proud of?",
            "image": "https://placehold.co/600x400/1F2937/E5E7EB?text=Project+3",
            "link": "#",
            "ratings": [],
            "avg_rating": 0
        }
    ]
}

@app.route('/')
def home():
    # Geolocation remains on the client-side (in index.html) for best accuracy.
    return render_template('index.html', data=portfolio_data)

@app.route('/rate', methods=['POST'])
def rate_project():
    # This logic is inspired by your new code.
    data = request.get_json()
    project_title = data.get('project')
    rating = data.get('rating')

    # Find the project and update its rating
    project_found = None
    for p in portfolio_data['projects']:
        if p['title'] == project_title:
            project_found = p
            break
    
    if project_found and rating:
        try:
            # Add the new rating and recalculate the average
            numeric_rating = int(rating)
            project_found['ratings'].append(numeric_rating)
            project_found['avg_rating'] = sum(project_found['ratings']) / len(project_found['ratings'])
            return jsonify({
                'status': 'success', 
                'message': f'Thank you for rating {project_title}!',
                'new_avg_rating': round(project_found['avg_rating'], 2)
            })
        except (ValueError, ZeroDivisionError):
             return jsonify({'status': 'error', 'message': 'Invalid rating data.'}), 400

    return jsonify({'status': 'error', 'message': 'Project not found.'}), 404


if __name__ == '__main__':
    app.run(debug=True)

