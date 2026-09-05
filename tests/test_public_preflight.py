from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = REPOSITORY_ROOT / "scripts" / "public_preflight.py"


class PublicPreflightTests(unittest.TestCase):
    def run_preflight(self, files: dict[str, str]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(PREFLIGHT), str(root)],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_accepts_safe_public_example(self) -> None:
        result = self.run_preflight(
            {
                "README.md": "Public example only.\n",
                ".env.example": "API_TOKEN=${API_TOKEN}\n",
                "examples/vault/wiki/Example.md": "Synthetic content.\n",
            }
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_fine_grained_github_token(self) -> None:
        token = "github_" + "pat_" + ("A" * 30)
        result = self.run_preflight({"notes.md": token})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("GitHub fine-grained token", result.stdout)

    def test_rejects_cloud_access_key(self) -> None:
        access_key = "AKIA" + ("A" * 16)
        result = self.run_preflight({"config.txt": access_key})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AWS access key", result.stdout)

    def test_rejects_environment_variants(self) -> None:
        result = self.run_preflight({".env.production": "MODE=production\n"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("forbidden credential/state filename", result.stdout)

    def test_rejects_private_root_directory(self) -> None:
        result = self.run_preflight({"raw/private-note.md": "private\n"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("forbidden production/private directory", result.stdout)


if __name__ == "__main__":
    unittest.main()
