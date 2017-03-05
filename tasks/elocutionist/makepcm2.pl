#! /usr/bin/perl

use strict;
use warnings;

use WAV;

$/ = undef;
$" = undef;

my $flagFile = shift;

my @samples;
for (@ARGV) {
	open IN, "<samples/$_.pcm" or die "can't open sample file $_: $!\n";
	binmode IN;
	push @samples, [<IN> =~ /.{2}/sg];
	close IN;
}

sub printSamples {
	my $out = shift;
#	print STDERR @_, "\n";
	printSample($out, $_) for @_;
}

my $last = $#{$samples[0]};
sub printSample {
	my ($out, $mask) = @_;
	my @m = split //, $mask;
	for my $i (0 .. $last) {
		for my $j (@m) {
			print $out ${$samples[$j]}[$i];
		}
	}
}

open IN, '<', $flagFile or die "can't open flag file: $!\n";
binmode IN;
my $flag;
binmode STDOUT;

my $size = 2 *(-s $flagFile) * ($last + 1);
print STDOUT createHeader $size;

printSamples(*STDOUT, unpack("B*", $flag) =~ /./sg) while (read IN, $flag, 65536);
