-- functions for custom terrein generation

meta = {
    water_colors    = {"blue", "green"},
    setting_type    = "runtime-global",
    -- List of pairs of name of preset and code to generate preset
    pattern_presets = {
            {"custom", nil},
            {"spiral", "Union(Spiral(1.3, 0.4), Rectangle(-105, -2, 115, 2))"},
            {"arithmetic spiral", "ArithmeticSpiral(50, 0.4)"},
            {"rectilinear spiral", "Zoom(RectSpiral(), 50)"},
            {"triple spiral", "AngularRepeat(Spiral(1.6, 0.5), 3)"},
            {"crossing spirals", "Union(Spiral(1.4, 0.4), Spiral(1 / 1.6, 0.2))"},
            {"natural archipelago",
                -- "NoiseCustom({exponent=1.5,noise={0.3,0.4,1,1,1.2,0.8,0.7,0.4,0.3,0.2},land_percent=0.13})"},
                "Union(" ..
                "NoiseCustom({exponent=1.5,noise={0.3,0.4,1,1,1.2,0.8,0.7,0.4,0.3,0.2},land_percent=0.07})," ..
                "NoiseCustom({exponent=1.9,noise={1,1,1,1,1,1,0.7,0.4,0.3,0.2},land_percent=0.1," ..
                "start_on_land=false,start_on_beach=false}))"},
            {"natural big islands",
                "NoiseCustom({exponent=2.3,noise={1,1,1,1,1,1,0.7,0.4,0.3,0.2},land_percent=0.2})"},
            {"natural continents",
                "NoiseCustom({exponent=2.4,noise={1,1,1,1,1,1,1,0.6,0.3,0.2},land_percent=0.35})"},
            {"natural half land",
                "NoiseCustom({exponent=2,noise={0.5,1,1,1,1,1,0.7,0.4,0.3,0.2},land_percent=0.5})"},
            {"natural big lakes",
                "NoiseCustom({exponent=2.3,noise={0.5,0.8,1,1,1,1,0.7,0.4,0.3,0.2},land_percent=0.65})"},
            {"natural medium lakes",
                "NoiseCustom({exponent=2.1,noise={0.3,0.6,1,1,1,1,0.7,0.4,0.3,0.2},land_percent=0.86})"},
            {"natural small lakes",
                -- "NoiseCustom({exponent=1.8,noise={0.2,0.3,0.4,0.6,1,1,0.7,0.4,0.3,0.2},land_percent=0.96})"},
                "NoiseCustom({exponent=1.5,noise={0.05,0.1,0.4,0.7,1,0.7,0.3,0.1},land_percent=0.92})"},
            {"pink noise (good luck...)", "NoiseExponent({exponent=1,land_percent = 0.35})"},
            {"radioactive", "Union(AngularRepeat(Halfplane(), 3), Circle(38))"},
            {"comb", "Zoom(Comb(), 50)"},
            {"cross", "Cross(50)"},
            {"cross and circles", "Union(Cross(20), ConcentricBarcode(30, 60))"},
            {"crossing bars", "Union(Barcode(nil, 10, 20), Barcode(nil, 20, 50))"},
            {"grid", "Zoom(Grid(), 50)"},
            {"skew grid", "Zoom(Affine(Grid(), 1, 1, 1, 0), 50)"},
            {"distorted grid", "Distort(Zoom(Grid(), 30))"},
            {"maze 1 (fibonacci)", "Tighten(Zoom(Maze1(), 50))"},
            {"maze 2 (DLA)", "Tighten(Zoom(Maze2(), 50))"},
            {"maze 3 (percolation)", "Tighten(Zoom(Maze3(0.6), 50))"},
            {"polar maze 3", "Zoom(AngularRepeat(Maze3(), 3), 50)"},
            {"bridged maze 3", "IslandifySquares(Maze3(), 50, 10, 4)"},
            {"thin branching fractal", "Fractal(1.5, 40, 0.4)"},
            {"mandelbrot", "Tile(Mandelbrot(300), 150, 315, -600, -315)"},
            {"jigsaw islands", "Zoom(JigsawIslands(0.3), 40)"},
            {"pink noise maze",
                "Intersection(Zoom(Maze2(), 50), NoiseExponent{exponent=1,land_percent=0.8})"},
            {"tiny pot holes", "TP(nil, Zoom(Maze3(0.997), 2))"},
            {"small pot holes", "TP(nil, Zoom(Maze3(0.994), 3))"}
    }
    -- void_pattern_presets = {
            -- {"tiny pot holes", "Maze3(0.997)"},
            -- {"small pot holes", "Zoom(Maze3(0.994), 3)"},
            -- {"custom", nil}
    -- }
}

function preset_by_name(name)
    for _, item in ipairs(meta.pattern_presets) do
        if item[1] == name then
            return item[2]
        end
    end
    return nil
end

local function map_first(xs)
    local result = {}
    for i, x in pairs(xs) do
        table.insert(result, x[1])
    end
    return result
end

local function mk_bool(name, def)
    return {name, "bool", def}
end
local function mk_str(name, def)
    return {name, "string", def}
end
local function mk_dropdown(name, opts, default)
    if default == nil then
        return {name, "string", opts[1], opts}
    else
        return {name, "string", default, opts}
    end
end
local function mk_int(name, def, range)
    if range == nil then
        return {name, "int", def}
    else
        return {name, "int", def, range}
    end
end

meta.settings = {
    mk_dropdown("pattern-preset", map_first(meta.pattern_presets), "maze 2 (DLA)"),
    mk_str("pattern-custom", "(lua code goes here)"),

    mk_str("pattern-v1", "nil"),
    mk_str("pattern-v2", "nil"),
    mk_str("pattern-v3", "nil"),
    mk_str("pattern-v4", "nil"),
    mk_str("pattern-v5", "nil"),
    mk_str("pattern-v6", "nil"),
    mk_str("pattern-v7", "nil"),
    mk_str("pattern-v8", "nil"),

    mk_dropdown("water-color", meta.water_colors),
    mk_int("seed", 0, {0, 2 ^ 32}),

    mk_bool("initial-landfill", false),
    mk_bool("force-initial-water", false),
    mk_bool("big-scan", false),
    mk_bool("screenshot", false),
    mk_bool("screenshot-zoom", false)
}
