import openai

# Set your API key
#openai.api_key = ""

# Example prompt
prompt = "Once upon a time"

# Call OpenAI's completion endpoint
response = openai.Completion.create(
    engine="text-davinci-002",  # Specify the GPT-2 engine
    prompt=prompt,
    max_tokens=50  # Maximum number of tokens (words) in the output
)

# Print the generated text
print(response.choices[0].text.strip())
