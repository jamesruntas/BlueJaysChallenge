# BlueJaysChallenge

Starting and stopping a Django web application is straightforward. Here's how you do it:

### Starting the Web App (Development Stage [Dockerized version to be implemented later]):

1. Ensure you're in your Django project directory.
   
2. Activate V Env
   - For Windows (CMD):
     ```bash
     myenv\Scripts\Activate.bat
     ```
   - For Windows (PowerShell):
     ```bash
     .\myenv\Scripts\Activate
     ```
   - For Linux/macOS:
     ```bash
     source myenv/bin/activate
     ```

3. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Stopping the Web App:

1. `Ctrl+C` in terminal 
