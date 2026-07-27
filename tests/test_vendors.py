from accacia.vendors import recommend_vendors, shortlist_vendors, VENDORS


def test_full_roster_present():
    names = {v.name for v in VENDORS}
    assert {"Adani Solar", "ReNew", "RenewSys", "Waaree"} <= names
    assert len(VENDORS) == 13


def test_ranking_puts_adani_first():
    # Adani: 7 designations + highest per-model avg (6.5) → top
    ranked = shortlist_vendors(require_metrics=True)
    assert ranked[0].name == "Adani Solar"


def test_min_designations_filter_excludes_name_only():
    seven = shortlist_vendors(min_designations=7)
    assert all(v.designations >= 7 for v in seven)
    # Waaree has strong breadth but no stated designation count → excluded
    assert "Waaree" not in {v.name for v in seven}


def test_require_metrics_drops_name_only_vendors():
    quantified = shortlist_vendors(require_metrics=True)
    assert all(v.designations is not None for v in quantified)
    assert "Grew Solar" not in {v.name for v in quantified}


def test_recommend_top_n():
    top3 = recommend_vendors(3)
    assert len(top3) == 3
    assert top3[0].name == "Adani Solar"


def test_none_metrics_sort_last_not_crash():
    # sorting must tolerate the name-only entries without error
    ranked = shortlist_vendors()
    assert len(ranked) == len(VENDORS)
    # a fully name-only vendor should not outrank a quantified one
    assert ranked[0].designations is not None
