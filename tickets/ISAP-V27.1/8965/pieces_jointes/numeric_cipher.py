#!/usr/bin/env python3
"""Encode ou decode un slug en code base62 de longueur fixe."""

import argparse
import hashlib
import math


SECRET = "IsapAdm1n"
OUTPUT_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
SOURCE_ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789-"
OUTPUT_LENGTH = 10
MAX_TEXT_LENGTH = 11


def encode_number(value: int, alphabet: str, width: int) -> str:
    """Encode un entier dans l'alphabet cible avec une longueur fixe."""

    if value < 0:
        raise ValueError("La valeur a encoder doit etre positive.")

    base = len(alphabet)
    if value == 0:
        return alphabet[0] * width

    chars = []
    current = value
    while current > 0:
        current, remainder = divmod(current, base)
        chars.append(alphabet[remainder])

    return "".join(reversed(chars)).rjust(width, alphabet[0])


def decode_number(encoded_text: str, alphabet: str) -> int:
    """Decode un entier depuis l'alphabet cible."""

    index_by_char = {char: index for index, char in enumerate(alphabet)}
    invalid_chars = [char for char in encoded_text if char not in index_by_char]
    if invalid_chars:
        raise ValueError("Le code contient des caracteres incompatibles avec l'alphabet base62.")

    base = len(alphabet)
    value = 0
    for char in encoded_text:
        value = value * base + index_by_char[char]

    return value


def rank_text(text: str) -> int:
    """Convertit un slug en entier."""

    index_by_char = {char: index for index, char in enumerate(SOURCE_ALPHABET)}
    invalid_chars = [char for char in text if char not in index_by_char]
    if invalid_chars:
        raise ValueError("Le texte ne peut contenir que des minuscules, chiffres ou '-'.")

    value = 0
    for char in text:
        value = value * len(SOURCE_ALPHABET) + index_by_char[char]

    return value


def unrank_text(value: int, text_length: int) -> str:
    """Reconstruit un slug de longueur fixe depuis son rang."""

    chars = [SOURCE_ALPHABET[0]] * text_length
    current = value

    for index in range(text_length - 1, -1, -1):
        current, remainder = divmod(current, len(SOURCE_ALPHABET))
        chars[index] = SOURCE_ALPHABET[remainder]

    if current != 0:
        raise ValueError("La valeur a decoder depasse la capacite du texte cible.")

    return "".join(chars)


def domain_size_for_max_length() -> int:
    """Retourne la taille du domaine cumule pour les longueurs 1 a MAX_TEXT_LENGTH."""

    return sum(len(SOURCE_ALPHABET) ** length for length in range(1, MAX_TEXT_LENGTH + 1))


def encoded_width_for_value(max_value: int) -> int:
    """Retourne la longueur base62 necessaire pour encoder une valeur maximale."""

    base = len(OUTPUT_ALPHABET)
    width = 1
    while base ** width <= max_value:
        width += 1
    return width


def rank_variable_length_text(text: str) -> tuple[int, int]:
    """Encode un texte variable dans le domaine cumule des longueurs autorisees."""

    text_length = len(text)
    if text_length < 1 or text_length > MAX_TEXT_LENGTH:
        raise ValueError(f"Le texte doit contenir entre 1 et {MAX_TEXT_LENGTH} caracteres.")

    offset = sum(len(SOURCE_ALPHABET) ** length for length in range(1, text_length))
    return offset + rank_text(text), domain_size_for_max_length()


def unrank_variable_length_text(value: int) -> str:
    """Reconstruit un texte variable depuis le domaine cumule des longueurs autorisees."""

    running_offset = 0
    for text_length in range(1, MAX_TEXT_LENGTH + 1):
        block_size = len(SOURCE_ALPHABET) ** text_length
        next_offset = running_offset + block_size
        if value < next_offset:
            return unrank_text(value - running_offset, text_length)
        running_offset = next_offset

    raise ValueError("Le code ne correspond a aucune longueur de texte autorisee.")


