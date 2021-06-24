#!/usr/bin/perl
use warnings;
use strict;

my $in = $ARGV[0];
my $out = $ARGV[1];
my $prev = "";
my $on_sentence = 0;

open(IN, '<', $in) or die $!;
open(OUT, '>', $out) or die $!;

while(<IN>){
   $on_sentence = ($prev =~ /<s>/ || $on_sentence) && not $_ =~ /<\/s>/;
   if ($on_sentence) {
      $_ =~ s/\n/ /;
	   print OUT $_;
   }
   print OUT "\n" if ($_ =~ /<\/s>/);
   $prev = $_;
}

close(IN);
close(OUT);
