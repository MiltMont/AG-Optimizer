#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct Node {
  int value;
  struct Node **neighbors; // Array of pointers to neighbors
  int num_neighbors;
} Node;

typedef struct Graph {
  Node **nodes; // Array of pointers to nodes
  int num_nodes;
} Graph;

// Function to create a node
Node *create_node(int value, int max_neighbors) {
  Node *node = (Node *)malloc(sizeof(Node));
  if (!node) {
    fprintf(stderr, "Error: Memory allocation failed for node.\n");
    exit(EXIT_FAILURE);
  }
  node->value = value;
  node->num_neighbors = rand() % (max_neighbors + 1);
  node->neighbors = (Node **)malloc(node->num_neighbors * sizeof(Node *));
  if (!node->neighbors && node->num_neighbors > 0) {
    fprintf(stderr, "Error: Memory allocation failed for neighbors.\n");
    exit(EXIT_FAILURE);
  }
  return node;
}

// Function to create a graph
Graph *create_graph(int num_nodes, int max_neighbors) {
  Graph *graph = (Graph *)malloc(sizeof(Graph));
  if (!graph) {
    fprintf(stderr, "Error: Memory allocation failed for graph.\n");
    exit(EXIT_FAILURE);
  }
  graph->num_nodes = num_nodes;
  graph->nodes = (Node **)malloc(num_nodes * sizeof(Node *));
  if (!graph->nodes) {
    fprintf(stderr, "Error: Memory allocation failed for graph nodes.\n");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < num_nodes; i++) {
    graph->nodes[i] = create_node(i, max_neighbors);
  }
  return graph;
}

// Function to connect nodes in the graph randomly
void connect_nodes(Graph *graph) {
  for (int i = 0; i < graph->num_nodes; i++) {
    for (int j = 0; j < graph->nodes[i]->num_neighbors; j++) {
      graph->nodes[i]->neighbors[j] = graph->nodes[rand() % graph->num_nodes];
    }
  }
}

// Function to print the graph
void print_graph(Graph *graph) {
  for (int i = 0; i < graph->num_nodes; i++) {
    printf("Node %d: ", graph->nodes[i]->value);
    for (int j = 0; j < graph->nodes[i]->num_neighbors; j++) {
      printf("%d ", graph->nodes[i]->neighbors[j]->value);
    }
    printf("\n");
  }
}

// Function to free a graph
void free_graph(Graph *graph) {
  for (int i = 0; i < graph->num_nodes; i++) {
    free(graph->nodes[i]->neighbors);
    free(graph->nodes[i]);
  }
  free(graph->nodes);
  free(graph);
}

int main() {
  srand(time(NULL));

  int num_nodes = 1000;   // Number of nodes
  int max_neighbors = 20; // Maximum neighbors per node

  printf("Creating a graph with %d nodes...\n", num_nodes);
  Graph *graph = create_graph(num_nodes, max_neighbors);
  connect_nodes(graph);

  printf("Graph created. Printing first 10 nodes:\n");
  for (int i = 0; i < 10; i++) {
    printf("Node %d has %d neighbors.\n", graph->nodes[i]->value,
           graph->nodes[i]->num_neighbors);
  }

  printf("Freeing the graph...\n");
  free_graph(graph);

  printf("Graph freed. Program completed successfully.\n");
  return 0;
}