def build_domain_mask(domain_size: int) -> int:
    """Construit un masque pseudo-aleatoire borne au domaine cible."""

    digest = hashlib.sha256(SECRET.encode("utf-8") + domain_size.to_bytes(16, byteorder="big")).digest()
    return int.from_bytes(digest, byteorder="big") % domain_size


def build_affine_parameters(domain_size: int, code_space: int) -> tuple[int, int]:
    """Construit une transformation affine inversible sur l'espace des codes."""

    seed = hashlib.sha256(
        SECRET.encode("utf-8")
        + domain_size.to_bytes(16, byteorder="big")
        + code_space.to_bytes(16, byteorder="big")
    ).digest()
    multiplier = max(1, int.from_bytes(seed[:16], byteorder="big") % code_space)
    offset = int.from_bytes(seed[16:], byteorder="big") % code_space

    while math.gcd(multiplier, code_space) != 1:
        multiplier += 1
        if multiplier >= code_space:
            multiplier = 1

    return multiplier, offset


def spread_rank(rank: int, domain_size: int, code_space: int) -> int:
    """Projette un rang sur tout l'espace de sortie fixe."""

    multiplier, offset = build_affine_parameters(domain_size, code_space)
    return (rank * multiplier + offset) % code_space


def unspread_rank(value: int, domain_size: int, code_space: int) -> int:
    """Inverse la projection sur l'espace de sortie fixe."""

    multiplier, offset = build_affine_parameters(domain_size, code_space)
    inverse_multiplier = pow(multiplier, -1, code_space)
    return ((value - offset) * inverse_multiplier) % code_space


def encode_slug(text: str) -> str:
    """Encode un slug vers un code base62 sur 10 caracteres."""

    rank, domain_size = rank_variable_length_text(text)
    masked = (rank + build_domain_mask(domain_size)) % domain_size
    minimum_length = encoded_width_for_value(domain_size - 1)
    if OUTPUT_LENGTH < minimum_length:
        raise ValueError(f"{OUTPUT_LENGTH} caracteres ne suffisent pas pour ce domaine.")

    if OUTPUT_LENGTH == minimum_length:
        return encode_number(masked, OUTPUT_ALPHABET, OUTPUT_LENGTH)

    code_space = len(OUTPUT_ALPHABET) ** OUTPUT_LENGTH
    spread_value = spread_rank(masked, domain_size, code_space)
    return encode_number(spread_value, OUTPUT_ALPHABET, OUTPUT_LENGTH)


def decode_slug(code: str) -> str:
    """Decode un code base62 sur 10 caracteres vers son slug d'origine."""

    if len(code) != OUTPUT_LENGTH:
        raise ValueError(f"Le code doit contenir exactement {OUTPUT_LENGTH} caracteres.")

    domain_size = domain_size_for_max_length()
    minimum_length = encoded_width_for_value(domain_size - 1)
    encoded_value = decode_number(code, OUTPUT_ALPHABET)

    if OUTPUT_LENGTH == minimum_length:
        masked = encoded_value
        if masked >= domain_size:
            raise ValueError("Le code depasse la capacite du domaine texte configure.")
    else:
        code_space = len(OUTPUT_ALPHABET) ** OUTPUT_LENGTH
        masked = unspread_rank(encoded_value, domain_size, code_space)
        if masked >= domain_size:
            raise ValueError("Le code n'appartient pas au domaine texte configure.")

    rank = (masked - build_domain_mask(domain_size)) % domain_size
    return unrank_variable_length_text(rank)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Encode ou decode un texte slug en code base62 fixe sur 10 caracteres.",
    )
    parser.add_argument("mode", choices=["encode", "decode"], help="Operation a effectuer")
    parser.add_argument("value", help="Texte a encoder ou code a decoder")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.mode == "encode":
            print(encode_slug(args.value))
            return

        print(decode_slug(args.value))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()