# BlueJaysChallenge

MLB Stats and News hub Django Application using mlb-stats-api

DEMO (Sept 4) Version 0.9.0

https://github.com/jamesruntas/BlueJaysChallenge/assets/71133703/9c19cc2a-3df9-4bc7-91dd-ac7bacf81d7e


### Starting the Web App:

1. git clone <https://github.com/jamesruntas/BlueJaysChallenge>

   
2. (Optional) Activate V Env in repo directory
     ```bash
     python -m venv venv
     ```
   
     ```bash
     .\venv\Scripts\activate
     ```
   

3. Dependencies 
     ```bash
     pip install -r requirements.txt
     ```
4. Start the Django development server:
   ```bash
   python myproject/manage.py runserver
   ```

   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Stopping the Web App:

1. `Ctrl+C` in terminal


ISSUES:
Players with accent characters in thier name arent seen by API call. ![image](https://github.com/jamesruntas/BlueJaysChallenge/assets/71133703/83011afc-7294-47f2-b659-56ae4f82d544)

