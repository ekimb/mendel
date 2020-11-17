from music_code import music_code
from utils import *
import argparse
from Bio import SeqIO

def kFilter(string):
    k = int(string)
    if k < 14 or k % 2 != 0:
        raise argparse.ArgumentTypeError('K-mer length has to be an even number greater than 14.')
    return k

def seqFilter(string):
    validDNA = 'ACGTN'
    seq = string.upper()
    if not all(i in validDNA for i in seq):
        raise argparse.ArgumentTypeError('Sequence has a non-ACGTN character.')
    return seq


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates musical compositions from DNA sequences')
    parser.add_argument('-k', metavar='k', type=kFilter, help='K-mer length (k) for a musical phrase')
    parser.add_argument('-s', metavar= 's', type=seqFilter, help='Sequence input as a string')
    parser.add_argument('-f', metavar='f', help='Sequence input as FASTA/FASTQ')
    parser.add_argument('-o', metavar='o', help='Output file (.wav) prefix')
    args = parser.parse_args()

# initialize
seq = args.s
k = args.k
fasta_sequences = SeqIO.parse(open(args.f),'fasta')
for fasta in fasta_sequences:
    name, seq = str(fasta.id), str(fasta.seq)
    print('Name: %s, sequence length %d, k-mer length %d' % (name, len(seq), k))
    melody, duration = createSeqMelody(seq, k)
    drums = drumBeat(duration)
    melody.time()
    drums.time()
    final = m.add_waves((drums, melody))
    final.bounce(args.o)

