"""Week 10 catalog lane stub — teaching SKU mismatch, separate from triage fixtures."""


def flag_mismatch(title: str, tags: list[str]) -> bool:
    title_l = title.lower()
    tag_blob = " ".join(tags).lower()
    if "nike" in title_l and any(w in tag_blob for w in ("kiondo", "sisal", "bag")):
        return True
    if "photo mismatch" in title_l or "wrong sku" in title_l:
        return True
    return False
