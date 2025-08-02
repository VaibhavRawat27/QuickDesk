import os
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, redirect, url_for, request,
    flash, send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user, UserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# --- App setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'quickdesksecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickdesk.db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# --- Models ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')

    is_active = db.Column(db.Boolean, default=True)

    tickets = db.relationship('Ticket', backref='owner', lazy=True)
    replies = db.relationship('TicketReply', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    attachment = db.Column(db.String(200))
    status = db.Column(db.String(50), default='Open')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(150), nullable=False)  # ✅ store user name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    replies = db.relationship('TicketReply', backref='ticket', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class TicketReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_name = db.Column(db.String(150), nullable=False)  # ✅ store reply author name
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# --- Login loader ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Role protection ---
def role_required(role_name):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role_name:
                flash("Access denied.", "warning")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper


# --- Routes ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            flash("Email already registered.", "danger")
            return redirect(url_for('register'))
        user = User(
            email=request.form['email'],
            name=request.form['name'],
            role='user'
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('Registered! Please log in.', "success")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Logged in successfully.', "success")

            # ✅ Role-based redirection
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'agent':
                return redirect(url_for('agent_dashboard'))
            else:
                return redirect(url_for('dashboard'))

        flash('Invalid credentials', "danger")
    return render_template('login.html')



@app.route('/admin/create-agent', methods=['POST'])
@login_required
@role_required('admin')
def create_agent():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if User.query.filter_by(email=email).first():
        flash("Email already exists.", "danger")
        return redirect(url_for('admin_dashboard'))

    new_agent = User(name=name, email=email, role='agent')
    new_agent.set_password(password)
    db.session.add(new_agent)
    db.session.commit()

    flash("Support agent created successfully.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-category', methods=['POST'])
@login_required
@role_required('admin')
def add_category():
    name = request.form.get('category')
    if name and not Category.query.filter_by(name=name).first():
        db.session.add(Category(name=name))
        db.session.commit()
        flash("Category added.", "success")
    else:
        flash("Category already exists or invalid.", "warning")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete-category/<int:category_id>')
@login_required
@role_required('admin')
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted.", "info")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/category/<string:category>')
@login_required
@role_required('admin')
def filter_by_category(category):
    tickets = Ticket.query.filter_by(category=category).order_by(Ticket.created_at.desc()).all()
    return render_template('admin_dashboard.html', tickets=tickets, filtered_category=category)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out.', "info")
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'user':
        flash("Access denied.", "warning")
        return redirect(url_for('login'))
    
    status_filter = request.args.get('status')
    query = Ticket.query.filter_by(user_id=current_user.id)

    # Filter by status if given
    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)

    tickets = query.order_by(Ticket.created_at.desc()).all()

    # Counts for tabs
    all_count = Ticket.query.filter_by(user_id=current_user.id).count()
    open_count = Ticket.query.filter_by(user_id=current_user.id, status='Open').count()
    inprogress_count = Ticket.query.filter_by(user_id=current_user.id, status='In Progress').count()
    resolved_count = Ticket.query.filter_by(user_id=current_user.id, status='Resolved').count()
    closed_count = Ticket.query.filter_by(user_id=current_user.id, status='Closed').count()

    return render_template('dashboard.html', tickets=tickets,
                           all_count=all_count, open_count=open_count,
                           inprogress_count=inprogress_count,
                           resolved_count=resolved_count,
                           closed_count=closed_count,
                           current_status=status_filter or 'all')



@app.route('/ticket/new', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        file = request.files.get('attachment')
        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        ticket = Ticket(
            subject=request.form['subject'],
            description=request.form['description'],
            category=request.form['category'],
            attachment=filename,
            user_id=current_user.id,
            user_name=current_user.name,
            status='Open'
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket created successfully!', "success")
        return redirect(url_for('dashboard'))
    return render_template('create_ticket.html')


@app.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role == 'user' and ticket.user_id != current_user.id:
        flash("Access denied.", "warning")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        reply_content = request.form.get('reply')
        if reply_content:
            reply = TicketReply(
                content=reply_content,
                ticket_id=ticket.id,
                user_id=current_user.id,
                author_name=current_user.name
            )
            db.session.add(reply)
            db.session.commit()
            flash('Reply added.', "success")
    replies = TicketReply.query.filter_by(ticket_id=ticket_id).order_by(TicketReply.created_at.asc()).all()
    return render_template('ticket_detail.html', ticket=ticket, replies=replies)


@app.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    status_filter = request.args.get('status')
    user_filter = request.args.get('user_role')

    # Filter tickets
    ticket_query = Ticket.query
    if status_filter and status_filter != 'all':
        ticket_query = ticket_query.filter_by(status=status_filter)
    tickets = ticket_query.order_by(Ticket.created_at.desc()).all()

    # Status counts for ticket tabs
    all_count = Ticket.query.count()
    open_count = Ticket.query.filter_by(status='Open').count()
    inprogress_count = Ticket.query.filter_by(status='In Progress').count()
    resolved_count = Ticket.query.filter_by(status='Resolved').count()
    closed_count = Ticket.query.filter_by(status='Closed').count()

    # Filter users by role
    if user_filter and user_filter != 'all':
        users = User.query.filter_by(role=user_filter).order_by(User.id.asc()).all()
    else:
        users = User.query.order_by(User.id.asc()).all()

    employee_count = User.query.filter_by(role='user').count()
    agent_count = User.query.filter_by(role='agent').count()
    admin_count = User.query.filter_by(role='admin').count()
    total_users = User.query.count()

   
    categories = Category.query.order_by(Category.name.asc()).all()

    return render_template('admin_dashboard.html',
                           users=users,
                           tickets=tickets,
                           all_count=all_count,
                           open_count=open_count,
                           inprogress_count=inprogress_count,
                           resolved_count=resolved_count,
                           closed_count=closed_count,
                           current_status=status_filter or 'all',
                           current_user_role=user_filter or 'all',
                           total_users=total_users,
                           employee_count=employee_count,
                           agent_count=agent_count,
                           admin_count=admin_count,
                           categories=categories)  


@app.route('/admin/user/<int:user_id>/toggle_status')
@login_required
@role_required('admin')
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash("Cannot deactivate another admin.", "danger")
        return redirect(url_for('admin_dashboard'))

    user.is_active = not user.is_active
    db.session.commit()
    flash(f"User {'activated' if user.is_active else 'deactivated'}.", "success")
    return redirect(url_for('admin_dashboard'))


@app.route('/agent')
@login_required
@role_required('agent')
def agent_dashboard():
    status_filter = request.args.get('status')
    if status_filter and status_filter != 'all':
        tickets = Ticket.query.filter_by(status=status_filter).order_by(Ticket.created_at.desc()).all()
    else:
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()

    # Count tickets by status
    all_count = Ticket.query.count()
    open_count = Ticket.query.filter_by(status='Open').count()
    inprogress_count = Ticket.query.filter_by(status='In Progress').count()
    resolved_count = Ticket.query.filter_by(status='Resolved').count()
    closed_count = Ticket.query.filter_by(status='Closed').count()

    return render_template('agent_dashboard.html', tickets=tickets,
                           all_count=all_count, open_count=open_count,
                           inprogress_count=inprogress_count,
                           resolved_count=resolved_count,
                           closed_count=closed_count,
                           current_status=status_filter or 'all')



@app.route('/agent/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
@role_required('agent')
def agent_ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if request.method == 'POST':
        status = request.form.get('status')
        if status:
            ticket.status = status
        reply_content = request.form.get('reply')
        if reply_content:
            reply = TicketReply(
                content=reply_content,
                ticket_id=ticket.id,
                user_id=current_user.id,
                author_name=current_user.name
            )
            db.session.add(reply)
        db.session.commit()
        flash('Ticket updated.', "success")
    replies = TicketReply.query.filter_by(ticket_id=ticket_id).order_by(TicketReply.created_at.asc()).all()
    return render_template('agent_ticket_detail.html', ticket=ticket, replies=replies)


@app.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# CLI helper to create default users
@app.cli.command("create-default-users")
def create_default_users():
    if not User.query.filter_by(email='admin@quick.com').first():
        admin = User(name='Admin', email='admin@quick.com', role='admin')
        admin.set_password('admin')
        db.session.add(admin)
    if not User.query.filter_by(email='agent@quick.com').first():
        agent = User(name='Agent', email='agent@quick.com', role='agent')
        agent.set_password('agent')
        db.session.add(agent)
    db.session.commit()
    print("✅ Default admin and agent created:")
    print("🔑 admin@quick.com / admin")
    print("🔑 agent@quick.com / agent")

@app.cli.command("create-default-categories")
def create_default_categories():
    defaults = ['Technical', 'Billing', 'General']
    added = 0
    for name in defaults:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
            added += 1
    db.session.commit()
    if added:
        print(f"✅ Added {added} default categories: {', '.join(defaults)}")
    else:
        print("ℹ️ Default categories already exist.")

@app.route('/ticket/<int:ticket_id>')
@login_required
@role_required('admin')  # Optional: restrict to admin or agent
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('view_ticket.html', ticket=ticket)

# --- Entry Point ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
