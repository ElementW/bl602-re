# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
# [GCC 9.3.0]
# Embedded file name: lib\bflb_toml.py
Instruction context:
   
 L.1001       168  LOAD_FAST                'addtosections'
                 170  LOAD_FAST                's'
                 172  BINARY_SUBSCR    
                 174  LOAD_FAST                'newsections'
                 176  LOAD_FAST                'section'
                 178  LOAD_STR                 '.'
                 180  BINARY_ADD       
                 182  LOAD_FAST                's'
                 184  BINARY_ADD       
                 186  STORE_SUBSCR     
                 188  JUMP_BACK           164  'to 164'
                 190  POP_BLOCK        
               192_0  COME_FROM_LOOP      158  '158'
                 192  JUMP_BACK            66  'to 66'
                 194  POP_BLOCK        
->             196_0  COME_FROM_LOOP       60  '60'
import re, sys, io, datetime
from datetime import tzinfo, timedelta
from os import linesep
from collections import OrderedDict
if sys.version_info < (3, ):
    _range = xrange
else:
    unicode = str
    _range = range
    basestring = str
    unichr = chr

def _detect_pathlib_path(p):
    if (3, 4) <= sys.version_info:
        import pathlib
        if isinstance(p, pathlib.PurePath):
            return True
    return False


def _ispath(p):
    if isinstance(p, basestring):
        return True
    return _detect_pathlib_path(p)


def _getpath(p):
    if (3, 6) <= sys.version_info:
        import os
        return os.fspath(p)
    if _detect_pathlib_path(p):
        return str(p)
    return p


try:
    FNFError = FileNotFoundError
except NameError:
    FNFError = IOError

TIME_RE = re.compile('([0-9]{2}):([0-9]{2}):([0-9]{2})(\\.([0-9]{3,6}))?')

class TomlDecodeError(ValueError):
    __doc__ = 'Base toml Exception / Error.'

    def __init__(self, msg, doc, pos):
        lineno = doc.count('\n', 0, pos) + 1
        colno = pos - doc.rfind('\n', 0, pos)
        emsg = '{} (line {} column {} char {})'.format(msg, lineno, colno, pos)
        ValueError.__init__(self, emsg)
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.lineno = lineno
        self.colno = colno


_number_with_underscores = re.compile('([0-9])(_([0-9]))*')

def _strictly_valid_num(n):
    n = n.strip()
    if not n:
        return False
    if n[0] == '_':
        return False
    if n[(-1)] == '_':
        return False
    if '_.' in n or ('._' in n):
        return False
    if len(n) == 1:
        return True
    if n[0] == '0':
        if n[1] not in ('.', 'o', 'b', 'x'):
            return False
    if n[0] == '+' or (n[0] == '-'):
        n = n[1:]
        if len(n) > 1:
            if n[0] == '0':
                if n[1] != '.':
                    return False
    if '__' in n:
        return False
    return True


def load(f, _dict=dict, decoder=None):
    """Parses named file or files as toml and returns a dictionary

    Args:
        f: Path to the file to open, array of files to read into single dict
           or a file descriptor
        _dict: (optional) Specifies the class of the returned toml dictionary

    Returns:
        Parsed toml file represented as a dictionary

    Raises:
        TypeError -- When f is invalid type
        TomlDecodeError: Error while decoding toml
        IOError / FileNotFoundError -- When an array with no valid (existing)
        (Python 2 / Python 3)          file paths is passed
    """
    if _ispath(f):
        with io.open((_getpath(f)), encoding='utf-8') as ffile:
            return loads(ffile.read(), _dict, decoder)
    else:
        if isinstance(f, list):
            from os import path as op
            from warnings import warn
            if not [path for path in f if op.exists(path)]:
                error_msg = 'Load expects a list to contain filenames only.'
                error_msg += linesep
                error_msg += 'The list needs to contain the path of at least one existing file.'
                raise FNFError(error_msg)
            if decoder is None:
                decoder = TomlDecoder()
            d = decoder.get_empty_table()
            for l in f:
                if op.exists(l):
                    d.update(load(l, _dict, decoder))
                else:
                    warn('Non-existent filename in list with at least one valid filename')

            return d
        try:
            return loads(f.read(), _dict, decoder)
        except AttributeError:
            raise TypeError('You can only load a file descriptor, filename or list')


_groupname_re = re.compile('^[A-Za-z0-9_-]+$')

