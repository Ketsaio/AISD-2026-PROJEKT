#include "models2.hpp"
#include <cmath>

Node::Node(double _x, double _y) : x(_x), y(_y) {}
Node::~Node() = default;

double Node::getDistance(const Node& other) const {
	return sqrt(pow(other.x - this->x, 2) + pow(other.y - this->y, 2));
}

Worker::Worker(double _x, double _y, Resource _pref) : Node(_x, _y), pref(_pref) {}
Worker::~Worker() = default;

Resource Worker::getPreference() const { return this->pref; }

Mine::Mine(double _x, double _y, Resource _res, int _cap) : Node(_x, _y), res(_res), capacity(_cap) {}
Mine::~Mine() = default;

Resource Mine::getResource() const { return this->res; }
int Mine::getCapacity() const { return this->capacity; }