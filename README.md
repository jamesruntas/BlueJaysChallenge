# BlueJaysChallenge

MLB Stats and News hub Django Application using mlb-stats-api

Version 1.0


### Starting the Web App:

1. git clone <https://github.com/jamesruntas/BlueJaysChallenge>

   
2. Start Docker Container 
   - in directory: ../BlueJaysChallenge/BlueJaysChallenge 
     ```bash
     docker-compose up
     ```

3. Access the App
    http://localhost:8000/

4. Stop the app:
   ```bash
   docker-compose down
   ```

ISSUES:
Players with accent characters in thier name arent seen by API call. ![image](https://github.com/jamesruntas/BlueJaysChallenge/assets/71133703/83011afc-7294-47f2-b659-56ae4f82d544)