def loads(s, _dict=dict, decoder=None):
    """Parses string as toml

    Args:
        s: String to be parsed
        _dict: (optional) Specifies the class of the returned toml dictionary

    Returns:
        Parsed toml file represented as a dictionary

    Raises:
        TypeError: When a non-string is passed
        TomlDecodeError: Error while decoding toml
    """
    implicitgroups = []
    if decoder is None:
        decoder = TomlDecoder(_dict)
    retval = decoder.get_empty_table()
    currentlevel = retval
    if not isinstance(s, basestring):
        raise TypeError('Expecting something like a string')
    if not isinstance(s, unicode):
        s = s.decode('utf8')
    original = s
    sl = list(s)
    openarr = 0
    openstring = False
    openstrchar = ''
    multilinestr = False
    arrayoftables = False
    beginline = True
    keygroup = False
    dottedkey = False
    keyname = 0
    for i, item in enumerate(sl):
        if item == '\r':
            if sl[(i + 1)] == '\n':
                sl[i] = ' '
                continue
        if keyname:
            if item == '\n':
                raise TomlDecodeError('Key name found without value. Reached end of line.', original, i)
            if openstring:
                if item == openstrchar:
                    keyname = 2
                    openstring = False
                    openstrchar = ''
                    continue
            else:
                if keyname == 1:
                    if item.isspace():
                        keyname = 2
                        continue
                    else:
                        if item == '.':
                            dottedkey = True
                            continue
                        else:
                            if not item.isalnum():
                                if not item == '_':
                                    if item == '-':
                                        continue
                                    else:
                                        if dottedkey:
                                            if sl[(i - 1)] == '.':
                                                if item == '"' or item == "'":
                                                    openstring = True
                                                    openstrchar = item
                                                    continue
                else:
                    if keyname == 2:
                        if item.isspace():
                            if dottedkey:
                                nextitem = sl[(i + 1)]
                                if not nextitem.isspace():
                                    if nextitem != '.':
                                        keyname = 1
                                        continue
                                    if item == '.':
                                        dottedkey = True
                                        nextitem = sl[(i + 1)]
                                        if not nextitem.isspace():
                                            if nextitem != '.':
                                                keyname = 1
                                                continue
                                            if item == '=':
                                                keyname = 0
                                                dottedkey = False
                                            else:
                                                raise TomlDecodeError("Found invalid character in key name: '" + item + "'. Try quoting the key name.", original, i)
                            if item == "'":
                                if openstrchar != '"':
                                    k = 1
                                    try:
                                        while sl[(i - k)] == "'":
                                            k += 1
                                            if k == 3:
                                                break

                                    except IndexError:
                                        pass

                                    if k == 3:
                                        multilinestr = not multilinestr
                                        openstring = multilinestr
                                    else:
                                        openstring = not openstring
                                    if openstring:
                                        openstrchar = "'"
                                    else:
                                        openstrchar = ''
                            if item == '"':
                                if openstrchar != "'":
                                    oddbackslash = False
                                    k = 1
                                    tripquote = False
                                    try:
                                        while sl[(i - k)] == '"':
                                            k += 1
                                            if k == 3:
                                                tripquote = True
                                                break

                                        if k == 1 or (k == 3 and tripquote):
                                            while sl[(i - k)] == '\\':
                                                oddbackslash = not oddbackslash
                                                k += 1

                                    except IndexError:
                                        pass

                                    if not oddbackslash:
                                        if tripquote:
                                            multilinestr = not multilinestr
                                            openstring = multilinestr
                                        else:
                                            openstring = not openstring
                                    if openstring:
                                        openstrchar = '"'
                                    else:
                                        openstrchar = ''
            if item == '#' and not openstring or keygroup or arrayoftables:
                j = i
                try:
                    while sl[j] != '\n':
                        sl[j] = ' '
                        j += 1

                except IndexError:
                    break

                if item == '[' and not openstring:
                    if not keygroup:
                        if not arrayoftables:
                            if beginline:
                                if len(sl) > i + 1 and sl[(i + 1)] == '[':
                                    arrayoftables = True
                                else:
                                    keygroup = True
                            else:
                                openarr += 1
                    if item == ']':
                        if not openstring:
                            if keygroup:
                                keygroup = False
                            elif arrayoftables:
                                if sl[(i - 1)] == ']':
                                    arrayoftables = False
                            else:
                                openarr -= 1
                        if item == '\n':
                            if openstring or multilinestr:
                                if not multilinestr:
                                    raise TomlDecodeError('Unbalanced quotes', original, i)
                                elif sl[(i - 1)] == "'" or sl[(i - 1)] == '"':
                                    if sl[(i - 2)] == sl[(i - 1)]:
                                        sl[i] = sl[(i - 1)]
                                        if sl[(i - 3)] == sl[(i - 1)]:
                                            sl[i - 3] = ' '
                            elif openarr:
                                sl[i] = ' '
                            else:
                                beginline = True
                        if beginline:
                            if sl[i] != ' ':
                                if sl[i] != '\t':
                                    beginline = False
                                    if not keygroup:
                                        if not arrayoftables:
                                            if sl[i] == '=':
                                                raise TomlDecodeError('Found empty keyname. ', original, i)
                                            else:
                                                keyname = 1

    s = ''.join(sl)
    s = s.split('\n')
    multikey = None
    multilinestr = ''
    multibackslash = False
    pos = 0
    for idx, line in enumerate(s):
        if idx > 0:
            pos += len(s[(idx - 1)]) + 1
        if multilinestr:
            if multibackslash or ('\n' not in multilinestr):
                line = line.strip()
            if line == '':
                if multikey:
                    if multibackslash:
                        continue
                if multikey:
                    if multibackslash:
                        multilinestr += line
                    else:
                        multilinestr += line
                    multibackslash = False
                    if len(line) > 2 and line[(-1)] == multilinestr[0]:
                        if line[(-2)] == multilinestr[0] and line[(-3)] == multilinestr[0]:
                            try:
                                value, vtype = decoder.load_value(multilinestr)
                            except ValueError as err:
                                try:
                                    raise TomlDecodeError(str(err), original, pos)
                                finally:
                                    err = None
                                    del err

                            currentlevel[multikey] = value
                            multikey = None
                            multilinestr = ''
                        else:
                            k = len(multilinestr) - 1
                            while k > -1:
                                if multilinestr[k] == '\\':
                                    multibackslash = not multibackslash
                                    k -= 1

                        if multibackslash:
                            multilinestr = multilinestr[:-1]
                    else:
                        multilinestr += '\n'
                        continue
        if line[0] == '[':
            arrayoftables = False
            if len(line) == 1:
                raise TomlDecodeError('Opening key group bracket on line by itself.', original, pos)
            else:
                if line[1] == '[':
                    arrayoftables = True
                    line = line[2:]
                    splitstr = ']]'
                else:
                    line = line[1:]
                    splitstr = ']'
                i = 1
                quotesplits = decoder._get_split_on_quotes(line)
                quoted = False
                for quotesplit in quotesplits:
                    if not quoted:
                        if splitstr in quotesplit:
                            break
                    i += quotesplit.count(splitstr)
                    quoted = not quoted

                line = line.split(splitstr, i)
                if len(line) < i + 1 or (line[(-1)].strip() != ''):
                    raise TomlDecodeError('Key group not on a line by itself.', original, pos)
                groups = splitstr.join(line[:-1]).split('.')
                i = 0
                while i < len(groups):
                    groups[i] = groups[i].strip()
                    if not len(groups[i]) > 0 or groups[i][0] == '"' or groups[i][0] == "'":
                        groupstr = groups[i]
                        j = i + 1
                        while not groupstr[0] == groupstr[(-1)]:
                            j += 1
                            if j > len(groups) + 2:
                                raise TomlDecodeError("Invalid group name '" + groupstr + "' Something " + 'went wrong.', original, pos)
                            else:
                                groupstr = '.'.join(groups[i:j]).strip()

                        groups[i] = groupstr[1:-1]
                        groups[i + 1:j] = []
                    else:
                        if not _groupname_re.match(groups[i]):
                            raise TomlDecodeError("Invalid group name '" + groups[i] + "'. Try quoting it.", original, pos)
                        i += 1

                currentlevel = retval
                for i in _range(len(groups)):
                    group = groups[i]
                    if group == '':
                        raise TomlDecodeError("Can't have a keygroup with an empty name", original, pos)
                    try:
                        currentlevel[group]
                        if i == len(groups) - 1:
                            if group in implicitgroups:
                                implicitgroups.remove(group)
                                if arrayoftables:
                                    raise TomlDecodeError("An implicitly defined table can't be an array", original, pos)
                            elif arrayoftables:
                                currentlevel[group].append(decoder.get_empty_table())
                            else:
                                raise TomlDecodeError('What? ' + group + ' already exists?' + str(currentlevel), original, pos)
                    except TypeError:
                        currentlevel = currentlevel[(-1)]
                        if group not in currentlevel:
                            currentlevel[group] = decoder.get_empty_table()
                            if i == len(groups) - 1:
                                if arrayoftables:
                                    currentlevel[group] = [
                                     decoder.get_empty_table()]
                    except KeyError:
                        if i != len(groups) - 1:
                            implicitgroups.append(group)
                        else:
                            currentlevel[group] = decoder.get_empty_table()
                            if i == len(groups) - 1:
                                if arrayoftables:
                                    currentlevel[group] = [
                                     decoder.get_empty_table()]

                    currentlevel = currentlevel[group]
                    if arrayoftables:
                        try:
                            currentlevel = currentlevel[(-1)]
                        except KeyError:
                            pass

        else:
            if line[0] == '{':
                if line[(-1)] != '}':
                    raise TomlDecodeError('Line breaks are not allowed in inlineobjects', original, pos)
                else:
                    try:
                        decoder.load_inline_object(line, currentlevel, multikey, multibackslash)
                    except ValueError as err:
                        try:
                            raise TomlDecodeError(str(err), original, pos)
                        finally:
                            err = None
                            del err

        if '=' in line:
            try:
                ret = decoder.load_line(line, currentlevel, multikey, multibackslash)
            except ValueError as err:
                try:
                    raise TomlDecodeError(str(err), original, pos)
                finally:
                    err = None
                    del err

            if ret is not None:
                multikey, multilinestr, multibackslash = ret

    return retval


