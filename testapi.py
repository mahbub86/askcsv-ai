import google.generativeai as genai

# Replace with your actual key or load from env/secrets
genai.configure(api_key="AIzaSyBXCIgjP_R_ki9ZAvwKpvIFmvJB1EZhF90")

# Use correct model name
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Test prompt
response = model.generate_content("Say hello from Gemini!")
print(response.text)
