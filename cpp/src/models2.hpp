#ifndef MODELS_HPP
#define MODELS_HPP

enum Resource {
	GOLD,
	COAL,
	COPPER,
	URANIUM
};

class Node {
protected:
	double x;
	double y;

public:
	Node(double _x, double _y);
	virtual ~Node();

	double getDistance(const Node&) const;
};

class Worker : public Node {
private:
	Resource pref;

public:
	Worker(double, double, Resource);
	~Worker();

	Resource getPreference() const;
};

class Mine : public Node {
private:
	Resource res;
	int capacity;

public:
	Mine(double, double, Resource, int);
	~Mine();

	Resource getResource() const;
	int getCapacity() const;
};

#endif