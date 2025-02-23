# CodeSentinel

**CodeSentinel** is a web-based platform that helps developers generate, review, and debug complete coding projects. It leverages a powerful AI assistant that can create full-stack applications based on user instructions. The platform also provides a live chat feature for real-time assistance.

## Features

- **Project Generation**: Generate a complete coding project based on user instructions. The AI generates all necessary files (HTML, CSS, JavaScript, backend code, etc.), and provides a preview and debugging analysis.
- **Live Chat Assistance**: Engage in real-time conversations with the AI to resolve coding issues, clarify concepts, or get help with debugging.
- **ZIP File Download**: Download the generated project as a ZIP file, ready for deployment.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI, Python
- **AI**: Groq AI (for project generation and live chat)
- **Deployment**: Vercel (for frontend), Heroku or any suitable hosting service (for backend)

## Prerequisites

Before running the application locally or deploying it to a platform like Vercel or Heroku, ensure you have the following prerequisites:

- Python 3.7 or later
- Node.js and npm (if using frontend tools)
- A **Vercel** account (for frontend deployment)
- A **Heroku** account (if deploying the backend there)
- **Groq API Key** (for interacting with the AI)
- Git installed

## Installation

### Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/CodeSentinel.git
cd CodeSentinel
Backend Setup (FastAPI)
Create a Virtual Environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the Backend Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set Up Your Environment Variables:

Create a .env file in the root directory and add your Groq API key:

env
Copy
Edit
GROQ_API_KEY=your_api_key_here
Run the Backend Server:

bash
Copy
Edit
uvicorn api.backend:app --reload
The backend will now be running at http://localhost:8000.

Frontend Setup (if applicable)
If you have a frontend to go along with the backend, follow these steps:

Install Frontend Dependencies (if you use npm or a similar package manager):

Navigate to the frontend directory (or your frontend directory), and run the following:

bash
Copy
Edit
cd frontend
npm install
Run the Frontend Locally:

If you're using a JavaScript framework like React or Vue, start the frontend server:

bash
Copy
Edit
npm start
This will launch the frontend at http://localhost:3000.

Set Up Vercel for Frontend Deployment
Install Vercel CLI:

If you don't have Vercel installed, you can install it using npm:

bash
Copy
Edit
npm install -g vercel
Deploy the Frontend:

Navigate to your frontend directory, then deploy using the Vercel CLI:

bash
Copy
Edit
vercel --prod
Follow the prompts to complete the deployment process. Vercel will provide a URL for your live frontend.

Set Up Backend Deployment (Heroku)
Create a Procfile for Heroku:

In your project root, create a file called Procfile with the following content:

plaintext
Copy
Edit
web: uvicorn api.backend:app --host 0.0.0.0 --port ${PORT:-5000}
Deploy to Heroku:

Install the Heroku CLI if you haven't yet.

Create a new Heroku app:

bash
Copy
Edit
heroku create your-app-name
Push your code to Heroku:

bash
Copy
Edit
git push heroku main
Set Up Environment Variables on Heroku:

Set your Groq API key on Heroku:

bash
Copy
Edit
heroku config:set GROQ_API_KEY=your_api_key_here
Access the Deployed Application:

After deployment, Heroku will provide a URL where your backend is live.

Running Locally
Start the backend server:

bash
Copy
Edit
uvicorn api.backend:app --reload
Start the frontend locally (if applicable):

bash
Copy
Edit
cd frontend
npm start
Access the app in your browser at http://localhost:3000 for the frontend and http://localhost:8000 for the backend.

API Endpoints
POST /assist: Generate a complete coding project based on user instructions.

Request Body: JSON object containing the instruction key with a string value describing the project.
Response: JSON object containing:
files: A dictionary of generated project files.
preview: HTML preview snippet.
debug: Debugging suggestions for the project.
zip_file: Path to the generated ZIP file.
POST /chat: Engage in real-time chat with the AI for coding help.

Request Body: JSON object containing the message key with a string value.
Response: JSON object containing the AI's reply.
GET /download/{zip_filename}: Download the generated project ZIP file.

Parameters: zip_filename — the name of the ZIP file you want to download.
Project Structure
Here is the basic project structure:

plaintext
Copy
Edit
CodeSentinel/
│
├── api/                      # Backend files
│   ├── backend.py            # FastAPI backend
│   ├── requirements.txt      # Python dependencies
│   ├── Procfile              # Heroku deployment file
│   └── .env                  # Environment variables (like GROQ API key)
│
├── frontend/                 # Frontend files
│   ├── index.html            # Main HTML file
│   ├── styles.css            # CSS styles
│   └── scripts.js            # JavaScript functionality (if needed)
│
├── .gitignore                # Git ignore file
└── README.md                 # This README file
Contributing
We welcome contributions! If you'd like to help improve the CodeSentinel platform, feel free to fork the repository, make changes, and create a pull request. Make sure to follow our coding standards and provide clear commit messages.

License
This project is licensed under the MIT License - see the LICENSE file for details.
