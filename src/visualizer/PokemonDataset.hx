package visualizer;

import haxe.ds.Vector;


typedef DatasetDoc = {
    slugs: Vector<String>,
    stats: Map<String, Dynamic>
};


class PokemonDataset extends Dataset {
    static public var DATASET_FILES(default, null) = ["pbr-gold.json", "pbr-platinum.json", "pbr-seel.json", "pbr-gold-1.2.json", "pbr-gold-1.2-2015-11-07.json"];
    static public var DATASET_NAMES(default, null) = ["Nkekev PBR Gold", "Nkekev PBR Platinum", "TPPVisuals PBR Seel", "Addarash1/Chaos_lord PBR Gold 1.2", "Chauzu PBR Gold 1.2 2015-11-07"];
    static public var DEFAULT_INDEX = 4;

    var datasets:Array<DatasetDoc>;

    public var slugs(get, null):Vector<String>;
    public var stats(get, null):Map<String, Dynamic>;

    public var datasetIndex = 0;

    public function new() {
        super();
        datasets = new Array<DatasetDoc>();
    }

    override public function load(callback) {
        loadOneDataset(callback);
    }

    function loadOneDataset(originalCallback) {
        var filename = DATASET_FILES[datasetIndex];

        makeRequest(filename, function (success) {
            if (success) {
                datasetIndex += 1;

                if (datasetIndex < DATASET_FILES.length) {
                    loadOneDataset(originalCallback);
                } else {
                    if (DEFAULT_INDEX >= 0) {
                        datasetIndex = DEFAULT_INDEX;
                    } else {
                        datasetIndex -= 1;
                    }
                    originalCallback(success);
                }
            } else {
                originalCallback(success);
            }
        });
    }

    override function loadDone(data:Dynamic) {
        var slugs = Reflect.field(data, "pokemon_slugs");
        var stats = Reflect.field(data, "stats");

        var datasetDoc = {
            slugs: slugs,
            stats: stats
        }

        datasets.push(datasetDoc);

        super.loadDone(data);
    }

    function get_slugs():Vector<String> {
        return datasets[datasetIndex].slugs;
    }

    function get_stats():Map<String, Dynamic> {
        return datasets[datasetIndex].stats;
    }

    public function getPokemonStats(slug:String):Dynamic {
        var pokemonStat = Reflect.field(stats, slug);
        Reflect.setField(pokemonStat, "slug", slug);
        return pokemonStat;
    }

    public function getSlug(pokemonNum:Int):String {
        for (slug in slugs) {
            var stats = getPokemonStats(slug);
            if (stats.number == pokemonNum) {
                return slug;
            }
        }

        throw "Unknown Pokemon number.";
    }
}
