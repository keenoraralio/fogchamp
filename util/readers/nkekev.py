import re

from util.readers.base import Reader


TYPO_REPLACEMENTS = {
    'Aurasphere': 'Aura Sphere',
    'DynamicPunch': 'Dynamic Punch',
    'Solarbeam': 'Solar Beam',
    'Recovery': 'Recover',
    'Shockwave': 'Shock Wave',
    'Twinneedle': 'Twineedle',
    'Icicle Cannon': 'Icicle Spear',
    'Adaptabillity': 'Adaptability',
    'Extremespeed': 'Extreme Speed',
    'Dragonbreath': 'Dragon Breath',
    'Hi Jump Kick': 'High Jump Kick',
    'Vaccum Wave': 'Vacuum Wave',
    'Iron Defence': 'Iron Defense',
    'Featherdance': 'Feather Dance',
    'Thundershock': 'Thunder Shock',
    'Grasswhistle': 'Grass Whistle',
}


class NkekevReader(Reader):
    def read_pbr_moveset(self, filename, row_has_gender=True):
        with self.read_csv(filename) as reader:
            prev_number = None

            for index, row in enumerate(reader):
                if index == 0:
                    continue

                if not row_has_gender:
                    row.insert(0, '-')

                (
                    gender,
                    number,
                    name,
                    ability,
                    move_a,
                    move_b,
                    move_c,
                    move_d,
                    iv,
                    hp,
                    attack,
                    defense,
                    special_attack,
                    special_defense,
                    speed,
                    nature,
                    item,
                    *dummy
                ) = row

                if not name:
                    continue

                if not number or number == '-':
                    number = prev_number

                name = rewrite_pokemon_name(name)
                number = int(number)
                iv = int(number)
                hp = int(hp)
                attack = int(attack)
                defense = int(defense)
                special_attack = int(special_attack)
                special_defense = int(special_defense)
                speed = int(speed)

                happiness = None

                moves = []

                for move in [move_a, move_b, move_c, move_d]:
                    if move:
                        happiness_match = re.search(r' \((\d+|max)\)', move)

                        if happiness_match:
                            happiness = happiness_match.group(1)

                            if happiness == 'max':
                                # Max as in max frustration pp, not happiness
                                happiness = 0
                            else:
                                happiness = int(happiness)

                        moves.append(slugify(move))

                doc = {
                    'gender': gender,
                    'name': name,
                    'slug': slugify(name),
                    'number': number,
                    'ability': slugify(ability),
                    'moves': moves,
                    'iv': iv,
                    'hp': hp,
                    'attack': attack,
                    'defense': defense,
                    'special_attack': special_attack,
                    'special_defense': special_defense,
                    'speed': speed,
                    'nature': slugify(nature),
                    'item': slugify(item),
                    'happiness': happiness,
                }

                move_type_override_match = re.search(r'Hidden Power \((\w+)\)', move_a)

                if move_type_override_match:
                    doc['move_type_override'] = slugify(move_type_override_match.group(1))

                yield doc

                prev_number = number

    def read_pbr_platinum(self):
        return self.read_pbr_moveset('pbr-platinum.csv')

    def read_pbr_gold(self):
        return self.read_pbr_moveset('pbr-gold.csv', row_has_gender=False)


def rewrite_pokemon_name(name):
    if name == 'Charmelon':
        name = 'Charmeleon'

    name = name.replace('♀', '-F').replace('♂', '-M')

    if name.startswith('Shiny '):
        return '{} (Shiny)'.format(name.replace('Shiny ', ''))

    return name


def slugify(name):
    name = name.strip()

    if name.startswith('Hidden Power'):
        name = 'Hidden Power'

    if name.startswith('HP '):
        name = 'Hidden Power'

    if name in TYPO_REPLACEMENTS:
        name = TYPO_REPLACEMENTS[name]

    name = name.replace(' (Sand)', ' (Sandy)')
    if name.endswith('-Sand'):
        name = name.replace('-Sand', '-Sandy')

    name = re.sub(r' \((\d+|max)\)', '', name)  # Things like "Frustation (90)"
    name = name.lower().replace(' ', '-')
    name = name.replace('toxik', 'toxic')
    name = re.sub(r'[^a-zA-Z0-9-]', '', name)
    return name
