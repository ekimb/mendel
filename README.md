`mendel`: Generating musical compositions from DNA sequences
=========

`mendel` is a Python library that can turn any DNA sequence into a musical composition.

## Background and Capabilities

`mendel` uses arbitrary mappings from k-mers of varying length in a sequence, along with density-based MinHash, to create melodic, and vaguely musical, pieces of music from input sequence data. The idea originated from [Song from π!](https://www.youtube.com/watch?v=OMq9he-5HUU) by David Macdonald which was composed in a similar manner (but for the digits of π). 

`mendel` currently outputs a a three-part piece: A drums section (optional), a rhythm section (chords), and a melody section (monophonic). It is currently very much open for any suggestions for improvement, as the musical pieces it outputs are seemingly random, but because of arbitrary musical choices, it's sort pleasing to the ear. 

## Requirements

[Music-Code](https://github.com/wesleyLaurence/Music-Code), and any requirements within, along with a working Python environment, are required.


## Installation


## Quick start


## Overview

## Input

`mendel` takes a single FASTA/FASTQ input, and requires the user to specify the k-mer length.

## Output data


## Running an example


## License

`mendel` is freely available under the [MIT License](https://opensource.org/licenses/MIT).

## Contributions and contact

I'm actively looking for any suggestions for improvement! Feel free to contact [me](http://people.csail.mit.edu/ekim/) at baris [at] mit [dot] edu, or make a pull request.
