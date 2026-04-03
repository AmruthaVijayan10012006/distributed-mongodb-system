from flask import Flask, request, jsonify
from pymongo import MongoClient
from config import MONGO_URIS

app = Flask(__name__)

@app.route('/')
def home():
    return {
        "message": "Distributed MongoDB System API is running!",
        "routes": ["/insert", "/get/<id>", "/update/<id>", "/delete/<id>"]
    }

# Connect to MongoDB nodes
clients = {node: MongoClient(uri) for node, uri in MONGO_URIS.items()}
dbs = {node: clients[node].get_database() for node in clients}

def get_primary_node(user_id):
    return f"node{user_id % 3 + 1}"

def get_replica_node(primary):
    nodes = ["node1", "node2", "node3"]
    nodes.remove(primary)
    return nodes[0]

# 🔹 INSERT
@app.route('/insert', methods=['POST'])
def insert():
    data = request.json
    user_id = data['id']

    primary = get_primary_node(user_id)
    replica = get_replica_node(primary)

    dbs[primary].users.insert_one(data)
    dbs[replica].users.insert_one(data)

    return jsonify({
        "message": f"Stored in {primary} and replicated to {replica}"
    })

# 🔹 GET
@app.route('/get/<int:user_id>', methods=['GET'])
def get(user_id):
    primary = get_primary_node(user_id)

    result = dbs[primary].users.find_one(
        {"id": user_id},
        {"_id": 0}
    )

    # fallback to replica if not found
    if not result:
        replica = get_replica_node(primary)
        result = dbs[replica].users.find_one(
            {"id": user_id},
            {"_id": 0}
        )

    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "User not found"})

# 🔹 UPDATE
@app.route('/update/<int:user_id>', methods=['PUT'])
def update(user_id):
    data = request.json

    primary = get_primary_node(user_id)
    replica = get_replica_node(primary)

    dbs[primary].users.update_one(
        {"id": user_id},
        {"$set": data}
    )

    dbs[replica].users.update_one(
        {"id": user_id},
        {"$set": data}
    )

    return jsonify({"message": "Updated successfully"})

# 🔹 DELETE
@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    primary = get_primary_node(user_id)
    replica = get_replica_node(primary)

    dbs[primary].users.delete_one({"id": user_id})
    dbs[replica].users.delete_one({"id": user_id})

    return jsonify({"message": "Deleted successfully"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host='0.0.0.0', port=port, debug=True)
    