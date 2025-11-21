import random
import globalVar
from .common_mutators import mutate
import copy

class JpgSegment:
    def __init__(self, marker: bytes, data: bytes):
        self.marker = marker
        self.data = data

    def encode(self, size=None):
        if self.marker == b"\xff\xda":
            return self.marker + self.data

        if size == None:
            # TODO: the strucutre is objectively wrong if we have to mod 255
            size = (2 + len(self.data)) % 255
        return self.marker + size.to_bytes(2, 'big') + self.data


def jpg_parse(file_content: bytes) -> list[JpgSegment]:
    segments = []
    i = 2

    # there is no chance the jpeg is spec compliant if its less than 6 bytes
    if (len(file_content) < 6):
        return []
    
    while i < len(file_content) - 2:
        marker = file_content[i:i+2]

        if marker == b'\xff\xda':
            data = file_content[i+2:len(file_content)-2]
            i = len(file_content)-2
        else:
            size = int.from_bytes(file_content[i+2:i+4], 'big')
            data = file_content[i+4:i+2+size]
            i = i+2+size
        
        segments.append(JpgSegment(marker, data))

    return segments

def _mutate_duplicate(segments: list[JpgSegment]) -> list[JpgSegment]:
    to_mutate = random.randint(1, len(segments) // 10 + 1)
    if random.random() < 0.01:
        to_mutate = 20000

    random_location = random.random() < 0.5

    for _ in range(to_mutate):
        index = random.randint(0, len(segments) - 1)
        if random_location:
            segments.insert(random.randint(0, len(segments) - 1), segments[index])
        else:
            segments.insert(index + 1, segments[index])

    return segments

def _mutate_change_marker(segments: list[JpgSegment]) -> list[JpgSegment]:
    to_mutate = random.randint(1, len(segments) // 3 + 1)

    if random.random() < 0.5:
        # comphrehensive list of markers
        marker = random.randint(0xffc0, 0xffff)
    else:
        # more common and interesting markers
        marker = random.choice([0xfffe, 0xffe0, 0xffd8, 0xffc0, 0xffc2, 0xffc4, 0xffdd, 0xffda, 0xffd0])
        
    marker = marker.to_bytes(2, 'big')

    for _ in range(to_mutate):
        random.choice(segments).marker = marker

    return segments

def _mutate_remove_segment(segments: list[JpgSegment]) -> list[JpgSegment]:
    segments.remove(random.choice(segments))
    return segments

def _mutate_segment(segments: list[JpgSegment]) -> list[JpgSegment]:
    segment = random.choice(segments)
    # segment.data = bytes(mutate(bytearray(segment.data)))
    return segments

# TODO: will generate random data half the time, and may draw upon segments 
# from other real example images the other half?
# def _mutate_add_segment(segments: list[JpgSegment]) -> list[JpgSegment]:
#     return segments

# TODO: consider structure inside of segments?

def _mutate_lengths(segments: list[JpgSegment]) -> list[JpgSegment]:
    """Since this is malformed input, our code is in jpg_mutate"""
    return segments

# mostly copy pasted from json_mutator
def jpg_mutate(sample_input: bytes) -> bytes:

    if not globalVar.corpus:
        globalVar.corpus.append(sample_input)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]
    elif random.random() < 0.3: #0.3 chance of adding a fresh copy
        globalVar.corpus.append(sample_input)

    # TODO: we need to refactor corpus stuff, but also the base image should be used at least like 50% of the time tbh imo because its so easy to make mistakes breaking the structure 

    # There's a chance it only has 1 segment
    segments = []
    while len(segments) == 0:
        src = copy.deepcopy(random.choice(globalVar.corpus))
        segments = jpg_parse(src)

    strategies = [
        _mutate_duplicate,
        _mutate_change_marker,
        _mutate_remove_segment,
        # _mutate_add_segment,
        _mutate_lengths,
        _mutate_segment
    ]

    strat_used = random.choice(strategies)
    mutated_segments = strat_used(segments)

    if strat_used == _mutate_lengths:
        def get_number():
            if random.random() < 0.8:
                return random.choice([0, 1, 2, 127, 128, 255])
            else:
                return random.randint(0, 255)

        encoded_segments = [
            segment.encode(get_number() if random.random() < 0.3 else None) 
            for segment in mutated_segments
        ]

        return b"\xff\xd8" + b''.join(encoded_segments) + b"\xff\xd9"


    mutated_segments = [segment.encode() for segment in mutated_segments]
    encoded_jpg = b"\xff\xd8" + b''.join(mutated_segments) + b"\xff\xd9"

    if random.random() < 0.1:
        globalVar.corpus.insert(0, encoded_jpg)
    else:
        globalVar.corpus.append(encoded_jpg)

    return encoded_jpg
