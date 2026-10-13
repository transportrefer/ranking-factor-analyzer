"""Shared Unicode tokenization and small language-specific lexical rules.

Unknown languages retain Unicode words but use no English lexical heuristics.
This is tokenization, not stemming or compound-word segmentation.
"""
from __future__ import annotations

import re
import unicodedata

_WORD_RE = re.compile(r"[^\W_]+(?:'[^\W_]+)*", re.UNICODE)
DANISH_STOPWORDS = frozenset("""
og i jeg det at en den til er som på de med han af for ikke der var mig sig
men et har om vi min havde ham hun nu over da fra du ud sin dem os op man
hans hvor eller hvad skal selv her alle vil blev kunne ind når være dog noget
ville jo deres efter ned skulle denne end dette mit også under have dig anden
hende mine alt meget sit sine vor mod disse hvis din nogle hos blive mange
sådan ved kun mere meget hvorfra hvorfor hvordan hvem hvilken hvilke hvornår
""".split())
QUESTION_WORDS = {
    "en": frozenset("who what when where why how which can do does is are".split()),
    "da": frozenset("hvem hvad hvornår hvor hvorfor hvordan hvilken hvilket hvilke kan er har skal bør må".split()),
}


def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFC", text or "").lower()


def tokens(text: str) -> list[str]:
    return _WORD_RE.findall(normalize_text(text))


def language_code(language: str) -> str:
    return (language or "en").lower().replace("_", "-").split("-")[0]


def stopwords(language: str, english: set[str]) -> set[str] | frozenset[str]:
    code = language_code(language)
    return english if code == "en" else DANISH_STOPWORDS if code == "da" else frozenset()


def default_language(country: str) -> str:
    return "da" if country.strip().lower() == "dk" else "en"
