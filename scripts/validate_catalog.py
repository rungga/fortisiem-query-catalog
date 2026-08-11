#!/usr/bin/env python3
"""Validate catalog structure and detect common publication hazards."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
QUERY_ROOT = ROOT / "queries"
ID_PATTERN = re.compile(r"^FSQ-[A-Z]+-[0-9]{3}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDER_PATTERN = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
DATE_LITERAL_PATTERN = re.compile(r"'20[0-9]{2}-[0-9]{2}-[0-9]{2}[ T][^']*'")
IPV4_LITERAL_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_{])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![A-Za-z0-9_}])"
)
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
UUID_PATTERN = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
    re.I,
)
MUTATING_SQL_PATTERN = re.compile(
    r"(?:\A|;)\s*(?:ALTER|ATTACH|CREATE|DELETE|DETACH|DROP|GRANT|INSERT|KILL|"
    r"OPTIMIZE|RENAME|REPLACE|REVOKE|SYSTEM|TRUNCATE|UPDATE)\b",
    re.I,
)
SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"\b(?:api[_-]?key|password|secret|token)\b\s*(?:=|:)",
    re.I,
)
REQUIRED_METADATA_KEYS = {
    "$schema",
    "id",
    "slug",
    "title",
    "origin",
    "platform",
    "query_type",
    "dialect",
    "category",
    "scope",
    "summary",
    "parameters",
    "privacy",
    "compatibility",
    "references",
    "license",
}
REQUIRED_DOCUMENTATION_SECTIONS = (
    "## Tujuan",
    "## Parameter",
    "## Alur Perhitungan",
    "## Kolom Hasil",
    "## Asumsi dan Keterbatasan",
    "## Validasi yang Disarankan",
    "## Referensi Resmi",
)
FORBIDDEN_QUERY_ARTIFACT_SUFFIXES = {
    ".csv",
    ".gif",
    ".jpeg",
    ".jpg",
    ".log",
    ".pcap",
    ".pdf",
    ".png",
    ".xlsx",
}
FORBIDDEN_REPOSITORY_SUFFIXES = FORBIDDEN_QUERY_ARTIFACT_SUFFIXES | {
    ".key",
    ".p12",
    ".pfx",
    ".pem",
    ".sql",
    ".zip",
}
TEXT_SUFFIXES = {
    "",
    ".json",
    ".md",
    ".py",
    ".tmpl",
    ".yaml",
    ".yml",
}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_metadata(path: Path, errors: list[str]) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"{relative(path)}: invalid JSON: {error}")
        return None

    if not isinstance(value, dict):
        errors.append(f"{relative(path)}: top-level JSON value must be an object")
        return None
    return value


def validate_metadata_shape(
    path: Path,
    metadata: dict[str, object],
    errors: list[str],
) -> None:
    missing = REQUIRED_METADATA_KEYS - metadata.keys()
    extra = metadata.keys() - REQUIRED_METADATA_KEYS
    if missing:
        errors.append(f"{relative(path)}: missing keys: {sorted(missing)}")
    if extra:
        errors.append(f"{relative(path)}: unknown keys: {sorted(extra)}")

    query_id = metadata.get("id")
    slug = metadata.get("slug")
    if not isinstance(query_id, str) or not ID_PATTERN.fullmatch(query_id):
        errors.append(f"{relative(path)}: invalid query id")
    if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
        errors.append(f"{relative(path)}: invalid slug")
    if metadata.get("$schema") != "../../../schema/query.schema.json":
        errors.append(f"{relative(path)}: unexpected schema path")
    if metadata.get("platform") != "FortiSIEM":
        errors.append(f"{relative(path)}: platform must be FortiSIEM")
    if metadata.get("dialect") != "ClickHouse SQL":
        errors.append(f"{relative(path)}: dialect must be ClickHouse SQL")
    if metadata.get("license") != "MIT":
        errors.append(f"{relative(path)}: license must be MIT")

    title = metadata.get("title")
    if not isinstance(title, dict):
        errors.append(f"{relative(path)}: title must be an object")
    else:
        if title.get("source") not in {"maintainer", "ai-assisted"}:
            errors.append(f"{relative(path)}: invalid title source")
        if title.get("reviewed_by_maintainer") is not True:
            errors.append(f"{relative(path)}: title requires maintainer review")
        for language in ("en", "id"):
            if not isinstance(title.get(language), str) or not title[language].strip():
                errors.append(f"{relative(path)}: title.{language} is required")

    origin = metadata.get("origin")
    if not isinstance(origin, dict):
        errors.append(f"{relative(path)}: origin must be an object")
    elif origin.get("third_party_code_included") is not False:
        errors.append(f"{relative(path)}: third-party code cannot be included")

    privacy = metadata.get("privacy")
    if not isinstance(privacy, dict) or privacy.get("status") != "sanitized":
        errors.append(f"{relative(path)}: privacy status must be sanitized")
    elif not privacy.get("removed_categories"):
        errors.append(f"{relative(path)}: removed privacy categories are required")

    compatibility = metadata.get("compatibility")
    if not isinstance(compatibility, dict):
        errors.append(f"{relative(path)}: compatibility must be an object")
    elif not isinstance(compatibility.get("tested_versions"), list):
        errors.append(f"{relative(path)}: tested_versions must be an array")

    references = metadata.get("references")
    if not isinstance(references, list) or not references:
        errors.append(f"{relative(path)}: at least one official reference is required")
    else:
        official_reference_found = False
        for index, reference in enumerate(references):
            if not isinstance(reference, dict):
                errors.append(f"{relative(path)}: reference {index} must be an object")
                continue
            url = reference.get("url")
            if not isinstance(url, str) or urlparse(url).scheme != "https":
                errors.append(f"{relative(path)}: reference {index} must use HTTPS")
                continue
            if urlparse(url).hostname == "docs.fortinet.com":
                official_reference_found = True
        if not official_reference_found:
            errors.append(f"{relative(path)}: a docs.fortinet.com reference is required")


def parameter_names(
    path: Path,
    metadata: dict[str, object],
    errors: list[str],
) -> set[str]:
    parameters = metadata.get("parameters")
    if not isinstance(parameters, list):
        errors.append(f"{relative(path)}: parameters must be an array")
        return set()

    names: list[str] = []
    for index, parameter in enumerate(parameters):
        if not isinstance(parameter, dict):
            errors.append(f"{relative(path)}: parameter {index} must be an object")
            continue
        name = parameter.get("name")
        if not isinstance(name, str) or not PLACEHOLDER_PATTERN.fullmatch(
            "{{" + name + "}}"
        ):
            errors.append(f"{relative(path)}: parameter {index} has an invalid name")
            continue
        names.append(name)

    if len(names) != len(set(names)):
        errors.append(f"{relative(path)}: parameter names must be unique")
    return set(names)


def validate_sql(path: Path, declared: set[str], errors: list[str]) -> None:
    try:
        sql = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        errors.append(f"{relative(path)}: cannot read SQL template: {error}")
        return

    placeholders = set(PLACEHOLDER_PATTERN.findall(sql))
    if placeholders != declared:
        errors.append(
            f"{relative(path)}: SQL placeholders {sorted(placeholders)} do not match "
            f"metadata parameters {sorted(declared)}"
        )
    if MUTATING_SQL_PATTERN.search(sql):
        errors.append(f"{relative(path)}: mutating or administrative SQL is forbidden")
    if not re.search(r"\bSELECT\b", sql, re.I):
        errors.append(f"{relative(path)}: SELECT statement not found")
    if not re.search(r"\bLIMIT\s+[0-9]+\b", sql, re.I):
        errors.append(f"{relative(path)}: a literal LIMIT is required")
    if "fsiem.events" in sql and "phRecvTime" not in sql:
        errors.append(f"{relative(path)}: event queries require a phRecvTime bound")

    sensitive_patterns = (
        (DATE_LITERAL_PATTERN, "literal operational date/time"),
        (IPV4_LITERAL_PATTERN, "literal IPv4 address"),
        (EMAIL_PATTERN, "email address"),
        (UUID_PATTERN, "UUID"),
        (SECRET_ASSIGNMENT_PATTERN, "possible secret assignment"),
        (
            re.compile(r"\bcustomer\s*=\s*'[^']+'", re.I),
            "literal customer name",
        ),
        (
            re.compile(r"\bcollectorId\s*=\s*[0-9]+", re.I),
            "literal collector ID",
        ),
        (
            re.compile(r"\breptDevName\s*=\s*'[^']+'", re.I),
            "literal collector or reporting device name",
        ),
    )
    for pattern, description in sensitive_patterns:
        if pattern.search(sql):
            errors.append(f"{relative(path)}: found {description}")


def validate_documentation(path: Path, errors: list[str]) -> None:
    try:
        documentation = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        errors.append(f"{relative(path)}: cannot read documentation: {error}")
        return

    for section in REQUIRED_DOCUMENTATION_SECTIONS:
        if section not in documentation:
            errors.append(f"{relative(path)}: missing section {section!r}")
    for pattern, description in (
        (IPV4_LITERAL_PATTERN, "literal IPv4 address"),
        (EMAIL_PATTERN, "email address"),
        (UUID_PATTERN, "UUID"),
        (SECRET_ASSIGNMENT_PATTERN, "possible secret assignment"),
    ):
        if pattern.search(documentation):
            errors.append(f"{relative(path)}: found {description}")


def validate_repository_hygiene(errors: list[str]) -> None:
    content_patterns = (
        (IPV4_LITERAL_PATTERN, "literal IPv4 address"),
        (EMAIL_PATTERN, "email address"),
        (UUID_PATTERN, "UUID"),
        (SECRET_ASSIGNMENT_PATTERN, "possible secret assignment"),
    )

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() in FORBIDDEN_REPOSITORY_SUFFIXES:
            errors.append(f"{relative(path)}: forbidden raw, secret, or rendered artifact")
            continue
        if path.name == ".env" or path.name.startswith(".env."):
            errors.append(f"{relative(path)}: environment file must not be committed")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"{relative(path)}: cannot inspect text content: {error}")
            continue
        for pattern, description in content_patterns:
            if pattern.search(content):
                errors.append(f"{relative(path)}: found {description}")


def main() -> int:
    errors: list[str] = []
    validate_repository_hygiene(errors)
    metadata_paths = sorted(QUERY_ROOT.glob("**/metadata.json"))
    if not metadata_paths:
        errors.append("queries: no metadata.json files found")

    known_ids: set[str] = set()
    known_slugs: set[str] = set()
    for metadata_path in metadata_paths:
        query_directory = metadata_path.parent
        sql_path = query_directory / "query.sql.tmpl"
        documentation_path = query_directory / "README.md"

        for required_path in (sql_path, documentation_path):
            if not required_path.is_file():
                errors.append(f"{relative(query_directory)}: missing {required_path.name}")

        for artifact in query_directory.iterdir():
            if artifact.suffix.lower() in FORBIDDEN_QUERY_ARTIFACT_SUFFIXES:
                errors.append(f"{relative(artifact)}: raw data or binary artifact forbidden")
            if artifact.suffix.lower() == ".sql":
                errors.append(f"{relative(artifact)}: rendered SQL must not be committed")

        metadata = load_metadata(metadata_path, errors)
        if metadata is None:
            continue
        validate_metadata_shape(metadata_path, metadata, errors)

        query_id = metadata.get("id")
        slug = metadata.get("slug")
        if isinstance(query_id, str):
            if query_id in known_ids:
                errors.append(f"{relative(metadata_path)}: duplicate query id {query_id}")
            known_ids.add(query_id)
            if not query_directory.name.startswith(query_id + "-"):
                errors.append(f"{relative(query_directory)}: directory must start with id")
        if isinstance(slug, str):
            if slug in known_slugs:
                errors.append(f"{relative(metadata_path)}: duplicate slug {slug}")
            known_slugs.add(slug)

        declared = parameter_names(metadata_path, metadata, errors)
        if sql_path.is_file():
            validate_sql(sql_path, declared, errors)
        if documentation_path.is_file():
            validate_documentation(documentation_path, errors)

    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Catalog validation passed for {len(metadata_paths)} query entry.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())