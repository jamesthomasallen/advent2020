from pathlib import Path


def read_data(day: str, sep: str = '\n') -> list[str]:
    path = Path(__file__).parent.parent / 'data' / (day+'.txt')
    return path.read_text().strip().split(sep)


def read_data_int(day: str) -> list[int]:
    return [int(i) for i in read_data(day)]


def read_data_dict(day: str) -> list[dict]:
    return [
        dict(tuple(item.split(':')) for item in group.split())
        for group in read_data(day, sep='\n\n')
    ]


def read_data_list(day: str) -> list[list[str]]:
    return [group.split('\n') for group in read_data(day, sep='\n\n')]
