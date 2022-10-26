
#IMPORTED from the server/gamehub project
#Makes the command ready for the program usage. The output type is a dictionary
def bakeCommand(command: str, localCommands: list[list[str, dict]]=()) -> dict[str, list, dict]: #bake request or response
	command = command.strip()
	if command != None or command != "":
		#Separating localCommands and tags for organizing them
		commandChunks = []
		for chunk in command.strip().split():
			if chunk != "":
				commandChunks.append(chunk)
		#Preparing the command result base for adding information to it
		command = {"name" : commandChunks[0], "subCommands" : [], "tags":{}}
		#Checking if the command is available in the localCommands list
		command["scope"] = "internal" if commandChunks[0] in [command for command in localCommands] else "external"
		#Adding the default tag values if available
		for commandConfig in localCommands:
			if commandConfig[0] == commandChunks[0] and len(commandConfig) > 1:
				command["tags"].update(commandConfig[1])
				break
		#Adding the tags and subcommands to the command info
		subcommandsEnded = False
		for index, tag in enumerate(commandChunks[1:]):
			if tag[0] == "-":
				subcommandsEnded = True
				command["tags"].update({tag : (commandChunks[index+2] if commandChunks[index+2][0] != "-" else True) if len(commandChunks) >= index + 3 else (True if not tag in command["tags"] else not command["tags"][tag])})
			elif not subcommandsEnded:
				command["subCommands"].append(tag)
		return command
	return False

def numParse(rawNum: str, *, baseNum: int | float | str = 0) -> int:
	return eval(rawNum.replace("~", str(baseNum)))