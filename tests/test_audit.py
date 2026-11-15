import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from indian_passport_extraction_claim_audit.audit import audit, claims_in, module_evidence
from indian_passport_extraction_claim_audit.phrases import INDIANPASSPORTEXTRACTION, NOINDIANPASSPORTEXTRACTION, GENERIC_NAMES
from indian_passport_extraction_claim_audit.__main__ import main

class AuditTests(unittest.TestCase):
    def repo(self, files):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for name, value in files.items():
            path = root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)
        return root

    def test_exact_vocabulary(self):
        self.assertEqual(INDIANPASSPORTEXTRACTION, POSITIVE)
        self.assertEqual(NOINDIANPASSPORTEXTRACTION, NEGATIVE)
        self.assertEqual(GENERIC_NAMES, NAMES)
        self.assertEqual(len(set(NAMES)), 24)

    def test_fences(self):
        for marker in ('```', '~~~', '   ````'):
            self.assertEqual(claims_in(marker+'text\nextract indian passport\n'+marker, 'README.md'), [])
        self.assertEqual(len(claims_in('`extract indian passport`', 'x')), 1)

    def test_boundaries_and_normalization(self):
        self.assertEqual(claims_in('xextract indian passportx', 'x'), [])
        self.assertEqual(claims_in("DOESN'T extract-indian-passport", 'x')[0]['family'], 'NOINDIANPASSPORTEXTRACTION')
        self.assertEqual(claims_in('extract indian passport data', 'x')[0]['phrase'], 'extract indian passport data')

    def test_findings_and_threshold(self):
        root = self.repo({'README.md':'extract indian passport', 'tests/test_x.py':'x.extract_indian_passport()'})
        self.assertEqual(audit(root)['findings'][0]['severity'], 'MEDIUM')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['audit', str(root)]), 0)
            self.assertEqual(main(['audit', str(root), '--fail-on','medium']), 2)
        (root/'README.md').write_text('does not extract indian passport')
        self.assertEqual(audit(root)['verdict'], 'PASS')
        (root/'app.py').write_text('x.extract_indian_passport()')
        self.assertEqual(audit(root)['findings'][0]['rule'], 'documented-no-indian-passport-extraction-claim-false')

    def test_no_source_and_one_per_family(self):
        root = self.repo({'README.md':'extract indian passport\n\nindian passport parser'})
        self.assertEqual(len(audit(root)['findings']), 1)
        self.assertEqual(audit(root)['findings'][0]['severity'], 'HIGH')
        (root/'README.md').write_text('no indian passport extraction')
        self.assertEqual(audit(root)['verdict'], 'PASS')

    def test_selection_and_ignore(self):
        root = self.repo({'other.md':'extract indian passport', 'nested/README.md':'extract indian passport', 'a/docs/n.md':'extract indian passport','vendor/a.py':'x.extract_indian_passport()'})
        self.assertEqual(len(audit(root)['claims']), 1)
        self.assertEqual(audit(root)['verdict'], 'PASS')
        self.assertEqual(audit(root, ['vendor'])['verdict'], 'FAIL')

    def test_symlinks(self):
        root = self.repo({'README.md':'extract indian passport'})
        other = self.repo({'app.py':'x.extract_indian_passport()'})
        (root/'linked').symlink_to(other, target_is_directory=True)
        (root/'app.py').symlink_to(other/'app.py')
        self.assertEqual(audit(root)['evidence'], [])

    def test_split_modules(self):
        root = self.repo({'README.md':'extract indian passport', 'a.py':'import mindee\nx=mindee.Client()', 'b.py':'import mindee\nx.parse(IndianPassportV1)'})
        self.assertEqual(audit(root)['evidence'], [])

    def test_cli(self):
        root = self.repo({'README.md':'extract indian passport'})
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(['audit',str(root),'--json']), 2)
        self.assertEqual(json.loads(out.getvalue())['verdict'], 'FAIL')
        for args in ([], ['wrong'], ['audit','--fail-on','HIGH'], ['audit','--ignore']):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                main(args)
            self.assertEqual(exc.exception.code, 1)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(['audit',str(root/'missing')]), 1)
        with contextlib.redirect_stdout(io.StringIO()) as output, self.assertRaises(SystemExit):
            main(['--version'])
        self.assertEqual(output.getvalue().strip(), '0.1.0')

    def test_self_audit(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(claims_in((root/'README.md').read_text(), 'README.md'), [])
        self.assertEqual(audit(root)['verdict'], 'PASS')

POSITIVE = ('indian passport extraction', 'extract indian passport', 'extracts indian passport', 'extracting indian passport', 'extract indian passports', 'extracts indian passports', 'extracting indian passports', 'indian passport parsing', 'indian passport parser', 'parse indian passport', 'parses indian passport', 'parse indian passports', 'parses indian passports', 'indian passport data extraction', 'extract indian passport data', 'indian passport field extraction', 'indian passport document extraction', 'extract indian passport documents', 'indian passport reader', 'indian passport scanning', 'scan indian passport', 'scans indian passport', 'scanning indian passport', 'indian passport recognition', 'recognize indian passport', 'extract indian passport fields', 'india passport extraction', 'extract india passport', 'extracts india passport', 'extracting india passport', 'extract india passports', 'extracts india passports', 'extracting india passports', 'india passport parsing', 'india passport parser', 'parse india passport', 'parses india passport', 'parse india passports', 'parses india passports', 'india passport data extraction', 'extract india passport data', 'india passport field extraction', 'india passport document extraction', 'extract india passport documents', 'india passport reader', 'india passport scanning', 'scan india passport', 'scans india passport', 'scanning india passport', 'india passport recognition')
NEGATIVE = ('no indian passport extraction', 'does not extract indian passport', 'does not extract indian passports', 'does not support indian passport extraction', 'without indian passport extraction', 'no indian passport parser', 'does not parse indian passport', 'does not parse indian passports', 'no india passport extraction', 'does not extract india passport', 'does not extract india passports', 'does not support india passport extraction', 'without india passport extraction', 'no india passport parser', 'does not parse india passport', 'does not parse india passports', 'indian passport extraction not supported', 'india passport extraction not supported', 'does not scan indian passport', 'does not scan india passport', 'no indian passport reader', 'no india passport reader', 'does not extract indian passport data', 'does not extract india passport data')
NAMES = ('extract_indian_passport', 'extract_indian_passports', 'parse_indian_passport', 'parse_indian_passports', 'extract_indian_passport_data', 'parse_indian_passport_data', 'indian_passport_extraction', 'indian_passport_reader', 'read_indian_passport', 'scan_indian_passport', 'scans_indian_passport', 'scanning_indian_passport', 'indian_passport_parsing', 'indian_passport_parser', 'indian_passport_recognition', 'recognize_indian_passport', 'indian_passport_field_extraction', 'indian_passport_document_extraction', 'extract_indian_passport_documents', 'get_indian_passport_data', 'indian_passport_data_extraction', 'extract_indian_passport_fields', 'parse_indian_passport_fields', 'indian_passport_scanning')

def phrase_test(phrase, family):
    def test(self):
        found = claims_in(phrase, 'README.md')
        self.assertEqual([(c['family'], c['phrase']) for c in found], [(family, phrase)])
    return test

for index, phrase in enumerate(POSITIVE):
    setattr(AuditTests, 'test_positive_%02d' % index, phrase_test(phrase, 'INDIANPASSPORTEXTRACTION'))
for index, phrase in enumerate(NEGATIVE):
    setattr(AuditTests, 'test_negative_%02d' % index, phrase_test(phrase, 'NOINDIANPASSPORTEXTRACTION'))

def evidence_test(source, expected):
    def test(self):
        self.assertEqual(bool(module_evidence(source)), expected, source)
    return test

for index, name in enumerate(NAMES):
    for suffix, source, expected in [
        ('attribute', 'client.'+name+'()', True),
        ('import', 'from provider import '+name+' as f\nf()', True),
        ('bare', name+'()', False),
        ('shadow', 'from provider import '+name+'\ndef '+name+'(): pass\n'+name+'()', False),
        ('method', 'class X:\n def '+name+'(self): pass\nx.'+name+'()', False),
        ('assignment', 'from provider import '+name+' as f\nf = other\nf()', False),
        ('annotation', 'from provider import '+name+' as f\nf: object = other\nf()', False),
        ('with', 'from provider import '+name+' as f\nwith ctx() as f:\n f()', False),
        ('async_with', 'from provider import '+name+' as f\nasync def go():\n async with ctx() as f:\n  f()', False),
    ]:
        setattr(AuditTests, 'test_generic_%02d_%s' % (index,suffix), evidence_test(source, expected))

PAIR = 'import mindee\nclient = mindee.Client()\nclient.parse(IndianPassportV1)'
CASES = [
(PAIR, True),
('from mindee import Client as C\nx=C()\nx.parse(product_class=product.ind.IndianPassportV1)', True),
('import mindee.product.ind\nx=mindee.Client()\nx.parse(mindee.product.ind.indian_passport.IndianPassportV1)', True),
('import mindee\nmindee.Client().parse(IndianPassportV1)', True),
('import mindee as m\nm.Client()\nx.parse(IndianPassportV1)', False),
('x.parse(IndianPassportV1)', False),
('import mindee\nx.parse(IndianPassportV1)', False),
('import mindee\nmindee.Client()', False),
(PAIR+'\ndef parse(): pass', False),
(PAIR+'\nclass IndianPassportV1: pass', False),
(PAIR+'\nmindee = other', False),
('from mindee import Client\nwith ctx() as Client:\n Client()\nx.parse(IndianPassportV1)', False),
('from mindee import Client\nClient: object = other\nClient()\nx.parse(IndianPassportV1)', False),
('from mindee import Client\ndef Client(): pass\nClient()\nx.parse(IndianPassportV1)', False),
('import mindee\nx=mindee.Client()\nx.parse("IndianPassportV1")', False),
('import mindee\nx=mindee.Client()\nx.parse(IndianPassportV1)\ninvalid !', False),
('"x.extract_indian_passport()"', False),
('# x.extract_indian_passport()', False),
('x.extract_indian_passport', False),
('import subprocess\nsubprocess.run(["extract_indian_passport"])', False),
]
OTHER_PRODUCTS = 'PassportV1 InternationalIdV2 DriverLicenseV1 IdCardV1 IdCardV2 HealthcareCardV1 HealthCardV1 ReceiptV5 InvoiceV4 InvoiceSplitterV1 MultiReceiptsDetectorV1 FinancialDocumentV1 BankCheckV1 BankAccountDetailsV1 BankAccountDetailsV2 PayslipV2 PayslipV3 BusinessCardV1 CustomV1 GeneratedV1 BillOfLadingV1 ResumeV1 DeliveryNoteV1 CarteGriseV1 EnergyBillV1 NutritionFactsLabelV1 MaterialCertificateV1 BarcodeReaderV1 CropperV1 UsMailV2 UsMailV3 IndianPassportV2 TypeIndianPassportV1'.split()
CASES += [(PAIR.replace('IndianPassportV1', p), False) for p in OTHER_PRODUCTS]
EXCLUDED = 'extract_passport parse_passport extract_passports parse_passports extract_passport_data parse_passport_data begin_analyze_document analyze_id read_mrz process_passport process_indian_passport process_indian_passport_url process_document process_any_document process_document_url process_any_document_url split_and_process_pdf split_and_process_pdf_url process_w2_document process_w9_document process_w8_document process_check process_bank_statement_document process_bussines_card_document classify_document is_indian_passport batch_process_documents analyze_document analyze_expense start_document_analysis get_expense_analysis image_to_string extract_text read_csv read_excel search findall extract parse'.split()
CASES += [('import mindee\nx.'+name+'("indian passport")', False) for name in EXCLUDED]
CASES += [('import requests\nrequests.post("https://api.edenai.run/v3/universal-ai", json={"model":"indian_passport"})', False)]
for index, (source, expected) in enumerate(CASES):
    setattr(AuditTests, 'test_route_%03d' % index, evidence_test(source, expected))

def selection_test(path, expected, test_only=False):
    def test(self):
        root = self.repo({'README.md':'extract indian passport', path:'x.extract_indian_passport()'})
        evidence = audit(root)['evidence']
        self.assertEqual(bool(evidence), expected)
        if evidence:
            self.assertEqual(evidence[0]['test'], test_only)
    return test
for index, path in enumerate(['fixtures/a.py','docs/a.py','examples/a.py','nested/fixtures/a.py','nested/docs/a.py','nested/examples/a.py']):
    setattr(AuditTests, 'test_excluded_path_%d' % index, selection_test(path, False))
for index, path in enumerate(['tests/a.py','nested/tests/a.py','test_app.py','app_test.py']):
    setattr(AuditTests, 'test_test_path_%d' % index, selection_test(path, True, True))

if __name__ == '__main__':
    unittest.main()