def _load_date(val):
    microsecond = 0
    tz = None
    try:
        if len(val) > 19:
            if val[19] == '.':
                if val[(-1)].upper() == 'Z':
                    subsecondval = val[20:-1]
                    tzval = 'Z'
                else:
                    subsecondvalandtz = val[20:]
                    if '+' in subsecondvalandtz:
                        splitpoint = subsecondvalandtz.index('+')
                        subsecondval = subsecondvalandtz[:splitpoint]
                        tzval = subsecondvalandtz[splitpoint:]
                    elif '-' in subsecondvalandtz:
                        splitpoint = subsecondvalandtz.index('-')
                        subsecondval = subsecondvalandtz[:splitpoint]
                        tzval = subsecondvalandtz[splitpoint:]
                    else:
                        tzval = None
                        subsecondval = subsecondvalandtz
                if tzval is not None:
                    tz = TomlTz(tzval)
                microsecond = int(int(subsecondval) * 10 ** (6 - len(subsecondval)))
            else:
                tz = TomlTz(val[19:])
    except ValueError:
        tz = None

    if '-' not in val[1:]:
        return
    try:
        if len(val) == 10:
            d = datetime.date(int(val[:4]), int(val[5:7]), int(val[8:10]))
        else:
            d = datetime.datetime(int(val[:4]), int(val[5:7]), int(val[8:10]), int(val[11:13]), int(val[14:16]), int(val[17:19]), microsecond, tz)
    except ValueError:
        return
    else:
        return d


