FogChamp
========

Pokémon Battle Revolution Matchup Visualizer for Twitch Plays Pokemon.


Quick Start
===========

You will need:

* Python 3+
* Haxe 3.2+
* Linux OS

1. Clone this repo
2. Initialize veekun's Pokedex: `git submodule init`
3. Generate the JSON files: `python3 -m util.csv2json`
4. Copy `static/` to `static/` on your web server
5. Copy the icons from http://veekun.com/dex/downloads to `static/veekun/icons/` on your web server
6. Copy the JSON files (`pbr-platnium.json`, `moves.json`, `descriptions.json`) to your web server
7. Copy the `script.js` file to your web server
8. Copy `visualizer.html` (rename to `index.html` if desired) & `style.css` to your web server.


Credits
=======

Copyright 2015 Christopher Foo. Licensed under the MIT license.

The PBR metadata was obtained from Nkekev's docs.

Contains mustache.js. MIT license.

This visualizer was inspired by Felk's visualizer which I can't find the complete source code to.


