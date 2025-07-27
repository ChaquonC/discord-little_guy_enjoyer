import os

from dotenv import load_dotenv
from little_guy_bot import resources

load_dotenv()
B = os.getenv('USER1')
T = os.getenv('USER2')
S = os.getenv('USER3')

PIKMIN_TYPES = {
    0: {
        'name': 'Blue Pikmin',
        'image': resources.blue_pikmin,
    },
    1: {
        'name': 'Yellow Pikmin',
        'image': resources.yellow_pikmin,
        'parent': B
    },
    2: {
        'name': 'Purple Pikmin',
        'image': resources.purple_pikmin,
        'parent': S
    },
    3: {
        'name': 'Red Pikmin',
        'image': resources.red_pikmin,
    },
    4: {
        'name': 'Winged Pikmin',
        'image': resources.winged_pikmin
    },
    5: {
        'name': 'White Pikmin',
        'image': resources.white_pikmin
    },
    6: {
        'name': 'Ice Pikmin',
        'image': resources.ice_pikmin
    },
    7: {
        'name': 'Rock Pikmin',
        'image': resources.rock_pikmin
    },
    8: {
        'name': 'Glow Pikmin',
        'image': resources.glow_pikmin,
        'owner': T
    },
    9: {
        'name': 'bulbmin',
        'image': resources.bulbmin
    }
}