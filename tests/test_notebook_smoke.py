import json
from pathlib import Path


def test_notebooks_are_valid_json():
    notebook_paths = sorted(Path("notebooks").rglob("*.ipynb"))
    assert notebook_paths, "No notebooks found in notebooks/"

    for nb_path in notebook_paths:
        payload = json.loads(nb_path.read_text(encoding="utf-8"))
        assert payload["nbformat"] == 4
        assert payload["cells"], f"{nb_path} has no cells"
