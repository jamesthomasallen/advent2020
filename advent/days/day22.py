from advent.util import read_data_list


def main() -> list[int]:
    deck_1, deck_2 = [[int(c) for c in cards[1:]] for cards in read_data_list('day22')]
    final_1, final_2, winner = play_combat(deck_1, deck_2, recursive=False)
    result_1 = count_score(final_1 if winner == 1 else final_2)
    final_1, final_2, winner = play_combat(deck_1, deck_2, recursive=True)
    result_2 = count_score(final_1 if winner == 1 else final_2)
    return [result_1, result_2]


def play_combat(deck_1: list[int], deck_2: list[int], recursive: bool,
                ) -> tuple[list[int], list[int], int]:
    history = []

    while True:
        if (deck_1, deck_2) in history:
            return deck_1, deck_2, 1
        history.append((deck_1, deck_2))

        if not deck_1 or not deck_2:
            return deck_1, deck_2, 1 if deck_1 else 2

        card_1, deck_1 = deck_1[0], deck_1[1:]
        card_2, deck_2 = deck_2[0], deck_2[1:]
        winning_card = combat_round(card_1, card_2, deck_1, deck_2, recursive=recursive)
        if winning_card == 1:
            deck_1 = deck_1 + [card_1, card_2]
        else:
            deck_2 = deck_2 + [card_2, card_1]


def combat_round(card_1: int, card_2: int, deck_1: list[int], deck_2: list[int], recursive: bool,
                 ) -> int:
    if recursive and len(deck_1) >= card_1 and len(deck_2) >= card_2:
        return play_combat(deck_1[:card_1], deck_2[:card_2], recursive=recursive)[-1]
    else:
        return 1 if card_1 > card_2 else 2


def count_score(deck: list[int]) -> int:
    return sum((i+1) * card for i, card in enumerate(deck[::-1]))
