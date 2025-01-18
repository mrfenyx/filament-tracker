from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import FilamentRoll, PrintJob

@app.route('/')
def index():
    rolls = FilamentRoll.query.all()
    print_jobs = PrintJob.query.order_by(PrintJob.id.desc()).all()  # Show latest prints first
    return render_template('index.html', rolls=rolls, print_jobs=print_jobs)

@app.route('/add_roll', methods=['POST'])
def add_roll():
    maker = request.form['maker']
    color = request.form['color']
    total_weight = float(request.form['total_weight'])
    remaining_weight = float(request.form['remaining_weight'])

    roll = FilamentRoll(maker=maker, color=color, total_weight=total_weight, remaining_weight=remaining_weight, in_use=True)
    db.session.add(roll)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/add_print', methods=['POST'])
def add_print():
    filament_id = int(request.form['filament_id'])
    length_used = float(request.form['length_used'])
    weight_used = float(request.form['weight_used'])  # Ensure float conversion
    project_name = request.form['project_name']

    roll = FilamentRoll.query.get(filament_id)
    if roll and roll.remaining_weight >= weight_used:
        print_job = PrintJob(filament_id=filament_id, length_used=length_used, weight_used=weight_used, project_name=project_name)
        db.session.add(print_job)
        roll.remaining_weight -= weight_used
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_roll/<int:roll_id>', methods=['POST'])
def delete_roll(roll_id):
    roll = FilamentRoll.query.get_or_404(roll_id)
    
    # Ensure all associated print jobs are deleted first
    PrintJob.query.filter_by(filament_id=roll.id).delete()

    db.session.delete(roll)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete_print/<int:print_id>', methods=['POST'])
def delete_print(print_id):
    print_job = PrintJob.query.get_or_404(print_id)

    # Restore the filament roll’s remaining weight
    filament = FilamentRoll.query.get(print_job.filament_id)
    if filament:
        filament.remaining_weight += print_job.weight_used

    db.session.delete(print_job)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/edit_roll/<int:roll_id>', methods=['POST'])
def edit_roll(roll_id):
    roll = FilamentRoll.query.get_or_404(roll_id)

    roll.maker = request.form['maker']
    roll.color = request.form['color']
    roll.total_weight = float(request.form['total_weight'])
    roll.remaining_weight = float(request.form['remaining_weight'])
    roll.in_use = 'in_use' in request.form  # Checkbox handling

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_print/<int:print_id>', methods=['POST'])
def edit_print(print_id):
    print_job = PrintJob.query.get_or_404(print_id)
    filament = FilamentRoll.query.get(print_job.filament_id)

    # Restore previous filament weight before updating
    if filament:
        filament.remaining_weight += print_job.weight_used

    # Update print job details
    print_job.project_name = request.form['project_name']
    print_job.length_used = float(request.form['length_used'])
    print_job.weight_used = float(request.form['weight_used'])
    print_job.filament_id = int(request.form['filament_id'])

    # Subtract new weight from the updated filament roll
    new_filament = FilamentRoll.query.get(print_job.filament_id)
    if new_filament:
        new_filament.remaining_weight -= print_job.weight_used

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/duplicate_roll/<int:roll_id>', methods=['POST'])
def duplicate_roll(roll_id):
    roll = FilamentRoll.query.get_or_404(roll_id)

    # Capture new values from the form
    new_maker = request.form['maker']
    new_color = request.form['color']
    new_total_weight = float(request.form['total_weight'])
    new_remaining_weight = float(request.form['remaining_weight'])
    new_in_use = 'in_use' in request.form  # Checkbox handling

    # Create a new roll with modified values
    new_roll = FilamentRoll(
        maker=new_maker,
        color=new_color,
        total_weight=new_total_weight,
        remaining_weight=new_remaining_weight,
        in_use=new_in_use
    )
    db.session.add(new_roll)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/duplicate_print/<int:print_id>', methods=['POST'])
def duplicate_print(print_id):
    print_job = PrintJob.query.get_or_404(print_id)

    # Capture new values from the form
    new_project_name = request.form['project_name']
    new_length_used = float(request.form['length_used'])
    new_weight_used = float(request.form['weight_used'])
    new_filament_id = int(request.form['filament_id'])

    # Create a new print job with modified values
    new_print_job = PrintJob(
        filament_id=new_filament_id,
        length_used=new_length_used,
        weight_used=new_weight_used,
        project_name=new_project_name
    )

    # Deduct weight from the selected filament roll
    new_filament = FilamentRoll.query.get(new_filament_id)
    if new_filament:
        new_filament.remaining_weight -= new_weight_used

    db.session.add(new_print_job)
    db.session.commit()

    return redirect(url_for('index'))
