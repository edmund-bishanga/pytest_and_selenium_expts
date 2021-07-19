#!/usr/bin/python

"""
Takes ingredients from a Bible Study
And summarises them
For a Faithful Spiritual meal
DAILY BREAD: To be shared with Online Neighbours

Ingredients: Inputs
+ Scripture

Process:
THE TEACHER IS A MOUTHPIECE, FOR GOD'S HOLY & LIVING WORD:
THE TEACHER HAS NOTHING TO SAY: JUST A FAITHFUL MOUTHPIECE
A MESSENGER/POSTMAN DELIVERING CHRIST'S MESSAGE
+ Read the Text
+ Seek the Author's Intent:
  * FATHER: Author
  * SON: Embodiment/Gist
  * SPIRIT: Interpreter
+ Share the Meal: with a Specific Audience
  * #UKCHRISTIANScholarAthletes
  * #Fitter_AfroBritishCHRISTIANFamilies
  * #UKCHRISTIANInformationTechnologists

Outputs:
+ Faithful Scriptural PostCard
  * The Passage: fresh, undiluted: bible.com link.
  * The Sermon: faithful, to best of the Teacher's knowledge
    + Diagram: GeoHistLitCulturalContext, VerseByVerse,
      TimelessPrinciples, PracticesForTODAYHereNow, MemoryVerse
    + YAHWEH'S Key Principles: Major, minor
  * The MemoryVerse: Cornerstone of the Passage, faithfully identified... always learning...
  * A helpful/faithful Song/Hymn: for Dessert...

"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=unused-import
# pylint: disable=missing-function-docstring

import argparse
import re
import sys
from pprint import pprint

BIBLE_ROOT_URL = 'https://www.bible.com'
LANGUAGE = 'en-GB'

BIBLE_VERSIONS = {
    'NKJV': '114',
}

BIBLE_BOOKS = {
    'Matthew': 'mat',
    'Mark': 'mrk',
    'Luke': 'luk',
    'John': 'jhn',
    'Acts': 'act',
    'Romans': 'rom',
    '1Corinthians': '1co',
    '2Corinthians': '2co',
    'Galatians': 'gal',
    'Ephesians': 'eph',
    'Philippians': 'php',
    'Colossians': 'col',
    '1Thessalonians': '1th',
    '2Thessalonians': '2th',
    '1Timothy': '1ti',
    '2Timothy': '2ti',
    'Titus': 'tit',
    'Philemon': 'phm',
    'Hebrews': 'heb',
    'James': 'jas',
    '1Peter': '1pe',
    '2Peter': '2pe',
    '1John': '1jn',
    '2John': '2jn',
    '3John': '3jn',
    'Jude': 'jud',
    'Revelation': 'rev',
}

def validate_inputs(inputs):
    input_format_err_msg = "invalid format: details, see --help/-h"
    if inputs.bible_passage:
        err_msg_bp = "{}: {}".format('-B|--bible-passage', input_format_err_msg)
        assert '.' in inputs.bible_passage, err_msg_bp

def get_passage_lnk(bible_passage_str):
    p_regex = r'(\w+).(\d+)v(\d+)' if 'v' in bible_passage_str else r'(\w+).(\d+)'
    has_end_verse = False
    for char in ['-', '_']:
        if char in bible_passage_str:
            p_regex = r'(\w+).(\d+)v(\d+)[-|_](\d+)'
            has_end_verse = True
    matched = re.match(p_regex, bible_passage_str)
    assert matched, 'invalid bible passage: {}\nDetails: -h|--help'.format(bible_passage_str)

    book = BIBLE_BOOKS.get(matched.group(1))
    if not book:
        resolver = 'should be one of these: {}'.format(BIBLE_BOOKS.keys())
        assert book, 'invalid Bible Book format: {}\n{}'.format(bible_passage_str, resolver)

    chapter = matched.group(2)
    start_verse = matched.group(3) if 'v' in bible_passage_str else ''
    end_verse = matched.group(4) if has_end_verse else ''
    verses = start_verse
    verses = verses + '-' + end_verse if has_end_verse else verses
    passage_lnk = '.'.join([book, chapter, verses]).strip('.')
    return passage_lnk

def main():
    """ Interactive function: Takes bible passage, provides summary. """
    args = argparse.ArgumentParser()
    args.add_argument(
        '-B', "--bible-passage", default='John3v16_19',
        help='char: Bible Passage in format: {Book}.{Chapter}v{StartVerse}_{EndVerse}'
    )
    args.add_argument(
        '-v', "--bible-version", default='NKJV',
        help='char: Version of the Bible, abbr e.g. ESV, KJV'
    )
    args.add_argument(
        '-M', "--memory-verse", default='John3v18',
        help='char: Cornerstone MemoryVerse, Today: Here, Now, this season'
    )
    args.add_argument(
        '-s', "--signature-key",
        help='char: Name of the appropriate Signature'
    )
    args.add_argument(
        '-d', "--diagram",
        help='png: SummaryDiagram of Sermon'
    )
    inputs = args.parse_args()

    print('\nInput validation:')
    validate_inputs(inputs)
    pprint(inputs)

    # Assemble the Bible Passage link
    # e.g. https://www.bible.com/en-GB/bible/114/jhn.3.16-19
    if inputs.bible_version in BIBLE_VERSIONS:
        version = BIBLE_VERSIONS[inputs.bible_version]
    else:
        ver_err_msg = '-v|--bible-version: should be one of', BIBLE_VERSIONS
        assert inputs.bible_version not in BIBLE_VERSIONS, ver_err_msg

    passage_lnk = get_passage_lnk(inputs.bible_passage)
    bible_passage_url = '/'.join([BIBLE_ROOT_URL, LANGUAGE, 'bible', version, passage_lnk])
    print('\nDEBUG: bible passage: URL: ', bible_passage_url)
    sys.exit(0)

    # Get the Memory Verse

    # Collate the Summary

    # Add Signature

    # Print output



if __name__ == '__main__':
    main()
