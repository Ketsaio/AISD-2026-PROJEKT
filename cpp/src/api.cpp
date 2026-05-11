#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "models2.hpp"
#include "algorithm.hpp"

namespace py = pybind11;

PYBIND11_MODULE(models, handle) {
	py::enum_<Resource>(handle, "Surowiec")
		.value("ZLOTO", Resource::GOLD)
		.value("WEGIEL", Resource::COAL)
		.value("MIEDZ", Resource::COPPER)
		.value("URAN", Resource::URANIUM);

	py::class_<Node>(handle, "Punkt")
		.def(py::init<double, double>())
		.def("dystans", &Node::getDistance)
		.def_readwrite("x", &Node::x)
		.def_readwrite("y", &Node::y);

	py::class_<Mine, Node>(handle, "Kopalnia")
		.def(py::init<double, double, Resource, int>())
		.def("getSurowiec", &Mine::getResource);

	py::class_<Worker, Node>(handle, "Krasnoludek")
		.def(py::init<double, double, Resource>())
		.def("getSurowiec", &Worker::getPreference);

	handle.def("mcmf", &minimumCostMaximumFlow);
}