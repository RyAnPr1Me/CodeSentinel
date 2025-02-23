import os
import zipfile
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from groq import Groq  # Install via: pip install groq
import uvicorn
from fastapi.responses import FileResponse
import shutil

app = FastAPI()

# Enable CORS (adjust allow_origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Models for project generation
# ---------------------------
class AssistRequest(BaseModel):
    instruction: str

class AssistResponse(BaseModel):
    files: dict       # e.g. {"index.html": "<!DOCTYPE html>..."}
    preview: str      # An HTML snippet for preview
    debug: str        # Debugging suggestions/analysis
    zip_file: str     # Path to the zip file

# ---------------------------
# Models for live chat
# ---------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Initialize the Groq client with your API key
client = Groq(api_key="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")

# Helper function to create the directory structure for files
def create_project_structure(files: dict) -> str:
    base_dir = "generated_project"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)  # Clean up the old project if it exists

    os.makedirs(base_dir)

    # Create files within their appropriate folders (e.g., static, src, templates)
    for file_path, content in files.items():
        file_dir = os.path.join(base_dir, os.path.dirname(file_path))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        with open(os.path.join(base_dir, file_path), "w") as file:
            file.write(content)

    return base_dir

# Helper function to zip the generated project
def zip_project(project_dir: str) -> str:
    zip_filename = f"{project_dir}.zip"
    shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', project_dir)
    return zip_filename

# Endpoint for generating a full project
@app.post("/assist", response_model=AssistResponse)
async def assist(request: AssistRequest):
    prompt = (
        f"Generate a complete coding project based on the following instruction: {request.instruction}\n\n"
        "The project should include all necessary files (HTML, CSS, JavaScript, backend code, etc.) and determine the "
        "appropriate programming languages and frameworks. Your output must be a valid JSON object with exactly three keys: "
        "'files', 'preview', and 'debug'.\n\n"
        "• 'files': an object mapping file paths (e.g., 'index.html', 'app.js', 'styles.css', 'server.py') to their code content.\n"
        "• 'preview': an HTML snippet that, when rendered, shows a preview of the website or application (if applicable).\n"
        "• 'debug': a detailed debugging analysis and suggestions for the generated project.\n\n"
        "Do not include any extra text outside of the JSON object."
    )

    try:
        generation_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a coding assistant that generates complete, production-ready projects."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        response_text = generation_completion.choices[0].message.content.strip()
        response_json = json.loads(response_text)
        if not all(key in response_json for key in ["files", "preview", "debug"]):
            raise ValueError("Response JSON missing required keys.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating project: {str(e)}")

    # Run a debugging pass on the generated project files
    debug_prompt = (
        f"Review the following generated project files and provide a detailed debugging analysis with suggestions for improvements:\n\n"
        f"{json.dumps(response_json['files'], indent=2)}\n\n"
        "Return only the debugging analysis text."
    )
    try:
        debug_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a senior software engineer specializing in debugging code."},
                {"role": "user", "content": debug_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_completion_tokens=512,
            top_p=1,
            stop=None,
            stream=False,
        )
        debug_analysis = debug_completion.choices[0].message.content.strip()
    except Exception as e:
        debug_analysis = f"Debugging pass failed: {str(e)}"

    # Create the project directory structure and write files
    try:
        base_dir = create_project_structure(response_json['files'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing project files: {str(e)}")

    # Zip the generated project
    try:
        zip_filename = zip_project(base_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error zipping project files: {str(e)}")

    return AssistResponse(
        files=response_json["files"],
        preview=response_json["preview"],
        debug=debug_analysis,
        zip_file=zip_filename  # Return the zip filename for download
    )

# Endpoint for live chat with the AI
@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_completion_tokens=512,
            top_p=1,
            stop=None,
            stream=False,
        )
        reply = chat_completion.choices[0].message.content.strip()
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to download the generated ZIP file
@app.get("/download/{zip_filename}")
async def download_zip(zip_filename: str):
    file_path = f"{zip_filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/zip', filename=zip_filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
