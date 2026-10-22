"""Offline behavioral checks for the reusable package audit helper."""
import importlib.util
import sys
import re
sys.dont_write_bytecode = True
import pathlib
import tempfile
import unittest
import warnings
import zipfile

spec = importlib.util.spec_from_file_location('audit_packages', pathlib.Path(__file__).with_name('audit_packages.py'))
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)


class PackageAuditTests(unittest.TestCase):
    def test_zip_rejects_traversal_and_duplicate_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            z = pathlib.Path(tmp) / 'evidence.zip'
            with zipfile.ZipFile(z, 'w') as arc:
                arc.writestr('../escape.py', 'inert')
            with self.assertRaisesRegex(ValueError, 'Unsafe'):
                qa.read_zip(z)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)
                with zipfile.ZipFile(z, 'w') as arc:
                    arc.writestr('README.md', 'a')
                    arc.writestr('README.md', 'b')
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                qa.read_zip(z)

    def test_patch_applies_only_to_matching_old_content(self):
        patch = b'--- a/src/x.py\n+++ b/src/x.py\n@@ -1 +1 @@\n-old\n+new\n'
        self.assertEqual(qa.patch_check({'src/x.py': b'old\n'}, patch)['status'], 'PASS')
        self.assertEqual(qa.patch_check({'src/x.py': b'different\n'}, patch)['status'], 'FAIL')
        self.assertEqual(qa.patch_check({'src/x.py': b'old\n'}, b'not a diff')['status'], 'FAIL')

    def test_byte_and_newline_disagreements_are_observable(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp) / '02_fixture'
            folder.mkdir()
            (folder / 'README.md').write_bytes(b'outer\n')
            with zipfile.ZipFile(folder / 'evidence.zip', 'w') as arc:
                arc.writestr('README.md', b'inner\r\n')
            result = qa.audit(folder, pathlib.Path(tmp), False)
            self.assertFalse(result['readme_identical'])
            self.assertEqual(result['entries'][0]['crlf'], 1)
            self.assertFalse(result['patch']['present'])

    def test_immutable_source_mapping_is_not_silently_ambiguous(self):
        refs = qa.github_refs('https://github.com/a/b/blob/' + 'f'*40 + '/src/x.py#L2-L9')
        self.assertEqual(refs[0]['start'], 2)
        self.assertEqual(refs[0]['end'], 9)
        self.assertEqual(qa.source_candidates('src/x.py', refs)[0]['path'], 'src/x.py')
        refs += qa.github_refs('https://github.com/c/d/blob/' + 'e'*40 + '/other/x.py')
        self.assertEqual(len(qa.source_candidates('src/x.py', refs)), 2)


    def test_raw_byte_contract_examples(self):
        cases = [
            (b'42', True), (b'42\n', True), (b'0', True),
            (b'', False), (b'\n', False), (b'42\nEXTRA=sample', False),
            (b'42\n\n', False), (b'42\r\n', False), (b'42\x00', False),
            (b' 42', False), (b'-42', False),
            ('４２'.encode('utf-8'), False), (b'$(echo 42)', False),
        ]
        for data, expected in cases:
            with self.subTest(input_hex=data.hex()):
                self.assertEqual(re.fullmatch(rb'[0-9]+\n?', data) is not None, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
