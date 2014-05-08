#!/usr/bin/python
# This file was derived from automatically generated code using the
# 3to2 script: http://pypi.python.org/pypi/3to2/
import seqdepot_p2
import unittest
import io
import os


class SeqDepotTestCase(unittest.TestCase):
    def test_aseq_id_from_md5_hex(self):
        fixtures = [
            [u'yg8A8H8N-4x1Ezf8WW-YbA', u'ca0f00f07f0dfb8c751337fc596f986c'],
            [u'naytI0dLM_rK2kaC1m3ZSQ', u'9dacad23474b33facada4682d66dd949'],
            [u'GS8z3QwN5MzpxU0aTuxuaA', u'192f33dd0c0de4cce9c54d1a4eec6e68']]
        for fixture in fixtures:
            aseq_id, md5_hex = fixture
            actual = seqdepot_p2.aseq_id_from_md5_hex(md5_hex)
            self.assertEqual(aseq_id, actual)
            # upper-case
            actual = seqdepot_p2.aseq_id_from_md5_hex(md5_hex.upper())
            self.assertEqual(aseq_id, actual)

    def test_aseq_id_from_sequence(self):
        fixtures = [
            [u'yg8A8H8N-4x1Ezf8WW-YbA',
             u'MTNVLIVEDEQAIRRFLRTALEGDGMRVFEAETLQRGLLEAATRKPDLIILDLGLPDGDGI' +
             u'EFIRDLRQWSAVPVIVLSARSEESDKIAALDAGADDYLSKPFGIGELQARLRVALRRHSAT' +
             u'TAPDPLVKFSDVTVDLAARVIHRGEEEVHLTPIEFRLLAVLLNNAGKVLTQRQLLNQVWGP' +
             u'NAVEHSHYLRIYMGHLRQKLEQDPARPRHFITETGIGYRFML'],
            [u'naytI0dLM_rK2kaC1m3ZSQ',
             u'MNNEPLRPDPDRLLEQTAAPHRGKLKVFFGACAGVGKTWAMLAEAQRLRAQGLDIVVGVVE' +
             u'THGRKDTAAMLEGLAVLPLKRQAYRGRHISEFDLDAALARRPALILMDELAHSNAPGSRHP' +
             u'KRWQDIEELLEAGIDVFTTVNVQHLESLNDVVSGVTGIQVRETVPDPFFDAADDVVLVDLP' +
             u'PDDLRQRLKEGKVYIAGQAERAIEHFFRKGNLIALRELALRRTADRVDEQMRAWRGHPGEE' +
             u'KVWHTRDAILLCIGHNTGSEKLVRAAARLASRLGSVWHAVYVETPALHRLPEKKRRAILSA' +
             u'LRLAQELGAETATLSDPAEEKAVVRYAREHNLGKIILGRPASRRWWRRETFADRLARIAPD' +
             u'LDQVLVALDEPPARTINNAPDNRSFKDKWRVQIQGCVVAAALCAVITLIAMQWLMAFDAAN' +
             u'LVMLYLLGVVVVALFYGRWPSVVATVINVVSFDLFFIAPRGTLAVSDVQYLLTFAVMLTVG' +
             u'LVIGNLTAGVRYQARVARYREQRTRHLYEMSKALAVGRSPQDIAATSEQFIASTFHARSQV' +
             u'LLPDDNGKLQPLTHPQGMTPWDDAIAQWSFDKGLPAGAGTDTLPGVPYQILPLKSGEKTYG' +
             u'LVVVEPGNLRQLMIPEQQRLLETFTLLVANALERLTLTASEEQARMASEREQIRNALLAAL' +
             u'SHDLRTPLTVLFGQAEILTLDLASEGSPHARQASEIRQHVLNTTRLVNNLLDMARIQSGGF' +
             u'NLKKEWLTLEEVVGSALQMLEPGLSSPINLSLPEPLTLIHVDGPLFERVLINLLENAVKYA' +
             u'GAQAEIGIDAHVEGENLQLDVWDNGPGLPPGQEQTIFDKFARGNKESAVPGVGLGLAICRA' +
             u'IVDVHGGTITAFNRPEGGACFRVTLPQQTAPELEEFHEDM'],
            [u'GS8z3QwN5MzpxU0aTuxuaA',
             u'MSGLRPALSTFIFLLLITGGVYPLLTTVLGQWWFPWQANGSLIREGDTVRGSALIGQNFTG' +
             u'NGYFHGRPSATAEMPYNPQASGGSNLAVSNPELDKLIAARVAALRAANPDASASVPVELVT' +
             u'ASASGLDNNITPQAAAWQIPRVAKARNLSVEQLTQLIAKYSQQPLVKYIGQPVVNIVELNL' +
             u'ALDKLDE']]
        for fixture in fixtures:
            aseq_id, sequence = fixture
            actual = seqdepot_p2.aseq_id_from_sequence(sequence)
            self.assertEqual(aseq_id, actual)

    def test_clean_sequence(self):
        fixtures = [
            [u'', u''],
            [u'ABC', u'A B C'],
            [u'abc', u'a b c'],
            [u'ABC', u' ABC '],
            [u'ABC', u"\n\r\t\f     ABC"],
            [u'A@B@C', u"A9B#C"]]
        for fixture in fixtures:
            expect, inp = fixture
            actual = seqdepot_p2.clean_sequence(inp)
            self.assertEqual(expect, actual)

    def test_find(self):
        sd = seqdepot_p2.SeqDepot()
        results = sd.find([u'naytI0dLM_rK2kaC1m3ZSQ',
                           u'GS8z3QwN5MzpxU0aTuxuaA'])
        self.assertEqual(2, len(results))
        self.assertEqual(894, results[0][u'data'][u'l'])
        results = sd.find(u'naytI0dLM_rK2kaC1m3ZSQ', label_tool_data=True)
        self.assertIn(u'acc', results[0][u'data'][u't'][u'pfam27'][0])

    def test_find_one(self):
        sd = seqdepot_p2.SeqDepot()
        ids = u'naytI0dLM_rK2kaC1m3ZSQ'
        seq = (u'MNNEPLRPDPDRLLEQTAAPHRGKLKVFFGACAGVGKTWAMLAEAQRLRAQGLDIVVGV' +
               u'VETHGRKDTAAMLEGLAVLPLKRQAYRGRHISEFDLDAALARRPALILMDELAHSNAPG' +
               u'SRHPKRWQDIEELLEAGIDVFTTVNVQHLESLNDVVSGVTGIQVRETVPDPFFDAADDV' +
               u'VLVDLPPDDLRQRLKEGKVYIAGQAERAIEHFFRKGNLIALRELALRRTADRVDEQMRA' +
               u'WRGHPGEEKVWHTRDAILLCIGHNTGSEKLVRAAARLASRLGSVWHAVYVETPALHRLP' +
               u'EKKRRAILSALRLAQELGAETATLSDPAEEKAVVRYAREHNLGKIILGRPASRRWWRRE' +
               u'TFADRLARIAPDLDQVLVALDEPPARTINNAPDNRSFKDKWRVQIQGCVVAAALCAVIT' +
               u'LIAMQWLMAFDAANLVMLYLLGVVVVALFYGRWPSVVATVINVVSFDLFFIAPRGTLAV' +
               u'SDVQYLLTFAVMLTVGLVIGNLTAGVRYQARVARYREQRTRHLYEMSKALAVGRSPQDI' +
               u'AATSEQFIASTFHARSQVLLPDDNGKLQPLTHPQGMTPWDDAIAQWSFDKGLPAGAGTD' +
               u'TLPGVPYQILPLKSGEKTYGLVVVEPGNLRQLMIPEQQRLLETFTLLVANALERLTLTA' +
               u'SEEQARMASEREQIRNALLAALSHDLRTPLTVLFGQAEILTLDLASEGSPHARQASEIR' +
               u'QHVLNTTRLVNNLLDMARIQSGGFNLKKEWLTLEEVVGSALQMLEPGLSSPINLSLPEP' +
               u'LTLIHVDGPLFERVLINLLENAVKYAGAQAEIGIDAHVEGENLQLDVWDNGPGLPPGQE' +
               u'QTIFDKFARGNKESAVPGVGLGLAICRAIVDVHGGTITAFNRPEGGACFRVTLPQQTAP' +
               u'ELEEFHEDM')
        obj = sd.find_one(ids, fields=u's,l')
        self.assertEqual(len(seq), obj[u'l'])
        self.assertEqual(ids, obj[u'id'])
        self.assertEqual(seq, obj[u's'])
        obj = sd.find_one(ids)
        self.assertEqual(len(seq), obj[u'l'])
        self.assertEqual(ids, obj[u'id'])
        self.assertEqual(seq, obj[u's'])
        # Attempt to get gis
        obj = sd.find_one(ids, fields=u'x(gi)')
        self.assertIn(u'gi', obj[u'x'])
        self.assertTrue(len(obj[u'x'][u'gi']) > 0)
        # Search via GI, PDB, UniProt, and MD5_Hex
        fixtures = {u'gi': 1651302, u'uni': u'B1X6M6_ECODH',
                    u'md5_hex': u'9dacad23474b33facada4682d66dd949'}
        for fixture in fixtures:
            obj = sd.find_one(fixtures[fixture], fields=u'l', type=fixture)
            self.assertIsNotNone(obj)
            self.assertEqual(len(seq), obj[u'l'])
            self.assertEqual(ids, obj[u'id'])
        # now by pdb
        obj = sd.find_one(u'4dpk', fields=u'l', type=u'pdb')
        self.assertIsNotNone(obj)
        self.assertEqual(359, obj[u'l'])
        self.assertEqual(u'-0tNbPaXZtNA2gGW668Kqg', obj[u'id'])

    def test_is_tool_done(self):
        sd = seqdepot_p2.SeqDepot()
        fixtures = [
            [False, u'', u''],
            [False, u'bob', u''],
            [False, None, None],
            [False, u'pfam26', None],
            [False, None, u'TTT'],
            [True, u'agfam1', u'T'],
            [True, u'agfam1', u'd'],
            [False, u'agfam1', u'-'],
            [False, u'ecf', u'TTT'],
            [True, u'ecf', u'TTdT'],
            [True, u'ecf', u'TTdd'],
            [True, u'ecf', u'TTdd-'],
            [True, u'ecf', u'TTdd-T'],
            [False, u'tigrfam', u'------------------'],
            [True, u'tigrfam', u'-----------------T']]
        for fixture in fixtures:
            expect, tool_id, status = fixture
            if expect:
                self.assertTrue(sd.is_tool_done(tool_id, status),
                                msg=u"{0} - {1}".format(tool_id, status))
            else:
                self.assertFalse(sd.is_tool_done(tool_id, status),
                                 msg=u"{0} - {1}".format(tool_id, status))

    def test_is_valid_aseq_id(self):
        fixtures = [
            [True, u'yg8A8H8N-4x1Ezf8WW-YbA'],
            [False, u'yg8A8H8N-4x1Ezf8WW-Yb'],
            [False, u'yg8A8H8N-4x1Ezf8WW-YbAA'],
            [False, None],
            [False, u''],
            [False, u'yg8A8H8N-4x1Ezf8WW-Yb@']]
        for fixture in fixtures:
            expect, inp = fixture
            actual = seqdepot_p2.is_valid_aseq_id(inp)
            if expect:
                self.assertTrue(actual)
            else:
                self.assertFalse(actual)

    def test_is_valid_field_string(self):
        fixtures = [
            [True, u''],
            [True, None],
            [True, u's'],
            [True, u'l'],
            [False, u'@'],
            [False, u'_!@#$'],
            [False, u'1234567'],
            [False, u'1A'],
            [True, u'A1'],
            [True, u's,l'],
            [True, u's(l)'],
            [False, u's()'],
            [True, u's(l),s(l)'],
            [True, u'a,b(c|d|e)'],
            [True, u'a,b(c),d(e|f)'],
            [False, u'a,b(c),d(e|@)'],
            [False, u'a,b(c),d(@|f)'],
            [False, u'a,b(@),d(e|f)'],
            [False, u'a,b(c),d( |f)'],
            [False, u' s']]
        for fixture in fixtures:
            expect, inp = fixture
            actual = seqdepot_p2.is_valid_field_string(inp)
            if expect:
                self.assertTrue(actual)
            else:
                self.assertFalse(actual)

    def test_md5_hex_from_aseq_id(self):
        fixtures = [
            [u'ca0f00f07f0dfb8c751337fc596f986c', u'yg8A8H8N-4x1Ezf8WW-YbA'],
            [u'9dacad23474b33facada4682d66dd949', u'naytI0dLM_rK2kaC1m3ZSQ'],
            [u'192f33dd0c0de4cce9c54d1a4eec6e68', u'GS8z3QwN5MzpxU0aTuxuaA']]
        for fixture in fixtures:
            md5_hex, aseq_id = fixture
            actual = seqdepot_p2.md5_hex_from_aseq_id(aseq_id)
            self.assertEqual(md5_hex, actual)

    def test_md5_hex_from_sequence(self):
        fixtures = [
            [u'ca0f00f07f0dfb8c751337fc596f986c',
             u'MTNVLIVEDEQAIRRFLRTALEGDGMRVFEAETLQRGLLEAATRKPDLIILDLGLPDGDGI' +
             u'EFIRDLRQWSAVPVIVLSARSEESDKIAALDAGADDYLSKPFGIGELQARLRVALRRHSAT' +
             u'TAPDPLVKFSDVTVDLAARVIHRGEEEVHLTPIEFRLLAVLLNNAGKVLTQRQLLNQVWGP' +
             u'NAVEHSHYLRIYMGHLRQKLEQDPARPRHFITETGIGYRFML'],
            [u'9dacad23474b33facada4682d66dd949',
             u'MNNEPLRPDPDRLLEQTAAPHRGKLKVFFGACAGVGKTWAMLAEAQRLRAQGLDIVVGVVE' +
             u'THGRKDTAAMLEGLAVLPLKRQAYRGRHISEFDLDAALARRPALILMDELAHSNAPGSRHP' +
             u'KRWQDIEELLEAGIDVFTTVNVQHLESLNDVVSGVTGIQVRETVPDPFFDAADDVVLVDLP' +
             u'PDDLRQRLKEGKVYIAGQAERAIEHFFRKGNLIALRELALRRTADRVDEQMRAWRGHPGEE' +
             u'KVWHTRDAILLCIGHNTGSEKLVRAAARLASRLGSVWHAVYVETPALHRLPEKKRRAILSA' +
             u'LRLAQELGAETATLSDPAEEKAVVRYAREHNLGKIILGRPASRRWWRRETFADRLARIAPD' +
             u'LDQVLVALDEPPARTINNAPDNRSFKDKWRVQIQGCVVAAALCAVITLIAMQWLMAFDAAN' +
             u'LVMLYLLGVVVVALFYGRWPSVVATVINVVSFDLFFIAPRGTLAVSDVQYLLTFAVMLTVG' +
             u'LVIGNLTAGVRYQARVARYREQRTRHLYEMSKALAVGRSPQDIAATSEQFIASTFHARSQV' +
             u'LLPDDNGKLQPLTHPQGMTPWDDAIAQWSFDKGLPAGAGTDTLPGVPYQILPLKSGEKTYG' +
             u'LVVVEPGNLRQLMIPEQQRLLETFTLLVANALERLTLTASEEQARMASEREQIRNALLAAL' +
             u'SHDLRTPLTVLFGQAEILTLDLASEGSPHARQASEIRQHVLNTTRLVNNLLDMARIQSGGF' +
             u'NLKKEWLTLEEVVGSALQMLEPGLSSPINLSLPEPLTLIHVDGPLFERVLINLLENAVKYA' +
             u'GAQAEIGIDAHVEGENLQLDVWDNGPGLPPGQEQTIFDKFARGNKESAVPGVGLGLAICRA' +
             u'IVDVHGGTITAFNRPEGGACFRVTLPQQTAPELEEFHEDM'],
            [u'192f33dd0c0de4cce9c54d1a4eec6e68',
             u'MSGLRPALSTFIFLLLITGGVYPLLTTVLGQWWFPWQANGSLIREGDTVRGSALIGQNFTG' +
             u'NGYFHGRPSATAEMPYNPQASGGSNLAVSNPELDKLIAARVAALRAANPDASASVPVELVT' +
             u'ASASGLDNNITPQAAAWQIPRVAKARNLSVEQLTQLIAKYSQQPLVKYIGQPVVNIVELNL' +
             u'ALDKLDE']]
        for fixture in fixtures:
            md5_hex, sequence = fixture
            actual = seqdepot_p2.md5_hex_from_sequence(sequence)
            self.assertEqual(md5_hex, actual)

    def test_read_fasta_sequence(self):
        fixtures = [
            [u""">""", [[u'', u'']]],
            [u""">1""", [[u'1', u'']]],
            [u""">1\n""", [[u'1', u'']]],
            [u""">1\nA""", [[u'1', u'A']]],
            [u""">1\nAB""", [[u'1', u'AB']]],
            [u""">1\nAB\n""", [[u'1', u'AB']]],
            [u""">1\nAB\nC""", [[u'1', u'ABC']]],
            [u""">1\nAB\nCD\n""", [[u'1', u'ABCD']]],
            [u""">1\nA\n>""", [[u'1', u'A'], [u'', u'']]],
            [u""">1\nA\n>2""", [[u'1', u'A'], [u'2', u'']]],
            [u""">1\nA\n>2\n""", [[u'1', u'A'], [u'2', u'']]],
            [u""">1\nA\n>2\nA""", [[u'1', u'A'], [u'2', u'A']]],
            [u""">1\nA\n>2\nB\n""", [[u'1', u'A'], [u'2', u'B']]],
            [u""">1\nA\n>2\nB\n>""", [[u'1', u'A'], [u'2', u'B'], [u'', u'']]],
            # Trim leading and trailing whitespace
            [u"""> 1 \nA\n""", [[u'1', u'A']]],
            # Invalid symbols
            [u""">!@#$\n12345678900""", [[u'!@#$', u'@@@@@@@@@@@']]],
            # Skip empty lines
            [u"""\n\n>1\nAB\n\n\tCD\n\n>2\n\nEF""", [[u'1', u'ABCD'],
                                                     [u'2', u'EF']]],
            [u""">Ecoli CheY\r\nABCDEF\r\n>Ecoli CheA\r\nGHI\r\nJKL\r\n""",
             [[u'Ecoli CheY', u'ABCDEF'], [u'Ecoli CheA', u'GHIJKL']]]]
        for fixture in fixtures:
            sd = seqdepot_p2.SeqDepot()
            fasta, expect = fixture
            actual = []
            fh = io.StringIO(fasta)
            seq = sd.read_fasta_sequence(fh)
            while seq:
                actual.append(seq)
                seq = sd.read_fasta_sequence(fh)
            self.assertEqual(len(expect), len(actual))
            for i in xrange(len(expect)):
                self.assertEqual(expect[i][0], actual[i][0])
                self.assertEqual(expect[i][1], actual[i][1])

    def test_save_image(self):
        sd = seqdepot_p2.SeqDepot()
        self.assertTrue(sd.save_image(3355692, None, type=u'gi'))
        self.assertTrue(os.path.isfile(u'3355692.png'))
        self.assertTrue(os.path.getsize(u'3355692.png') > 24)
        os.remove(u'3355692.png')

    def test_tool_fields(self):
        sd = seqdepot_p2.SeqDepot()
        self.assertIsNone(sd.tool_fields(u'bob'))
        self.assertIsNotNone(sd.tool_fields(u'das'))
        names = sd.tool_fields(u'das')
        self.assertEqual(5, len(names))
        self.assertEqual(u'start', names[0])
        self.assertEqual(u'stop', names[1])
        self.assertEqual(u'peak', names[2])
        self.assertEqual(u'peak_score', names[3])
        self.assertEqual(u'evalue', names[4])

    def test_tool_names(self):
        sd = seqdepot_p2.SeqDepot()
        tool_names = sd.tool_names()
        checks = {}
        for name in tool_names:
            checks[name] = 1
        self.assertIn(u'das', checks)
        self.assertIn(u'tigrfam', checks)

    def test_tools(self):
        sd = seqdepot_p2.SeqDepot()
        tools = sd.tools()
        self.assertIn(u'das', tools)
        self.assertIn(u'ecf', tools)


if __name__ == u'__main__':
    unittest.main()
