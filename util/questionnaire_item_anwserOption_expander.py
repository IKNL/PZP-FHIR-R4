#!/usr/bin/env python3
"""Expand Questionnaire ``answerValueSet`` references into inline ``answerOption`` lists.

Why this exists
---------------
The NLM LHC-Forms tool (https://lhcforms.nlm.nih.gov/) cannot resolve ``answerValueSet``
references against a terminology server. To preview/use the ACP Questionnaire there, every
question that points at a ValueSet needs the matching codes materialised as ``answerOption``.

What the script does
--------------------
For every ``Questionnaire`` resource found in ``input/resources`` it walks the item tree and,
for each item that has an ``answerValueSet``, it:

  1. Resolves the ValueSet, looking first in the local ``fsh-generated/resources`` folder and
     then in the FHIR package cache (``~/.fhir/packages``). The packages to scan are taken
     from the ``dependencies:`` block of ``sushi-config.yaml``; if that is missing, the
     resolved dependency list in ``fhirpkg.lock.json`` is used instead. As a last resort the
     whole package cache is searched.
  2. Expands it:
       * a pre-computed ``expansion.contains`` is used as-is when present;
       * otherwise ``compose.include`` is processed - explicit ``concept`` lists are used
         directly, ``valueSet`` imports are resolved recursively, and a bare ``system``
         (whole code system) is enumerated from the resolved CodeSystem;
       * ``compose.exclude`` entries are removed;
       * the CodeSystem is consulted to fill in a missing ``display``.
  3. Replaces the item's ``answerValueSet`` with the resulting ``answerOption`` array.

Because the form is Dutch, the Dutch (``nl-NL``) designation is preferred for the display,
falling back to the concept's base ``display`` and finally the code.

Some ValueSets reference a CodeSystem we have no access to (e.g. the UZI based
``SpecialismeCodelijst``). For those a fixed answer list is supplied via ``HARDCODED_ANSWER_OPTIONS``.

The original files are left untouched; a copy suffixed with ``-expanded`` is written next to
each source Questionnaire.

Usage
-----
    python util/questionnaire_item_anwserOption_expander.py
    python util/questionnaire_item_anwserOption_expander.py --input-dir input/resources
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------------------

# Repository root (this file lives in <root>/util/).
ROOT = Path(__file__).resolve().parent.parent

# Where the source Questionnaires live and where expanded copies are written.
DEFAULT_INPUT_DIR = ROOT / "input" / "resources"

# Locally generated conformance resources (ValueSets / CodeSystems produced by SUSHI).
FSH_GENERATED_DIR = ROOT / "fsh-generated" / "resources"

# Resolved dependency list (authoritative); fall back to sushi-config.yaml if absent.
LOCK_FILE = ROOT / "fhirpkg.lock.json"
SUSHI_CONFIG = ROOT / "sushi-config.yaml"

# FHIR package cache. Honour the standard override, otherwise ~/.fhir/packages.
import os

FHIR_PACKAGE_CACHE = Path(
    os.environ.get("FHIR_PACKAGE_CACHE", Path.home() / ".fhir" / "packages")
)

# Suffix added to the expanded copy (before the .json extension).
OUTPUT_SUFFIX = "-expanded"

# Preferred display language (the form is Dutch).
PREFERRED_LANGUAGE = "nl-NL"

# SNOMED CT system URL. SNOMED designations often carry a trailing semantic tag in
# parentheses (e.g. "ja (kwalificatiewaarde)"); that tag is stripped from the display.
SNOMED_SYSTEM = "http://snomed.info/sct"

# ValueSets that cannot be resolved from the packages (their CodeSystem is not available).
# Map the ValueSet canonical URL to a fixed list of FHIR answerOption entries.
HARDCODED_ANSWER_OPTIONS = {
    # Functie (Specialisme) - SpecialismeCodelijst. Imports UZI based code lists that are
    # not distributed in the package cache, so a representative subset is hardcoded.
    "http://decor.nictiz.nl/fhir/ValueSet/2.16.840.1.113883.2.4.3.11.60.121.11.22--20200901000000": [
        {"valueCoding": {"system": "http://fhir.nl/fhir/NamingSystem/uzi-rolcode", "code": "01.000", "display": "Arts"}},
        {"valueCoding": {"system": "http://fhir.nl/fhir/NamingSystem/uzi-rolcode", "code": "01.015", "display": "Huisarts"}},
        {"valueCoding": {"system": "http://fhir.nl/fhir/NamingSystem/uzi-rolcode", "code": "01.047", "display": "Specialist ouderengeneeskunde"}},
        {"valueCoding": {"system": "http://fhir.nl/fhir/NamingSystem/uzi-rolcode", "code": "30.000", "display": "Verpleegkundige"}},
        {"valueCoding": {"system": "http://fhir.nl/fhir/NamingSystem/uzi-rolcode", "code": "81.000", "display": "Physician assistant"}},
        {"valueCoding": {"system": "http://fhir.nl/fhir/NamingSystem/uzi-rolcode", "code": "99.000", "display": "Zorgverlener andere zorg"}},
    ],
}


# --------------------------------------------------------------------------------------
# Resource resolver: maps canonical URL -> file path for ValueSets and CodeSystems.
# --------------------------------------------------------------------------------------


class ResourceResolver:
    """Locate ValueSet / CodeSystem resources locally and in the FHIR package cache."""

    def __init__(self) -> None:
        # url -> Path. Local (fsh-generated) entries take precedence over package entries.
        self._valuesets: dict[str, Path] = {}
        self._codesystems: dict[str, Path] = {}
        # Cache of loaded JSON resources keyed by path.
        self._loaded: dict[Path, dict] = {}
        self._scanned_full_cache = False

        self._index_local()
        self._index_declared_packages()

    # -- index building -----------------------------------------------------------------

    def _register(self, url: str | None, resource_type: str | None, path: Path) -> None:
        if not url or not resource_type:
            return
        target = self._valuesets if resource_type == "ValueSet" else (
            self._codesystems if resource_type == "CodeSystem" else None
        )
        if target is None:
            return
        # First registration wins (local before packages, declared deps before fallback).
        target.setdefault(url, path)

    def _index_local(self) -> None:
        """Index ValueSets / CodeSystems generated locally by SUSHI."""
        if not FSH_GENERATED_DIR.is_dir():
            return
        for path in FSH_GENERATED_DIR.glob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if isinstance(data, dict):
                self._register(data.get("url"), data.get("resourceType"), path)
                # Cache it - we already paid the read cost.
                self._loaded[path] = data

    def _package_dirs_from_dependencies(self) -> list[Path]:
        """Determine which package directories to index from the project dependencies."""
        deps: dict[str, str] = {}

        # Primary source: the dependencies declared in sushi-config.yaml.
        if SUSHI_CONFIG.is_file():
            deps.update(_parse_sushi_dependencies(SUSHI_CONFIG))

        # Fallback: the resolved dependency list in fhirpkg.lock.json.
        if not deps and LOCK_FILE.is_file():
            try:
                lock = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
                deps.update(lock.get("dependencies", {}))
            except (json.JSONDecodeError, OSError):
                pass

        # hl7.fhir.r4.core is always needed for base FHIR code systems.
        deps.setdefault("hl7.fhir.r4.core", "4.0.1")

        dirs: list[Path] = []
        for pkg_id, version in deps.items():
            candidate = FHIR_PACKAGE_CACHE / f"{pkg_id}#{version}"
            if candidate.is_dir():
                dirs.append(candidate)
            else:
                print(f"  ! dependency package not found in cache: {pkg_id}#{version}",
                      file=sys.stderr)
        return dirs

    def _index_package_dir(self, pkg_dir: Path) -> None:
        index_file = pkg_dir / "package" / ".index.json"
        if not index_file.is_file():
            return
        try:
            index = json.loads(index_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        for entry in index.get("files", []):
            rtype = entry.get("resourceType")
            if rtype not in ("ValueSet", "CodeSystem"):
                continue
            filename = entry.get("filename")
            if not filename:
                continue
            self._register(entry.get("url"), rtype, pkg_dir / "package" / filename)

    def _index_declared_packages(self) -> None:
        for pkg_dir in self._package_dirs_from_dependencies():
            self._index_package_dir(pkg_dir)

    def _index_full_cache(self) -> None:
        """Fallback: index every package in the cache (used only when a URL is missing)."""
        if self._scanned_full_cache or not FHIR_PACKAGE_CACHE.is_dir():
            return
        self._scanned_full_cache = True
        for pkg_dir in FHIR_PACKAGE_CACHE.iterdir():
            if pkg_dir.is_dir():
                self._index_package_dir(pkg_dir)

    # -- loading ------------------------------------------------------------------------

    def _load(self, path: Path) -> dict | None:
        if path in self._loaded:
            return self._loaded[path]
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
        self._loaded[path] = data
        return data

    def get_valueset(self, url: str) -> dict | None:
        url = _strip_version(url)
        if url not in self._valuesets:
            self._index_full_cache()
        path = self._valuesets.get(url)
        return self._load(path) if path else None

    def get_codesystem(self, url: str) -> dict | None:
        url = _strip_version(url)
        if url not in self._codesystems:
            self._index_full_cache()
        path = self._codesystems.get(url)
        return self._load(path) if path else None


def _strip_version(url: str) -> str:
    """Drop a trailing ``|version`` from a canonical reference."""
    return url.split("|", 1)[0] if url else url


def _parse_sushi_dependencies(config_path: Path) -> dict[str, str]:
    """Minimal parser for the ``dependencies:`` block of sushi-config.yaml.

    Avoids a hard dependency on PyYAML. Only handles the simple ``id: version`` form,
    which is what this project uses.
    """
    deps: dict[str, str] = {}
    try:
        lines = config_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return deps

    in_block = False
    dep_re = re.compile(r"^(\s*)([A-Za-z0-9._-]+)\s*:\s*([^\s#]+)")
    for line in lines:
        stripped = line.strip()
        if not in_block:
            if stripped.startswith("dependencies:"):
                in_block = True
            continue
        # Stop when a new top-level (non-indented, non-comment) key starts.
        if stripped and not line[0].isspace() and not stripped.startswith("#"):
            break
        if not stripped or stripped.startswith("#"):
            continue
        m = dep_re.match(line)
        if m:
            deps[m.group(2)] = m.group(3)
    return deps


# --------------------------------------------------------------------------------------
# ValueSet expansion
# --------------------------------------------------------------------------------------


_SNOMED_SEMANTIC_TAG = re.compile(r"\s*\([^()]*\)\s*$")


def _clean_display(display: str | None, system: str | None) -> str | None:
    """Strip the trailing SNOMED semantic tag (e.g. " (kwalificatiewaarde)") from a display."""
    if display and system == SNOMED_SYSTEM:
        stripped = _SNOMED_SEMANTIC_TAG.sub("", display).strip()
        if stripped:
            return stripped
    return display


def _dutch_display(concept: dict, system: str | None = None) -> str | None:
    """Return the preferred display for a concept, favouring the Dutch designation.

    For SNOMED concepts a parenthesis-free designation is preferred, and any remaining
    trailing semantic tag is stripped (so "ja (kwalificatiewaarde)" becomes "ja").
    """
    nl_values = [
        d["value"] for d in concept.get("designation", [])
        if d.get("language") == PREFERRED_LANGUAGE and d.get("value")
    ]
    display = None
    if nl_values:
        # Prefer a Dutch designation without a parenthetical part, if one exists.
        display = next((v for v in nl_values if "(" not in v), nl_values[0])
    else:
        display = concept.get("display")
    return _clean_display(display, system)


def _codesystem_display_map(codesystem: dict, system: str | None = None) -> dict[str, str]:
    """Flatten a (possibly hierarchical) CodeSystem into code -> display."""
    result: dict[str, str] = {}

    def walk(concepts: list) -> None:
        for concept in concepts:
            code = concept.get("code")
            if code is not None:
                result[code] = _dutch_display(concept, system) or concept.get("display") or code
            if concept.get("concept"):
                walk(concept["concept"])

    walk(codesystem.get("concept", []))
    return result


class ValueSetExpander:
    def __init__(self, resolver: ResourceResolver) -> None:
        self.resolver = resolver

    def expand(self, url: str) -> list[dict]:
        """Expand a ValueSet URL into a list of FHIR ``answerOption`` entries."""
        if url in HARDCODED_ANSWER_OPTIONS:
            return [dict(opt) for opt in HARDCODED_ANSWER_OPTIONS[url]]

        codings = self._expand_to_codings(url, seen=set())
        return [{"valueCoding": coding} for coding in codings]

    def _expand_to_codings(self, url: str, seen: set[str]) -> list[dict]:
        url = _strip_version(url)
        if url in seen:
            return []  # guard against circular imports
        seen.add(url)

        valueset = self.resolver.get_valueset(url)
        if valueset is None:
            raise LookupError(f"ValueSet not found: {url}")

        codings: list[dict] = []

        # 1. Pre-computed expansion wins.
        expansion = valueset.get("expansion", {})
        for contains in expansion.get("contains", []):
            self._collect_contains(contains, codings)
        if codings:
            return _dedupe(codings)

        compose = valueset.get("compose", {})

        # 2. Includes.
        for include in compose.get("include", []):
            codings.extend(self._expand_include(include, seen))

        # 3. Excludes - drop matching (system, code) pairs.
        excluded = set()
        for exclude in compose.get("exclude", []):
            for coding in self._expand_include(exclude, seen):
                excluded.add((coding.get("system"), coding.get("code")))
        if excluded:
            codings = [c for c in codings if (c.get("system"), c.get("code")) not in excluded]

        return _dedupe(codings)

    def _collect_contains(self, contains: dict, out: list[dict]) -> None:
        if not contains.get("abstract") and contains.get("code") is not None:
            coding = {}
            if contains.get("system"):
                coding["system"] = contains["system"]
            coding["code"] = contains["code"]
            display = _dutch_display(contains, contains.get("system"))
            if display:
                coding["display"] = display
            out.append(coding)
        for child in contains.get("contains", []):
            self._collect_contains(child, out)

    def _expand_include(self, include: dict, seen: set[str]) -> list[dict]:
        codings: list[dict] = []

        # Imported ValueSets.
        for imported_url in include.get("valueSet", []):
            try:
                codings.extend(self._expand_to_codings(imported_url, seen))
            except LookupError as exc:
                print(f"    ! could not resolve imported ValueSet: {exc}", file=sys.stderr)

        system = include.get("system")

        if "concept" in include and system:
            # Explicit concept list; fill in missing displays from the CodeSystem.
            cs_map: dict[str, str] | None = None
            for concept in include["concept"]:
                display = _dutch_display(concept, system)
                if not display:
                    if cs_map is None:
                        codesystem = self.resolver.get_codesystem(system)
                        cs_map = _codesystem_display_map(codesystem, system) if codesystem else {}
                    display = cs_map.get(concept.get("code"))
                coding = {"system": system, "code": concept.get("code")}
                if display:
                    coding["display"] = display
                codings.append(coding)
        elif system and "filter" not in include:
            # Whole code system - enumerate it from the resolved CodeSystem.
            codesystem = self.resolver.get_codesystem(system)
            if codesystem is None:
                print(f"    ! cannot enumerate system (CodeSystem not found): {system}",
                      file=sys.stderr)
            else:
                for code, display in _codesystem_display_map(codesystem, system).items():
                    coding = {"system": system, "code": code}
                    if display:
                        coding["display"] = display
                    codings.append(coding)
        elif system and "filter" in include:
            print(f"    ! filter-based include not supported for system: {system}",
                  file=sys.stderr)

        return codings


def _dedupe(codings: list[dict]) -> list[dict]:
    """Remove duplicate (system, code) codings, preserving order."""
    seen: set[tuple] = set()
    result: list[dict] = []
    for coding in codings:
        key = (coding.get("system"), coding.get("code"))
        if key not in seen:
            seen.add(key)
            result.append(coding)
    return result


# --------------------------------------------------------------------------------------
# Questionnaire processing
# --------------------------------------------------------------------------------------


def process_items(items: list[dict], expander: ValueSetExpander, stats: dict) -> None:
    """Recursively expand answerValueSet references on a list of Questionnaire items."""
    for item in items:
        value_set_url = item.get("answerValueSet")
        if value_set_url:
            stats["found"] += 1
            try:
                options = expander.expand(value_set_url)
            except LookupError as exc:
                stats["failed"] += 1
                print(f"  ! {exc} (linkId={item.get('linkId')})", file=sys.stderr)
                options = None
            if options:
                # Merge with any existing answerOption, then drop the reference so LHC
                # uses the inline options instead of trying to resolve the ValueSet.
                existing = item.get("answerOption", [])
                item["answerOption"] = _merge_options(existing, options)
                del item["answerValueSet"]
                stats["expanded"] += 1
                print(f"  + linkId={item.get('linkId')}: {len(options)} options "
                      f"from {value_set_url}")
            elif options is not None:
                print(f"  ! linkId={item.get('linkId')}: 0 options from {value_set_url}",
                      file=sys.stderr)

        if item.get("item"):
            process_items(item["item"], expander, stats)


def _merge_options(existing: list[dict], expanded: list[dict]) -> list[dict]:
    """Append expanded options to any pre-existing ones, de-duplicating by coding."""
    seen: set[tuple] = set()
    merged: list[dict] = []
    for opt in list(existing) + list(expanded):
        coding = opt.get("valueCoding", {})
        key = (coding.get("system"), coding.get("code"))
        if key not in seen:
            seen.add(key)
            merged.append(opt)
    return merged


def process_questionnaire(path: Path, expander: ValueSetExpander) -> bool:
    """Expand one Questionnaire file. Returns True if an expanded copy was written."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"! skipping {path.name}: {exc}", file=sys.stderr)
        return False

    if not isinstance(data, dict) or data.get("resourceType") != "Questionnaire":
        return False

    print(f"\nProcessing {path.name} ...")
    stats = {"found": 0, "expanded": 0, "failed": 0}
    process_items(data.get("item", []), expander, stats)

    if stats["found"] == 0:
        print("  (no answerValueSet references found)")
        return False

    out_path = path.with_name(f"{path.stem}{OUTPUT_SUFFIX}{path.suffix}")
    out_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  -> wrote {out_path.relative_to(ROOT)} "
          f"(found {stats['found']}, expanded {stats['expanded']}, failed {stats['failed']})")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR,
                        help=f"directory to scan for Questionnaires (default: {DEFAULT_INPUT_DIR})")
    args = parser.parse_args()

    input_dir: Path = args.input_dir
    if not input_dir.is_dir():
        print(f"Input directory does not exist: {input_dir}", file=sys.stderr)
        return 1

    print(f"FHIR package cache: {FHIR_PACKAGE_CACHE}")
    resolver = ResourceResolver()
    expander = ValueSetExpander(resolver)

    written = 0
    for path in sorted(input_dir.glob("*.json")):
        # Skip the expanded copies themselves.
        if path.stem.endswith(OUTPUT_SUFFIX):
            continue
        if process_questionnaire(path, expander):
            written += 1

    print(f"\nDone. Expanded copies written: {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
