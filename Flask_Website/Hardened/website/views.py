"""
Store where users can navigate to (that is not related to auth)
"""
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# init blueprint
views = Blueprint('views', __name__)

# Define a view or a route

# Route for homepage. Will run when directed to home (/)
# Login_required decorator will require user to be logged in to view home
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        # Input validation
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        # Only owner of note can delete
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    # Make sure you return something, so empty json
    return jsonify({})
