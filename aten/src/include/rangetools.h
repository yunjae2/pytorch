#include <iostream>
#include <string>
#include <vector>

using namespace std;

typedef struct range {
	string name;
	unsigned long addr;
	unsigned long size;
} range;

enum range_type {
	INPUT_RANGE = 0,
	WEIGHT_RANGE,
	BIAS_RANGE,
	NR_RANGE_TYPES,
};

vector<range> ranges;
int nr_ranges;
int nr = -1;

string range_name[NR_RANGE_TYPES] = {
	"input",
	"weight",
	"bias",
};

void new_ranges(void) {
	nr++;
	nr_ranges = 0;
	ranges.clear();
}

void add_range(int rtype, void *addr, unsigned long size) {
	string name = range_name[rtype] + std::to_string(nr);
	ranges.push_back({name, (unsigned long) addr, size});
	nr_ranges++;
}

void print_ranges() {
	for (int i = 0; i < nr_ranges; i++) {
		std::cout << ranges[i].name << ":" << std::endl;
		std::cout << "    addr: " << ranges[i].addr << std::endl;
		std::cout << "    size: " << ranges[i].size << std::endl;
	}
}
