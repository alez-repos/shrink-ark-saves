# shrink.py: ARK:SE Save shrinker

`shrink.py` is a utility designed to optimize the size of official ARK: Survival Evolved save files by removing unnecessary tribes.

## Prerequisites

> **Note**: An alternative is to download the pre-packaged release, which is set up, includes python and is ready to run after you edit the config.yml file.

1. **Python Installation**: Ensure Python is installed on your machine.
2. **Repository Setup**:
   - Clone the GitHub repository.
   - Navigate to the repository directory.
   - Set up a virtual environment:
     ```bash
     python -m venv env
     ```
   - Install the required dependencies:
     ```bash
     python -m pip install -r requirements.txt
     ```

3. **Execution**:
   ```bash
   python shrink.py
   ```

## Usage Guide

1. **Initial Setup**:
   - Launch the official save to generate the `AuditLog*.json` file, which the program utilizes.
   - If unfamiliar with this process, consider using the [ARK Server Manager (ASM)](https://arkservermanager.freeforums.net/thread/5193/downloads) for ease.
   - Use the following options in the "Server Args" field:
     ```
     -culture=en -newsaveformat -usestore -parseservertojson
     ```
   - Ensure "Enable RCON" is checked. Note the RCON port and the server's admin password for later configuration in the application.
   - Install the [ARK Server API](https://gameservershub.com/forums/resources/ark-server-api.12/) and the [ExtendedRCON](https://gameservershub.com/forums/resources/extended-rcon.13/) plugin on the server.

2. **Server Interaction**:
   - Start the server and log in with your character.
   - Gain administrative privileges with:
     ```
     enablecheats <password>
     ```
   - Activate cheat player view:
     ```
     setcheatplayer 1
     ```
      > You can also get your TribeID if you run the program. Before starting it will show all detected tribes in the JSON, just search for your tribe name and copy the ID, then Ctrl+c and edit the config file.

3. **Configuration**:
   - In `config.yml`, list the TribeIDs you wish to retain, along with the RCON parameters (password, host, and port) and JSON dump filename. Multiple tribes can be listed, one per line.

4. **Program Execution**:
   - With the server running, execute the program.
   - The program operates in two phases:
     1. Removes all tribes, except those listed in `config.yml`, starting from the smallest based on structure count. Tribes with more than 10,000 structures will prompt for confirmation due to potential server crash risks.
   
        > Optionally, a `destroy.txt` file can be generated, containing commands to remove large tribes. Follow the in-program instructions to execute these commands within the game. This is the recommended method to delete large (>10k structures) tribes.
     2. Deletes all players without an associated tribe.
  

5. **Final Steps**:
   - After program execution, in the game, run:
     ```
     cheat saveworld
     ```
   - Close the server and retrieve the optimized game save from the `SavedArks` folder. This process can significantly reduce save file sizes. (e.g., from 2.4GB to 200MB in some tests).