def _load_unicode_escapes(v, hexbytes, prefix):
    skip = False
    i = len(v) - 1
    while i > -1:
        if v[i] == '\\':
            skip = not skip
            i -= 1

    for hx in hexbytes:
        if skip:
            skip = False
            i = len(hx) - 1
            while i > -1:
                if hx[i] == '\\':
                    skip = not skip
                    i -= 1

            v += prefix
            v += hx
            continue
        else:
            hxb = ''
            i = 0
            hxblen = 4
            if prefix == '\\U':
                hxblen = 8
            hxb = ''.join(hx[i:i + hxblen]).lower()
            if hxb.strip('0123456789abcdef'):
                raise ValueError('Invalid escape sequence: ' + hxb)
            if hxb[0] == 'd':
                if hxb[1].strip('01234567'):
                    raise ValueError('Invalid escape sequence: ' + hxb + '. Only scalar unicode points are allowed.')
            v += unichr(int(hxb, 16))
            v += unicode(hx[len(hxb):])

    return v


_escapes = [
 '0', 'b', 'f', 'n', 'r', 't', '"']
_escapedchars = [
 '\x00', '\x08', '\x0c', '\n', '\r', '\t', '"']
_escape_to_escapedchars = dict(zip(_escapes, _escapedchars))

def _unescape(v):
    """Unescape characters in a TOML string."""
    i = 0
    backslash = False
    while i < len(v):
        if backslash:
            backslash = False
            if v[i] in _escapes:
                v = v[:i - 1] + _escape_to_escapedchars[v[i]] + v[i + 1:]
            else:
                if v[i] == '\\':
                    v = v[:i - 1] + v[i:]
                else:
                    if not v[i] == 'u' or v[i] == 'U':
                        i += 1
                    else:
                        raise ValueError('Reserved escape sequence used')
            continue
        elif v[i] == '\\':
            backslash = True
        i += 1

    return v


class InlineTableDict(object):
    __doc__ = 'Sentinel subclass of dict for inline tables.'


