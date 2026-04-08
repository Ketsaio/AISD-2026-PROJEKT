#include "pybind11/pybind11.h"
#include "models2.hpp"
// #include "algorithms.hpp"

namespace py = pybind11;

PYBIND11_MODULE(models, handle) {
	py::enum_<Resource>(handle, "Surowiec")
		.value("ZLOTO", Resource::GOLD)
		.value("WEGIEL", Resource::COAL)
		.value("MIEDZ", Resource::COPPER)
		.value("URAN", Resource::URANIUM);

	py::class_<Node>(handle, "Punkt")
		.def(py::init<double, double>())
		.def("dystans", &Node::getDistance);

	py::class_<Mine, Node>(handle, "Kopalnia")
		.def(py::init<double, double, Resource, int>());

	py::class_<Worker, Node>(handle, "Krasnoludek")
		.def(py::init<double, double, Resource>());
}