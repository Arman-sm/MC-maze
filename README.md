# MC-maze
## **A python maze creator/solver**

This program communicates with the server via the mcpi_e library on the client and the raspberry juice plugin on the server to make mazes by getting the maze map from an api provided by Yasan academy.

For using the program you have to send your [commands](#Commands) as messages in the chat.

This program is a completely new way of doing an exercise in the academy ( The academy solves the problem and you can just follow or do it in any other way you want )

Credit to yasan academy for the idea of making a maze creator/solver
## **Requirements**
1. Installing the raspberry juice plugin on the server
2. Installing the libraries on the client from the requirements.txt file
3. Entering the server address, raspberry juice port, minecraft username into the program
```python
server = Minecraft.create("SERVER_ADDRESS", 4711, "USERNAME")
```
## **Commands**
