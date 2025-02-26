from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Set your Groq API key here
AI_KEY = os.getenv(
    "GROQ_API_KEY"
)

if not AI_KEY:
    raise ValueError(
        "Masukan GROQ API KEY ke environment masing2 atau pake hardcoded version."
    )

client = Groq(
    api_key=AI_KEY,
)

# System Prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are an expert AI specializing in content creation and digital marketing. Your task is to generate powerful, engaging, and highly relevant content ideas based on the provided criteria."  
    "**Guidelines for your response:**"
    "1. **Sharp & Clear** → Deliver direct, actionable content ideas without unnecessary fluff."  
    "2. **Detailed & Specific** → Each idea should be unique, well-explained, and tailored to the given inputs."  
    "3. **Simple & Effective** → Keep ideas easy to understand but impactful."
    "4. **Trendy & Data-Driven** → Leverage current trends and best practices for engagement."
    "5. **Actionable Format** → Provide responses as numbered lists with concise explanations."  
    "**Example Format:**"
    "🔥 *Content Idea #1:* [Title]"
    "- 🎯 **Why it works:** [Short explanation]"
    "- 🎥 **Format:** [Short video, carousel, blog, livestream, etc.]"
    "- 🎯 **Best for:** [Platform & Target Audience]"
    "- 💡 **Bonus Tip:** [Optional extra insight]"
    "Always respond in this structured and engaging way. Do not include your thought process. Your goal is to maximize clarity, impact, and engagement."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    goal = data.get('goal', '')
    platform = data.get('platform', '')
    content_type = data.get('content_type', '')
    target_audience = data.get('target_audience', '')
    competitors = data.get('competitors', '')
    trends = data.get('trends', '')

    user_prompt = f"""
    Generate AI-powered content ideas based on the following criteria:
    - Goal: {goal}
    - Platform: {platform}
    - Content Type: {content_type}
    - Target Audience: {target_audience}
    - Competitors: {competitors}
    - Trends: {trends}
    """

    try:
        response = client.chat.completions.create(
            model="qwen-2.5-32b",  # Change to Groq-supported model if needed
            messages=[SYSTEM_PROMPT, {"role": "user", "content": user_prompt}]
        )

        ai_response = response.choices[0].message.content

    except Exception as e:
        ai_response = f"Error: {str(e)}"

    return jsonify({'content_ideas': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
