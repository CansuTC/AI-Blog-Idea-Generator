import openai
import os

api_key = os.getenv("OPENAI_API_KEY")


client = openai.OpenAI(api_key=api_key)

user_topic = input("Enter a topic for AI-generated blog ideas: ")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Give me 3 blog post ideas about {user_topic}. Provide each idea as a headline followed by a short paragraph explaining the topic."}
    ]
)

ai_content = response.choices[0].message.content

filename = f"blog_ideas_{user_topic.replace(' ', '_')}.txt"

with open(filename, "w", encoding="utf-8") as file:
    file.write(f"## Blog Post Ideas for {user_topic}\n\n")
    file.write(ai_content)

print(f"\nAI-Generated Blog Post Ideas saved to {filename}")
