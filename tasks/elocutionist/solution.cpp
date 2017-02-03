#include <cstdio>
#include <vector>
#include <algorithm>

typedef unsigned long long ull;

char headers[44];

bool tryParse(const std::vector<unsigned short>& samples, ull skip, ull length, unsigned zero, unsigned one, std::vector<int>& bits) {
	skip += length;
	if (skip >= samples.size())
		return 1;

	if (samples[skip] == zero) {
		bits.push_back(0);
		if (tryParse(samples, skip, length, zero, one, bits))
			return 1;
		bits.pop_back();
	}

	if (samples[skip] == one) {
		bits.push_back(1);
		if (tryParse(samples, skip, length, zero, one, bits))
			return 1;
		bits.pop_back();
	}

	return false;
}

int main() {
	fread(headers, 44, 1, stdin);

	unsigned short sample;
	std::vector<unsigned short> samples;
	while(fread(&sample, 2, 1, stdin))
		samples.push_back(sample);

	fprintf(stderr, "end read, readed %lu samples\n", samples.size());

	std::vector<int> bits;
	bits.push_back(1);
	for (ull length = 33000; ; ++length) {
			for (ull skip = 0; skip < length; ++skip) {
				unsigned zero  = samples[skip + length];
				unsigned one = samples[skip];
				if (zero && one && zero != one && tryParse(samples, skip, length, zero, one, bits)) {
					fprintf(stderr, "samples: %lu, length: %llu, bits: %lu\n", samples.size(), length, bits.size());
					for (size_t i = 0; i < bits.size(); i += 8) {
						int ch = 0;
						for (int j = 0; j < 8; ++j)
							ch = 2 * ch + bits[i + j];
						printf("%c", ch);
					}
					return 0;
				}
			}
		if (!(length % 1000))
			fprintf(stderr, "try sum %llu, failed\n", length);
	}
}
