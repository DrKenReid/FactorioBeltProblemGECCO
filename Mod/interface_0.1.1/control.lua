local version = 1

-- test command to print a player's position
commands.add_command("pos", "send stats", function(table)
	p = game.players[1].position
	rcon.print(p)
	game.players[1].print(p)
end)
