# AI Chatbot for E-commerce Product Website
This project is an AI chatbot developed using Python, Flask, PostgreSQL, OpenAI API, and speech recognition libraries. The chatbot assists users in an e-commerce setting, specifically for products.
## Features
* Voice and Text Interaction: Users can interact with the chatbot using both voice commands and text inputs.
* Product Recommendations: The chatbot provides personalized product recommendations based on user queries and preferences.
* Checkout Assistance: It assists users with the checkout process, including providing shipping information and payment details.
* Data Analysis: The chatbot analyzes data from a PostgreSQL database to answer user queries and provide insights.
## Project Structure
- database_data.json: JSON file containing product details retrieved from the PostgreSQL database.
- env.example: Example environment file containing placeholders for sensitive information.
- app.py: Main Flask application file containing the chatbot logic and routes.
- database.py: Create database_data.json file
- requirements.txt: File listing all dependencies required to run the project.
##Setup Instructions
1. Clone the repository to your local machine:
git clone https://github.com/sona3ms/Website_chatbot.git
2. Install dependencies:
pip install -r requirements.txt
3. Create a .env file with your environment variables:
OPENAI_API_KEY=your_openai_key_here
DB_NAME=your_database_name
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
4. Run:
python database.p
5. Start the Flask application:
python app.py
6. Access the chatbot at http://localhost:5000 in your web browser.
## Usage
- Access the chatbot interface in your web browser.
- Enter text queries or use voice commands starting with "voice:" followed by your query.
- The chatbot will process the input, retrieve data from the database, and provide responses accordingly.


