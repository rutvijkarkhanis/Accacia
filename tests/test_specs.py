from accacia.specs import SiteConditions, recommend_spec


def test_default_rule_when_no_priority():
    rec = recommend_spec(SiteConditions())
    assert rec.rule == "default"
    assert "TOPCon" in rec.technology


def test_space_constrained_wins_over_climate():
    # space-constrained is highest priority even in a hot climate
    rec = recommend_spec(SiteConditions(space_constrained=True, climate="hot"))
    assert rec.rule == "space-constrained"
    assert "HJT" in rec.technology or "IBC" in rec.technology


def test_aesthetic_returns_back_contact():
    rec = recommend_spec(SiteConditions(aesthetic_sensitive=True))
    assert rec.rule == "aesthetic"
    assert "IBC" in rec.technology or "BC" in rec.technology


def test_reflective_mount_bifacial():
    rec = recommend_spec(SiteConditions(reflective_ground_mount=True))
    assert rec.rule == "reflective-mount"
    assert "Bifacial" in rec.technology


def test_hot_climate_hjt():
    rec = recommend_spec(SiteConditions(climate="hot"))
    assert rec.rule == "hot-climate"
    assert "HJT" in rec.technology


def test_cool_climate_prefers_topcon():
    rec = recommend_spec(SiteConditions(climate="cool"))
    assert rec.rule == "cool-climate"
    assert rec.technology == "TOPCon"


def test_payback_focused_topcon_with_upgrade():
    rec = recommend_spec(SiteConditions(payback_focused=True))
    assert rec.rule == "payback-focused"
    assert rec.upgrade_offer is not None


def test_priority_ordering_long_hold_below_hot():
    # a hot-climate long-hold asset should match hot-climate first
    rec = recommend_spec(SiteConditions(climate="hot", long_hold=True))
    assert rec.rule == "hot-climate"
