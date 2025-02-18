from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import io
import contextlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64

# Import custom data structures
from data_structure import LinkedList, Stack

# Flask app initialization
app = Flask(__name__)
# Enable CORS for all routes
CORS(app)  

# Global instances of our data structures
# For storing login info
user_ll = LinkedList()    
# For project history/autosave
project_stack = Stack()   

# Endpoint to execute code
@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        # Get code from request
        code = request.json.get('code', '')
        
        # Create string buffer to capture output
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        # Capture output
        with contextlib.redirect_stdout(output_buffer):
            with contextlib.redirect_stderr(error_buffer):
                try:
                    # Execute the code
                    exec(code, {'np': np, 'plt': plt})
                    
                    # Check if a plot was created
                    if plt.get_fignums():
                        # Save plot to memory buffer
                        img_buffer = io.BytesIO()
                        plt.savefig(img_buffer, format='png')
                        img_buffer.seek(0)
                        plot_data = base64.b64encode(img_buffer.read()).decode()
                        plt.close('all')  # Clear plots
                    else:
                        plot_data = None
                    
                    return jsonify({
                        'output': output_buffer.getvalue(),
                        'error': error_buffer.getvalue(),
                        'plot': plot_data
                    })
                
                except Exception as e:
                    return jsonify({
                        'error': str(e),
                        'output': output_buffer.getvalue()
                    })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'})

###############################
# New Endpoints for Data Structures
###############################

# Endpoint for user registration.
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    # Expecting "username" and "password_hash" in data.
    user_ll.insert(data)  # Adds to linked list and posts to DB.
    return jsonify({"message": "User registered successfully."}), 201

# Endpoint for user login.
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password_hash")
    user = user_ll.find(username, key_func=lambda x: x.get("username"))
    if user and user.get("password_hash") == password:
        return jsonify({"message": "Login successful."}), 200
    return jsonify({"message": "Invalid credentials."}), 401

# Endpoint to retrieve project history (or autosave records) for a given user.
@app.route('/projects/<int:user_id>', methods=['GET'])
def get_projects(user_id):
    projects = project_stack.get_from_db(user_id)
    return jsonify(projects), 200

# Endpoint to post (save) a new project history/autosave record.
@app.route('/projects', methods=['POST'])
def add_project():
    data = request.json
    # Expecting keys: user_id, project_name, and data in the payload.
    project_stack.push(data)
    return jsonify({"message": "Project saved successfully."}), 201

if __name__ == '__main__':
    app.run(debug=True)