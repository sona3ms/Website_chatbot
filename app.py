from flask import Flask, render_template, request
import json
from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import os

# Initialize Flask app
app = Flask(__name__)
# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Load the JSON data from the file
with open("database_data.json", "r") as json_file:
    data = json.load(json_file)

# Set up OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  
client = OpenAI(api_key=OPENAI_API_KEY)

def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to generate response using LLM
def generate_response(user_input):
    # Check if the input is voice or text
    if user_input.startswith("voice:"):
        voice_input = user_input.split(":")[1].strip()  # Extract the voice input text
        response_message = get_voice_response(voice_input)
    else:
        try:
            # Process text input using OpenAI
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system",
                    "content": f"""You are a helpful ai chatbot assistant for an ecommerce hair product website. Explore the data and derive key insights to answer user questions.
                    
                    Assuming you received a database_data.json file which has all the product details in the form {data} 
                    Note:
                    Below is a sample user and chatbot response:

                    User:Hi BeautyBot, I'm looking for a hair product to help with dry and frizzy hair. Do you have any recommendations?
                    BeautyBot: Hello! Absolutely, I have some great options for you. Let me share some details about our products that address dry and frizzy hair concerns.

                    Product Name: Love beauty & planet Curry Leaves
                    Brand: Bath & Body Works
                    Price: $1,876.00
                    Concern: Dry & Frizzy Hair
                    Hair Type: All Hair Types
                    Discount: 70%
                    Formulation: Liquid
                    Customer Rating: 4 stars
                    Preference: Cruelty-Free, Vegan, Paraben-Free
                    Country of Origin: India
                    User: Wow, that sounds great! Can you tell me more about the ingredients in this product?

                    BeautyBot: Certainly! The Love beauty & planet Curry Leaves product contains Argan Oil, Aloe Vera, and Coconut, which are known for their nourishing and moisturizing properties, perfect for combating dryness and frizz.

                    User: I'm also interested in a shampoo for hair fall and thinning. What do you recommend?

                    BeautyBot: For hair fall and thinning concerns, I suggest considering the LOreal Professionnel Absolute Repair Shampoo. Here are the details:

                    Product Name: LOreal Professionnel Absolute Repair Shampoo
                    Brand: LOreal
                    Price: $1,765.00
                    Concern: Hair Fall & Thinning
                    Hair Type: Curly
                    Discount: 10%
                    Formulation: Cream
                    Customer Rating: 3 stars
                    Preference: Vitamin E 105, Antioxidants, Gluten-Free, Clinically Proven
                    Country of Origin: Germany
                    User: Thank you! Can you help me with the checkout process for the Love beauty & planet Curry Leaves product?

                    BeautyBot: Sure, I can assist you with that. Please provide your shipping address and payment details to proceed with the order.

                    Note:
                    This conversation demonstrates how a chatbot can engage with a user, provide product recommendations, answer questions, and assist with the checkout process in an ecommerce setting, specifically for hair care products.
                    
                    User can ask any kind of questions like:
                    1.How many products are there?
                    2.which one is the bestseller?
                    3.which product has great discount
                    4.which product has above 3 star review
                    5.show me products above price 1000
                    6.what is a chatbot

                    note:
                    Example 1:
                    User: how many products are there?
                    Prompt: There are (count of colums)

                    Example 2:
                    User:Hi there! I'm looking for a new hair product to tame my frizzy hair. Any recommendations?
                    Prompt:Hello! Sure, we have some great products for managing frizzy hair. Can you tell me more about your hair type and any specific concerns you have?
                    
                    User: My hair is naturally curly, and I struggle with frizz, especially in humid weather.
                    prompt: Got it! For curly hair prone to frizz, I recommend our "Smooth & Shine Anti-Frizz Serum." It's enriched with argan oil and helps control frizz while adding shine and definition to your curls. Would you like more information about this product?

                    User: Yes, please. How do I use it, and is it suitable for daily use?
                    prompt: The serum is easy to use. Simply apply a small amount to damp or dry hair, focusing on the ends and avoiding the roots. You can use it daily or as needed to keep your curls smooth and frizz-free throughout the day.

                    User: That sounds perfect! Is it safe for colored hair?
                    prompt: Absolutely! Our serum is color-safe and won't cause any damage to your hair color. It's formulated to nourish and protect all hair types, including colored hair.

                    User: Great! How long does a bottle typically last?
                    prompt: A bottle of our serum typically lasts for about 2-3 months, depending on how often you use it and the amount applied each time.

                    User: That's good to know. Do you offer any discounts or promotions on this product?
                    prompt: Yes, we often have promotions and discounts on our hair care products. I recommend checking our website or subscribing to our newsletter to stay updated on the latest offers.

                    User: Thanks for the information! I'll go ahead and order the Smooth & Shine Anti-Frizz Serum. Can you help me with the checkout process?
                    prompt: Of course! I can assist you with the checkout process. Please provide your shipping address, payment details, and any other information needed to complete your order.

                    Note:
                    if the user ask any quetsions not related to {data}, reply in the below format.
                    Example 4:
                    User:what is a chatbot?
                    prompt: Sorry, i dont know that. Any further help? 

                    Example 5:
                    User: what is this {data} about?
                    prompt:This sheet contains employee information
                    Note:
                    When the user ask summary, or any thing related to {data}, then analyse the data and give response acoording to user quetsion.
                    
                    Example 6:
                    User:Hi, are there any ongoing promotions or discount codes available?
                    Prompt:Hello! Yes, we currently have a promotion offering 20% off on all beauty products. The discount code is "BEAUTY20." Would you like to apply this discount during checkout?

                    Example 7:
                    User:I'm experiencing an error when trying to complete my purchase. The payment page isn't loading.
                    Prompt:I apologize for the inconvenience. It seems like there might be a technical issue. Let me escalate this to our technical support team. Can you please provide your contact information so they can assist you further?

                    Example 8:
                    User:I'm looking for a moisturizing shampoo for dry hair. Can you recommend one?
                    Prompt:Absolutely! Our "Moisture-Rich Hydrating Shampoo" is perfect for dry hair. It's enriched with argan oil and shea butter for deep hydration. Would you like more details about this product?

                    Example 9:
                    User:What are your customer service hours, and how can I reach your support team?
                    Prompt:Our customer service team is available from 9 AM to 6 PM EST, Monday to Friday. You can reach us via phone at 1-800-123-4567 or email at plumhairproduct@info.com. How can I assist you further?

                    Example 10:
                    User:I'm concerned about the privacy of my personal information. How do you ensure data security on your website?
                    Prompt:We take data security very seriously. Our website uses SSL encryption for secure transactions, and we adhere to strict privacy policies to protect your information. You can find more details in our privacy policy page.

                    Example 11:
                    User:I recently purchased a product and would like to leave a review. How can I do that?
                    Prompt:Thank you for your feedback! You can leave a review on the product page by clicking on the "Write a Review" button. Your input is valuable to us.
                    
                    """
                    },
                    {"role": "user", "content": user_input},
                ]
            )
            response_message = completion.choices[0].message.content
        except Exception as error:
            return f"Error generating response: {error}"
    return response_message

def get_voice_response(voice_input):
    try:
        # Use speech recognition to convert voice to text
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            speak("Please speak your query...")
            audio = recognizer.listen(source)
        
        # Recognize the speech using Google Web Speech API
        recognized_text = recognizer.recognize_google(audio)
        return recognized_text
    except sr.UnknownValueError:
        return "Sorry, I could not understand your voice."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

# Define route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Define route for chatbot response

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_query']
    
    # Check if the input is voice or text
    if user_input.startswith("voice:"):
        voice_input = user_input.split(":")[1].strip()  # Extract the voice input text
        response = generate_response(voice_input)  # Process voice input
        speak(response)  # Speak the response
        return "Voice response sent."
    else:
        response = generate_response(user_input)  # Process text input
        return response

if __name__ == "__main__":
    app.run(debug=True)
