"""This file was derived from automatically generated code using the
3to2 script: http://pypi.python.org/pypi/3to2/

AUTHOR

Brandon Invergo, <brandon at invergo.net>
Davi Ortega, <davi.ortega at gmail.com>
Luke Ulrich, <ulrich.luke+sci at gmail.com>

BUGS

Please report any bugs or feature requests to the AUTHOR.

LICENSE AND COPYRIGHT

Copyright 2013 Luke Ulrich.

This program is free software; you can redistribute it and/or modify it
under the terms of either: the GNU General Public License as published
by the Free Software Foundation; or the Artistic License.

See http://docs.python.org/2/license.html for more information.

"""


import json
import hashlib
import base64
import re
import binascii
import urllib2
import urllib
import urlparse
import string
from io import open


API_URL = u'http://seqdepot.net/api/v1'
VERSION = u'0.01'


def _aseq_id_from_md5_bytes(md5_bytes):
    u"""Convert a base 64 bytes object to an aseq ID."""

    md5_bytes64 = base64.urlsafe_b64encode(md5_bytes)
    aseq_id = md5_bytes64.replace(b'=', b'')
    return aseq_id.decode(u'utf-8')


def aseq_id_from_md5_hex(md5_hex):
    u"""Convert an MD5 hexadecimal string into its aseqId equivalent.

    Parameters:
        MD5hex: hexadecimal MD5 string

    Return:
        aseqId
    """
    md5_bytes = binascii.unhexlify(md5_hex)
    aseq_id = _aseq_id_from_md5_bytes(md5_bytes)
    return aseq_id


def aseq_id_from_sequence(sequence):
    u"""Compute the aseqId for a given sequence.

    It is recommended that all sequences are cleaned before calling
    this method.

    Parameters:
        sequence

    Returns:
        aseqId
    """
    md5 = hashlib.md5(sequence.replace(u'-', u'').encode(u'utf-8'))
    md5_bytes = md5.digest()
    aseq_id = _aseq_id_from_md5_bytes(md5_bytes)
    return aseq_id


def clean_sequence(sequence):
    u"""Clean up a sequence.

    This function removes all whitespace characters from sequence and
    replaces all digits or non-word characters with an ampersand
    character (for easy identification of invalid symbols).

    Parameters:
        sequence: sequence character string

    Returns:
        string

    """
    try:
        sequence = re.sub(ur'\s', u'', sequence)
        sequence = re.sub(ur'\W|\d', u'@', sequence)
    except:
        print u'Missing sequence parameter'
    return sequence


def is_valid_aseq_id(aseq_id):
    u"""Return True if aseqId is validly formatted; False otherwise."""
    if aseq_id is None:
        return False
    if re.match(u'[A-Za-z0-9_-]{22}$', aseq_id) is not None:
        return True
    else:
        return False


def is_valid_field_string(fields):
    u"""Check if the requested field string is valid.

    Parameters:
        fields

    Returns:
        boolean
    """
    if not fields:
        return True
    primaries = unicode(fields).split(u',')
    for primary in primaries:
        p = re.match(u'^([A-Za-z_-][A-Za-z0-9-_]*)(?:\(([A-Za-z0-9-_|]+)\))?$',
                     primary)
        if p is None:
            return False
        if p.groups()[1]:
            for sub_field in p.groups()[1].split(u'|'):
                if not sub_field:
                    return False
    return True


def md5_hex_from_aseq_id(aseq_id):
    u"""Convert an aseqId to its equivalent MD5 hexadecimal representation.

    Parameters:
        aseq_id

    Returns:
        MD5 hexadecimal string
    """
    if not aseq_id:
        print u'Missing aseqId parameter'
    if not is_valid_aseq_id(aseq_id):
        print u'Converting invalid Aseq ID: ' + aseq_id
    trans_table = string.maketrans('-_', '+/')
    aseq_id = aseq_id.encode('ascii').translate(trans_table).encode('utf-8')
    aseq_id += u'=' * (24 - len(aseq_id))
    aseq_id_bytes = aseq_id.encode(u'utf-8')
    aseq_id_base64 = base64.decodestring(aseq_id_bytes)
    return binascii.hexlify(aseq_id_base64).decode(u'utf-8')


def md5_hex_from_sequence(sequence):
    u"""Compute the hexadecimal MD5 digest for a given sequence.

    It is recommended that all sequences are cleaned before calling
    this method.

    Parameters:
        sequence

    Returns:
        MD5 hexadecimal string
    """
    if not sequence:
        print u'Missing sequence parameter'
        return None
    md5_sum = hashlib.md5(sequence.encode(u'utf-8'))
    md5_hex = binascii.hexlify(md5_sum.digest())
    return md5_hex.decode(u'utf-8')


