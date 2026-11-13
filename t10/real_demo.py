"""Compare BFS correctness and algorithmic work on synthetic and real graphs."""
import argparse
import math
from pathlib import Path
from time import perf_counter
import tracemalloc

from .bfs import bfs
from .graph import (grid_graph, load_brainlinks, path_graph, star_graph,
                    tree_graph)
from .queues import BASELINE_QUEUES


def measure_bfs(graph, queue_class, start=0):
    """Return BFS output, elapsed seconds, peak traced bytes, and counters."""
    tracemalloc.start()
    started = perf_counter()
    distances, stats = bfs(graph, start, queue_class, with_stats=True)
    elapsed = perf_counter() - started
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    stats = dict(stats)
    stats.update(time_seconds=elapsed, peak_bytes=peak_bytes)
    return distances, stats


def graph_positions(graph, layout, width, height):
    """Return readable SVG coordinates for a known graph layout."""
    count = len(graph)
    positions = {}
    if layout == "path":
        margin = 55
        step = (width - 2 * margin) / max(count - 1, 1)
        positions = {vertex: (margin + vertex * step, height / 2)
                     for vertex in range(count)}
    elif layout == "star":
        center = (width / 2, height / 2)
        radius = min(width, height) * 0.37
        positions[0] = center
        for vertex in range(1, count):
            angle = 2 * math.pi * (vertex - 1) / max(count - 1, 1)
            positions[vertex] = (
                center[0] + radius * math.cos(angle),
                center[1] + radius * math.sin(angle),
            )
    elif layout == "grid":
        columns = 8
        margin_x, margin_y = 90, 75
        step_x = (width - 2 * margin_x) / (columns - 1)
        step_y = (height - 2 * margin_y) / 4
        positions = {
            vertex: (margin_x + (vertex % columns) * step_x,
                     margin_y + (vertex // columns) * step_y)
            for vertex in range(count)
        }
    elif layout == "tree":
        levels = {}
        for vertex in range(count):
            level = (vertex + 1).bit_length() - 1
            levels.setdefault(level, []).append(vertex)
        margin_y = 60
        level_step = (height - 2 * margin_y) / max(len(levels) - 1, 1)
        for level, vertices in levels.items():
            step_x = width / (len(vertices) + 1)
            for index, vertex in enumerate(vertices, 1):
                positions[vertex] = (index * step_x, margin_y + level * level_step)
    else:
        center_x, center_y = width / 2, height / 2
        radius = min(width, height) * 0.39
        for vertex in range(count):
            angle = 2 * math.pi * vertex / count
            positions[vertex] = (
                center_x + radius * math.cos(angle),
                center_y + radius * math.sin(angle),
            )
    return positions


def write_svg(graph, distances, labels, output, title="BFS graph",
              layout="circular"):
    """Write a dependency-free SVG using a layout suited to the graph shape."""
    width, height = 1200, 760
    positions = graph_positions(graph, layout, width, height)
    count = len(graph)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        f"<title>{title}</title>",
        '<rect width="100%" height="100%" fill="white"/>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
        'refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" '
        'fill="#64748b"/></marker></defs>',
    ]
    for source, neighbors in enumerate(graph):
        x1, y1 = positions[source]
        for target in neighbors:
            x2, y2 = positions[target]
            lines.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                'stroke="#94a3b8" stroke-width="1" marker-end="url(#arrow)"/>'
            )
    for vertex, (x, y) in positions.items():
        color = "#2563eb" if distances[vertex] >= 0 else "#cbd5e1"
        lines.extend((
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="16" fill="{color}" '
            'stroke="#1e293b"/>',
            f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" '
            f'font-size="9" fill="white">{labels[vertex]}</text>',
        ))
    lines.append(
        '<text x="20" y="30" font-size="18" font-family="sans-serif">'
        f"{title}: BFS-reachable vertices in blue</text>"
    )
    lines.append("</svg>")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def run_case(name, graph, expected):
    """Compare every queue using existing algorithmic work counters."""
    edge_count = sum(len(neighbors) for neighbors in graph)
    print(f"\n{name} (V={len(graph)}, E={edge_count}, source=0)")
    print(f"{'Queue':30} {'Result':6} {'Visited':>8} {'Peak queue':>10} "
          f"{'Shifted':>10} {'Copied':>10} {'Resizes':>8}")
    for queue_class in BASELINE_QUEUES:
        distances, stats = bfs(graph, 0, queue_class, with_stats=True)
        if distances != expected:
            raise RuntimeError(f"BFS result mismatch for {name} and "
                               f"{queue_class.__name__}")
        reachable = sum(distance >= 0 for distance in distances)
        print(
            f"{queue_class.__name__:30} {'PASS':6} {reachable:8d} "
            f"{stats['peak']:10d} {stats['shifted']:10d} "
            f"{stats['copied']:10d} {stats['resizes']:8d}"
        )


def synthetic_shapes():
    """Return four synthetic workloads, independent of the real edge sample."""
    count = 40
    shapes = (
        ("Synthetic Path", path_graph(count)),
        ("Synthetic Star", star_graph(count)),
        ("Synthetic Binary tree", tree_graph(count)),
        ("Synthetic Grid 5x8", grid_graph(5, 8)),
    )
    return shapes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="brainlinks.dat",
                        help="local two-column brainlinks edge list")
    parser.add_argument("--edges", type=int, default=40,
                        help="number of unique edges to sample")
    parser.add_argument("--output-dir", default="bfs_visualizations",
                        help="directory for one SVG per graph")
    parser.add_argument("--no-svg", action="store_true",
                        help="skip SVG files, recommended for larger edge samples")
    args = parser.parse_args()
    try:
        graph, summary = load_brainlinks(args.dataset, args.edges)
    except (OSError, ValueError) as error:
        parser.error(f"Cannot load dataset {args.dataset}: {error}")

    print("BFS correctness and algorithmic work counters (not timing benchmarks)")
    print("  Peak queue = maximum queued vertices, not a complete BFS layer size.")
    visualizations = []
    for name, real_graph in synthetic_shapes():
        expected = bfs(real_graph, 0, BASELINE_QUEUES[0])
        run_case(name, real_graph, expected)
        output = Path(args.output_dir) / f"{name.lower().replace(' ', '_')}.svg"
        layout = ("path" if "Path" in name else
                  "star" if "Star" in name else
                  "tree" if "tree" in name else "grid")
        if not args.no_svg:
            write_svg(real_graph, expected, list(range(len(real_graph))),
                      output, name, layout)
            visualizations.append(output)

    print("\nBrainlinks sample metadata: "
          "{rows} rows read, {edges} unique edges, {vertices} vertices".format(**summary))
    expected = bfs(graph, 0, BASELINE_QUEUES[0])
    run_case("Real Brainlinks directed edge sample", graph, expected)
    output = Path(args.output_dir) / "brainlinks_sample.svg"
    if not args.no_svg:
        write_svg(graph, expected, summary["labels"], output,
                  "Real Brainlinks directed edge sample", "circular")
        visualizations.append(output)
    if visualizations:
        print("  graph visualizations:")
    for visualization in visualizations:
        print(f"    {visualization.resolve()}")


if __name__ == "__main__":
    main()
