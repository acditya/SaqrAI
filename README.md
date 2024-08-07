<h1>Team SaqrAI: TurView - Interview Chatbot for AI71xLablab.ai Falcon Hackathon</h1>

<h2>Overview</h2>
<p>Welcome to TurView, an AI-powered interview chatbot developed for the Falcon Hackathon. TurView is designed to revolutionize the interview process by leveraging Falcon's advanced language models and AI71's API Hub. With TurView, users can conduct seamless and intelligent interviews, streamlining the hiring process and enhancing candidate evaluation.</p>

<h2>Features</h2>
<ul>
    <li><strong>Automated Interviews:</strong> Conduct interviews using TII's Falcon-180B-Chat and Falcon-40B-Instruct LLMs from AI71's API.</li>
    <li><strong>Speak with AI:</strong> Text-to-Speech Software to Directly Communicate with the AI, bypassing the usual keyboard-and-mouse approach.</li>
    <li><strong>Audio Transcription:</strong> Convert audio responses to text for easy analysis.</li>
    <li><strong>User Registration:</strong> Securely register users and manage interview data.</li>
    <li><strong>Conversation Handling:</strong> Interactive and dynamic question generation and answer analysis.</li>
    <li><strong>Database Integration:</strong> Store and manage user and interview data using SQLite.</li>
    <li><strong>AI-based CV Formatter:</strong> Upgrade any CV to ATS format in seconds to help accelerate career development.</li>
    <li><strong>Dynamic Bespoke TurView Webpage:</strong> Navigate TurView's offerings through our self-developed web interface developed in entirety on Flask.</li>
</ul>

<h2>Getting Started</h2>

<h3>Prerequisites</h3>
<ul>
    <li>Python 3.8+</li>
    <li>AI71</li>
    <li>Flask</li>
    <li>SQLite3</li>
    <li>Faster Whisper</li>
    <li>PyTTSx3</li>
    <li>PyPDF2</li>
    <li>docx2pdf</li>
    <li>docx2txt</li>
</ul>

<h3>Installation</h3>
<pre>
<code>
git clone https://github.com/acditya/SaqrAI.git
cd TurView
pip install -r requirements.txt
python app.py
</code>
</pre>

<h3>Configuration</h3>
<ul>
    <li><strong>Upload Folder:</strong> Configure the upload folder for audio and CV files in the <code>app.config</code> section.</li>
    <li><strong>Secret Key:</strong> Set a secure secret key for session management.</li>
</ul>

<h2>Contributing</h2>
<ol>
    <li>Fork the repository.</li>
    <li>Create a new branch:
        <pre><code>git checkout -b feature-branch</code></pre>
    </li>
    <li>Make your changes and commit them:
        <pre><code>git commit -m "Add new feature"</code></pre>
    </li>
    <li>Push to the branch:
        <pre><code>git push origin feature-branch</code></pre>
    </li>
    <li>Open a pull request to merge your changes into the main branch.</li>
</ol>

<h2>Educational Career Prep Tool</h2>
<p>TurView is not just an interview chatbot; it is an educational career preparation tool designed to help users enhance their interview skills and streamline their job application process. By interfacing with Falcon-180B-Chat and Falcon-40B-Instruct LLMs, TurView provides intelligent and dynamic interview experiences. Additionally, our AI-based CV formatter ensures that your resume meets ATS standards, helping you stand out to potential employers and accelerate your career development.</p>