class TomlDecoder(object):

    def __init__(self, _dict=dict):
        self._dict = _dict

    def get_empty_table(self):
        return self._dict()

    def get_empty_inline_table(self):

        class DynamicInlineTableDict(self._dict, InlineTableDict):
            __doc__ = 'Concrete sentinel subclass for inline tables.\n            It is a subclass of _dict which is passed in dynamically at load\n            time\n\n            It is also a subclass of InlineTableDict\n            '

        return DynamicInlineTableDict()

    def load_inline_object(self, line, currentlevel, multikey=False, multibackslash=False):
        candidate_groups = line[1:-1].split(',')
        groups = []
        if len(candidate_groups) == 1:
            if not candidate_groups[0].strip():
                candidate_groups.pop()
            while len(candidate_groups) > 0:
                candidate_group = candidate_groups.pop(0)
                try:
                    _, value = candidate_group.split('=', 1)
                except ValueError:
                    raise ValueError('Invalid inline table encountered')

                value = value.strip()
                if not (value[0] == value[(-1)] and value[0] in ('"', "'")):
                    if not value[0] in '-0123456789':
                        if not value in ('true', 'false'):
                            if value[0] == '[':
                                if not value[(-1)] == ']':
                                    if not value[0] == '{' or value[(-1)] == '}':
                                        groups.append(candidate_group)
                                    elif len(candidate_groups) > 0:
                                        candidate_groups[0] = candidate_group + ',' + candidate_groups[0]
                                else:
                                    raise ValueError('Invalid inline table value encountered')

            for group in groups:
                status = self.load_line(group, currentlevel, multikey, multibackslash)
                if status is not None:
                    break

    def _get_split_on_quotes(self, line):
        doublequotesplits = line.split('"')
        quoted = False
        quotesplits = []
        if len(doublequotesplits) > 1:
            if "'" in doublequotesplits[0]:
                singlequotesplits = doublequotesplits[0].split("'")
                doublequotesplits = doublequotesplits[1:]
                while len(singlequotesplits) % 2 == 0:
                    if len(doublequotesplits):
                        singlequotesplits[(-1)] += '"' + doublequotesplits[0]
                        doublequotesplits = doublequotesplits[1:]
                        if "'" in singlequotesplits[(-1)]:
                            singlequotesplits = singlequotesplits[:-1] + singlequotesplits[(-1)].split("'")

                quotesplits += singlequotesplits
        for doublequotesplit in doublequotesplits:
            if quoted:
                quotesplits.append(doublequotesplit)
            else:
                quotesplits += doublequotesplit.split("'")
                quoted = not quoted

        return quotesplits

    def load_line(self, line, currentlevel, multikey, multibackslash):
        i = 1
        quotesplits = self._get_split_on_quotes(line)
        quoted = False
        for quotesplit in quotesplits:
            if not quoted:
                if '=' in quotesplit:
                    break
            i += quotesplit.count('=')
            quoted = not quoted

        pair = line.split('=', i)
        strictly_valid = _strictly_valid_num(pair[(-1)])
        if _number_with_underscores.match(pair[(-1)]):
            pair[-1] = pair[(-1)].replace('_', '')
        while len(pair[(-1)]):
            if pair[(-1)][0] != ' ':
                if pair[(-1)][0] != '\t':
                    if pair[(-1)][0] != "'":
                        if pair[(-1)][0] != '"':
                            if pair[(-1)][0] != '[':
                                if pair[(-1)][0] != '{':
                                    if pair[(-1)] != 'true':
                                        if pair[(-1)] != 'false':
                                            try:
                                                float(pair[(-1)])
                                                break
                                            except ValueError:
                                                pass

                                            if _load_date(pair[(-1)]) is not None:
                                                break
                                            else:
                                                i += 1
                                                prev_val = pair[(-1)]
                                                pair = line.split('=', i)
                                                if prev_val == pair[(-1)]:
                                                    raise ValueError('Invalid date or number')
                                            if strictly_valid:
                                                strictly_valid = _strictly_valid_num(pair[(-1)])

        pair = [
         '='.join(pair[:-1]).strip(), pair[(-1)].strip()]
        if '.' in pair[0]:
            if '"' in pair[0] or "'" in pair[0]:
                quotesplits = self._get_split_on_quotes(pair[0])
                quoted = False
                levels = []
                for quotesplit in quotesplits:
                    if quoted:
                        levels.append(quotesplit)
                    else:
                        levels += [level.strip() for level in quotesplit.split('.')]
                    quoted = not quoted

            else:
                levels = pair[0].split('.')
            while levels[(-1)] == '':
                levels = levels[:-1]

            for level in levels[:-1]:
                if level == '':
                    continue
                else:
                    if level not in currentlevel:
                        currentlevel[level] = self.get_empty_table()
                    currentlevel = currentlevel[level]

            pair[0] = levels[(-1)].strip()
        else:
            if pair[0][0] == '"' or (pair[0][0] == "'"):
                if pair[0][(-1)] == pair[0][0]:
                    pair[0] = pair[0][1:-1]
        if len(pair[1]) > 2:
            if pair[1][0] == '"' or (pair[1][0] == "'"):
                if not (pair[1][1] == pair[1][0]and pair[1][2] == pair[1][0]and len(pair[1]) > 5and pair[1][(-1)] == pair[1][0] and pair[1][2] == pair[1][0] and pair[1][(-3)] == pair[1][0]):
                    k = len(pair[1]) - 1
                    while k > -1:
                        if pair[1][k] == '\\':
                            multibackslash = not multibackslash
                            k -= 1

                    if multibackslash:
                        multilinestr = pair[1][:-1]
                    else:
                        multilinestr = pair[1] + '\n'
                    multikey = pair[0]
                else:
                    pass
            value, vtype = self.load_value(pair[1], strictly_valid)
        try:
            currentlevel[pair[0]]
            raise ValueError('Duplicate keys!')
        except TypeError:
            raise ValueError('Duplicate keys!')
        except KeyError:
            if multikey:
                return (multikey, multilinestr, multibackslash)
            else:
                currentlevel[pair[0]] = value

    def load_value(self, v, strictly_valid=True):
        if not v:
            raise ValueError('Empty value is invalid')
        if v == 'true':
            return (True, 'bool')
        if v == 'false':
            return (False, 'bool')
        if v[0] == '"' or (v[0] == "'"):
            quotechar = v[0]
            testv = v[1:].split(quotechar)
            triplequote = False
            triplequotecount = 0
            if len(testv) > 1:
                if testv[0] == '':
                    if testv[1] == '':
                        testv = testv[2:]
                        triplequote = True
            closed = False
            for tv in testv:
                if tv == '':
                    if triplequote:
                        triplequotecount += 1
                    else:
                        closed = True
                else:
                    oddbackslash = False
                    try:
                        i = -1
                        j = tv[i]
                        while j == '\\':
                            oddbackslash = not oddbackslash
                            i -= 1
                            j = tv[i]

                    except IndexError:
                        pass

                    if not oddbackslash:
                        if closed:
                            raise ValueError('Stuff after closed string. WTF?')
                if triplequote:
                    if triplequotecount > 1:
                        closed = True
                    else:
                        triplequotecount = 0

            if quotechar == '"':
                escapeseqs = v.split('\\')[1:]
                backslash = False
                for i in escapeseqs:
                    if i == '':
                        backslash = not backslash
                    if i[0] not in _escapes:
                        if i[0] != 'u':
                            if i[0] != 'U':
                                if not backslash:
                                    raise ValueError('Reserved escape sequence used')
                                if backslash:
                                    backslash = False

                for prefix in ('\\u', '\\U'):
                    if prefix in v:
                        hexbytes = v.split(prefix)
                        v = _load_unicode_escapes(hexbytes[0], hexbytes[1:], prefix)

                v = _unescape(v)
            if not len(v) > 1 or v[1] == quotechar:
                if len(v) < 3 or (v[1] == v[2]):
                    v = v[2:-2]
                return (v[1:-1], 'str')
        if v[0] == '[':
            return (self.load_array(v), 'array')
        if v[0] == '{':
            inline_object = self.get_empty_inline_table()
            self.load_inline_object(v, inline_object)
            return (
             inline_object, 'inline_object')
        if TIME_RE.match(v):
            h, m, s, _, ms = TIME_RE.match(v).groups()
            time = datetime.time(int(h), int(m), int(s), int(ms) if ms else 0)
            return (
             time, 'time')
        parsed_date = _load_date(v)
        if parsed_date is not None:
            return (parsed_date, 'date')
        if not strictly_valid:
            raise ValueError('Weirdness with leading zeroes or underscores in your number.')
        itype = 'int'
        neg = False
        if v[0] == '-':
            neg = True
            v = v[1:]
        elif v[0] == '+':
            v = v[1:]
        v = v.replace('_', '')
        lowerv = v.lower()
        if not '.' in v:
            if 'x' not in v and 'e' in v or 'E' in v:
                if '.' in v:
                    if v.split('.', 1)[1] == '':
                        raise ValueError('This float is missing digits after the point')
                if v[0] not in '0123456789':
                    raise ValueError("This float doesn't have a leading digit")
                v = float(v)
                itype = 'float'
            else:
                pass
            if len(lowerv) == 3:
                if lowerv == 'inf' or (lowerv == 'nan'):
                    v = float(v)
                    itype = 'float'
                if itype == 'int':
                    v = int(v, 0)
                if neg:
                    return (0 - v, itype)
            return (
             v, itype)

    def bounded_string(self, s):
        if len(s) == 0:
            return True
        if s[(-1)] != s[0]:
            return False
        i = -2
        backslash = False
        while len(s) + i > 0:
            if s[i] == '\\':
                backslash = not backslash
                i -= 1
            else:
                break

        return not backslash

    def load_array(self, a):
        atype = None
        retval = []
        a = a.strip()
        if '[' not in a[1:-1] or '' != a[1:-1].split('[')[0].strip():
            strarray = False
            tmpa = a[1:-1].strip()
            if tmpa != '':
                if tmpa[0] == '"' or (tmpa[0] == "'"):
                    strarray = True
            if not a[1:-1].strip().startswith('{'):
                a = a[1:-1].split(',')
            else:
                new_a = []
                start_group_index = 1
                end_group_index = 2
                in_str = False
                while end_group_index < len(a[1:]):
                    if a[end_group_index] == '"' or (a[end_group_index] == "'"):
                        if in_str:
                            backslash_index = end_group_index - 1
                            while backslash_index > -1:
                                if a[backslash_index] == '\\':
                                    in_str = not in_str
                                    backslash_index -= 1

                        in_str = not in_str
                    if in_str or a[end_group_index] != '}':
                        end_group_index += 1
                        continue
                    else:
                        end_group_index += 1
                        new_a.append(a[start_group_index:end_group_index])
                        start_group_index = end_group_index + 1
                        while start_group_index < len(a[1:]):
                            if a[start_group_index] != '{':
                                start_group_index += 1

                        end_group_index = start_group_index + 1

                a = new_a
            b = 0
            if strarray:
                while b < len(a) - 1:
                    ab = a[b].strip()
                    while self.bounded_string(ab):
                        if len(ab) > 2:
                            if ab[0] == ab[1]== ab[2]:
                                if ab[(-2)] != ab[0]:
                                    if ab[(-3)] != ab[0]:
                                        a[b] = a[b] + ',' + a[(b + 1)]
                                        ab = a[b].strip()
                                        if b < len(a) - 2:
                                            a = a[:b + 1] + a[b + 2:]
                                    else:
                                        a = a[:b + 1]

                    b += 1

        else:
            al = list(a[1:-1])
            a = []
            openarr = 0
            j = 0
            for i in _range(len(al)):
                if al[i] == '[':
                    openarr += 1
                else:
                    if al[i] == ']':
                        openarr -= 1
                if al[i] == ',':
                    if not openarr:
                        a.append(''.join(al[j:i]))
                        j = i + 1

            a.append(''.join(al[j:]))
        for i in _range(len(a)):
            a[i] = a[i].strip()
            if a[i] != '':
                nval, ntype = self.load_value(a[i])
                if atype:
                    if ntype != atype:
                        raise ValueError('Not a homogeneous array')
                else:
                    atype = ntype
                retval.append(nval)

        return retval


