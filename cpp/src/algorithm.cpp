#include "algorithm.hpp"

using std::vector;
using std::pair;
using std::min;
using std::size_t;

struct Edge {
	int to;
	int capacity;
	double cost;
	int reverseIdx;
};

class Graph {
private:
	int numNodes;
	vector<vector<Edge>> adjacencyList;

	void processGraph(int sourceIdx, int sinkIdx) {
		while (true) {
			// BELLMAN FORD
			// distance source to each node
			vector<double> dist(numNodes, __INT_MAX__);
			dist[sourceIdx] = 0.0f;

			// path tracking
			vector<int> parentNode(numNodes, -1);
			vector<int> parentEdge(numNodes, -1);

			// relaxing all edges up to n - 1 times
			for (int counter = 0; counter < numNodes - 1; ++counter) {
				// optimization allowing the algorithm to break after a pass without a change
				bool updated = false;

				// for each node
				for (int i = 0; i < numNodes; ++i) {
					// skip if not reached yet
					if (dist[i] == __INT_MAX__) continue;

					// for each edge in node's adj.list
					for (size_t j = 0; j < adjacencyList[i].size(); ++j) {
						// simplification
						Edge& edge = adjacencyList[i][j];

						// distance to cur node + cost to target less than current best distance to target edge
						if (edge.capacity > 0 && dist[i] + edge.cost < dist[edge.to]) {
							// update with smaller distance
							dist[edge.to] = dist[i] + edge.cost;
							// save path
							parentNode[edge.to] = i;
							parentEdge[edge.to] = j;

							updated = true;
						}
					}
				}
				if (!updated) break;
			}

			// sink unreachable meaning its full
			if (dist[sinkIdx] == __INT_MAX__) break;
			// SKIPPED NEGATIVE CHECK ASSUMING DATA IS ALWAYS VALID
			// BELLMAN FORD END

			// FORD KULKERSON
			int pushFlow = __INT_MAX__;
			// start at sink
			int currentIdx = sinkIdx;
			// walk backwards finding the lowest capacity on the way
			while (currentIdx != sourceIdx) {
				int pNode = parentNode[currentIdx];
				int pEdge = parentEdge[currentIdx];

				// find lowest possible cap
				pushFlow = min(pushFlow, adjacencyList[pNode][pEdge].capacity);

				// like linked list
				currentIdx = pNode;
			}

			// restart from sink
			currentIdx = sinkIdx;
			while (currentIdx != sourceIdx) {
				int pNode = parentNode[currentIdx];
				int pEdge = parentEdge[currentIdx];
				// find the reverse edge idx for updating
				int reverseIdx = adjacencyList[pNode][pEdge].reverseIdx;

				// update capacities
				adjacencyList[pNode][pEdge].capacity -= pushFlow;
				adjacencyList[currentIdx][reverseIdx].capacity += pushFlow;

				currentIdx = pNode;
			}
			// FORD KULKERSON END
		}
	}

public:
	Graph(int n) : numNodes(n), adjacencyList(n) {}
	~Graph() = default;

	void addEdge(int from, int to, int cap, double cost) {
		// forward
		adjacencyList[from].push_back(Edge{ to, cap, cost, (int)adjacencyList[to].size() });
		// reverse for algorithms
		adjacencyList[to].push_back(Edge{ from, 0, -cost, (int)adjacencyList[from].size() - 1 });
	}

	vector<pair<int, int>> getAssignments(int dwarves, int mines) {
		processGraph(0, adjacencyList.size() - 1);
		vector<pair<int, int>> out;

		// 0 is source, then dwarves, then mines, then numNodes - 1 is sink
		for (int i = 1; i <= dwarves; ++i) {
			// for each edge in nodes' adj.list
			for (Edge& edge : adjacencyList[i]) {
				// make sure target is mine
				bool isMineNode = (edge.to > dwarves && edge.to <= dwarves + mines);

				// cap == 0 means assigned by algorithm
				if (isMineNode && edge.capacity == 0) {
					// calculate idx in mines array
					int mineIdx = edge.to - dwarves;

					// i - 1 is idx in dwarf array
					out.push_back({ i - 1, mineIdx - 1});
				}
			}
		}

		return out;
	}
};

vector<pair<int, int>> minimumCostMaximumFlow(const std::vector<Worker>& workers, const std::vector<Mine>& mines) {
	int dwarfCounter = workers.size();
	int mineCounter = mines.size();

	constexpr int sourceIdx = 0;
	int sinkIdx = dwarfCounter + mineCounter + 1;

	Graph graph{ dwarfCounter + mineCounter + 2 };

	// add edges from supersource to dwarves
	for (int i = 1; i <= dwarfCounter; ++i) {
		graph.addEdge(sourceIdx, i, 1, 0);
	}

	// add edges from dwarves to mines
	for (int i = 1; i <= dwarfCounter; ++i) {
		for (int j = 1; j <= mineCounter; ++j) {
			double distance = workers[i - 1].getDistance(mines[j - 1]);
			int mineNodeIdx = dwarfCounter + j;
			graph.addEdge(i, mineNodeIdx, 1, distance);
		}
	}

	// add edges from mines to supersink
	for (int i = 1; i <= mineCounter; ++i) {
		int mineNodeIdx = dwarfCounter + i;
		graph.addEdge(mineNodeIdx, sinkIdx, mines[i - 1].getCapacity(), 0);
	}

	return graph.getAssignments(dwarfCounter, mineCounter);
}
