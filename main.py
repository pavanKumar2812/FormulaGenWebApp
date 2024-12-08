from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import base64
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

genai.configure(api_key="AIzaSyBIOvgKl01wOqvXs0b9b1lD9dZA_ELdnN4")
model = genai.GenerativeModel('gemini-1.5-flash')
# model = genai.GenerativeModel('gemini-pro')

@app.route("/")
def render_root():
    return render_template("index.html")

@app.route("/SendFormula", methods=["POST"])
def send_text():
    try:
        # Get data sent from the frontend
        data = request.get_json()  # Correctly parse the JSON payload
        print(data)  # Debugging: Log the received data

        # Extract formula description
        user_input = data.get("formula_description", "").strip()
        if not user_input:
            return jsonify({"error_message": "No input provided"}), 400

        # Generate LaTeX code using the Generative Model
        prompt = f"You are a LaTeX generator model. The user will give you the name or description of a formula. If you know it, you provide the LaTeX code visualizing it. No explanation, just LaTeX. Formula: {user_input}"
        print(f"Prompt sent to model: {prompt}")  # Debugging

        response = model.generate_content(prompt)  # Ensure this method call is correct
        latex_code = response.text.strip()
        print(f"Generated LaTeX Code: {latex_code}")  # Debugging

        # Send the response back to the frontend
        return jsonify({
            "latex_code": latex_code,
        })
    except Exception as e:
        # Log the exception for debugging
        print("Error:", str(e))
        return jsonify({"error_message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)