def dump(o, f):
    """Writes out dict as toml to a file

    Args:
        o: Object to dump into toml
        f: File descriptor where the toml should be stored

    Returns:
        String containing the toml corresponding to dictionary

    Raises:
        TypeError: When anything other than file descriptor is passed
    """
    if not f.write:
        raise TypeError('You can only dump an object to a file descriptor')
    d = dumps(o)
    f.write(d)
    return d


def dumps--- This code section failed: ---

 L. 983         0  LOAD_STR                 ''
                2  STORE_FAST               'retval'

 L. 984         4  LOAD_FAST                'encoder'
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    22  'to 22'

 L. 985        12  LOAD_GLOBAL              TomlEncoder
               14  LOAD_FAST                'o'
               16  LOAD_ATTR                __class__
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  STORE_FAST               'encoder'
             22_0  COME_FROM            10  '10'

 L. 986        22  LOAD_FAST                'encoder'
               24  LOAD_METHOD              dump_sections
               26  LOAD_FAST                'o'
               28  LOAD_STR                 ''
               30  CALL_METHOD_2         2  '2 positional arguments'
               32  UNPACK_SEQUENCE_2     2 
               34  STORE_FAST               'addtoretval'
               36  STORE_FAST               'sections'

 L. 987        38  LOAD_FAST                'retval'
               40  LOAD_FAST                'addtoretval'
               42  INPLACE_ADD      
               44  STORE_FAST               'retval'

 L. 988        46  SETUP_LOOP          204  'to 204'
             48_0  COME_FROM           200  '200'
               48  LOAD_FAST                'sections'
               50  POP_JUMP_IF_FALSE   202  'to 202'

 L. 989        52  LOAD_FAST                'encoder'
               54  LOAD_METHOD              get_empty_table
               56  CALL_METHOD_0         0  '0 positional arguments'
               58  STORE_FAST               'newsections'

 L. 990        60  SETUP_LOOP          196  'to 196'
               62  LOAD_FAST                'sections'
               64  GET_ITER         
             66_0  COME_FROM           192  '192'
               66  FOR_ITER            194  'to 194'
               68  STORE_FAST               'section'

 L. 991        70  LOAD_FAST                'encoder'
               72  LOAD_METHOD              dump_sections

 L. 992        74  LOAD_FAST                'sections'
               76  LOAD_FAST                'section'
               78  BINARY_SUBSCR    
               80  LOAD_FAST                'section'
               82  CALL_METHOD_2         2  '2 positional arguments'
               84  UNPACK_SEQUENCE_2     2 
               86  STORE_FAST               'addtoretval'
               88  STORE_FAST               'addtosections'

 L. 994        90  LOAD_FAST                'addtoretval'
               92  POP_JUMP_IF_TRUE    102  'to 102'
               94  LOAD_FAST                'addtoretval'
               96  POP_JUMP_IF_TRUE    158  'to 158'
               98  LOAD_FAST                'addtosections'
              100  POP_JUMP_IF_TRUE    158  'to 158'
            102_0  COME_FROM            92  '92'

 L. 995       102  LOAD_FAST                'retval'
              104  POP_JUMP_IF_FALSE   130  'to 130'
              106  LOAD_FAST                'retval'
              108  LOAD_CONST               -2
              110  LOAD_CONST               None
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  LOAD_STR                 '\n\n'
              118  COMPARE_OP               !=
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 996       122  LOAD_FAST                'retval'
              124  LOAD_STR                 '\n'
              126  INPLACE_ADD      
              128  STORE_FAST               'retval'
            130_0  COME_FROM           120  '120'
            130_1  COME_FROM           104  '104'

 L. 997       130  LOAD_FAST                'retval'
              132  LOAD_STR                 '['
              134  LOAD_FAST                'section'
              136  BINARY_ADD       
              138  LOAD_STR                 ']\n'
              140  BINARY_ADD       
              142  INPLACE_ADD      
              144  STORE_FAST               'retval'

 L. 998       146  LOAD_FAST                'addtoretval'
              148  POP_JUMP_IF_FALSE   158  'to 158'

 L. 999       150  LOAD_FAST                'retval'
              152  LOAD_FAST                'addtoretval'
              154  INPLACE_ADD      
              156  STORE_FAST               'retval'
            158_0  COME_FROM           148  '148'
            158_1  COME_FROM           100  '100'
            158_2  COME_FROM            96  '96'

 L.1000       158  SETUP_LOOP          192  'to 192'
              160  LOAD_FAST                'addtosections'
              162  GET_ITER         
            164_0  COME_FROM           188  '188'
              164  FOR_ITER            190  'to 190'
              166  STORE_FAST               's'

 L.1001       168  LOAD_FAST                'addtosections'
              170  LOAD_FAST                's'
              172  BINARY_SUBSCR    
              174  LOAD_FAST                'newsections'
              176  LOAD_FAST                'section'
              178  LOAD_STR                 '.'
              180  BINARY_ADD       
              182  LOAD_FAST                's'
              184  BINARY_ADD       
              186  STORE_SUBSCR     
              188  JUMP_BACK           164  'to 164'
              190  POP_BLOCK        
            192_0  COME_FROM_LOOP      158  '158'
              192  JUMP_BACK            66  'to 66'
              194  POP_BLOCK        
            196_0  COME_FROM_LOOP       60  '60'

 L.1002       196  LOAD_FAST                'newsections'
              198  STORE_FAST               'sections'
              200  JUMP_BACK            48  'to 48'
            202_0  COME_FROM            50  '50'
              202  POP_BLOCK        
            204_0  COME_FROM_LOOP       46  '46'

 L.1003       204  LOAD_FAST                'retval'
              206  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 196_0


