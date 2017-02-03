from flask import Flask, request, render_template, jsonify, abort, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
import database


app = Flask(__name__)
db = database.DatabaseContext()
db.connect()

# Set up test schema
bob = db.User(name='Bob', email='bob@example.com')
db.session.add(bob)
db.session.commit()
print bob.id


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
    return jsonify(user.to_dict())


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
    props = request.get_json(force=True)
    for key, value in props.iteritems():
        if key == 'email':
            user.email = value
        elif key == 'name':
            user.name = value
        else:
            abort(400, "Unsupported parameter '%s'" % key)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('get_user', user_id=user.id))


@app.route('/api/goals', methods=['POST'])
def create_goal():
    print 'Meek'
    props = request.get_json(force=True)
    for prop in ['user', 'start_ts', 'warmup_period', 'loss_period', 'loss_rate']:
        if not prop in props:
            print 'Queek'
            abort(400, "Missing required parameter '%s'" % prop)

    print 'Bleak'
    end_ts = None  # Optional variable may not otherwise get set.
    for prop, value in props.iteritems():
        if prop == 'user':
            user_id = parse_or_400(value, int, "User ID must be an integer")
            user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
        elif prop == 'start_ts':
            start_ts = parse_or_400(value, string_to_date, "Invalid timestamp for start_ts: " + value)
        elif prop == 'end_ts':
            end_ts = parse_or_400(value, string_to_date, "Invalid timestamp for end_ts: " + value)
        elif prop == 'warmup_period':
            warmup_period = parse_or_400(value, int, "Warmup period must be an integer")
        elif prop == 'loss_period':
            loss_period = parse_or_400(value, int, "Loss period must be an integer")
        elif prop == 'loss_rate':
            loss_rate = parse_or_400(value, int ,"Loss rate must be an integer")
        else:
            print 'En fleek'
            abort(400, "Unsupported parameter '%s'" % prop)

    print 'Chic'
    goal = db.Goal(user=user,
                   start_ts=start_ts, end_ts=end_ts,
                   warmup_period=warmup_period,
                   loss_period=loss_period, loss_rate=loss_rate)

    # TODO validate against existing groups and rewrite times as needed without concurrency bugs!

    db.session.add(goal)
    db.session.commit()
    return redirect(url_for('get_goal', goal_id=goal.id))


@app.route('/api/goals/<int:goal_id>', methods=['GET'])
def get_goal(goal_id):
    goal = one_or_404(db.Goal.query.filter(db.Goal.id == goal_id), 'Goal')
    return jsonify(goal.to_dict())


@app.route('/api/measurements', methods=['POST'])
def create_measurement():
    props = request.get_json(force=True)
    for prop in ['user', 'weight', 'timestamp', 'is_estimate']:
        if not prop in props:
            abort(400, "Missing required parameter '%s'" % prop)

    for prop, value in props.iteritems():
        if prop == 'user':
            user_id = parse_or_400(value, int, "User ID must be an integer")
            user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
        elif prop == 'weight':
            weight = parse_or_400(value, int, "Weight must be an integer")
        elif prop == 'timestamp':
            timestamp = parse_or_400(value, string_to_date, "Invalid timestamp for loss_period: " + value)
        elif prop == 'is_estimate':
            if isinstance(value, bool):
                is_estimate = value
            else:
                abort(400, "is_estimate must be a boolean")
        else:
            abort(400, "Unsupported parameter '%s'" % prop)

    measurement = db.Measurement(user=user, weight=weight, timestamp=timestamp, is_estimate=is_estimate)
    db.session.add(measurement)
    db.session.commit()
    return redirect(url_for('get_measurement', measurement_id=measurement.id))


@app.route('/api/measurements/<int:measurement_id>', methods=['GET'])
def get_measurement(measurement_id):
    measurement = one_or_404(db.Measurement.query.filter(db.Measurement.id == measurement_id), 'Measurement')
    return jsonify(measurement.to_dict())


