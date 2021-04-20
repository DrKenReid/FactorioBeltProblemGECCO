require("item")

-- Code for replacing the water in the map
local noise = require("noise") -- From the core mod

if settings.startup['ctg-enable'].value and settings.startup['ctg-remove-default-water'].value then
    -- Note sure what probability_expression does. Setting it to zero does not turn off water.
    local nowater = {
            probability_expression = noise.to_noise_expression(-math.huge)
        }

    local t = data.raw.tile
    t.water.autoplace = nowater
    t.deepwater.autoplace = nowater
    t['water-green'].autoplace = nowater
    t['deepwater-green'].autoplace = nowater
end