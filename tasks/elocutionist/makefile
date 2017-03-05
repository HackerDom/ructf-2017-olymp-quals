.PHONY: all clean cleanAll

all: flag.flac

flag.flac: flag.png makepcm2.pl
	./makepcm2.pl flag.png 0 1 | flac -f -8 - -o flag.flac

flag.png: flag.txt makepng.pl
	./makepng.pl

clean:
	-rm flag.png

cleanAll: clean
	-rm flag.flac
