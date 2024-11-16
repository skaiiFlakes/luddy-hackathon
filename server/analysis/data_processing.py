# JSON pre-processing for financial data
# Perform call on sentiment analysis
from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Directory to store generated files
OUTPUT_DIR = "output_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to preprocess data
def preprocess_data(input_data):
    # Convert input data into a DataFrame
    if isinstance(input_data, pd.DataFrame):
        df = input_data
    else:
        df = pd.DataFrame(input_data)

    # Standardize the data format (example)
    if "industry" not in df.columns or "kpi" not in df.columns:
        raise ValueError("Input data must include 'industry' and 'kpi' columns.")

    # Add any required transformations or cleaning here
    df["kpi_value"] = df.get("kpi_value", pd.Series([None] * len(df)))

    return df

# Endpoint to handle CSV or JSON input
@app.route('/upload_data', methods=['POST'])
def upload_data():
    try:
        if 'file' in request.files:
            # Handle CSV file upload
            file = request.files['file']
            df = pd.read_csv(file)

        elif request.json:
            # Handle JSON input
            data = request.json
            df = pd.DataFrame(data)

        else:
            raise ValueError("No input data provided. Submit a CSV file or JSON payload.")

        # Preprocess data
        processed_df = preprocess_data(df)

        # Save standardized CSV
        output_path = os.path.join(OUTPUT_DIR, "processed_data.csv")
        processed_df.to_csv(output_path, index=False)

        return jsonify({"message": "Data processed and saved.", "file_path": output_path}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)