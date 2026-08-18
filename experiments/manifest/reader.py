from pyaxmlparser import APK


class ManifestReader:

    def __init__(self, apk_path):
        self.apk = APK(apk_path)


    def analyze(self):

        return {
            "package": self.apk.package,
            "version_code": self.apk.get_androidversion_code(),
            "version_name": self.apk.get_androidversion_name(),

            "sdk": {
                "min": self.apk.get_min_sdk_version(),
                "target": self.apk.get_target_sdk_version()
            },

            "permissions": self.apk.get_permissions(),

            "activities": self.apk.get_activities()
        }
