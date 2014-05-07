#!/usr/bin/python

import SeqDepot
import unittest
import io
import os

class SeqDepotTestCase(unittest.TestCase):

    def test_aseqIdFromMD5Hex(self):
        fixtures = [
            ['yg8A8H8N-4x1Ezf8WW-YbA', 'ca0f00f07f0dfb8c751337fc596f986c'],
            ['naytI0dLM_rK2kaC1m3ZSQ', '9dacad23474b33facada4682d66dd949'],
            ['GS8z3QwN5MzpxU0aTuxuaA', '192f33dd0c0de4cce9c54d1a4eec6e68'] ]

        for fixture in fixtures:
            aseqId, md5hex = fixture
            actual = SeqDepot.aseqIdFromMD5Hex(md5hex)
            self.assertEqual(aseqId, actual)

            #upper-case
            actual = SeqDepot.aseqIdFromMD5Hex(md5hex.upper())
            self.assertEqual(aseqId, actual)

    def test_aseqIdFromSequence(self):
        fixtures = [
              ['yg8A8H8N-4x1Ezf8WW-YbA', 'MTNVLIVEDEQAIRRFLRTALEGDGMRVFEAETLQRGLLEAATRKPDLIILDLGLPDGDGIEFIRDLRQWSAVPVIVLSARSEESDKIAALDAGADDYLSKPFGIGELQARLRVALRRHSATTAPDPLVKFSDVTVDLAARVIHRGEEEVHLTPIEFRLLAVLLNNAGKVLTQRQLLNQVWGPNAVEHSHYLRIYMGHLRQKLEQDPARPRHFITETGIGYRFML'],
              ['naytI0dLM_rK2kaC1m3ZSQ', 'MNNEPLRPDPDRLLEQTAAPHRGKLKVFFGACAGVGKTWAMLAEAQRLRAQGLDIVVGVVETHGRKDTAAMLEGLAVLPLKRQAYRGRHISEFDLDAALARRPALILMDELAHSNAPGSRHPKRWQDIEELLEAGIDVFTTVNVQHLESLNDVVSGVTGIQVRETVPDPFFDAADDVVLVDLPPDDLRQRLKEGKVYIAGQAERAIEHFFRKGNLIALRELALRRTADRVDEQMRAWRGHPGEEKVWHTRDAILLCIGHNTGSEKLVRAAARLASRLGSVWHAVYVETPALHRLPEKKRRAILSALRLAQELGAETATLSDPAEEKAVVRYAREHNLGKIILGRPASRRWWRRETFADRLARIAPDLDQVLVALDEPPARTINNAPDNRSFKDKWRVQIQGCVVAAALCAVITLIAMQWLMAFDAANLVMLYLLGVVVVALFYGRWPSVVATVINVVSFDLFFIAPRGTLAVSDVQYLLTFAVMLTVGLVIGNLTAGVRYQARVARYREQRTRHLYEMSKALAVGRSPQDIAATSEQFIASTFHARSQVLLPDDNGKLQPLTHPQGMTPWDDAIAQWSFDKGLPAGAGTDTLPGVPYQILPLKSGEKTYGLVVVEPGNLRQLMIPEQQRLLETFTLLVANALERLTLTASEEQARMASEREQIRNALLAALSHDLRTPLTVLFGQAEILTLDLASEGSPHARQASEIRQHVLNTTRLVNNLLDMARIQSGGFNLKKEWLTLEEVVGSALQMLEPGLSSPINLSLPEPLTLIHVDGPLFERVLINLLENAVKYAGAQAEIGIDAHVEGENLQLDVWDNGPGLPPGQEQTIFDKFARGNKESAVPGVGLGLAICRAIVDVHGGTITAFNRPEGGACFRVTLPQQTAPELEEFHEDM'],
              ['GS8z3QwN5MzpxU0aTuxuaA', 'MSGLRPALSTFIFLLLITGGVYPLLTTVLGQWWFPWQANGSLIREGDTVRGSALIGQNFTGNGYFHGRPSATAEMPYNPQASGGSNLAVSNPELDKLIAARVAALRAANPDASASVPVELVTASASGLDNNITPQAAAWQIPRVAKARNLSVEQLTQLIAKYSQQPLVKYIGQPVVNIVELNLALDKLDE'] ]

        for fixture in fixtures:
            aseqId, sequence = fixture
            actual = SeqDepot.aseqIdFromSequence(sequence)
            self.assertEqual(aseqId,actual)

    def test_cleanSequence(self):
        fixtures = [
                ['', ''],
                ['ABC', 'A B C'],
                ['abc', 'a b c'],
                ['ABC', ' ABC '],
                ['ABC', "\n\r\t\f     ABC"],
                ['A@B@C', "A9B#C"]]
        for fixture in fixtures:
            expect, inp = fixture
            actual = SeqDepot.cleanSequence(inp)
            self.assertEqual(expect, actual)

    def test_find(self):
        sd = SeqDepot.new()
        results = sd.find(['naytI0dLM_rK2kaC1m3ZSQ', 'GS8z3QwN5MzpxU0aTuxuaA']);
        self.assertEqual(2, len(results));
        self.assertEqual(894, results[0]['data']['l']);

        results = sd.find('naytI0dLM_rK2kaC1m3ZSQ', {'labelToolData' : 1})


    def test_findOne(self):
        sd = SeqDepot.new()

        ids = 'naytI0dLM_rK2kaC1m3ZSQ'
        seq = 'MNNEPLRPDPDRLLEQTAAPHRGKLKVFFGACAGVGKTWAMLAEAQRLRAQGLDIVVGVVETHGRKDTAAMLEGLAVLPLKRQAYRGRHISEFDLDAALARRPALILMDELAHSNAPGSRHPKRWQDIEELLEAGIDVFTTVNVQHLESLNDVVSGVTGIQVRETVPDPFFDAADDVVLVDLPPDDLRQRLKEGKVYIAGQAERAIEHFFRKGNLIALRELALRRTADRVDEQMRAWRGHPGEEKVWHTRDAILLCIGHNTGSEKLVRAAARLASRLGSVWHAVYVETPALHRLPEKKRRAILSALRLAQELGAETATLSDPAEEKAVVRYAREHNLGKIILGRPASRRWWRRETFADRLARIAPDLDQVLVALDEPPARTINNAPDNRSFKDKWRVQIQGCVVAAALCAVITLIAMQWLMAFDAANLVMLYLLGVVVVALFYGRWPSVVATVINVVSFDLFFIAPRGTLAVSDVQYLLTFAVMLTVGLVIGNLTAGVRYQARVARYREQRTRHLYEMSKALAVGRSPQDIAATSEQFIASTFHARSQVLLPDDNGKLQPLTHPQGMTPWDDAIAQWSFDKGLPAGAGTDTLPGVPYQILPLKSGEKTYGLVVVEPGNLRQLMIPEQQRLLETFTLLVANALERLTLTASEEQARMASEREQIRNALLAALSHDLRTPLTVLFGQAEILTLDLASEGSPHARQASEIRQHVLNTTRLVNNLLDMARIQSGGFNLKKEWLTLEEVVGSALQMLEPGLSSPINLSLPEPLTLIHVDGPLFERVLINLLENAVKYAGAQAEIGIDAHVEGENLQLDVWDNGPGLPPGQEQTIFDKFARGNKESAVPGVGLGLAICRAIVDVHGGTITAFNRPEGGACFRVTLPQQTAPELEEFHEDM'
        obj = sd.findOne(ids, {'fields' : 's,l'})
        self.assertEqual(len(seq), obj['l'])
        self.assertEqual(ids, obj['id'])
        self.assertEqual(seq, obj['s'])

        obj = sd.findOne(ids)
        self.assertEqual(len(seq), obj['l'])
        self.assertEqual(ids, obj['id'])
        self.assertEqual(seq, obj['s'])

        # Attempt to get gis
        obj = sd.findOne(ids, {'fields' : 'x(gi)'})
        assert(obj['x']['gi'])
        assert(len(obj['x']['gi']) > 0)

        # Search via GI, PDB, UniProt, and MD5_Hex
        fixtures = { 'gi' : 1651302, 'uni':'B1X6M6_ECODH', 'md5_hex' : '9dacad23474b33facada4682d66dd949' }

        for fixture in list(fixtures.keys()):
            obj = sd.findOne(fixtures[fixture], {'fields' : 'l', 'type' : fixture})
            assert(obj);
            self.assertEqual(len(seq), obj['l'])
            self.assertEqual(ids, obj['id'])

            # now by pdb
        obj = sd.findOne('4dpk', {'fields' : 'l', 'type' :'pdb'})
        assert(obj)
        self.assertEqual(359, obj['l']);
        self.assertEqual('-0tNbPaXZtNA2gGW668Kqg', obj['id'])

    def test_isToolDone(self):
        sd = SeqDepot.new()

        fixtures = [
            [0, '', ''],
            [0, 'bob', ''],
            [0, None, None],
            [0, 'pfam26', None],
            [0, None, 'TTT'],
            [1, 'agfam1', 'T'],
            [1, 'agfam1', 'd'],
            [0, 'agfam1', '-'],
            [0, 'ecf', 'TTT'],
            [1, 'ecf', 'TTdT'],
            [1, 'ecf', 'TTdd'],
            [1, 'ecf', 'TTdd-'],
            [1, 'ecf', 'TTdd-T'],
            [0, 'tigrfam', '------------------'],
            [1, 'tigrfam', '-----------------T'] ]

        i = 0
        for fixture in fixtures:
            expect, toolId, status = fixture
            i += 1
            if expect:
                assert(sd.isToolDone(toolId, status))
            else:
                assert(not sd.isToolDone(toolId, status))


    def test_isValidAseqId(self):
        fixtures = [
            [1, 'yg8A8H8N-4x1Ezf8WW-YbA'],
            [0, 'yg8A8H8N-4x1Ezf8WW-Yb'],
            [0, 'yg8A8H8N-4x1Ezf8WW-YbAA'],
            [0, None],
            [0, ''],
            [0, 'yg8A8H8N-4x1Ezf8WW-Yb@'] ]

        for fixture in fixtures:
            expect, inp = fixture
            actual = SeqDepot.isValidAseqId(inp)
            if expect:
                assert(actual)
            else:
                assert( not actual)

    def test_isValidFieldString(self):
        fixtures = [
            [1, ''],
            [1, None],
            [1, 's'],
            [1, 'l'],
            [0, '@'],
            [0, '_!@#$'],
            [0, '1234567'],
            [0, '1A'],
            [1, 'A1'],

            [1, 's,l'],
            [1, 's(l)'],
            [0, 's()'],
            [1, 's(l),s(l)'],
            [1, 'a,b(c|d|e)'],
            [1, 'a,b(c),d(e|f)'],
            [0, 'a,b(c),d(e|@)'],
            [0, 'a,b(c),d(@|f)'],
            [0, 'a,b(@),d(e|f)'],
            [0, 'a,b(c),d( |f)'],
            [0, ' s'] ]
        for fixture in fixtures:
            expect, inp = fixture
            actual = SeqDepot.isValidFieldString(inp)
            if expect:
                assert(actual)
            else:
                assert(not actual)

    def test_MD5HexFromAseqId(self):
        fixtures = [
            ['ca0f00f07f0dfb8c751337fc596f986c', 'yg8A8H8N-4x1Ezf8WW-YbA'],
            ['9dacad23474b33facada4682d66dd949', 'naytI0dLM_rK2kaC1m3ZSQ'],
            ['192f33dd0c0de4cce9c54d1a4eec6e68', 'GS8z3QwN5MzpxU0aTuxuaA'] ];

        for fixture in fixtures:
            md5hex, aseqId = fixture
            actual = SeqDepot.MD5HexFromAseqId(aseqId);
            self.assertEqual(md5hex, actual);

    def test_MD5HexFromSequence(self):
        fixtures = [
            ['ca0f00f07f0dfb8c751337fc596f986c', 'MTNVLIVEDEQAIRRFLRTALEGDGMRVFEAETLQRGLLEAATRKPDLIILDLGLPDGDGIEFIRDLRQWSAVPVIVLSARSEESDKIAALDAGADDYLSKPFGIGELQARLRVALRRHSATTAPDPLVKFSDVTVDLAARVIHRGEEEVHLTPIEFRLLAVLLNNAGKVLTQRQLLNQVWGPNAVEHSHYLRIYMGHLRQKLEQDPARPRHFITETGIGYRFML'],
            ['9dacad23474b33facada4682d66dd949', 'MNNEPLRPDPDRLLEQTAAPHRGKLKVFFGACAGVGKTWAMLAEAQRLRAQGLDIVVGVVETHGRKDTAAMLEGLAVLPLKRQAYRGRHISEFDLDAALARRPALILMDELAHSNAPGSRHPKRWQDIEELLEAGIDVFTTVNVQHLESLNDVVSGVTGIQVRETVPDPFFDAADDVVLVDLPPDDLRQRLKEGKVYIAGQAERAIEHFFRKGNLIALRELALRRTADRVDEQMRAWRGHPGEEKVWHTRDAILLCIGHNTGSEKLVRAAARLASRLGSVWHAVYVETPALHRLPEKKRRAILSALRLAQELGAETATLSDPAEEKAVVRYAREHNLGKIILGRPASRRWWRRETFADRLARIAPDLDQVLVALDEPPARTINNAPDNRSFKDKWRVQIQGCVVAAALCAVITLIAMQWLMAFDAANLVMLYLLGVVVVALFYGRWPSVVATVINVVSFDLFFIAPRGTLAVSDVQYLLTFAVMLTVGLVIGNLTAGVRYQARVARYREQRTRHLYEMSKALAVGRSPQDIAATSEQFIASTFHARSQVLLPDDNGKLQPLTHPQGMTPWDDAIAQWSFDKGLPAGAGTDTLPGVPYQILPLKSGEKTYGLVVVEPGNLRQLMIPEQQRLLETFTLLVANALERLTLTASEEQARMASEREQIRNALLAALSHDLRTPLTVLFGQAEILTLDLASEGSPHARQASEIRQHVLNTTRLVNNLLDMARIQSGGFNLKKEWLTLEEVVGSALQMLEPGLSSPINLSLPEPLTLIHVDGPLFERVLINLLENAVKYAGAQAEIGIDAHVEGENLQLDVWDNGPGLPPGQEQTIFDKFARGNKESAVPGVGLGLAICRAIVDVHGGTITAFNRPEGGACFRVTLPQQTAPELEEFHEDM'],
            ['192f33dd0c0de4cce9c54d1a4eec6e68', 'MSGLRPALSTFIFLLLITGGVYPLLTTVLGQWWFPWQANGSLIREGDTVRGSALIGQNFTGNGYFHGRPSATAEMPYNPQASGGSNLAVSNPELDKLIAARVAALRAANPDASASVPVELVTASASGLDNNITPQAAAWQIPRVAKARNLSVEQLTQLIAKYSQQPLVKYIGQPVVNIVELNLALDKLDE'] ]

        for fixture in fixtures:
            md5hex, sequence = fixture
            actual = SeqDepot.MD5HexFromSequence(sequence);
            self.assertEqual(md5hex, actual);


    def test_readFastaSequence(self):
        sd = SeqDepot.new()
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
            ["""\n\n>1\nAB\n\n\tCD\n\n>2\n\nEF""", [['1', 'ABCD'], ['2', 'EF']]],

            [""">Ecoli CheY\r\nABCDEF\r\n>Ecoli CheA\r\nGHI\r\nJKL\r\n""", [['Ecoli CheY', 'ABCDEF'], ['Ecoli CheA', 'GHIJKL']]] ]

        for fixture in fixtures:
            sd = SeqDepot.new()
            fasta, expect = fixture
            actual = []
            fh = io.StringIO(fasta)
            seq = sd.readFastaSequence(fh)
            while seq:
                actual.append(seq)
                seq = sd.readFastaSequence(fh)

            self.assertEqual(len(expect), len(actual))
            i = 0
            for i in range(len(expect)):
                self.assertEqual(expect[i][0], actual[i][0])
                self.assertEqual(expect[i][1], actual[i][1])

    def test_saveImage(self):
        sd = SeqDepot.new()
        assert(sd.saveImage(3355692, None, {'type' : 'gi'}))
        assert(os.path.isfile('3355692.png'))
        assert(os.path.getsize('3355692.png') > 24)
        os.remove('3355692.png')

    def test_toolFields(self):
        sd = SeqDepot.new()
        self.assertIsNone(sd.toolFields('bob'))
        assert(sd.toolFields('das'))
        names = sd.toolFields('das')
        self.assertEqual(5, len(names))
        self.assertEqual('start', names[0])
        self.assertEqual('stop', names[1])
        self.assertEqual('peak', names[2])
        self.assertEqual('peak_score', names[3])
        self.assertEqual('evalue', names[4])

    def test_toolNames(self):
        sd = SeqDepot.new()
        toolNames = sd.toolNames()
        checks = {}
        for name in toolNames:
            checks[name] = 1
        assert(checks['das'])
        assert(checks['tigrfam'])


    def test_tools(self):
        sd = SeqDepot.new()
        tools = sd.tools()

        assert(tools['das']);
        assert(tools['ecf']);




if __name__ == '__main__':
    unittest.main()

