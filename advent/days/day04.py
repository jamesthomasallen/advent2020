import re

from advent.util import read_data_dict


REQUIRED = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')


def main() -> list[int]:
    passports = read_data_dict('day04')
    n_valid_1 = sum(has_passport_keys(passport) for passport in passports)
    n_valid_2 = sum(is_valid_passport(passport) for passport in passports)
    return [n_valid_1, n_valid_2]


def has_passport_keys(passport: dict) -> bool:
    return all(r in passport for r in REQUIRED)


def is_valid_passport(passport: dict) -> bool:
    return (
        has_passport_keys(passport) and
        is_valid_byr(passport['byr']) and
        is_valid_iyr(passport['iyr']) and
        is_valid_eyr(passport['eyr']) and
        is_valid_hgt(passport['hgt']) and
        is_valid_hcl(passport['hcl']) and
        is_valid_ecl(passport['ecl']) and
        is_valid_pid(passport['pid'])
    )


def bool_match(pattern: str, string: str) -> bool:
    return bool(re.match(pattern, string))


def is_int_in_range(int_str: str, lower: int, upper: int) -> bool:
    return int_str.isdigit() and lower <= int(int_str) <= upper


def is_valid_byr(byr_str: str) -> bool:
    return is_int_in_range(byr_str, 1920, 2002)


def is_valid_iyr(iyr_str: str) -> bool:
    return is_int_in_range(iyr_str, 2010, 2020)


def is_valid_eyr(eyr_str: str) -> bool:
    return is_int_in_range(eyr_str, 2020, 2030)


def is_valid_hgt(hgt_str: str) -> bool:
    return (
        (bool_match(r'\d+cm', hgt_str) and is_int_in_range(hgt_str[:-2], 150, 193)) or
        (bool_match(r'\d+in', hgt_str) and is_int_in_range(hgt_str[:-2], 59, 76))
    )


def is_valid_hcl(hcl_str: str) -> bool:
    return bool_match(r'#[0-9a-f]{6}', hcl_str)


def is_valid_ecl(ecl_str: str) -> bool:
    return ecl_str in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')


def is_valid_pid(pid_str: str) -> bool:
    return len(pid_str) == 9 and is_int_in_range(pid_str, 0, 999999999)
