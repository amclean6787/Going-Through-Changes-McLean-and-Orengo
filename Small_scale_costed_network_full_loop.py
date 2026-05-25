import grass.script as gs
import csv as csvlib

# Setup
points_vector = "EDG_urban"

scenarios = [
    {
        "label":            "ALAG",
        "corridor_raster":  "MINNORM_CORRIDORS_ALLFAC_AUG",
        "cost_raster":      "EMP_ALLFAC_AUG_93m_SEA45",
    },
    {
        "label":            "ALFB",
        "corridor_raster":  "MINNORM_CORRIDORS_ALLFAC_FEB",
        "cost_raster":      "EMP_ALLFAC_FEB_93m_SEA45",
    },
    {
        "label":            "NOFB",
        "corridor_raster":  "MINNORM_CORRIDORS_NOFAC",
        "cost_raster":      "EMP_NOFAC_93m_SEA45",
    },
    {
        "label":            "CDAG",
        "corridor_raster":  "MINNORM_CORRIDORS_NOCOLD_AUG",
        "cost_raster":      "EMP_NOCOLD_AUG_93m_SEA45",
    },
    {
        "label":            "CDFB",
        "corridor_raster":  "MINNORM_CORRIDORS_NOCOLD_FEB",
        "cost_raster":      "EMP_NOCOLD_FEB_93m_SEA45",
    },
    {
        "label":            "SDAG",
        "corridor_raster":  "MINNORM_CORRIDORS_NOSAND_AUG",
        "cost_raster":      "EMP_NOSAND_AUG_93m_SEA45",
    },
    {
        "label":            "SDFB",
        "corridor_raster":  "MINNORM_CORRIDORS_NOSAND_FEB",
        "cost_raster":      "EMP_NOSAND_FEB_93m_SEA45",
    },
    {
        "label":            "HIAG",
        "corridor_raster":  "MINNORM_CORRIDORS_NOHEIGHT_AUG",
        "cost_raster":      "EMP_NOHEIGHT_AUG_93m_SEA45",
    },
    {
        "label":            "HIFB",
        "corridor_raster":  "MINNORM_CORRIDORS_NOHEIGHT_FEB",
        "cost_raster":      "EMP_NOHEIGHT_FEB_93m_SEA45",
    },
    {
        "label":            "SNAG",
        "corridor_raster":  "MINNORM_CORRIDORS_NOSNOW_AUG",
        "cost_raster":      "EMP_NOSNOW_AUG_93m_SEA45",
    },
    {
        "label":            "SNFB",
        "corridor_raster":  "MINNORM_CORRIDORS_NOSNOW_FEB",
        "cost_raster":      "EMP_NOSNOW_FEB_93m_SEA45",
    },
]

# Define Point Function
def db_select(map, columns, where=None):
    kwargs = dict(map=map, columns=columns, flags="c")
    if where:
        kwargs["where"] = where
    raw = gs.read_command("v.db.select", **kwargs).strip()
    rows = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) < 2:
            continue
        rows[parts[0]] = parts[1:]
    return rows

# Import Points
raw = db_select(points_vector, "cat,Ancient_To")
point_ids   = list(raw.keys())
name_by_cat = {cat: vals[0] for cat, vals in raw.items()}

