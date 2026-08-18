from anbe.manifest import ManifestAnalyzer

apk="/data/data/com.termux/files/home/storage/downloads/120/base.apk"

r = ManifestAnalyzer().analyze(apk)

print(r)
