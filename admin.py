import os
import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import uuid
import csv
import io

from app import db
from models import User, Attendance
from utils import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get attendance statistics
    total_users = User.query.count()
    
    # Today's statistics
    today = datetime.datetime.now().date()
    today_start = datetime.datetime.combine(today, datetime.time.min)
    today_end = datetime.datetime.combine(today, datetime.time.max)
    today_attendance = Attendance.query.filter(
        Attendance.check_in_time >= today_start,
        Attendance.check_in_time <= today_end
    ).count()
    
    # Get recent attendance records
    recent_attendance = db.session.query(
        Attendance, User
    ).join(
        User, Attendance.user_id == User.id
    ).order_by(
        Attendance.check_in_time.desc()
    ).limit(10).all()
    
    # Monthly statistics
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    
    monthly_stats = db.session.query(
        db.func.extract('day', Attendance.check_in_time).label('day'),
        db.func.count(Attendance.id).label('count')
    ).filter(
        db.extract('month', Attendance.check_in_time) == current_month,
        db.extract('year', Attendance.check_in_time) == current_year
    ).group_by('day').all()
    
    # Format data for chart
    days = [d[0] for d in monthly_stats]
    counts = [d[1] for d in monthly_stats]
    
    return render_template(
        'admin/index.html',
        total_users=total_users,
        today_attendance=today_attendance,
        recent_attendance=recent_attendance,
        days=days,
        counts=counts
    )


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    search = request.args.get('search', '')
    role = request.args.get('role', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (User.full_name.ilike(f'%{search}%'))
        )
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.order_by(User.created_at.desc()).all()
    
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        department = request.form.get('department')
        position = request.form.get('position')
        
        # Validate username and email
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('admin.add_user'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('admin.add_user'))
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            role=role,
            department=department,
            position=position
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('User has been created successfully.', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/edit_user.html', user=None)


@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        department = request.form.get('department')
        position = request.form.get('position')
        password = request.form.get('password')
        
        # Check if email already exists
        if email != user.email and User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        # Update user
        user.email = email
        user.full_name = full_name
        user.role = role
        user.department = department
        user.position = position
        
        if password:
            user.set_password(password)
        
        db.session.commit()
        
        flash('User has been updated successfully.', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/edit_user.html', user=user)


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User has been deleted successfully.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/attendance')
@login_required
@admin_required
def attendance():
    search = request.args.get('search', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    status = request.args.get('status', '')
    
    # Base query with join
    query = db.session.query(Attendance, User).join(User, Attendance.user_id == User.id)
    
    # Apply filters
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (User.full_name.ilike(f'%{search}%'))
        )
    
    if date_from:
        date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(Attendance.check_in_time >= date_from_obj)
    
    if date_to:
        date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
        query = query.filter(Attendance.check_in_time <= date_to_obj)
    
    if status:
        query = query.filter(Attendance.status == status)
    
    # Order by check-in time (newest first)
    attendances = query.order_by(Attendance.check_in_time.desc()).all()
    
    return render_template(
        'admin/attendance.html',
        attendances=attendances,
        search=search,
        date_from=date_from,
        date_to=date_to,
        status=status
    )


@admin_bp.route('/attendance/delete/<int:attendance_id>', methods=['POST'])
@login_required
@admin_required
def delete_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    
    db.session.delete(attendance)
    db.session.commit()
    
    flash('Attendance record has been deleted successfully.', 'success')
    return redirect(url_for('admin.attendance'))


@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    # Department statistics
    dept_stats = db.session.query(
        User.department,
        db.func.count(User.id).label('user_count')
    ).group_by(User.department).all()
    
    # Attendance statistics by status
    status_stats = db.session.query(
        Attendance.status,
        db.func.count(Attendance.id).label('count')
    ).group_by(Attendance.status).all()
    
    # Weekly attendance
    today = datetime.datetime.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    
    daily_stats = []
    for i in range(7):
        day = start_of_week + datetime.timedelta(days=i)
        day_start = datetime.datetime.combine(day, datetime.time.min)
        day_end = datetime.datetime.combine(day, datetime.time.max)
        count = Attendance.query.filter(
            Attendance.check_in_time >= day_start,
            Attendance.check_in_time <= day_end
        ).count()
        daily_stats.append({
            'day': day.strftime('%A'),
            'date': day.strftime('%Y-%m-%d'),
            'count': count
        })
    
    return render_template(
        'admin/reports.html',
        dept_stats=dept_stats,
        status_stats=status_stats,
        daily_stats=daily_stats
    )


@admin_bp.route('/export/attendance', methods=['GET'])
@login_required
@admin_required
def export_attendance():
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = db.session.query(
        User.id,
        User.username,
        User.full_name,
        User.department,
        Attendance.check_in_time,
        Attendance.check_out_time,
        Attendance.status,
        Attendance.location,
        Attendance.notes
    ).join(User, Attendance.user_id == User.id)
    
    # Apply date filters
    if date_from:
        date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(Attendance.check_in_time >= date_from_obj)
    
    if date_to:
        date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
        query = query.filter(Attendance.check_in_time <= date_to_obj)
    
    # Order by check-in time
    results = query.order_by(Attendance.check_in_time.desc()).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'User ID', 'Username', 'Full Name', 'Department',
        'Check-in Time', 'Check-out Time', 'Status', 'Location', 'Notes'
    ])
    
    # Write data
    for row in results:
        writer.writerow([
            row.id,
            row.username,
            row.full_name,
            row.department,
            row.check_in_time.strftime('%Y-%m-%d %H:%M:%S') if row.check_in_time else '',
            row.check_out_time.strftime('%Y-%m-%d %H:%M:%S') if row.check_out_time else '',
            row.status,
            row.location,
            row.notes
        ])
    
    # Prepare response
    from flask import Response
    output.seek(0)
    
    filename = f"attendance_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )
