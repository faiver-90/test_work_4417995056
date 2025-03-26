from flask import Blueprint


bp = Blueprint('users', __name__)


@bp.route('/')
def index():
    return 'Flask + SQLite работает!'


# @bp.route('/users', methods=['GET'])
# def get_users():
#     with SessionLocal() as session:
#         users = session.query(User).all()
#         return jsonify([{"id": u.id, "name": u.name} for u in users])
#
#
# @bp.route('/users', methods=['POST'])
# def create_user():
#     data = request.json
#     new_user = User(name=data["name"])
#     with SessionLocal() as session:
#         session.add(new_user)
#         session.commit()
#         return jsonify({"message": "User created", "id": new_user.id})
