import tempfile
import unittest
from pathlib import Path

from agent_session_repro_bundle_checker_20260711.cli import check_bundle, main


class T(unittest.TestCase):
    def test_complete_passes(self):
        with tempfile.TemporaryDirectory() as d:
            for f in ['prompt.txt', 'commands.log', 'git-status.txt', 'redactions.txt', 'environment.txt']:
                (Path(d) / f).write_text('ok')
            self.assertEqual(check_bundle(d)['status'], 'pass')

    def test_secret_penalty(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / 'prompt.txt').write_text('auth_token = sample-secret-value')
            r = check_bundle(d)
            self.assertTrue(r['secret_hits'])
            self.assertEqual(r['status'], 'review')
            self.assertNotIn('sample-secret-value', r['secret_hits'][0]['text'])

    def test_markdown_format_preserves_exit_policy(self):
        with tempfile.TemporaryDirectory() as d:
            for f in ['prompt.txt', 'commands.log', 'git-status.txt', 'redactions.txt', 'environment.txt']:
                (Path(d) / f).write_text('ok')
            self.assertEqual(main([d, '--format', 'markdown']), 0)
            (Path(d) / 'commands.log').write_text('password=sample-secret-value')
            self.assertEqual(main([d, '--format', 'markdown']), 1)


if __name__ == '__main__':
    unittest.main()
