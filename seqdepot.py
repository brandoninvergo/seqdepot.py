import json
import hashlib
import base64
import re
import binascii
import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse


API_URL = 'http://seqdepot.net/api/v1'
VERSION = '0.01'


def _aseq_id_from_base64(bytes64):
    """Convert a base 64 bytes object to an aseq ID."""

    trans_table = bytes64.maketrans('/+ ', '_-')
    aseq_id = bytes64.translate(trans_table, b'=\n')
    return aseq_id


def aseq_id_from_md5_hex(md5_hex):
    """Convert an MD5 hexadecimal string into its aseqId equivalent.

    Parameters:
        MD5hex: hexadecimal MD5 string

    Return:
        aseqId
    """
    md5_bytes = binascii.unhexlify(md5_hex)
    md5_bytes64 = base64.encodebytes(md5_bytes)
    return _aseq_id_from_base64(md5_bytes64)


def aseq_id_from_sequence(sequence):
    """Compute the aseqId for a given sequence.

    It is recommended that all sequences are cleaned before calling
    this method.

    Parameters:
        sequence

    Returns:
        aseqId
    """
    md5sum = hashlib.md5(sequence.translate(None, '-'))
    md5_bytes64 = base64.encodebytes(md5sum.digest())
    return _aseq_id_from_base64(md5_bytes64)


def clean_sequence(sequence):
    """Clean up a sequence.

    This function removes all whitespace characters from sequence and
    replaces all digits or non-word characters with an ampersand
    character (for easy identification of invalid symbols).

    Parameters:
        sequence: sequence character string

    Returns:
        string

    """
    try:
        sequence = re.sub(r'\s', '', sequence)
        sequence = re.sub(r'\W|\d', '@', sequence)
    except:
        print('Missing sequence parameter')
    return sequence


def is_valid_aseq_id(aseq_id=None):
    """Return True if aseqId is validly formatted; False otherwise."""
    if aseq_id is None:
        return False
    if re.match('[A-Za-z0-9_-]{22}$', aseq_id) is not None:
        return True
    else:
        return False


def is_valid_field_string(fields=None):
    """Check if the requested field string is valid.

    Parameters:
        fields

    Returns:
        boolean
    """
    if not fields:
        return True
    primaries = str(fields).split(',')
    for primary in primaries:
        p = re.match('^([A-Za-z_-][A-Za-z0-9-_]*)(?:\(([A-Za-z0-9-_|]+)\))?$',
                     primary)
        if p is None:
            return False
        if p.groups()[1]:
            for sub_field in p.groups()[1].split('|'):
                if not sub_field:
                    return False
    return True


def md5_hex_from_aseq_id(aseq_id=''):
    """Convert an aseqId to its equivalent MD5 hexadecimal representation.

    Parameters:
        aseq_id

    Returns:
        MD5 hexadecimal string
    """
    if not aseq_id:
        print('Missing aseqId parameter')

    if not is_valid_aseq_id(aseq_id):
        print('Converting invalid Aseq ID: ' + aseq_id)
    trans_table = aseq_id.maketrans('-_', '+/')
    aseq_id = aseq_id.translate(trans_table)
    aseq_id += '=' * (24 - len(aseq_id))
    aseq_id_bytes = aseq_id.encode('utf-8')
    aseq_id_base64 = base64.decodebytes(aseq_id_bytes)
    return binascii.hexlify(aseq_id_base64).decode('utf-8')


def md5_hex_from_sequence(sequence=''):
    """Compute the hexadecimal MD5 digest for a given sequence.

    It is recommended that all sequences are cleaned before calling
    this method.

    Parameters:
        sequence

    Returns:
        MD5 hexadecimal string
    """
    if not sequence:
        print('Missing sequence parameter')
        return None
    md5_sum = hashlib.md5(sequence.encode('utf-8'))
    md5_hex = binascii.hexlify(md5_sum.digest())
    return md5_hex.decode('utf-8')