class SeqDepot(object):

    u"""A SeqDepot database utility class

    The SeqDepot class facilitates interacting with the public
    SeqDepot database via its RESTful interface. This package also
    provides helper methods such as a FASTA parser routine for working
    with sequences, and methods for manipulating identifiers.
    """

    def __init__(self):
        # Internal string buffer used for reading fasta sequences
        self.fasta_buffer = None
        # Store any error here
        self.last_error = None
        # After querying the REST api for tool info, cache the result
        self.tool_cache = None
        self.tool_position = {}

    def find(self, ids, **kwargs):
        u"""Retrieve fields for aseq_ids from SeqDepot.

        All fields are returned by default; however, a subset may be
        returned by specifying the desired fields (see below).

        Returns a mixed array of hashes or nulls, indicating whether
        the respective requested aseq_id was found. Any nulls in the
        array indicate that the requested Aseq ID was not found - not
        that some other error occurred.

        Parameters:
            ids: single or array of Aseq ID | GI | UniProt ID | PDB ID | MD5 hex

            dictionary: accepts the following fields

            type: <string> type of identifier defaults to aseq_id, but
                may also be gi, uni, pdb, md5_hex

            fields (optional): comma-separated string of primary
                fields, secondary fields must be listed in
                parentheses, separated with pipe (|) symbols, and
                immediately suffix the respective primary field name.
                For example:

                s,l   --> Returns the sequence and length primary fields

                l,t,x --> Returns the length and all tool and cross-references

                l,t(pfam26|smart) --> Returns the length primary field
                    and pfam and smart secondary fields of t

                l,t(pfam26|smart),x(gi) --> Same as the above plus any
                    gi numbers

            label_tool_data: <boolean> defaults to False; if True,
                converts any tool data (the t field) into an array of
                dictionary with meaningful names.

        Returns:
            (null | mixed array of dictionary and nulls): dictionary
                if the given Aseq ID was successfully located or null
                otherwise; null indicates that an error occurred -
                check last_error for details.
        """
        if isinstance(ids, list):
            ids_list = [unicode(i) for i in ids]
        elif isinstance(ids, unicode) or isinstance(ids, int):
            ids_list = [ids]
        else:
            print u'Missing ids parameter or invalid id type (string or list)'
        self._clear_error()
        url = API_URL + u'/aseqs'
        stringy_params = self._url_params(**kwargs)
        url += u'?' + stringy_params
        data = u'\n' + u'\n'.join(ids_list)
        request = urllib2.Request(url, data.encode(u'utf-8'))
        content = self._lwp_response(request).read()
        results = []
        re_iter = re.finditer(ur'(\S.*)', content.decode(u'utf-8'))
        for i in re_iter:
            line = i.groups()[0]
            queryId, code, aseID, json_f = line.split(u'\t')[:4]
            try:
                code = int(code)
            except ValueError:
                code = None
            result = {u'code': code, u'query': queryId}
            if code == 200:
                result[u'data'] = json.loads(json_f)
                if (u'label_tool_data' in kwargs and
                        kwargs[u'label_tool_data'] and
                        u't' in result[u'data']):
                    result[u'data'][u't'] = self._label_tool_data(
                        result[u'data'][u't'])
            results.append(result)
        return results

    def find_one(self, ids, **kwargs):
        u"""Retrieve fields for aseq_id from SeqDepot.

        All fields are returned by default; however, a subset may be
        returned by specifying the desired fields (see find for
        details).

        A null return value indicates that either the aseq_id does not
        exist in SeqDepot or an error occurred. Call last_error() to
        retrieve details about any errors. If the aseq_id does not
        exist, then last_error() will return null.

        Parameters:
            Aseq ID | GI | UniProt ID | PDB ID | MD5 hex
            params (optional, see find documentation)

        Returns:
            Dictionary if successfully found; null if not found or an
            error occurred - call last_error() for details.
        """
        self._clear_error()
        ids = unicode(ids)
        url = API_URL + u'/aseqs/' + ids
        stringyParams = self._url_params(**kwargs)
        url += u'?' + stringyParams
        content = self._lwp_response(url).read()
        result = json.loads(content.decode(u'utf-8'))
        if u'labelTooldata' in kwargs and u't' in result:
            result[u't'] = self._label_tool_data(result[u't'])
        return result

    def is_tool_done(self, tool_id, status):
        u"""Return True if the requested tool has completed.

        The tool is marked as done from the status string. The status
        string corresponds to the _s field in SeqDepot and contains
        information about which predictive self.tool_cache have been
        executed and whether any results were found with this
        tool. See the main documentation for more details.

        Parameters:
            toolId <string>
            status <string>

        Returns:
            boolean

            Null is returned if toolId is not valid.
        """
        if tool_id is None or status is None:
            return False
        self.tool_cache = self.tools()
        if not self.tool_cache:
            print u'Unable to fetch tool metadata from SeqDepot: {0}'.format(
                self.last_error)
        if tool_id in self.tool_position:
            pos = self.tool_position[tool_id]
        else:
            print u"ToolId not recognized"
            return False
        try:
            if status[pos] != u'-':
                return True
        except:
            return False
        return False

    def read_fasta_sequence(self, fh):
        u"""Read a FASTA-formatted sequence from an open file handle.

        An array containing the header and the cleaned sequence is
        returned. The header will not contain the > symbol. Returns
        null if there are no more sequences to be read from the file.

        Whitespace is trimmed from both ends of the header line.

        Parameters:
            fh: non-null open filehandle

        Return:
            Array containing the header and cleaned sequence if a sequence was
            read; None otherwise
        """
        line = self.fasta_buffer if self.fasta_buffer else fh.readline()
        self.fasta_buffer = None
        while line:
            if re.match(u'^\s*$', line):
                line = fh.readline()
                continue
            if line[0] != u'>':
                raise Exception(
                    u'Invalid FASTA file. Header line must begin with a ' +
                    u'greater than symbol\nLine: {0}'.format(line))
            line = re.sub(u'\s+$', u'', line)
            header = line[1:]
            header = re.sub(u'^\s+', u'', header)
            sequence = u''
            line = fh.readline()
            while line:
                if line[0] != u'>':
                    sequence += line
                    line = fh.readline()
                    continue
            # We got the next header line. Save it for the next call
            # to this method.
                self.fasta_buffer = line
                break
            sequence = clean_sequence(sequence)
            return [header, sequence]
        return None

    def save_image(self, idss, file_name=None, **kwargs):
        u"""Save an image of the corresponding aseq.

        Parameters:
            id: <string|number> Aseq ID | GI | UniProt ID | PDB ID | MD5 hex
            fileName: <string> optional; defaults to the id with the
                appropriate image extension
            params: <dictionary>
            fields => <string> see find documentation
            type => type of id (aseq_id | gi | uni | pdb | md5_hex)
            format => png | svg: type of image to save; defaults to png
        """
        try:
            ids = unicode(idss)
        except:
            return None
        url = API_URL + u'/aseqs/' + ids
        format_s = u'png'
        self._clear_error()
        if len(kwargs) == 1 and u'format' in kwargs:
            if kwargs[u'format'] == u'svg':
                format_s = u'svg'
        url += u'.' + format_s
        stringy_params = self._url_params(**kwargs)
        url += u'?' + stringy_params
        if file_name is None:
            fileName = ids + u'.' + format_s
        response = self._lwp_response(url)
        if response:
            if format_s == u'png':
                output = open(fileName, u'wb')
            else:
                output = open(fileName, u'w')
            output.write(response.read())
            output.close()
            return True
        else:
            return None

    def tool_fields(self, tool_name):
        u"""Return the field names associated with toolName.

        Parameters:
            toolName: string of toolname

        Returns:
            array of strings (empty array if toolName is not valid) OR
            None if an error occurred.
        """
        self.tool_cache = self.tools()
        if self.tool_cache and tool_name in self.tool_cache:
            if self.tool_cache[tool_name][u'f']:
                return self.tool_cache[tool_name][u'f']
            else:
                return None
        else:
            return None

    def tools(self):
        u"""Return dictionary of predictive tool_cache available at SeqDepot."""
        if self.tool_cache is not None:
            return self.tool_cache
        else:
            content = self._lwp_response(API_URL + u'/tools.json').read()
        ordered_tools = json.loads(content.decode(u'utf-8'))[u'results']
        # Create a tool position lookup
        for i in xrange(len(ordered_tools)):
            idt = ordered_tools[i][u'id']
            self.tool_position[idt] = i
        myhash = dict((i[u'id'], i) for i in ordered_tools)
        return myhash

    def tool_names(self):
        u"""Return an array of tool names used by SeqDepot."""
        return list(self.tools().keys())

    # Private Methods:

    def _lwp(self):
        return

    def _clear_error(self):
        self.last_error = None

    def _url_params(self, **kwargs):
        # suggestion: Since there are only few valid type, why not
        # check prior to url submition?
        par_list = []
        if u'fields' in kwargs:
            if is_valid_field_string(kwargs[u'fields']):
                par_list.append(u'fields='+kwargs[u'fields'])
            else:
                print u'Invalid fields parameter'
        if u'type' not in kwargs:
            kwargs[u'type'] = u'aseq_id'
        par_list.append(u'type='+kwargs[u'type'])
        return u'&'.join(par_list)

    def _label_tool_data(self, t):
        result = {}
        for tool_id in t:
            rows = t[tool_id]
            if not isinstance(rows, list):
                result[tool_id] = rows
                continue
            field_names = self.tool_fields(tool_id)
            hashes = []
            for row in rows:
                myhash = {}
                for i, datum in enumerate(row):
                    myhash[field_names[i]] = datum
                hashes.append(myhash)
            result[tool_id] = hashes
        return result

    def _lwp_response(self, request):
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            print ' '.join([u'\n\nUnable to connect to server;',
                            u'timeout or other internal error'])
            error = json.loads(e.read().decode(u'utf-8'))
            self.last_error = error[u'message']
            return None
        return response
