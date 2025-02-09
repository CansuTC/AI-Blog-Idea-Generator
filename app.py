import os
from flask import Flask, render_template, request, send_from_directory
import openai
from dotenv import load_dotenv
import random  # Added back for port selection

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_topic = request.form["topic"]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a digital marketing expert with deep knowledge of SEO and audience engagement. You generate blog ideas that are optimized for search engines and drive reader interaction."},
                {"role": "user", "content": f"Give me 3 blog post ideas about {user_topic}. Provide each idea as a bold headline followed by a short paragraph explaining the topic."}
            ]
        )
        ai_content = response.choices[0].message.content

        import re
        ai_content = re.sub(r"\*\*(.*?)\*\*", r"\1", ai_content)
        ai_content = ai_content.replace("1.", "<div class='idea-card'><h3 class='headline'>1. ")\
                               .replace("2.", "</h3></div><div class='idea-card'><h3 class='headline'>2. ")\
                               .replace("3.", "</h3></div><div class='idea-card'><h3 class='headline'>3. ")\
                               .replace('\n', '</h3><p class="body-text">') + "</p></div>"

        keywords = [
             f"{user_topic} tips",
             f"{user_topic} guide",
             f"best {user_topic} ideas",
             f"{user_topic} blog topics",
             f"how to write about {user_topic}",
             f"{user_topic} marketing",
             f"SEO for {user_topic}",
             f"{user_topic} trends",
             f"{user_topic} content strategy",
             f"{user_topic} insights"
        ]

        return render_template("index.html", topic=user_topic, ideas=ai_content, keywords=", ".join(keywords))

    return render_template("index.html", topic=None, ideas=None)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", random.randint(5000, 9000)))  # Automatically picks a free port
    app.run(host="0.0.0.0", port=port)