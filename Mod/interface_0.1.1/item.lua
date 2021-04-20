local my_inserter = table.deepcopy(data.raw["inserter"]["fast-inserter"])
-- to insert a new item based on fast inserter which needs no power
my_inserter.name = "inputinserter"
my_inserter.energy_source.type = "void"

data:extend{my_inserter}


