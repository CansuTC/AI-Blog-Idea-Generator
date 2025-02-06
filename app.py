import os
import random
import openai
from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# OpenAI API key setup
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    """Handles homepage and AI blog idea generation."""
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

        # Properly format headlines and paragraphs
        ai_content = ai_content.replace("1.", "<div class='idea-card'><h3><strong>1.</strong> ")\
                               .replace("2.", "</h3></div><div class='idea-card'><h3><strong>2.</strong> ")\
                               .replace("3.", "</h3></div><div class='idea-card'><h3><strong>3.</strong> ")\
                               .replace('\n', '<p>') + "</p></div>"

        # Remove any extra '**' that OpenAI might add
        ai_content = ai_content.replace("**", "")

        return render_template("index.html", topic=user_topic, ideas=ai_content)

    return render_template("index.html", topic=None, ideas=None)

@app.route('/favicon.ico')
def favicon():
    """Serves the favicon."""
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", random.randint(5000, 9000)))  # Uses automatic port selection
    app.run(host="0.0.0.0", port=port)