from flask import Flask, render_template, request, jsonify
from datetime import datetime

# Flask App Setup
app = Flask(__name__)

# Verification Function
def verify_drug(batch_number, drug_id, nafdac_number, database):
    # Step 1: Retrieve Batch Information
    batch_info = database.get_batch_info(batch_number, drug_id, nafdac_number)
    if not batch_info:
        return {"status": "Invalid", "message": "Batch number or NAFDAC number not found."}

    # Step 2: Validate Batch Number and NAFDAC Number
    if batch_info['drug_id'] != drug_id or batch_info['nafdac_number'] != nafdac_number:
        return {"status": "Invalid", "message": "Batch number or NAFDAC number does not match drug ID"}

    # Step 3: Check Expiry Date
    current_date = datetime.now().date()
    expiry_date = batch_info['expiry_date']
    if current_date > expiry_date:
        return {"status": "Invalid", "message": "Drug has expired"}

    # Step 4: Log Verification Attempt
    database.log_verification_attempt(user_id=1, batch_id=batch_info['batch_id'], verification_time=current_date, status="Valid")

    # Step 5: Return Verification Result
    return {"status": "Valid", "message": "Drug is valid and safe to use"}

# Mock Database Class
class Database:
    def get_batch_info(self, batch_number, drug_id, nafdac_number):
        # Mock database lookup
        sample_batches = [
            {"batch_id": 1, "batch_number": "LOT2024AB123", "drug_id": "DRG00123", "nafdac_number": "A7-1234", "expiry_date": datetime(2025, 1, 1).date()},
            {"batch_id": 2, "batch_number": "XYZ789", "drug_id": "DRG00124", "nafdac_number": "B2-4567", "expiry_date": datetime(2023, 6, 1).date()}
        ]
        for batch in sample_batches:
            if batch['batch_number'] == batch_number and batch['drug_id'] == drug_id and batch['nafdac_number'] == nafdac_number:
                return batch
        return None

    def log_verification_attempt(self, user_id, batch_id, verification_time, status):
        # Mock logging
        print(f"Logged verification attempt: User {user_id}, Batch {batch_id}, Time {verification_time}, Status {status}")

# Create a database instance
database = Database()

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    batch_number = data.get('batch_number')
    drug_id = data.get('drug_id')
    nafdac_number = data.get('nafdac_number')

    # Verify the drug using the provided function
    result = verify_drug(batch_number, drug_id, nafdac_number, database)

    # Return result as JSON
    return jsonify(result)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
