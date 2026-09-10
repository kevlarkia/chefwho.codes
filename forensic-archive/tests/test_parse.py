from forensic_archive.parse import parse_exclusions, parse_items


def test_parse_exclusions_from_trailing_json_fence() -> None:
    response = """
    Validation complete.

    ```json
    {
      "exclusions": [
        {"id": "EXT-002", "reason": "placeholder", "rule": "placeholder"}
      ]
    }
    ```
    """
    exclusions = parse_exclusions(response)
    assert exclusions == [
        {"id": "EXT-002", "reason": "placeholder", "rule": "placeholder"}
    ]


def test_parse_exclusions_accepts_bare_array() -> None:
    response = 'Kept EXT-001.\n[{"id": "EXT-003", "reason": "too thin"}]'
    exclusions = parse_exclusions(response)
    assert exclusions[0]["id"] == "EXT-003"
    assert exclusions[0]["rule"] == "unspecified"


def test_parse_items_from_primary_tail() -> None:
    response = """
    PRIMARY

    ```json
    {"items": [{"id": "EXT-001", "text": "A fact", "evidence": "VERBATIM"}]}
    ```
    """
    items = parse_items(response)
    assert items[0]["id"] == "EXT-001"
    assert items[0]["text"] == "A fact"
