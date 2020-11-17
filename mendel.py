from music_code import music_code
import mmh3
import itertools

# initialize
m = music_code.MusicCode(120)

def buildDisjointKmers(seq, k):
    kmers = []
    print(len(seq))
    
    for i in range(0, len(seq)- len(seq) % k, k):
        kmer = seq[i:i+k]
        print(i)
        kmers.append(kmer)
    return kmers

def hashKmer(kmer):
    h = mmh3.hash64(kmer, 42)[0]
    if h < 0: h += 2**64
    return h

def getHashes(seq, k):
    kmers = buildKmers(seq, k)
    hashes = [hashKmer(kmer) for kmer in kmers]
    return hashes

def createDict():
    scale = ['E2', 'F#2', 'G2', 'A2', 'B2', 'C3', 'D3', 'E3', 'F#3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'rest']
    alphabet = ['A', 'C', 'G', 'T']
    noteDict = {}
    perms = []
    for i in range(4):
        for j in range(4):
            noteDict[alphabet[i] + alphabet[j]] = scale[j+4*i]
    return noteDict
    
def createKmerPhrase(kmer, noteDict):
    chunks = [kmer[i:i+2] for i in range(0, len(kmer), 2)]
    if noteDict[chunks[0]] == 'rest':
        phrase = m.rest(1/8)
    else:
        phrase = m.create_wave([noteDict[chunks[0]]],'sine', 1/8)
    for i in range(1, len(chunks)):
        if noteDict[chunks[i]] == 'rest':
            print("rest")
            phrase = m.join_waves((phrase, m.rest(1/8)))
        else:
            note = m.create_wave([noteDict[chunks[i]]], 'sine', 1/8)
            phrase = m.join_waves((phrase, note))
    return phrase

def createSeqMelody(seq, k):
    noteDict = createDict()
    print(noteDict)
    kmers = buildDisjointKmers(seq, k)
    print(kmers)
    phrases = [createKmerPhrase(kmer, noteDict) for kmer in kmers]
    seqMelody = phrases[0]
    for i in range(1, len(phrases)):
        seqMelody = m.join_waves((seqMelody, phrases[i]))
    return seqMelody

seq = 'ACTTGTCAACGCATTGCACGTTGCAGCGACGCCTACGTTCGACACCCTTA'
k = 16
createSeqMelody(seq, k).bounce()