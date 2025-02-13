import glob
import sys
from flask import Blueprint, Flask, current_app, g, render_template, send_file, session
import ijson
import matplotlib
matplotlib.use('Agg')  # Set non-GUI backend
import matplotlib.pyplot as plt
from datetime import datetime
import os
import uuid
import io

from flaskr.auth import login_required
print('Hello world!', file=sys.stderr)

bp = Blueprint('grades', __name__)

def generate_graph(username):
    static_folder = os.path.join(current_app.root_path, 'static', 'images')
    os.makedirs(static_folder, exist_ok=True)
    
    # Delete prior graphs for the user (files starting with username_)
    pattern = os.path.join(static_folder, f"{username}_*.png")
    for filepath in glob.glob(pattern):
        try:
            os.remove(filepath)
            print(f"Deleted old graph: {filepath}")
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")

    # Generate a new unique filename for the graph
    graph_filename = f"{username}_{uuid.uuid4().hex[:8]}.png"
    graph_path = os.path.join(static_folder, graph_filename)
    
    try:
        with open('user_data.json', 'r') as f:
            user_entries = list(ijson.items(f, f'{username}.item'))
    except FileNotFoundError:
        print("Data file not found")
        return None, "Data file not found"
    
    if not user_entries:
        print("User not found")
        return None, f"User '{username}' not found"
    
    filenames = user_entries[::2]
    grades = user_entries[1::2]
    
    if len(filenames) != len(grades):
        print("Data format error")
        return None, "Data format error"
    
    entry_numbers = list(range(1, len(grades) + 1))
    
    plt.figure()
    plt.plot(entry_numbers, grades, marker='o', linestyle='-')
    plt.xlabel('All Time Grades')
    plt.ylabel('Grade')
    plt.title(f'Grades for {username}')
    plt.xticks(entry_numbers)
    plt.yticks(ticks=[0,10,20,30,40,50,60,70,80,90,100])
    plt.grid(True)
    
    plt.savefig(graph_path)
    plt.close()
    
    return graph_filename, None
@bp.route('/grades')
@login_required
def show_grades():
    username = g.user['username']
    static_folder = os.path.join(current_app.root_path, 'static', 'images')

    # Ensure the directory exists before trying to list its contents
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    user_images = [f for f in os.listdir(static_folder) if f.startswith(username)]
    user_images.sort(reverse=True)
    user_image = user_images[0] if user_images else None

    # Retrieve the latest grade from the user_data.json
    latest_grade = None
    try:
        with open('user_data.json', 'r') as f:
            user_entries = list(ijson.items(f, f'{username}.item'))
        if user_entries:
            # Expecting data in pairs: [filename1, grade1, filename2, grade2, ...]
            grades = user_entries[1::2]
            if grades:
                latest_grade = grades[-1]
    except Exception as e:
        current_app.logger.error("Error reading user data: " + str(e))

    return render_template('user_graph_display.html', user_image=user_image, latest_grade=latest_grade)

def test_generate_graph():
    """Test function for graph generation"""
    test_user = "testuser"
    print(f"Testing graph generation for user: {test_user}")
    graph_filename, error = generate_graph(test_user)
    
    if error:
        print(f"Error: {error}")
    else:
        print(f"Graph generated at: static/images/{graph_filename}")
        print(f"File exists: {os.path.exists(os.path.join('static/images', graph_filename))}")
# Modify the existing __name__ block at the bottom


if __name__ == '__main__':
        test_generate_graph()