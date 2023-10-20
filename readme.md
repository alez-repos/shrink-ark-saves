# shrink.py: ARK:SE Save shrinker

`shrink.py` is an utility designed to optimize the size of official ARK: Survival Evolved save files by removing unnecessary tribes.

## Prerequisites

> **Note**: An alternative is to download the [pre-packaged release for Windows](https://github.com/alez-repos/shrink-ark-saves/releases/tag/latest), which is set up, includes python and is ready to run after you edit the config.yml file.

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
   - Look to an structure that belong to you. Note the TribeID.
      > Another way to get your TribeID: Edit the config.yml to add the JSON and run `shrink.py`. When `shrink.py` starts it will show a list of Tribes ordered by structures and number of dinos. Find your tribe, keep the TribeID for the next step and press Control+C to interrupt the program.

3. **Configuration**:
   - In `config.yml`, list the TribeIDs you wish to retain, along with the RCON parameters (password, host, and port) and JSON dump filename. Multiple tribes can be listed, one per line.

4. **Program Execution**:
   - With the server running, execute the program.
   - The program operates in two phases:
     1. Removes all tribes, except those listed in `config.yml`, starting from the smallest based on structure count. Tribes with more than 10,000 structures will prompt for confirmation due to potential server crash risks. It is recommended to reply 'a'.
   
        > When you choose 'a', a `destroy.txt` file will be generated, containing commands to remove large tribes. Follow the in-program instructions to execute these commands within the game. This is the recommended method to delete large (>10k structures) tribes.

         Basically at the end of phase 1, once the `destroy.txt` file contains all the large tribes, you will copy it to a path inside ARK client installation and run in-game, as admin, `exec destroy.txt` one time per tribe inside the file. You will notice that you dont need to run the exec command again when the response in the console only contains lines indicating that 0 structures have been deleted.

        Note that the path where you have to copy `destroy.txt` is inside your CLIENT installation, NOT SERVER. If you copy it to server installation or to another incorrect path by mistake it wont work and no messages will be shown in game console.
     2. Deletes all players without an associated tribe.
  

5. **Final Steps**:
   - After program execution, in the game, run:
     ```
     cheat saveworld
     ```
   - Close the server and retrieve the optimized game save from the `SavedArks` folder. This process can significantly reduce save file sizes. (e.g., from 2.4GB to 200MB in some tests).