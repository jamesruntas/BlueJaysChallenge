# BlueJaysChallenge

MLB Stats and News hub Django Application using mlb-stats-api

DEMO (Sept 6) Version 0.9.0

https://github.com/jamesruntas/BlueJaysChallenge/assets/71133703/9c19cc2a-3df9-4bc7-91dd-ac7bacf81d7e


### Starting the Web App (Development Stage [Dockerized version to be implemented later]):

1. Ensure in directory BlueJaysChallennge/BlueJaysChallenge
   
2. Activate V Env
   - For Windows (CMD):
     ```bash
     myenv\Scripts\Activate
     ```
   - For Windows (PowerShell):
     ```bash
     .\myenv\Scripts\Activate
     ```
   - For Linux/macOS:
     ```bash
     source myenv/bin/activate
     ```

3. cd myproject 

4. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Stopping the Web App:

1. `Ctrl+C` in terminal


ISSUES:
Easy Fix low Priority(Sept 1) Players with accent characters in thier name arent seen by API call. ![image](https://github.com/jamesruntas/BlueJaysChallenge/assets/71133703/83011afc-7294-47f2-b659-56ae4f82d544)

