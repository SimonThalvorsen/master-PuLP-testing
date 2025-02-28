import subprocess
import re
import itertools

# Define parameters to test
vertex_balance_values = [1.05, 1.10, 1.15]  # Example values for -v
edge_balance_values = [0.5, 0.7, 0.9]  # Example values for -e

graph_file = "grid.metis"
num_parts = 12

def run_pulp(v, e):
    """Runs PuLP with given -v and -e values and extracts Edge Cut and Max Cut."""
    command = ["./pulp", graph_file, str(num_parts), "-v", str(v), "-e", str(e), "-q",  "-s", str(123)]
    print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    
    # Extract Edge Cut and Max Cut from output
    edge_cut_match = re.search(r"Edge Cut: (\d+)", output)
    max_cut_match = re.search(r"Max Cut: (\d+)", output)
    
    edge_cut = int(edge_cut_match.group(1)) if edge_cut_match else None
    max_cut = int(max_cut_match.group(1)) if max_cut_match else None
    
    return v, e, edge_cut, max_cut

# Run the tests
results = []
for v, e in itertools.product(vertex_balance_values, edge_balance_values):
    v, e, edge_cut, max_cut = run_pulp(v, e)
    results.append((v, e, edge_cut, max_cut))
    print(f"v={v}, e={e} -> Edge Cut: {edge_cut}, Max Cut: {max_cut}")

# Save results to a file
with open("pulp_results_regular.txt", "w") as f:
    f.write("Vertex Balance (v) | Edge Balance (e) | Edge Cut | Max Cut\n")
    f.write("----------------------------------------------------\n")
    for v, e, edge_cut, max_cut in results:
        f.write(f"{v:.2f} | {e:.2f} | {edge_cut} | {max_cut}\n")

print("Results saved to pulp_results.txt")

