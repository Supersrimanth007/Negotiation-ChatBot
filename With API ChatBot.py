import openai
import os
import random

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'  # Replace with your actual OpenAI API key

# Set base price and range
base_price = 100

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" if you have access
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response['choices'][0]['message']['content']

def negotiate(user_input):
    user_input = user_input.lower()
    response = ""

    if "price" in user_input:
        try:
            proposed_price = int(user_input.split("price")[1].strip())
            if proposed_price < base_price - (base_price * 0.1):
                response = f"The price you offered is too low. I can offer you a price of {base_price - (base_price * 0.05)}."
            elif proposed_price > base_price + (base_price * 0.1):
                response = f"The price you offered is too high. How about {base_price + (base_price * 0.05)} instead?"
            else:
                response = f"Your offer of {proposed_price} is acceptable. Shall we proceed?"
        except ValueError:
            response = "Please provide a valid price."

    elif "accept" in user_input:
        response = "Great! The deal is accepted at the agreed price."

    elif "reject" in user_input:
        response = "I'm sorry to hear that. If you have another offer, let me know!"

    elif "bundle" in user_input:
        bundle_discount = random.uniform(0.1, 0.2)
        discounted_price = base_price * (1 - bundle_discount)
        response = f"I can offer you a bundle discount of {bundle_discount*100:.1f}%. The discounted price would be {discounted_price:.2f}. What do you think?"

    elif "discount" in user_input:
        max_discount = 0.15
        discount_amount = random.uniform(0.05, max_discount)
        discounted_price = base_price * (1 - discount_amount)
        response = f"I can offer you a discount of {discount_amount*100:.1f}%. The discounted price would be {discounted_price:.2f}. Does this work for you?"

    else:
        # Generate response based on user input
        response = generate_response(user_input)

    return response

# Interactive chat loop
print("Welcome to the Negotiation Chatbot! Type 'exit' to end the conversation.")
print("Chatbot: What is your desired price for the product?")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break
    response = negotiate(user_input)
    print(f"Chatbot: {response}")