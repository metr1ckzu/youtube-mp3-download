import uuid
import re
from unicodedata import normalize

import youtube_dl

def slugify(text, delim='-'):
    """
    Slugifies a string.
    This is slightly different from the built-in one in Django.
    Source: http://stackoverflow.com/questions/9042515/normalizing-unicode-\
        text-to-filenames-etc-in-python
    """
    result = []

    re_obj = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
    for word in re_obj.split(text):
        word = normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8')
        word = word.replace('/', '')
        if word:
            result.append(word)

    return delim.join(result)


def create_filename(value):
    """
    Generate a valid filename.

    Non-ASCII characters will be deleted from the value and replace spaces with
    underscores. Slashes and percent signs are also stripped.
    """
    filename = slugify(value, '_')

    # Generate a random filename if the title only contains non-ASCII
    # characters (i.e. slugifying it deletes everything).
    if not filename:
        filename = uuid.uuid4()

    return '{}.mp3'.format(filename)


def get_video_info(url):
    """
    Retrieve the YouTube videos' information without downloading it.

    Source: http://stackoverflow.com/questions/18054500/how-to-use-youtube-dl-\
            from-a-python-programm/18947879#18947879
    """
    ydl = youtube_dl.YoutubeDL()
    ydl.add_default_info_extractors()

    try:
        return ydl.extract_info(url, download=False)
    except youtube_dl.DownloadError:
        return None
