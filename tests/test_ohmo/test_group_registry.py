"""Tests for persistent managed-group records."""

from pathlib import Path

from ohmo.group_registry import load_managed_group_record, save_managed_group_record


def test_managed_group_record_round_trip_and_corruption(tmp_path: Path) -> None:
    workspace = tmp_path / ".ohmo-home"
    params = {"workspace": workspace, "channel": "feishu", "chat_id": "chat-1"}
    path = save_managed_group_record(
        **params, owner_open_id="owner-1", name="Project group",
    )

    loaded = load_managed_group_record(**params)
    assert loaded is not None
    assert loaded["chat_id"] == "chat-1"
    assert loaded["name"] == "Project group"

    path.write_text("{broken JSON", encoding="utf-8")
    assert load_managed_group_record(**params) is None

    path.write_text("[]", encoding="utf-8")
    assert load_managed_group_record(**params) is None
