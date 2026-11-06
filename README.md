# CampusConnect

**Name:** Jay R. Cañezo  
**Section:** G5

CampusConnect is a Django application with account registration, login, profile editing, and a campus dashboard.

## Run locally

1. Install Python, then open a terminal in the project directory.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Apply database migrations and start the development server:

   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```

5. Open http://127.0.0.1:8000/ in your browser. Sign up to create an account.
