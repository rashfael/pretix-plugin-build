import os
import subprocess

from django.core import management
from setuptools.command.build import build

here = os.path.abspath(os.path.dirname(__file__))
npm_installed = False


class CustomBuild(build):
    def run(self):
        locale_found = False
        for dirpath, dirnames, filenames in os.walk('.', topdown=True):
            for dirname in dirnames:
                if dirname == 'locale':
                    locale_found = True
                    break

        if locale_found:
            management.call_command('compilemessages', verbosity=1)

        if (os.path.exists('vite.config.ts')
                and os.path.exists('package.json')):
            self._build_vite()

        build.run(self)

    def _build_vite(self):
        """Install npm deps and run vite build."""
        print("Installing npm dependencies...")
        subprocess.check_call(['npm', 'ci'])

        print("Building Vite assets...")
        subprocess.check_call(['npx', 'vite', 'build'])