# Main Loop
for scenario in scenarios:
    label           = scenario["label"]
    corridor_raster = scenario["corridor_raster"]
    cost_raster     = scenario["cost_raster"]

    gs.message(f"\n{'='*60}")
    gs.message(f"SCENARIO: {label}")
    gs.message(f"{'='*60}")

    # Intermediate raster names
    binary_raster   = f"binary_network_{label}"
    neighbor_raster = f"neighbor_network_{label}"
    thinned_raster  = f"thinned_network_{label}"
    cost_surface    = f"cumulative_cost_surface_{label}"
    drain_raster    = f"drainage_paths_{label}"
    drain_binary    = f"drain_binary_{label}"
    merged_raster   = f"merged_network_{label}"
    costed_network  = f"costed_network_{label}"

    # Step 1: Create Minimal Costed Network

    gs.message(f"[{label}] Step 1: Binary raster...")
    gs.mapcalc(
        f"{binary_raster} = if({corridor_raster} >= 1 && {corridor_raster} <= 2, 1, null())",
        overwrite=True
    )
    gs.message(f"[{label}] Step 1: Done.")

    gs.message(f"[{label}] Step 2: Neighbourhood minimum...")
    gs.run_command(
        "r.neighbors",
        input=binary_raster,
        output=neighbor_raster,
        method="minimum",
        size=9,
        flags="c",
        overwrite=True,
        quiet=True
    )
    gs.message(f"[{label}] Step 2: Done.")

    gs.message(f"[{label}] Step 3: Thinning (this may take a while)...")
    gs.run_command(
        "r.thin",
        input=neighbor_raster,
        output=thinned_raster,
        iterations=100,
        overwrite=True,
        quiet=True
    )
    gs.message(f"[{label}] Step 3: Thinning complete.")

    gs.message(f"[{label}] Step 4.1: Cumulative cost surface from network...")
    gs.run_command(
        "r.cost",
        input=cost_raster,
        output=cost_surface,
        start_raster=thinned_raster,
        flags="k",
        overwrite=True,
        quiet=True
    )
    gs.message(f"[{label}] Step 4.1: Done.")

    gs.message(f"[{label}] Step 4.2: Drainage paths from points...")
    gs.run_command(
        "r.drain",
        input=cost_surface,
        output=drain_raster,
        start_points=points_vector,
        flags="d",
        overwrite=True,
        quiet=True
    )
    gs.message(f"[{label}] Step 4.2: Done.")

    gs.message(f"[{label}] Step 4.3: Merging network and drain paths...")
    gs.mapcalc(
        f"{drain_binary} = if(!isnull({drain_raster}), 1, null())",
        overwrite=True
    )
    gs.run_command(
        "r.patch",
        input=f"{thinned_raster},{drain_binary}",
        output=merged_raster,
        overwrite=True,
        quiet=True
    )
    gs.run_command("g.remove", type="raster", name=drain_binary, flags="f", quiet=True)
    gs.message(f"[{label}] Step 4.3: Done.")

    gs.message(f"[{label}] Step 5: Assigning costs...")
    gs.mapcalc(
        f"{costed_network} = if(!isnull({merged_raster}), {cost_raster}, null())",
        overwrite=True
    )
    gs.message(f"[{label}] Step 5: Done.")

    # Cleanup step 1 intermediates
    for r in [binary_raster, neighbor_raster, thinned_raster,
              cost_surface, drain_raster, merged_raster]:
        gs.run_command("g.remove", type="raster", name=r, flags="f", quiet=True)

    # Step 2: run r.cost across network for each point

    gs.message(f"[{label}] Script 2: r.cost from each point...")
    cumulative_rasters = []

    for i, pid in enumerate(point_ids, 1):
        single_point  = f"point_{pid}_{label}"
        output_raster = f"cumulative_cost_{label}_{pid}"
        cumulative_rasters.append(output_raster)

        gs.message(f"[{label}] Script 2: Point {i}/{len(point_ids)} (cat={pid})...")
        gs.run_command(
            "v.extract",
            input=points_vector,
            output=single_point,
            where=f"cat={pid}",
            overwrite=True,
            quiet=True
        )
        gs.run_command(
            "r.cost",
            input=costed_network,
            start_points=single_point,
            output=output_raster,
            overwrite=True,
            quiet=True
        )
        gs.run_command(
            "g.remove",
            type="vector",
            name=single_point,
            flags="f",
            quiet=True
        )

    gs.message(f"[{label}] Script 2: All points done.")

    # Step 3: Build and export cost matrix

    gs.message(f"[{label}] Script 3: Building cost matrix...")

    try:
        gs.run_command("v.db.dropcolumn", map=points_vector, columns="tmp_cost", quiet=True)
    except:
        pass

    gs.run_command(
        "v.db.addcolumn",
        map=points_vector,
        columns="tmp_cost DOUBLE PRECISION"
    )

    rows = []

    for i, from_id in enumerate(point_ids, 1):
        gs.message(f"[{label}] Script 3: Sampling from point {i}/{len(point_ids)}...")
        cost_raster_tmp = f"cumulative_cost_{label}_{from_id}"

        gs.run_command(
            "v.what.rast",
            map=points_vector,
            raster=cost_raster_tmp,
            column="tmp_cost",
            quiet=True
        )

        values = db_select(points_vector, "cat,tmp_cost")

        for to_id, val in values.items():
            if point_ids.index(to_id) <= point_ids.index(from_id):
                continue
            cost = val[0].strip()
            if not cost or cost.lower() in ("null", "none", ""):
                continue
            rows.append({
                "from_id": name_by_cat[from_id],
                "to_id":   name_by_cat[to_id],
                "cost":    cost
            })

    gs.run_command("v.db.dropcolumn", map=points_vector, columns="tmp_cost", quiet=True)

    csv_path = f"{label}_network_cost_matrix.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csvlib.DictWriter(f, fieldnames=["from_id", "to_id", "cost"])
        writer.writeheader()
        writer.writerows(rows)
    gs.message(f"[{label}] Written: {csv_path}")

    # Cleanup cumulative cost rasters
    for r in cumulative_rasters:
        gs.run_command("g.remove", type="raster", name=r, flags="f", quiet=True)

gs.message("\nAll scenarios complete.")