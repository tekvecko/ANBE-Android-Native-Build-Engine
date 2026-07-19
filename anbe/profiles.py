#!/usr/bin/env python3


CAPACITOR_VITE = {

    "name":
    "capacitor-vite-android",

    "detect":
    [
        "Capacitor",
        "Vite"
    ],

    "steps":
    [

        "npm install",

        "npm run build",

        "npx cap sync android",

        "cd android && ./gradlew clean assembleDebug --stacktrace"

    ],

    "artifact":
    "android/app/build/outputs/apk/debug/app-debug.apk"

}



FLUTTER = {

    "name":
    "flutter-android",

    "detect":
    [
        "Flutter"
    ],

    "steps":
    [

        "flutter pub get",

        "flutter build apk"

    ],

    "artifact":
    "build/app/outputs/flutter-apk/app-release.apk"

}



NATIVE_ANDROID = {

    "name":
    "native-android-gradle",

    "detect":
    [
        "Android Gradle"
    ],

    "steps":
    [

        "cd android && ./gradlew clean assembleDebug --stacktrace"

    ],

    "artifact":
    "android/app/build/outputs/apk/debug/app-debug.apk"

}


PROFILES=[

    CAPACITOR_VITE,

    FLUTTER,

    NATIVE_ANDROID

]

