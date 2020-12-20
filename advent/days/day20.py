from typing import Iterator, Optional
from math import prod, sqrt
import re

from advent.util import read_data


MONSTER = '''
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
'''.strip('\n')


def main() -> list[int]:
    tiles_raw = read_data('day20', sep='\n\n')
    tiles = process_tiles(tiles_raw)
    layout = find_layout(tiles)
    result_1 = prod([layout[i][j]['index'] for i in (0, -1) for j in (0, -1)])
    image = stitch_image(layout)
    new_image, monsters = count_monsters(image)
    result_2 = new_image.count('#')
    return [result_1, result_2]


def process_tiles(tiles_raw: list[str]) -> list[dict]:
    return [process_tile(tile_raw) for tile_raw in tiles_raw]


def process_tile(tile_raw: str) -> dict:
    title, image = tile_raw.split(':\n')
    return {
        'raw': tile_raw,
        'orientations': catalogue_orientations(image, int(title.removeprefix('Tile '))),
    }


def catalogue_orientations(image: str, index: int) -> list[dict]:
    result = []
    for orientated in list_orientations(image):
        rows = orientated.split('\n')
        result.append({
            'image': orientated,
            'top': rows[0],
            'bottom': rows[-1],
            'left': ''.join(r[0] for r in rows),
            'right': ''.join(r[-1] for r in rows),
            'index': index,
        })
    return result


def list_orientations(image: str) -> list[str]:
    return list_rotations(image) + list_rotations(flip_image(image))


def list_rotations(image: str) -> list[str]:
    result = [image]
    for _ in range(3):
        image = rotate_image(image)
        result.append(image)
    return result


def rotate_image(image: str) -> str:
    return '\n'.join(''.join(x) for x in zip(*[r[::-1] for r in image.split('\n')]))


def flip_image(image: str) -> str:
    return '\n'.join(image.split('\n')[::-1])


def find_layout(tiles: list[dict]) -> list[list[dict]]:
    length = int(sqrt(len(tiles)))
    empty = [[None for _ in range(length)] for _ in range(length)]
    return next(yield_layouts(empty, tiles, 0, 0))


def yield_layouts(layout: list[list[Optional[dict]]], tiles: list[dict], i_row: int, i_col: int,
                  ) -> Iterator[list[list[dict]]]:
    requirements = {}
    if i_row != 0:
        requirements['top'] = layout[i_row-1][i_col]['bottom']
    if i_col != 0:
        requirements['left'] = layout[i_row][i_col-1]['right']
    if i_col == len(layout)-1:
        next_col = 0
        next_row = i_row + 1
    else:
        next_col = i_col + 1
        next_row = i_row
    for tile in tiles:
        others = [t for t in tiles if t is not tile]
        for orientation in tile['orientations']:
            if all(orientation[key] == value for key, value in requirements.items()):
                new_layout = [
                    row if ir != i_row else
                    [t if ic != i_col else orientation for ic, t in enumerate(row)]
                    for ir, row in enumerate(layout)
                ]
                if others:
                    yield from yield_layouts(new_layout, others, next_row, next_col)
                else:
                    yield new_layout


def stitch_image(layout: list[list[dict]]) -> str:
    rows = []
    tile_height = len(layout[0][0]['image'].split('\n'))
    for tile_row in layout:
        for i in range(1, tile_height-1):
            rows.append(
                ''.join(
                    tile['image'].split('\n')[i][1:-1] for tile in tile_row
                )
            )
    return '\n'.join(rows)


def count_monsters(image: str) -> tuple[str, int]:
    for orientated in list_orientations(image):
        new_image, monsters = count_monsters_orientation(orientated)
        if monsters:
            return new_image, monsters
    raise RuntimeError


def count_monsters_orientation(image: str) -> tuple[str, int]:
    monster_re, monster_highlight = prepare_monster_re(image)
    count = 0
    new_count = -1
    while new_count != 0:
        image, new_count = re.subn(monster_re, monster_highlight, image, flags=re.DOTALL)
        count += new_count
    return image, count


def prepare_monster_re(image: str) -> tuple[str, str]:
    monster_padded = pad_monster(image)
    monster_re = '#'.join(
        '(.{'+str(len(spaces))+'})' if spaces else ''
        for spaces in monster_padded.split('#')
    )
    monster_highlight = ''
    i = 1
    for spaces in monster_padded.split('#'):
        if spaces:
            monster_highlight = monster_highlight + '\\' + str(i)
            i += 1
        monster_highlight = monster_highlight + 'O'
    monster_highlight = monster_highlight[:-1]
    return monster_re, monster_highlight


def pad_monster(image: str) -> str:
    image_width = len(image.split('\n')[0])
    monster_rows = MONSTER.split('\n')
    monster_width = len(monster_rows[0])
    padding = ' ' * (image_width - monster_width + 1)
    monster_padded = ''.join(
        row + padding for row in monster_rows[:-1]
    ) + monster_rows[-1]
    return monster_padded
