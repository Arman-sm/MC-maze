# MC-maze
A python maze creator/solver

The program communicates with the server via the mcpi_e library on the client and the rasberry juice plugin on the server.

## Requirements
1. Installing the rasberry juice plugin on the server
2. Installing the mcpi_e and the multipledispatch libraries on the client ( you can install them with this ```pip install requirements.txt``` )
3. Entering the server address, rasberry juice port, minecraft usernameinto the program
```python
server = Minecraft.create("SERVER_ADDRESS", 4711, "USERNAME")
```
