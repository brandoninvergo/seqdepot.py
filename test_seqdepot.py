#!/usr/bin/python

import seqdepot
import unittest
import io
import os


class SeqDepotTestCase(unittest.TestCase):
    def test_aseq_id_from_md5_hex(self):
        fixtures = [
            ['yg8A8H8N-4x1Ezf8WW-YbA', 'ca0f00f07f0dfb8c751337fc596f986c'],
            ['naytI0dLM_rK2kaC1m3ZSQ', '9dacad23474b33facada4682d66dd949'],
            ['GS8z3QwN5MzpxU0aTuxuaA', '192f33dd0c0de4cce9c54d1a4eec6e68']]
        for fixture in fixtures:
            aseq_id, md5_hex = fixture
            actual = seqdepot.aseq_id_from_md5_hex(md5_hex)
            self.assertEqual(aseq_id, actual)
            # upper-case
            actual = seqdepot.aseq_id_from_md5_hex(md5_hex.upper())
            self.assertEqual(aseq_id, actual)

    def test_aseq_id_from_sequence(self):
        fixtures = [
            ['yg8A8H8N-4x1Ezf8WW-YbA',
             'MTNVLIVEDEQAIRRFLRTALEGDGMRVFEAETLQRGLLEAATRKPDLIILDLGLPDGDGIE' +
             'FIRDLRQWSAVPVIVLSARSEESDKIAALDAGADDYLSKPFGIGELQARLRVALRRHSATTA' +
             'PDPLVKFSDVTVDLAARVIHRGEEEVHLTPIEFRLLAVLLNNAGKVLTQRQLLNQVWGPNAV' +
             'EHSHYLRIYMGHLRQKLEQDPARPRHFITETGIGYRFML'],
            ['naytI0dLM_rK2kaC1m3ZSQ',
             'MNNEPLRPDPDRLLEQTAAPHRGKLKVFFGACAGVGKTWAMLAEAQRLRAQGLDIVVGVVET' +
             'HGRKDTAAMLEGLAVLPLKRQAYRGRHISEFDLDAALARRPALILMDELAHSNAPGSRHPKR' +
             'WQDIEELLEAGIDVFTTVNVQHLESLNDVVSGVTGIQVRETVPDPFFDAADDVVLVDLPPDD' +
             'LRQRLKEGKVYIAGQAERAIEHFFRKGNLIALRELALRRTADRVDEQMRAWRGHPGEEKVWH' +
             'TRDAILLCIGHNTGSEKLVRAAARLASRLGSVWHAVYVETPALHRLPEKKRRAILSALRLAQ' +
             'ELGAETATLSDPAEEKAVVRYAREHNLGKIILGRPASRRWWRRETFADRLARIAPDLDQVLV' +
             'ALDEPPARTINNAPDNRSFKDKWRVQIQGCVVAAALCAVITLIAMQWLMAFDAANLVMLYLL' +
             'GVVVVALFYGRWPSVVATVINVVSFDLFFIAPRGTLAVSDVQYLLTFAVMLTVGLVIGNLTA' +
             'GVRYQARVARYREQRTRHLYEMSKALAVGRSPQDIAATSEQFIASTFHARSQVLLPDDNGKL' +
             'QPLTHPQGMTPWDDAIAQWSFDKGLPAGAGTDTLPGVPYQILPLKSGEKTYGLVVVEPGNLR' +
             'QLMIPEQQRLLETFTLLVANALERLTLTASEEQARMASEREQIRNALLAALSHDLRTPLTVL' +
             'FGQAEILTLDLASEGSPHARQASEIRQHVLNTTRLVNNLLDMARIQSGGFNLKKEWLTLEEV' +
             'VGSALQMLEPGLSSPINLSLPEPLTLIHVDGPLFERVLINLLENAVKYAGAQAEIGIDAHVE' +
             'GENLQLDVWDNGPGLPPGQEQTIFDKFARGNKESAVPGVGLGLAICRAIVDVHGGTITAFNR' +
             'PEGGACFRVTLPQQTAPELEEFHEDM'],
            ['GS8z3QwN5MzpxU0aTuxuaA',
             'MSGLRPALSTFIFLLLITGGVYPLLTTVLGQWWFPWQANGSLIREGDTVRGSALIGQNFTGN' +
             'GYFHGRPSATAEMPYNPQASGGSNLAVSNPELDKLIAARVAALRAANPDASASVPVELVTAS' +
             'ASGLDNNITPQAAAWQIPRVAKARNLSVEQLTQLIAKYSQQPLVKYIGQPVVNIVELNLALD' +
             'KLDE']]
        for fixture in fixtures:
            aseq_id, sequence = fixture
            actual = seqdepot.aseq_id_from_sequence(sequence)
            self.assertEqual(aseq_id, actual)

    def test_clean_sequence(self):
        fixtures = [
            ['', ''],
            ['ABC', 'A B C'],
            ['abc', 'a b c'],
            ['ABC', ' ABC '],
            ['ABC', "\n\r\t\f     ABC"],
            ['A@B@C', "A9B#C"]]
        for fixture in fixtures:
            expect, inp = fixture
            actual = seqdepot.clean_sequence(inp)
            self.assertEqual(expect, actual)

    def test_find(self):
        sd = seqdepot.SeqDepot()
        results = sd.find(['naytI0dLM_rK2kaC1m3ZSQ',
                           'GS8z3QwN5MzpxU0aTuxuaA'])
        self.assertEqual(2, len(results))
        self.assertEqual(894, results[0]['data']['l'])
        results = sd.find('naytI0dLM_rK2kaC1m3ZSQ', label_tool_data=True)
        self.assertIn('acc', results[0]['data']['t']['pfam27'][0])

    def test_find_one(self):
        sd = seqdepot.SeqDepot()
        ids = 'naytI0dLM_rK2kaC1m3ZSQ'
        seq = ('MNNEPLRPDPDRLLEQTAAPHRGKLKVFFGACAGVGKTWAMLAEAQRLRAQGLDIVVGVV' +
               'ETHGRKDTAAMLEGLAVLPLKRQAYRGRHISEFDLDAALARRPALILMDELAHSNAPGSR' +
               'HPKRWQDIEELLEAGIDVFTTVNVQHLESLNDVVSGVTGIQVRETVPDPFFDAADDVVLV' +
               'DLPPDDLRQRLKEGKVYIAGQAERAIEHFFRKGNLIALRELALRRTADRVDEQMRAWRGH' +
               'PGEEKVWHTRDAILLCIGHNTGSEKLVRAAARLASRLGSVWHAVYVETPALHRLPEKKRR' +
               'AILSALRLAQELGAETATLSDPAEEKAVVRYAREHNLGKIILGRPASRRWWRRETFADRL' +
               'ARIAPDLDQVLVALDEPPARTINNAPDNRSFKDKWRVQIQGCVVAAALCAVITLIAMQWL' +
               'MAFDAANLVMLYLLGVVVVALFYGRWPSVVATVINVVSFDLFFIAPRGTLAVSDVQYLLT' +
               'FAVMLTVGLVIGNLTAGVRYQARVARYREQRTRHLYEMSKALAVGRSPQDIAATSEQFIA' +
               'STFHARSQVLLPDDNGKLQPLTHPQGMTPWDDAIAQWSFDKGLPAGAGTDTLPGVPYQIL' +
               'PLKSGEKTYGLVVVEPGNLRQLMIPEQQRLLETFTLLVANALERLTLTASEEQARMASER' +
               'EQIRNALLAALSHDLRTPLTVLFGQAEILTLDLASEGSPHARQASEIRQHVLNTTRLVNN' +
               'LLDMARIQSGGFNLKKEWLTLEEVVGSALQMLEPGLSSPINLSLPEPLTLIHVDGPLFER' +
               'VLINLLENAVKYAGAQAEIGIDAHVEGENLQLDVWDNGPGLPPGQEQTIFDKFARGNKES' +
               'AVPGVGLGLAICRAIVDVHGGTITAFNRPEGGACFRVTLPQQTAPELEEFHEDM')
        obj = sd.find_one(ids, fields='s,l')
        self.assertEqual(len(seq), obj['l'])
        self.assertEqual(ids, obj['id'])
        self.assertEqual(seq, obj['s'])
        obj = sd.find_one(ids)
        self.assertEqual(len(seq), obj['l'])
        self.assertEqual(ids, obj['id'])
        self.assertEqual(seq, obj['s'])
        # Attempt to get gis
        obj = sd.find_one(ids, fields='x(gi)')
        self.assertIn('gi', obj['x'])
        self.assertTrue(len(obj['x']['gi']) > 0)
        # Search via GI, PDB, UniProt, and MD5_Hex
        fixtures = {'gi': 1651302, 'uni': 'B1X6M6_ECODH',
                    'md5_hex': '9dacad23474b33facada4682d66dd949'}
        for fixture in fixtures:
            obj = sd.find_one(fixtures[fixture], fields='l', type=fixture)
            self.assertIsNotNone(obj)
            self.assertEqual(len(seq), obj['l'])
            self.assertEqual(ids, obj['id'])
        # now by pdb
        obj = sd.find_one('4dpk', fields='l', type='pdb')
        self.assertIsNotNone(obj)
        self.assertEqual(359, obj['l'])
        self.assertEqual('-0tNbPaXZtNA2gGW668Kqg', obj['id'])

    def test_is_tool_done(self):
        sd = seqdepot.SeqDepot()
        fixtures = [
            [False, '', ''],
            [False, 'bob', ''],
            [False, None, None],
            [False, 'pfam26', None],
            [False, None, 'TTT'],
            [True, 'agfam1', 'T'],
            [True, 'agfam1', 'd'],
            [False, 'agfam1', '-'],
            [False, 'ecf', 'TTT'],
            [True, 'ecf', 'TTdT'],
            [True, 'ecf', 'TTdd'],
            [True, 'ecf', 'TTdd-'],
            [True, 'ecf', 'TTdd-T'],
            [False, 'tigrfam', '------------------'],
            [True, 'tigrfam', '-----------------T']]
        for fixture in fixtures:
            expect, tool_id, status = fixture
            if expect:
                self.assertTrue(sd.is_tool_done(tool_id, status),
                                msg="{0} - {1}".format(tool_id, status))
            else:
                self.assertFalse(sd.is_tool_done(tool_id, status),
                                 msg="{0} - {1}".format(tool_id, status))

    def test_is_valid_aseq_id(self):
        fixtures = [
            [True, 'yg8A8H8N-4x1Ezf8WW-YbA'],
            [False, 'yg8A8H8N-4x1Ezf8WW-Yb'],
            [False, 'yg8A8H8N-4x1Ezf8WW-YbAA'],
            [False, None],
            [False, ''],
            [False, 'yg8A8H8N-4x1Ezf8WW-Yb@']]
        for fixture in fixtures:
            expect, inp = fixture
            actual = seqdepot.is_valid_aseq_id(inp)
            if expect:
                self.assertTrue(actual)
            else:
                self.assertFalse(actual)

    def test_is_valid_field_string(self):
        fixtures = [
            [True, ''],
            [True, None],
            [True, 's'],
            [True, 'l'],
            [False, '@'],
            [False, '_!@#$'],
            [False, '1234567'],
            [False, '1A'],
            [True, 'A1'],
            [True, 's,l'],
            [True, 's(l)'],
            [False, 's()'],
            [True, 's(l),s(l)'],
            [True, 'a,b(c|d|e)'],
            [True, 'a,b(c),d(e|f)'],
            [False, 'a,b(c),d(e|@)'],
            [False, 'a,b(c),d(@|f)'],
            [False, 'a,b(@),d(e|f)'],
            [False, 'a,b(c),d( |f)'],
            [False, ' s']]
        for fixture in fixtures:
            expect, inp = fixture
            actual = seqdepot.is_valid_field_string(inp)
            if expect:
                self.assertTrue(actual)
            else:
                self.assertFalse(actual)

    def test_md5_hex_from_aseq_id(self):
        fixtures = [
            ['ca0f00f07f0dfb8c751337fc596f986c', 'yg8A8H8N-4x1Ezf8WW-YbA'],
            ['9dacad23474b33facada4682d66dd949', 'naytI0dLM_rK2kaC1m3ZSQ'],
            ['192f33dd0c0de4cce9c54d1a4eec6e68', 'GS8z3QwN5MzpxU0aTuxuaA']]
        for fixture in fixtures:
            md5_hex, aseq_id = fixture
            actual = seqdepot.md5_hex_from_aseq_id(aseq_id)
            self.assertEqual(md5_hex, actual)

    def test_md5_hex_from_sequence(self):
        fixtures = [
            ['ca0f00f07f0dfb8c751337fc596f986c',
             'MTNVLIVEDEQAIRRFLRTALEGDGMRVFEAETLQRGLLEAATRKPDLIILDLGLPDGDGIE' +
             'FIRDLRQWSAVPVIVLSARSEESDKIAALDAGADDYLSKPFGIGELQARLRVALRRHSATTA' +
             'PDPLVKFSDVTVDLAARVIHRGEEEVHLTPIEFRLLAVLLNNAGKVLTQRQLLNQVWGPNAV' +
             'EHSHYLRIYMGHLRQKLEQDPARPRHFITETGIGYRFML'],
            ['9dacad23474b33facada4682d66dd949',
             'MNNEPLRPDPDRLLEQTAAPHRGKLKVFFGACAGVGKTWAMLAEAQRLRAQGLDIVVGVVET' +
             'HGRKDTAAMLEGLAVLPLKRQAYRGRHISEFDLDAALARRPALILMDELAHSNAPGSRHPKR' +
             'WQDIEELLEAGIDVFTTVNVQHLESLNDVVSGVTGIQVRETVPDPFFDAADDVVLVDLPPDD' +
             'LRQRLKEGKVYIAGQAERAIEHFFRKGNLIALRELALRRTADRVDEQMRAWRGHPGEEKVWH' +
             'TRDAILLCIGHNTGSEKLVRAAARLASRLGSVWHAVYVETPALHRLPEKKRRAILSALRLAQ' +
             'ELGAETATLSDPAEEKAVVRYAREHNLGKIILGRPASRRWWRRETFADRLARIAPDLDQVLV' +
             'ALDEPPARTINNAPDNRSFKDKWRVQIQGCVVAAALCAVITLIAMQWLMAFDAANLVMLYLL' +
             'GVVVVALFYGRWPSVVATVINVVSFDLFFIAPRGTLAVSDVQYLLTFAVMLTVGLVIGNLTA' +
             'GVRYQARVARYREQRTRHLYEMSKALAVGRSPQDIAATSEQFIASTFHARSQVLLPDDNGKL' +
             'QPLTHPQGMTPWDDAIAQWSFDKGLPAGAGTDTLPGVPYQILPLKSGEKTYGLVVVEPGNLR' +
             'QLMIPEQQRLLETFTLLVANALERLTLTASEEQARMASEREQIRNALLAALSHDLRTPLTVL' +
             'FGQAEILTLDLASEGSPHARQASEIRQHVLNTTRLVNNLLDMARIQSGGFNLKKEWLTLEEV' +
             'VGSALQMLEPGLSSPINLSLPEPLTLIHVDGPLFERVLINLLENAVKYAGAQAEIGIDAHVE' +
             'GENLQLDVWDNGPGLPPGQEQTIFDKFARGNKESAVPGVGLGLAICRAIVDVHGGTITAFNR' +
             'PEGGACFRVTLPQQTAPELEEFHEDM'],
            ['192f33dd0c0de4cce9c54d1a4eec6e68',
             'MSGLRPALSTFIFLLLITGGVYPLLTTVLGQWWFPWQANGSLIREGDTVRGSALIGQNFTGN' +
             'GYFHGRPSATAEMPYNPQASGGSNLAVSNPELDKLIAARVAALRAANPDASASVPVELVTAS' +
             'ASGLDNNITPQAAAWQIPRVAKARNLSVEQLTQLIAKYSQQPLVKYIGQPVVNIVELNLALD' +
             'KLDE']]
        for fixture in fixtures:
            md5_hex, sequence = fixture
            actual = seqdepot.md5_hex_from_sequence(sequence)
            self.assertEqual(md5_hex, actual)

    def test_read_fasta_sequence(self):
        fixtures = [
            [""">""", [['', '']]],
            [""">1""", [['1', '']]],
            [""">1\n""", [['1', '']]],
            [""">1\nA""", [['1', 'A']]],
            [""">1\nAB""", [['1', 'AB']]],
            [""">1\nAB\n""", [['1', 'AB']]],
            [""">1\nAB\nC""", [['1', 'ABC']]],
            [""">1\nAB\nCD\n""", [['1', 'ABCD']]],
            [""">1\nA\n>""", [['1', 'A'], ['', '']]],
            [""">1\nA\n>2""", [['1', 'A'], ['2', '']]],
            [""">1\nA\n>2\n""", [['1', 'A'], ['2', '']]],
            [""">1\nA\n>2\nA""", [['1', 'A'], ['2', 'A']]],
            [""">1\nA\n>2\nB\n""", [['1', 'A'], ['2', 'B']]],
            [""">1\nA\n>2\nB\n>""", [['1', 'A'], ['2', 'B'], ['', '']]],
            # Trim leading and trailing whitespace
            ["""> 1 \nA\n""", [['1', 'A']]],
            # Invalid symbols
            [""">!@#$\n12345678900""", [['!@#$', '@@@@@@@@@@@']]],
            # Skip empty lines
            ["""\n\n>1\nAB\n\n\tCD\n\n>2\n\nEF""", [['1', 'ABCD'],
                                                    ['2', 'EF']]],
            [""">Ecoli CheY\r\nABCDEF\r\n>Ecoli CheA\r\nGHI\r\nJKL\r\n""",
             [['Ecoli CheY', 'ABCDEF'], ['Ecoli CheA', 'GHIJKL']]]]
        for fixture in fixtures:
            sd = seqdepot.SeqDepot()
            fasta, expect = fixture
            actual = []
            fh = io.StringIO(fasta)
            seq = sd.read_fasta_sequence(fh)
            while seq:
                actual.append(seq)
                seq = sd.read_fasta_sequence(fh)
            self.assertEqual(len(expect), len(actual))
            for i in range(len(expect)):
                self.assertEqual(expect[i][0], actual[i][0])
                self.assertEqual(expect[i][1], actual[i][1])

    def test_save_image(self):
        sd = seqdepot.SeqDepot()
        self.assertTrue(sd.save_image(3355692, None, type='gi'))
        self.assertTrue(os.path.isfile('3355692.png'))
        self.assertTrue(os.path.getsize('3355692.png') > 24)
        os.remove('3355692.png')

    def test_tool_fields(self):
        sd = seqdepot.SeqDepot()
        self.assertIsNone(sd.tool_fields('bob'))
        self.assertIsNotNone(sd.tool_fields('das'))
        names = sd.tool_fields('das')
        self.assertEqual(5, len(names))
        self.assertEqual('start', names[0])
        self.assertEqual('stop', names[1])
        self.assertEqual('peak', names[2])
        self.assertEqual('peak_score', names[3])
        self.assertEqual('evalue', names[4])

    def test_tool_names(self):
        sd = seqdepot.SeqDepot()
        tool_names = sd.tool_names()
        checks = {}
        for name in tool_names:
            checks[name] = 1
        self.assertIn('das', checks)
        self.assertIn('tigrfam', checks)

    def test_tools(self):
        sd = seqdepot.SeqDepot()
        tools = sd.tools()
        self.assertIn('das', tools)
        self.assertIn('ecf', tools)


if __name__ == '__main__':
    unittest.main()
