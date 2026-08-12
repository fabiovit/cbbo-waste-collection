import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "cbbo_waste_collection"


def test_manifest_key_order():
    manifest = json.loads(
        (INTEGRATION / "manifest.json").read_text(encoding="utf-8"),
        object_pairs_hook=dict,
    )
    assert list(manifest) == [
        "domain",
        "name",
        "codeowners",
        "config_flow",
        "dependencies",
        "documentation",
        "integration_type",
        "iot_class",
        "issue_tracker",
        "version",
    ]


def test_config_entry_only_schema_declared():
    init = (INTEGRATION / "__init__.py").read_text(encoding="utf-8")
    assert "CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)" in init
    assert "from homeassistant.helpers.typing import ConfigType" in init