def _dump_str(v):
    if sys.version_info < (3, ):
        if hasattr(v, 'decode'):
            if isinstance(v, str):
                v = v.decode('utf-8')
    v = '%r' % v
    if v[0] == 'u':
        v = v[1:]
    singlequote = v.startswith("'")
    if singlequote or (v.startswith('"')):
        v = v[1:-1]
    if singlequote:
        v = v.replace("\\'", "'")
        v = v.replace('"', '\\"')
    f = v[:]
    v = v.split('\\x')
    while len(v) > 1:
        i = -1
        if not v[0]:
            v = v[1:]
        v[0] = v[0].replace('\\\\', '\\')
        joinx = v[0][i] != '\\'
        while v[0][:i]:
            if v[0][i] == '\\':
                joinx = not joinx
                i -= 1

        if joinx:
            joiner = 'x'
        else:
            joiner = 'u00'
        v = [
         v[0] + joiner + v[1]] + v[2:]
        import os
        if os.path.isfile(f):
            v[0] = v[0].replace('\\', '\\\\')

    return unicode('"' + v[0] + '"')


def _dump_float(v):
    return '{0:.16}'.format(v).replace('e+0', 'e+').replace('e-0', 'e-')


def _dump_time(v):
    utcoffset = v.utcoffset()
    if utcoffset is None:
        return v.isoformat()
    return v.isoformat()[:-6]


