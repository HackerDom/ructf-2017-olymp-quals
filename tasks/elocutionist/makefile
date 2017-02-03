.PHONY: all clean cleanAll solve

all: flag.flac

flag.flac: flag.png makepcm2.pl
	./makepcm2.pl flag.png 0 1 | flac -f -8 - -o flag.flac

flag.png: flag.txt makepng.pl
	./makepng.pl

clean:
	-rm flag.png

cleanAll: clean
	-rm flag.flac

solve: solution.png

solution.png: flag.flac solution
	flac -d flag.flac -o - | ./solution > solution.png

solution: solution.cpp
	g++ -O2 solution.cpp -o solution
