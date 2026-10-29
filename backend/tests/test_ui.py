"""M4: API support for the web UI (district picker, ambiguity chooser, UI config) and the static UI itself."""
import re
from pathlib import Path

from fastapi.testclient import TestClient

from evideo.api.main import create_app
from evideo.models import QueryRequest
from evideo.parser import parse

FRONTEND = Path(__file__).resolve().parents[2] / "frontend"


def test_picked_region_wins_over_text():
    p = parse(QueryRequest(text="How much was under water on 2024-07-11?", region="barpeta|assam"))
    assert p.region == "barpeta|assam" and p.place_name == "Barpeta, Assam" and not p.problems


def test_unknown_picked_region_falls_back_to_text():
    p = parse(QueryRequest(text="How much of Barpeta was under water on 2024-07-11?", region="nowhere|x"))
    assert p.region == "barpeta|assam"


def test_ambiguous_name_returns_keys_for_chooser():
    p = parse(QueryRequest(text="How much of Aurangabad was under water on 2024-08-10?"))
    assert "ambiguous_area" in p.problems
    assert len(p.candidate_keys) == len(p.candidates) >= 2
    for label, key in zip(p.candidates, p.candidate_keys):
        assert key.split("|")[0] in label.lower()
    # each key resolves to that district when sent back as a pick
    again = parse(QueryRequest(text=p.text, region=p.candidate_keys[0]))
    assert not again.problems and again.place_name == p.candidates[0]


def test_ui_config_and_static_ui():
    c = TestClient(create_app())
    cfg = c.get("/v1/ui-config").json()
    assert 0 < cfg["abstain_below"] < 1 and cfg["bands"] and cfg["examples"]
    assert all("text" in e and "label" in e for e in cfg["examples"])
    html = c.get("/").text
    for landmark in ('id="q"', 'role="combobox"', 'role="progressbar"', 'id="card"', 'id="map"', "vendor/leaflet/leaflet.js"):
        assert landmark in html
    assert c.get("/vendor/leaflet/leaflet.js").status_code == 200


def test_frontend_has_no_em_dashes_and_no_external_scripts():
    for f in FRONTEND.glob("*.*"):
        text = f.read_text(encoding="utf-8")
        assert "\u2014" not in text, f.name
        if f.suffix == ".html":
            assert not re.search(r'<script[^>]+src="https?://', text), "scripts must be vendored for offline installs"


def test_parse_step_returns_the_technical_configuration_without_running():
    c = TestClient(create_app())
    r = c.post("/v1/parse", json={"text": "How much of Barpeta was under water on 2024-07-11?"}).json()
    assert r["parsed"]["problems"] == [] and r["parsed"]["region"] == "barpeta|assam"
    cfg = r["config"]
    assert cfg["instrument"] == "sar_water_otsu" and cfg["instrument_version"] and cfg["n_tiles"] > 100 and not cfg["too_large"]
    assert cfg["publish_threshold"] == 0.6 and "enabled" in cfg["terrain"]
    assert {i["value"] for i in r["intents"]} >= {"water_extent", "water_change", "vegetation_change"}


def test_config_step_can_change_the_analysis_and_reports_missing_pieces():
    c = TestClient(create_app())
    base = {"text": "How much of Barpeta was under water on 2024-07-11?"}
    r = c.post("/v1/parse", json={**base, "intent": "water_change"}).json()
    assert r["parsed"]["intent"] == "water_change" and r["parsed"]["problems"] == ["need_two_dates"]
    amb = c.post("/v1/parse", json={"text": "How much of Aurangabad was under water on 2024-08-10?"}).json()
    assert "ambiguous_area" in amb["parsed"]["problems"] and amb["config"]["n_tiles"] == 0
    oos = c.post("/v1/parse", json={"text": "How many cars are parked in Barpeta on 2024-07-11?"}).json()
    assert oos["parsed"]["problems"] == ["out_of_scope"]


def test_ui_is_the_three_step_wizard_with_a_permanent_map():
    html = TestClient(create_app()).get("/").text
    for landmark in ('id="stage-ask"', 'id="stage-config"', 'id="intent"', 'id="tech"', 'class="clay panel mapbox"', "<title>Tellio</title>"):
        assert landmark in html
    assert html.index('id="stage-config"') < html.index('id="understood"') < html.index('id="card"') < html.index('id="map"')