class TomlEncoder(object):

    def __init__(self, _dict=dict, preserve=False):
        self._dict = _dict
        self.preserve = preserve
        self.dump_funcs = {str: _dump_str, 
         unicode: _dump_str, 
         list: self.dump_list, 
         bool: lambda v: unicode(v).lower(), 
         int: lambda v: v, 
         float: _dump_float, 
         datetime.datetime: lambda v: v.isoformat().replace('+00:00', 'Z'), 
         datetime.time: _dump_time, 
         datetime.date: lambda v: v.isoformat()}

    def get_empty_table(self):
        return self._dict()

    def dump_list(self, v):
        retval = '['
        for u in v:
            retval += ' ' + unicode(self.dump_value(u)) + ','

        retval += ']'
        return retval

    def dump_inline_table(self, section):
        """Preserve inline table in its compact syntax instead of expanding
        into subsection.

        https://github.com/toml-lang/toml#user-content-inline-table
        """
        retval = ''
        if isinstance(section, dict):
            val_list = []
            for k, v in section.items():
                val = self.dump_inline_table(v)
                val_list.append(k + ' = ' + val)

            retval += '{ ' + ', '.join(val_list) + ' }\n'
            return retval
        return unicode(self.dump_value(section))

    def dump_value(self, v):
        dump_fn = self.dump_funcs.get(type(v))
        if dump_fn is None:
            if hasattr(v, '__iter__'):
                dump_fn = self.dump_funcs[list]
        if dump_fn is not None:
            return dump_fn(v)
        return self.dump_funcs[str](v)

    def dump_sections(self, o, sup):
        retstr = ''
        if sup != '':
            if sup[(-1)] != '.':
                sup += '.'
        retdict = self._dict()
        arraystr = ''
        for section in o:
            section = unicode(section)
            qsection = section
            if not re.match('^[A-Za-z0-9_-]+$', section):
                if '"' in section:
                    qsection = "'" + section + "'"
                else:
                    qsection = '"' + section + '"'
            if not isinstance(o[section], dict):
                arrayoftables = False
                if isinstance(o[section], list):
                    for a in o[section]:
                        if isinstance(a, dict):
                            arrayoftables = True

                if arrayoftables:
                    for a in o[section]:
                        arraytabstr = '\n'
                        arraystr += '[[' + sup + qsection + ']]\n'
                        s, d = self.dump_sections(a, sup + qsection)
                        if s:
                            if s[0] == '[':
                                arraytabstr += s
                            else:
                                arraystr += s
                        while d:
                            newd = self._dict()
                            for dsec in d:
                                s1, d1 = self.dump_sections(d[dsec], sup + qsection + '.' + dsec)
                                if s1:
                                    arraytabstr += '[' + sup + qsection + '.' + dsec + ']\n'
                                    arraytabstr += s1
                                else:
                                    for s1 in d1:
                                        newd[dsec + '.' + s1] = d1[s1]

                            d = newd

                        arraystr += arraytabstr

                elif o[section] is not None:
                    retstr += qsection + ' = ' + unicode(self.dump_value(o[section])) + '\n'
            else:
                if self.preserve and isinstance(o[section], InlineTableDict):
                    retstr += qsection + ' = ' + self.dump_inline_table(o[section])
                else:
                    retdict[qsection] = o[section]

        retstr += arraystr
        return (
         retstr, retdict)


class TomlPreserveInlineDictEncoder(TomlEncoder):

    def __init__(self, _dict=dict):
        super(TomlPreserveInlineDictEncoder, self).__init__(_dict, True)


class TomlArraySeparatorEncoder(TomlEncoder):

    def __init__(self, _dict=dict, preserve=False, separator=','):
        super(TomlArraySeparatorEncoder, self).__init__(_dict, preserve)
        if separator.strip() == '':
            separator = ',' + separator
        elif separator.strip(' \t\n\r,'):
            raise ValueError('Invalid separator for arrays')
        self.separator = separator

    def dump_list(self, v):
        t = []
        retval = '['
        for u in v:
            t.append(self.dump_value(u))

        while t != []:
            s = []
            for u in t:
                if isinstance(u, list):
                    for r in u:
                        s.append(r)

                else:
                    retval += ' ' + unicode(u) + self.separator

            t = s

        retval += ']'
        return retval


class TomlOrderedDecoder(TomlDecoder):

    def __init__(self):
        super(self.__class__, self).__init__(_dict=OrderedDict)


class TomlOrderedEncoder(TomlEncoder):

    def __init__(self):
        super(self.__class__, self).__init__(_dict=OrderedDict)


class TomlTz(tzinfo):

    def __init__(self, toml_offset):
        if toml_offset == 'Z':
            self._raw_offset = '+00:00'
        else:
            self._raw_offset = toml_offset
        self._sign = -1 if self._raw_offset[0] == '-' else 1
        self._hours = int(self._raw_offset[1:3])
        self._minutes = int(self._raw_offset[4:6])

    def tzname(self, dt):
        return 'UTC' + self._raw_offset

    def utcoffset(self, dt):
        return self._sign * timedelta(hours=(self._hours), minutes=(self._minutes))

    def dst(self, dt):
        return timedelta(0)
