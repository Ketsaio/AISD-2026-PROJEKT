cmake_minimum_required(VERSION 3.4...3.18)
project(models)

add_subdirectory(pybind11)
pybind11_add_module(models 
	src/api.cpp
	src/models2.cpp
	# src/algorithms.cpp
)

set_target_properties(models
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "../py"
    LIBRARY_OUTPUT_DIRECTORY "../py"
    RUNTIME_OUTPUT_DIRECTORY "../py"
)