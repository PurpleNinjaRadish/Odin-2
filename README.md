# Odin demo · Project Cerberus

**Open the demo: [purpleninjaradish.github.io/Odin-2](https://purpleninjaradish.github.io/Odin-2/)**

Odin, the Secure Student Analyzer, version 0.10.0-alpha. Every student and teacher in this demo is invented. Never enter real student information here: the real Odin runs offline on the Project Cerberus server at school.

## Test it on another device

Scan this code with the phone's or tablet's camera, or type the address above:

![QR code for https://purpleninjaradish.github.io/Odin-2/](qr-code.png)

To install it as an app with its own icon:

| Device | How |
| --- | --- |
| iPhone or iPad | Open the link in **Safari**, tap **Share**, then **Add to Home Screen** |
| Android | Open the link in **Chrome**, tap **⋮**, then **Install app** (or **Add to Home screen**) |
| Computer | In Chrome or Edge, click the install button at the right of the address bar |

On a phone, the bar at the bottom holds Class, Student, Focus, Practice and Fluency, and **More** has the other views. **Menu** (top right) has the class, Reading or Math, and Codes or Names.

**Scan the sheets with a phone: DI-ana (new).** [DI-ana](https://github.com/PurpleNinjaRadish/DI-ana) (Diagnostic testing and Intervention automatic analysis) is a separate app that reads Odin's paper pre-checks, practice sheets and post-checks with the phone's camera: hold the phone over each sheet until it beeps. Try its demo here: **[DI-ana demo](https://purpleninjaradish.github.io/Odin-2/diana/)**; a walkthrough opens the first time (print its sample sheets, fill in a few bubbles, and scan them; or try pretend pictures). The Android app: [diana-android.apk](https://github.com/PurpleNinjaRadish/DI-ana/raw/android-build/diana-android.apk). DI-ana's demo has its own sheets: sheets printed from this Odin demo have other numbers. Odin's own **Scan sheets** now reads phone photos too.

**New in 0.10: writing with AI, and tests and worksheets.** On the Fluency tab, **New passages** writes a reading passage with AI (or type your own). In DI-ana, **Make tests and worksheets** makes an answer sheet for any multiple-choice worksheet (from its PDF, where DI-ana counts the questions) or a test written with AI, each with an answer key sheet to bubble in and scan. In these demos the page calls the AI you choose itself (an AI on your own computer, a free tier, or a paid one); a key you type is kept only while the page is open. The AI is told only the grade, subject, skill and topic, never anything about a student.

**Practice sheets on paper or as PDF (0.9.4).** On the **Practice** tab, under **View, print or save as PDF**, pick **Pre-checks**, **Practice packets**, **Post-checks** or **Answer keys**, then **Print** or **Save as PDF**. Tap a sheet in a student's row to save just that sheet, or all of that student's sheets. Print at 100% (actual size): a printed PDF scans back into Odin like any printed sheet.

**Each device keeps its own changes.** Marks, checks and readings you make in the demo stay in that browser on that device. Nothing is shared between devices, and nothing is sent anywhere. To start over on a device, clear this site's data in the browser's settings.

## Odin Student: the students' app

**Open it: [purpleninjaradish.github.io/Odin-2/student.html](https://purpleninjaradish.github.io/Odin-2/student.html)**, or scan:

![QR code for Odin Student](qr-student.png)

Odin Student is what a student sees: only their own work, set out like a game. In the demo there's no sign-in: pick a class and an invented student (Room 112 has the most to try; Liam T. has lots of readings).

- **Stars and a rank** that grow with their work, and **Almost there**: the achievements they're closest to.
- **This week's quests:** the reading quest (first reading, practice, final reading, with the voice that helps) and a quest for each subject's sheets. In Room 112 it's Friday, so the post-checks are next. Finish one to see **Achievement unlocked!**
- **My progress:** records, a bar for each week's best reading, and checks before and after practice.
- **Trophy case:** 19 achievements that unlock as bronze, silver and gold medals.

The microphone works in Google Chrome on a computer, or in the Odin app for Android below.

Students never see support tiers, levels or other students. It installs as its own app with a teal icon (iPhone: Safari › Share › Add to Home Screen; Android: Chrome › Install app). Work done in Odin Student shows in the teacher view on the same device. At school, students sign in with a class code and picture password, a QR card, or the teacher unlocks the device.

## Odin Student app for Android (test)

A separate app for **students' tablets and phones**, in teal (0.9). It opens only Odin Student: each student's own practice sheets, reading out loud with the voice, badges and progress. You can also use the **Odin** app below set to **Students**, the way it worked in 0.8.2 (0.9.3). If one doesn't hear you, try the other.

**Download: [odin-student-android.apk](https://purpleninjaradish.github.io/Odin-2/odin-student-android.apk)**, or scan this on the Android tablet or phone:

![QR code for the Odin Student app for Android](qr-student-android.png)

1. Open the download and install it (see step 1 below if Android asks).
2. Open **Odin Student**, then **Try the demo (invented students)**. Android asks to let Odin Student record audio: choose **While using the app** (it's for reading out loud; speech stays on the device and nothing is recorded). Pick a class and a student.
3. On the student's page, in the reading quest, press **Read again** (practice). When the sign at the top says **Listening**, read the story aloud. Stop on a word for 2 seconds, or misread one: the voice says the word, you say it back, and it praises you when you say it right (or says "Not quite" and lets you try again).
4. **Teacher: Odin's address** on the first screen goes back to the setup screen, to type the school server's address.

## Odin app for Android (test)

On Android, the **Odin app** (for teachers) adds the microphone to fluency practice. When a student stops on a word or misreads it, the voice says the word and asks the student to say it. Odin listens, waits for the answer, and goes on. It uses Android's own **on-device** speech recognition, so the voice never leaves the phone, and nothing is recorded.

**Download: [odin-android.apk](https://purpleninjaradish.github.io/Odin-2/odin-android.apk)**, or scan this on the Android phone or tablet:

![QR code for the Odin app for Android](qr-android.png)

**Already have the app?** Install this one over it (version 0.9.5). For students' devices, use the **Odin Student** app above, or this app set to **Students**.

1. Open the download. Android asks to allow installing apps from this source (the browser or Files): allow it, then **Install**. If Google Play Protect warns about an unknown app, choose **More details**, then **Install anyway**: it is a test build, signed with a test key, not from the Play Store.
2. Open **Odin**. Under **Who uses this device?** choose **A teacher**, or **Students** to open Odin Student (as in 0.8.2). Then **Try the demo (invented students)**.
3. Open **Fluency**. The status line says whether this device can recognize speech on the device. If it offers **Set up speech on this device**, press it once (a one-time download from Google).
4. Press **Test the microphone**, allow the microphone, and read the sentence on the screen out loud. Odin shows what it heard, how fast the phone started listening, and whether words came while you read or only when you paused.
5. On a student's row, press **Open**, then **Practice on this device** and **Start practice**. When the sign at the top says **Listening**, read the passage aloud. Stop on a word for 2 seconds, or misread one: the voice says the word, waits for you to say it right, and praises you. While you keep reading, the voice stays quiet.

The microphone needs **Android 12 or newer** with Google's speech services. On older devices the app still opens Odin, and fluency uses **Teacher scores**. For real students, the app opens the school's Project Cerberus server instead (type its `https://` address), only with the school's written approval.

## Things to try

- **Student:** a student's levels, primary and secondary needs, and support tier.
- **Focus:** the weekly focus groups, with pre- and post-checks.
- **Practice:** open a sheet, then **Start on this device** for the locked student mode.
- **Fluency:** **Watch a sample reading** shows the reading screen with the voice guide. Speaking into the microphone works where speech is recognized on the device itself: an up-to-date Google Chrome on a computer, or the [Odin app for Android](#odin-app-for-android-test). iPhones and iPads can't yet, so there the teacher scores the reading.

## What's in this repository

| File | What it is |
| --- | --- |
| `index.html` | The demo page, with the invented students built in |
| `manifest.webmanifest`, `icons/`, `sw.js`, `offline.html` | What lets the demo install as an app. The service worker stores only the offline page and an icon |
| `qr-code.png` | The QR code above |
| `student.html`, `student.webmanifest`, `qr-student.png` | Odin Student, the students' app, and its QR code |
| `odin-android.apk`, `qr-android.png` | The Odin app for Android, for teachers (test build), and its QR code |
| `odin-student-android.apk`, `qr-student-android.png` | The Odin Student app for Android, with the demo built in (test build), and its QR code |
| `.github/workflows/static.yml` | Publishes the repository to GitHub Pages on every push to `main` |
| `server.py`, `Dockerfile`, `.dockerignore` | From an earlier hosted demo (version 0.2). The page above doesn't use them |

The full Odin server, with its wiki and tests, lives in a separate private repository.
