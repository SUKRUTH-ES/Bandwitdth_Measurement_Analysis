#!/usr/bin/env python3
import csv
from pathlib import Path


def main():
    csv_path = Path("results/bandwidth_results.csv")
    if not csv_path.exists():
        raise SystemExit("results/bandwidth_results.csv not found. Run the bandwidth tests first.")

    rows = []
    with csv_path.open() as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            if not row["throughput_mbps"]:
                continue
            rows.append(
                {
                    "topology": row["topology"],
                    "ping_avg_ms": float(row["ping_avg_ms"]) if row["ping_avg_ms"] else None,
                    "throughput_mbps": float(row["throughput_mbps"]),
                }
            )

    if not rows:
        raise SystemExit("No parsed throughput rows found in results/bandwidth_results.csv.")

    rows.sort(key=lambda item: item["throughput_mbps"], reverse=True)
    best = rows[0]
    worst = rows[-1]

    print("Bandwidth Analysis Summary")
    print("==========================")
    for row in rows:
        print(
            f"{row['topology']}: throughput={row['throughput_mbps']:.2f} Mbits/sec, "
            f"avg_ping={row['ping_avg_ms']:.3f} ms"
        )

    print()
    print(f"Best throughput topology : {best['topology']} ({best['throughput_mbps']:.2f} Mbits/sec)")
    print(f"Worst throughput topology: {worst['topology']} ({worst['throughput_mbps']:.2f} Mbits/sec)")
    print(
        "Interpretation: topologies with fewer bottleneck links and lower cumulative delay "
        "should produce higher throughput and lower latency."
    )


if __name__ == "__main__":
    main()
