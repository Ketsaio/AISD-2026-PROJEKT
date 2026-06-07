CPP = g++
CPPFLAGS = -O3 -Wall -shared -std=c++11 -fPIC
SOURCES = src/api.cpp src/models2.cpp src/algorithm.cpp

all: models

models:
	$(CPP) $(CPPFLAGS) $$(python3-config --includes) -Isrc $(SOURCES) -o ../py/models$$(python3-config --extension-suffix)

headertree:
	$(CPP) $(CPPFLAGS) -H -E $$(python3-config --includes) -Isrc $(SOURCES) 2>&1 > /dev/null | grep "pybind11"

clean:
	rm ../py/models$$(python3-config --extension-suffix)