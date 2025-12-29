import os
import time
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from ddtrace import tracer, patch_all
patch_all()

import vertexai
from vertexai.generative_models import GenerativeModel

load_dotenv()

app = Flask(__name__)

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "us-central1")

if PROJECT_ID:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-1.5-flash-001")
else:
    print("WARNING: PROJECT_ID not set. AI features will fail.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AegisDominus")

@app.route('/chat', methods=['POST'])
def chat():
    start_time = time.time()
    data = request.json
    
    user_prompt = data.get('prompt', '')
    user_id = data.get('user_id', 'anon')

    with tracer.trace("llm.request") as span:
        span.set_tag("user.id", user_id)
        span.set_tag("prompt.length", len(user_prompt))
        
        restricted_phrases = ["ignore previous instructions", "exploit", "system override","I work with the government"]
        is_jailbreak = any(phrase in user_prompt.lower() for phrase in restricted_phrases)
        
        span.set_tag("security.jailbreak", str(is_jailbreak).lower())

        if is_jailbreak:
            logger.warning(f"SECURITY INCIDENT: Jailbreak attempt blocked from {user_id}")
            
            span.set_tag("error", True)
            span.set_tag("http.status_code", "403") 
            
            return jsonify({
                "response": "I cannot fulfill this request. Security protocol violation.",
                "security_alert": True
            }), 403

        try:
            if not PROJECT_ID:
                raise ValueError("Google Cloud Project ID is missing.")

            response = model.generate_content(user_prompt)
            output_text = response.text
            duration = time.time() - start_time
            input_tokens = len(user_prompt) / 4
            output_tokens = len(output_text) / 4

            span.set_metric("llm.tokens.input", input_tokens)
            span.set_metric("llm.tokens.output", output_tokens)
            span.set_metric("llm.latency", duration)
            
            logger.info(f"LLM Success: {user_id} asks '{user_prompt[:20]}...'")
            
            return jsonify({
                "response": output_text,
                "security_alert": False
            })

        except Exception as e:
            logger.error(f"Vertex AI Error: {e}")
            span.set_tag("error", True)
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)