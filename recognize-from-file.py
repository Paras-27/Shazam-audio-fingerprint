import argparse
from itertools import zip_longest

from termcolor import colored

import libs.fingerprint as fingerprint
from libs.db_sqlite import SqliteDatabase, SQLITE_MAX_VARIABLE_NUMBER
from libs.reader_file import FileReader


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def find_matches(db, samples, Fs=fingerprint.DEFAULT_FS):
    hashes = fingerprint.fingerprint(samples, Fs=Fs)
    return return_matches(db, hashes)


def return_matches(db, hashes):
    mapper = {}
    for audio_hash, offset in hashes:
        mapper[audio_hash.upper()] = offset
    values = mapper.keys()

    for split_values in grouper(values, SQLITE_MAX_VARIABLE_NUMBER):
        # @todo move to db related files
        query = """
      SELECT upper(hash), song_fk, offset
      FROM fingerprints
      WHERE upper(hash) IN (%s)
    """
        query = query % ', '.join('?' * len(split_values))

        x = db.executeAll(query, split_values)
        matches_found = len(x)

        if matches_found > 0:
            msg = '   ** found %d hash matches (step %d/%d)'
            print(colored(msg, 'green') % (
                matches_found,
                len(split_values),
                len(values)
            ))
        else:
            msg = '   ** not matches found (step %d/%d)'
            print(colored(msg, 'red') % (
                len(split_values),
                len(values)
            ))

        for audio_hash, sid, offset in x:
            yield sid, offset - mapper[audio_hash]


def align_matches(db, matches):
    diff_counter = {}
    largest = 0
    largest_count = 0
    song_id = -1

    for tup in matches:
        sid, diff = tup

        if diff not in diff_counter:
            diff_counter[diff] = {}

        if sid not in diff_counter[diff]:
            diff_counter[diff][sid] = 0

        diff_counter[diff][sid] += 1

        if diff_counter[diff][sid] > largest_count:
            largest = diff
            largest_count = diff_counter[diff][sid]
            song_id = sid

    songM = db.get_song_by_id(song_id)

    nseconds = round(float(largest) / fingerprint.DEFAULT_FS *
                     fingerprint.DEFAULT_WINDOW_SIZE *
                     fingerprint.DEFAULT_OVERLAP_RATIO, 5)

    return {
        "SONG_ID": song_id,
        "SONG_NAME": songM[1],
        "CONFIDENCE": largest_count,
        "OFFSET": int(largest),
        "OFFSET_SECS": nseconds
    }


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f", "--file", type=argparse.FileType("r"), required=True)
    args = parser.parse_args()

    song = args.file.name
    args.file.close()

    r = FileReader(song)  # only get filename

    # get data,fs,file_hash,extension,songname,num_channels
    data = r.parse_audio()
    Fs = data["Fs"]

    db = SqliteDatabase()
    matches = []
    for channel in data['channels']:
        # TODO: Remove prints or change them into optional logging.
        matches.extend(find_matches(db, channel, Fs=Fs))

    total_matches_found = len(matches)

    print("")

    if total_matches_found:
        print(colored(f" ** totally found {total_matches_found} hash matches", "green"))

        song = align_matches(db, matches)

        print(
            colored(
                f" => song: {song['SONG_NAME']} (id={song['SONG_ID']})\n"
                f"    offset: {song['OFFSET']} ({song['OFFSET_SECS']} secs)\n"
                f"    confidence: {song['CONFIDENCE']}",
                "green"
            )
        )
    else:
        print(colored(" ** not matches found at all", "red"))


if __name__ == "__main__":
    main()