@app.route('/api/measurements/<int:measurement_id>', methods=['PUT'])
def update_measurement(measurement_id):
    props = request.get_json(force=True)
    measurement = one_or_404(db.Measurement.query.filter(db.Measurement.id == measurement_id), 'Measurement')

    for prop, value in props.iteritems():
        if prop == 'weight':
            measurement.weight = parse_or_400(value, int, "weight must be an integer")
        elif prop == 'timestamp':
            measurement.timestamp = parse_or_400(value, string_to_date, "Invalid timestamp for loss_period: " + value)
        elif prop == 'is_estimate':
            if isinstance(value, bool):
                measurement.is_estimate = value
            else:
                abort(400, "is_estimate must be a boolean")
        else:
            abort(400, "Unsupported parameter '%s'" % prop)

    db.session.add(measurement)
    db.session.commit()
    return redirect(url_for('get_measurement', measurement_id=measurement.id))


@app.route('/api/meals', methods=['POST'])
def create_meal():
    props = request.get_json(force=True)
    for prop in ['user', 'amount', 'timestamp', 'is_estimate']:
        if not prop in props:
            abort(400, "Missing required parameter '%s'" % prop)

    for prop, value in props.iteritems():
        if prop == 'user':
            user_id = parse_or_400(value, int, "User ID must be an integer")
            user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
        elif prop == 'amount':
            amount = parse_or_400(value, int, "amount must be an integer")
        elif prop == 'timestamp':
            timestamp = parse_or_400(value, string_to_date, "Invalid timestamp for loss_period: " + value)
        elif prop == 'is_estimate':
            if isinstance(value, bool):
                is_estimate = value
            else:
                abort(400, "is_estimate must be a boolean")
        else:
            abort(400, "Unsupported parameter '%s'" % prop)

    meal = db.Meal(user=user, amount=amount, timestamp=timestamp, is_estimate=is_estimate)
    db.session.add(meal)
    db.session.commit()
    return redirect(url_for('get_meal', meal_id=meal.id))


@app.route('/api/meals/<int:meal>', methods=['GET'])
def get_meal(meal_id):
    meal = one_or_404(db.Measurement.query.filter(db.Meal.id == meal_id), 'Meal')
    return jsonify(meal.to_dict())


@app.route('/api/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    props = request.get_json(force=True)
    meal = one_or_404(db.Meal.query.filter(db.Meal.id == meal_id), 'Meal')

    for prop, value in props.iteritems():
        if prop == 'amount':
            meal.amount = parse_or_400(value, int, "amount must be an integer")
        elif prop == 'timestamp':
            meal.timestamp = parse_or_400(value, string_to_date, "Invalid timestamp for loss_period: " + value)
        elif prop == 'is_estimate':
            if isinstance(value, bool):
                meal.is_estimate = value
            else:
                abort(400, "is_estimate must be a boolean")
        else:
            abort(400, "Unsupported parameter '%s'" % prop)

    db.session.add(meal)
    db.session.commit()
    return redirect(url_for('get_measurement', meal_id=meal.id))


@app.route('/api/users/<int:user_id>/goal', methods=['GET'])
def get_user_current_goal(user_id):
    user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
    current_goal = max(user.goals, key=lambda goal: goal.start_ts)
    return jsonify(current_goal.to_dict())


@app.route('/api/users/<int:user_id>/goals', methods=['GET'])
def get_user_goals(user_id):
    user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
    return jsonify(sorted([goal.to_dict() for goal in user.goals], key=lambda goal: goal['start_ts']))


@app.route('/api/users/<int:user_id>/weight', methods=['GET'])
def get_user_weight(user_id):
    user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
    last_weight = max(user.measurements, key=lambda measurement: measurement.weight)
    return jsonify(last_weight.to_dict())


@app.route('/api/users/<int:user_id>/measurements', methods=['GET'])
def get_user_measurements(user_id):
    user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
    return jsonify(sorted([m.to_dict() for m in user.measurements], key=lambda m: m['timestamp']))


@app.route('/api/users/<int:user_id>/meals', methods=['GET'])
def get_user_meals(user_id):
    user = one_or_404(db.User.query.filter(db.User.id == user_id), 'User')
    return jsonify(sorted([m.to_dict() for m in user.meals], key=lambda m: m['timestamp']))


def one_or_404(query, type=None):
    try:
        return query.one()
    except NoResultFound:
        if type is None:
            abort(404, "Failed to find required resource")
        else:
            abort(404, "%s not found" % type)


def parse_or_400(val, parser, msg):
    try:
        return parser(val)
    except (ValueError, TypeError):
        print 'Eek'
        abort(400, msg)


def string_to_date(date_str):
    return None  # TODO


def date_to_string(date):
    return ''  # TODO
