#ifndef T10_SAMPLES_H
#define T10_SAMPLES_H
#include "graph.h"
typedef enum { SAMPLE_PATH, SAMPLE_STAR, SAMPLE_DIAMOND } SampleKind;
/* Six vertices each, source zero. Hand-computed expected distances. */
GraphStatus sample_graph(SampleKind kind, Graph **out);
const int *sample_distances(SampleKind kind);
const char *sample_name(SampleKind kind);
#endif
