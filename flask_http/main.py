from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Иван", "age": 25, "position": "Разработчик"},
    {"id": 2, "name": "Анна", "age": 30, "position": "Дизайнер"}
]
next_id = 3


@app.route('/users', methods=['GET'])
def get_all():
    return jsonify(users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_one(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "Не найден"}), 404


@app.route('/users', methods=['POST'])
def create():
    global next_id
    data = request.get_json()

    if not data or 'name' not in data or 'age' not in data:
        return jsonify({"error": "Заполните обязательые поля"}), 400

    new_user = {
        "id": next_id,
        "name": data['name'],
        "age": data['age'],
        "position": data.get('position', 'Не указана')
    }

    users.append(new_user)
    next_id += 1
    return jsonify(new_user), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Нет данных"}), 400

    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i] = {
                "id": user_id,
                "name": data.get('name', user['name']),
                "age": data.get('age', user['age']),
                "position": data.get('position', user['position'])
            }
            return jsonify(users[i])

    return jsonify({"error": "Не найден"}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    global users
    old = len(users)
    users = [u for u in users if u["id"] != user_id]

    if len(users) < old:
        return jsonify({"message": "Удален"})
    return jsonify({"error": "Не найден"}), 404


if __name__ == '__main__':
    app.run(debug=True)