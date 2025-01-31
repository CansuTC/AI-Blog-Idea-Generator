from flask import Flask, render_template, request, send_from_directory
import openai
import os

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
                {"role": "user", "content": f"Give me 3 blog post ideas about {user_topic}. Provide each idea as a headline followed by a short paragraph explaining the topic."}
            ]
        )

        ai_content = response.choices[0].message.content
        return render_template("index.html", topic=user_topic, ideas=ai_content)

    return render_template("index.html", topic=None, ideas=None)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)