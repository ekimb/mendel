
from music_code import music_code
import mmh3
m = music_code.MusicCode(120)

def buildDisjointKmers(seq, k):
    kmers = []
    print(len(seq))
    for i in range(0, len(seq)- len(seq) % k, k):
        kmer = seq[i:i+k]
        print(i)
        kmers.append(kmer)
    return kmers

def GCcontent(lmer):
    GC = 0
    for char in lmer:
        if char == 'G' or char == 'C':
            GC += 1
    return float(GC/len(lmer))


def hashKmer(kmer):
    h = mmh3.hash64(kmer, 42)[0]
    if h < 0: h += 2**64
    return h

def createNoteDict():
    scale = ['E2', 'F#2', 'G2', 'A2', 'B2', 'C3', 'D3', 'E3', 'F#3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'rest']
    alphabet = ['A', 'C', 'G', 'T']
    noteDict = {}
    perms = []
    for i in range(4):
        for j in range(4):
            noteDict[alphabet[i] + alphabet[j]] = scale[j+4*i]
    for i in range(4):
            noteDict[alphabet[i] + 'N'] = 'rest'
            noteDict['N' + alphabet[i]] = 'rest'

    return noteDict

def createDurationList(kmer):
    k = len(kmer)
    durationList = []
    totalDuration = 0
    quarterNotes = 2
    eighthNotes = 4
    l = k  - k//2 + 1
    for i in range(k - l + 1):
        lmer = kmer[i:i+l]
        lmerGC = GCcontent(lmer)
        print(lmerGC)
        if lmerGC < 0.5 and quarterNotes > 0:
            durationList.append(0.25)
            totalDuration += 0.25
            quarterNotes -= 1
        elif lmerGC >= 0.5 and eighthNotes > 0:
            durationList.append(0.125)
            totalDuration += 0.125
            eighthNotes -= 1
        if quarterNotes == 0 and eighthNotes == 0: break
    return durationList, totalDuration

def addNote(noteDict, seqChunk, waveType, duration):
    if noteDict[seqChunk] == 'rest':
        note = m.rest(duration)
    else:
        note = m.create_wave([noteDict[seqChunk]], waveType, duration)
    return note

def createKmerPhrase(kmer, noteDict):
    chunks = [kmer[i:i+2] for i in range(0, len(kmer), 2)]
    durationList, kmerDuration = createDurationList(kmer)
    print(durationList)
    phrase = addNote(noteDict, chunks[0], 'sine', durationList[0])
    for i in range(1, len(durationList)):
        note = addNote(noteDict, chunks[i], 'sine', durationList[i])
        phrase = m.join_waves((phrase, note))
    return phrase, kmerDuration

def createSeqMelody(seq, k):
    noteDict = createNoteDict()
    print(noteDict)
    kmers = buildDisjointKmers(seq, k)
    print(kmers)
    phrases = []
    totalDuration = 0
    for kmer in kmers:
        phrase, kmerDuration = createKmerPhrase(kmer, noteDict)
        phrases.append(phrase)
        totalDuration += kmerDuration
    seqMelody = phrases[0]
    for i in range(1, len(phrases)):
        seqMelody = m.join_waves((seqMelody, phrases[i]))
    return seqMelody, totalDuration

def drumBeat(duration):
    kick = m.sample('kick',0).time_edit(1/4)
    snare = m.sample('snare',0).time_edit(1/4)
    hihat = m.sample('hihat',2).time_edit(1/16)
    kickLoop = m.join_waves((kick, m.rest(1/4))).loop(int(duration*2))
    snareLoop = m.join_waves((m.rest(1/4), snare)).loop(int(duration*2))
    hihatLoop = m.join_waves((hihat)).loop(int(duration*8))

    # verify times are the same, if not go back and adjust code
    kickLoop.time()
    snareLoop.time()
    hihatLoop.time()

    # add kick and snare waves together
    mix = m.add_waves((kickLoop, snareLoop, hihatLoop))
    return mix