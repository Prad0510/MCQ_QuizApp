🧠 MCQ Quiz App

This is a dynamic and interactive Multiple-Choice Question (MCQ) quiz application built using Streamlit and the Gemini API from Google. The app allows users to generate quizzes on any topic, with customizable difficulty and question count.
✨ Features
Topic Generation: Create quizzes on any topic you choose.
Customizable Difficulty: Select from Easy, Medium, or Hard difficulty levels.
Variable Question Count: Choose to generate 3, 5, 10, or 15 questions.
Real-Time Feedback: Get instant feedback on whether your answer is correct or incorrect.
Answer Explanation: Learn more with a detailed explanation for each correct answer.
Results & Analytics: View your final score, and see a breakdown of your performance by difficulty.
Downloadable Results: Export your quiz results as a CSV file for further analysis.
🚀 Getting Started
Follow these simple steps to set up and run the application on your local machine.
Prerequisites
Python 3.8+
A Google Gemini API Key: You can obtain one for free from the Google AI Studio.
Installation
Clone the repository:
git clone <your-repository-url>
cd <your-project-folder>


Create a virtual environment and install dependencies:
It's recommended to use a virtual environment to manage project dependencies.
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt


Configure your API Key:
The application requires an API key to communicate with the Gemini API.
Create a new file named .env in the root directory of the project.
Add the following line to the .env file, replacing YOUR_GEMINI_API_KEY with your actual key:
GEMINI_API_KEY=YOUR_GEMINI_API_KEY


Running the App
Once you have completed the setup, you can run the application with this command:
streamlit run app.py


This will launch a local server and open the app in your web browser.
📁 Project Structure
/
├── app.py                  # The main Streamlit application script
├── .env.example            # A template for the required environment variables
├── requirements.txt        # Lists the project's Python dependencies
└── README.md               # This file


Note: Please ensure the app.py and .env files are in the same directory.

