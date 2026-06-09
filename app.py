from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ── Model ────────────────────────────────────────────
class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    status      = db.Column(db.String(20), default='pending')
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'description': self.description,
            'status':      self.status,
            'created_at':  self.created_at.isoformat()
        }

with app.app_context():
    db.create_all()

# ── Routes ───────────────────────────────────────────

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    if data.get('status') and data['status'] not in ['pending', 'in_progress', 'done']:
        return jsonify({'error': 'Invalid status value'}), 400
    task = Task(
        title       = data['title'],
        description = data.get('description', ''),
        status      = data.get('status', 'pending')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    status_filter = request.args.get('status')
    if status_filter:
        tasks = Task.query.filter_by(status=status_filter).all()
    else:
        tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks]), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        if data['status'] not in ['pending', 'in_progress', 'done']:
            return jsonify({'error': 'Invalid status value'}), 400
        task.status = data['status']
    db.session.commit()
    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task {task_id} deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