class new(object):

    """A SeqDepot database utility class

    The SeqDepot class facilitates interacting with the public
    SeqDepot database via its RESTful interface. This package also
    provides helper methods such as a FASTA parser routine for working
    with sequences, and methods for manipulating identifiers.
    """

    def __init__(self):
        # Internal string buffer used for reading fasta sequences
        self.fastaBuffer = None
        # Store any error here
        self.lastError = None
        # After querying the REST api for tool info, cache the result
        self.toolCache = None

        self.toolPosition = {}

    def find(self, ids, params={}):
        """Retrieve fields for aseq_ids from SeqDepot.

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

            labelToolData: <boolean> defaults to False; if True,
                converts any tool data (the t field) into an array of
                dictionary with meaningful names.

        Returns:
            (null | mixed array of dictionary and nulls): dictionary
                if the given Aseq ID was successfully located or null
                otherwise; null indicates that an error occurred -
                call lastError() for details.
        """
        if ids.__class__ == list:
            ids_list = [str(i) for i in ids]
        elif ids.__class__ == str or ids.__class__ == int:
            ids_list = [ids]
        else:
            print('Missing ids parameter or invalid id type (string or list)')

        self.clearError_()

        url = API_URL + '/aseqs'
        stringyParams = self.urlParams_(params)

        url += '?' + stringyParams
        data = '\n' + '\n'.join(ids_list)
        request = urllib.request.Request(url, data.encode('utf-8'))
        content = self.lwpResponse(request).read()

        results = []
        re_iter = re.finditer(r'(\S.*)', content.decode('utf-8'))
        for i in re_iter:
            line = i.groups()[0]
            queryId, code, aseID, json_f = line.split('\t')[:4]
            try:
                code = int(code)
            except ValueError:
                code = None
            result = {'code': code, 'query': queryId}
            if code == 200:
                result['data'] = json.loads(json_f)
                if ('labelTooldata' in list(params.keys()) and
                        't' in list(result['data'].keys())):
                    result['data']['t'] = self._label_tool_data(
                        result['data']['t'])
            results.append(result)
        return results

    def find_one(self, ids, params={}):
        """Retrieve fields for aseq_id from SeqDepot.

        All fields are returned by default; however, a subset may be
        returned by specifying the desired fields (see find for
        details).

        A null return value indicates that either the aseq_id does not
        exist in SeqDepot or an error occurred. Call lastError() to
        retrieve details about any errors. If the aseq_id does not
        exist, then lastError() will return null.

        Parameters:
            Aseq ID | GI | UniProt ID | PDB ID | MD5 hex
            params (optional, see find documentation)

        Returns:
            Dictionary if successfully found; null if not found or an
            error occurred - call lastError() for details.
        """
        self.clearError_()
        ids = str(ids)
        url = API_URL + '/aseqs/' + ids
        stringyParams = self.urlParams_(params)
        url += '?' + stringyParams
        content = self.lwpResponse(url).read()
        result = json.loads(content.decode('utf-8'))
        if ('labelTooldata' in list(params.keys()) and
                't' in list(result.keys())):
            result['t'] = self.labelToolData_(result['t'])
        return result

    def is_tool_done(self, toolId=None, status=None):
        """Return True if the requested tool has completed.

        The tool is marked as done from the status string. The status
        string corresponds to the _s field in SeqDepot and contains
        information about which predictive self.toolCache have been
        executed and whether any results were found with this
        tool. See the main documentation for more details.

        Parameters:
            toolId <string>
            status <string>

        Returns:
            boolean

            Null is returned if toolId is not valid.
        """
        if toolId is None:
            return False
        if status is None:
            return False

        tools = self.tools()
        if not self.toolCache:
            print('Unable to fetch tool metadata from SeqDepot: {0}'.format(
                self.lastError);

#############PATCH - Handling wrong ToolID ##########################
        if toolId in list(self.toolPosition.keys()):
            pos = self.toolPosition[toolId]
        else:
            print("ToolId not recognized")
            return False
#################END PATCH ##########################################
#################ORIGINAL############################################
#        pos = self.toolPosition[toolId]
#####################################################################
        if pos.__class__ is int:
            if pos < len(status):
                if status[pos] != '-':
                    return True
        return False

    def prime_fasta_buffer(self, buffer):
        """Set the internal fastaBuffer to the argument, fastaBuffer.

        This is useful when an input stream has already been partially
        read but not processed as part of the FASTA parsing. For
        example, when reading a line from STDIN to determine if it is
        FASTA data.

        Parameters:
            fastaBuffer: <string>
        """
        self.fastaBuffer = buffer

    def read_fasta_sequence(self, fh):
        """Read a FASTA-formatted sequence from an open file handle.

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
        line = self.fastaBuffer if self.fastaBuffer else fh.readline()
        self.fastaBuffer = None
        while line:
            if re.match('^\s*$', line):
                line = fh.readline()
                continue

            if line[0] != '>':
                raise Exception(
                    'Invalid FASTA file. Header line must begin with a ' +
                    'greater than symbol\nLine: {0}'.format(line))

            line = re.sub('\s+$', '', line)
            header = line[1:]
            header = re.sub('^\s+', '', header)#.decode('string_escape')
            sequence = ''
            line = fh.readline()
            while line:
                if line[0] != '>':
                    sequence += line
                    line = fh.readline()
                    continue

            # We got the next header line. Save it for the next call
            # to this method.
                self.fastaBuffer = line
                break

            sequence = clean_sequence(sequence)
            return [header, sequence]

        return None

    def reset_fasta_buffer(self):
        """Clear the internal buffer used to read FASTA sequences.

        Call this method before read_fasta_sequence if all of the
        following are true:
            1) changing filehandles
            2) the filehandle has been partially read from
            3) the filehandle has not been completely read through to the end
        """
        self.fastaBuffer = None

    def save_image(self, idss = '', fileName = None, params = {}):
        """Save an image of the corresponding aseq.

        Parameters:
            id: <string|number> Aseq ID | GI | UniProt ID | PDB ID | MD5 hex
            fileName: <string> optional; defaults to the id with the
                appropriate image extension
            params: <dictionary>
            fields => <string> see find documentation
            type => type of id (aseq_id | gi | uni | pdb | md5_hex)
            format => png | svg: type of image to save; defaults to png
        """
        ids = str(idss)
        url = API_URL + '/aseqs/' + ids
        format_s = 'png'
        self.clearError_()
        if params != {}:
            if list(params.keys()) == ['format']:
                if params['format'] == 'svg':
                    format_s = 'svg'
        url += '.' + format_s
        stringyParams = self.urlParams_(params)
        url += '?' + stringyParams
        if fileName is None:
            fileName = ids + '.' + format_s
        response = self.lwpResponse(url)
        if response:
            if format_s == 'png':
                output = open(fileName,'wb')
            else:
                output = open(fileName,'w')
            output.write(response.read())
            output.close()
            return 1
        else:
            return None

    def tool_fields(self, toolName):
        """Return the field names associated with toolName.

        Parameters:
            toolName: string of toolname

        Returns:
            array of strings (empty array if toolName is not valid) OR
            None if an error occurred.
        """
        self.toolCache = self.tools()
        if self.toolCache and toolName in list(self.toolCache.keys()):
            if self.toolCache[toolName]['f']:
                return self.toolCache[toolName]['f']
            else:
                return None
        else:
            return None

    def tools(self):
        """Return dictionary of predictive toolCache available at SeqDepot."""
        if self.toolCache != None:
            return self.toolCache
        else:
            content = self.lwpResponse(API_URL + '/tools.json').read()

        orderedTools = json.loads(content.decode('utf-8'))['results']

        # Create a tool position lookup
        for i in range(len(orderedTools)):
            idt = orderedTools[i]['id']
            self.toolPosition[idt] = i
        myhash = { i['id']:i for i in orderedTools}
        self.toolCache = myhash
        return self.toolCache

    def tool_names(self):
        """Return an array of tool names used by SeqDepot."""
        return list(self.tools().keys())

    # Private Methods:

    def _lwp(self):
        return

    def _clear_error(self):
        self.lastError = None

    def _url_params(self, params = {}):
        #suggestion: Since there are only few valid type, why not
        #check prior to url submition?
        par_list = []
        if 'fields' in list(params.keys()):
            if is_valid_field_string(params['fields']):
                par_list.append('fields=' + params['fields'])
            else:
                print('Invalid fields parameter')

        if 'type' not in list(params.keys()):
            params['type'] = 'aseq_id'

        par_list.append('type='+params['type'])
        return '&'.join(par_list)

    def _label_tool_data(self,t={}):
        result = {}
        for toolId in list(t.keys()):
            rows = t[toolId]
            if rows.__class__ != list:
                result[toolId] = rows
                continue

            fieldNames = self.tool_fields(toolId)
            hashes = []
            for i in rows:
                myhash = {}
                myhash[fieldNames] = row
                hashes.append(myhash)
            result[toolId] = hashes
        return result

    def _lwp_response(self,request=None):
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            print('\n\nUnable to connect to server; ' +
                  'timeout or other internal error')
            error = json.loads(e.read().decode('utf-8'))
            self.lastError = error['message']
            return None
        return response

"""AUTHOR

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
