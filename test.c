#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Simple node structure
typedef struct Node {
  int value;
  char *data;
  struct Node *next;
} Node;

// Create a new node with a data buffer
Node *createNode(int value, int bufferSize) {
  Node *node = malloc(sizeof(Node));
  if (!node)
    return NULL;

  node->value = value;
  node->data = malloc(bufferSize);
  node->next = NULL;

  // Fill buffer with some data
  if (node->data) {
    memset(node->data, value % 256, bufferSize);
  }

  return node;
}

// Free a linked list
void freeList(Node *head) {
  while (head) {
    Node *temp = head;
    head = head->next;
    free(temp->data);
    free(temp);
  }
}

int main() {
  srand(time(NULL));
  clock_t start = clock();

  // Create a linked list with large data buffers
  Node *head = NULL;
  const int NUM_NODES = 1000;
  const int BUFFER_SIZE = 1024; // 1KB per node

  // Build list
  for (int i = 0; i < NUM_NODES; i++) {
    Node *node = createNode(rand(), BUFFER_SIZE);
    if (node) {
      node->next = head;
      head = node;
    }
  }

  // Perform some operations on the data
  Node *current = head;
  int sum = 0;
  while (current) {
    sum += current->value;
    for (int i = 0; i < BUFFER_SIZE; i++) {
      sum += current->data[i];
    }
    current = current->next;
  }

  // Clean up
  freeList(head);

  // Print results and timing
  clock_t end = clock();
  double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

  printf("Sum: %d\n", sum);
  printf("Time: %f seconds\n", time_spent);

  return 0;
}
