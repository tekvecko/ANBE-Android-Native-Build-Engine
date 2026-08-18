"""
ANBE Android Manifest Layer.

This package is reserved for AndroidManifest.xml / APK
inspection.

Build-level ANBE manifests live in:

    anbe.build_manifest

The alias below exists temporarily for compatibility with
older Builder and Pipeline code.
"""

from ..build_manifest import BuildManifest

Manifest = BuildManifest

__all__ = [
    "BuildManifest",
    "Manifest",
]

