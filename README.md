# Medimind – Deep Space Medical AI

**Medimind** is a Flask-based web application designed to provideautonomous medical guidance for astronauts on deep-space missions. Crew members can report symptoms and receive AI-generated medical information in real-time, even in offline or communication blackout scenarios.

> **Disclaimer:** This AI provides **educational content only** and is **not a substitute for professional medical advice**.

---

## Features

- **User Authentication**  
  Sign up and log in securely with hashed passwords. Sessions track individual users.

- **Symptom-Based Diagnosis**  
  Users answer questions about space-relevant symptoms. AI generates educational guidance.

- **AI Placeholder Integration**  
  Currently uses a placeholder function (`ask_biomedlm`). Can be replaced with BioGPT or advanced diagnostic AI.

- **Flask & SQLite Backend**  
  Stores users locally in an SQLite database. Passwords are securely hashed with Werkzeug.

- **Responsive Frontend**  
  Modern login/signup UI with animated, tech-inspired design.

---

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd medimind

