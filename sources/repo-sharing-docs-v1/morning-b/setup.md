# Setup

These steps are written for a coding agent (Claude Code, Codex) running on the
reader's Mac. The agent does the technical work; the reader does the three
things in "What you do yourself", ideally before the agent starts.

## What you do yourself

1. **Create an OpenRouter key.** Sign up at [OpenRouter](https://openrouter.ai/),
   add credit under [Credits](https://openrouter.ai/settings/credits) ($5 covers
   several books and months of daily use, by our estimate), and create a key under
   [Keys](https://openrouter.ai/settings/keys). You can set a spending limit on
   the key.
2. **Create a YouTube Data API key** (free, optional). In the
   [Google Cloud console](https://console.cloud.google.com/), create a project,
   [enable the YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com),
   then create an API key under
   [Credentials](https://console.cloud.google.com/apis/credentials). Without it,
   books build fine but get no videos.
3. **Let the Mac install apps on your phone.** On the phone, open Settings →
   About phone and tap **Build number** seven times to unlock Developer options.
   Then, in Settings → System → Developer options, turn on **USB debugging** and
   connect the phone with a cable. The phone asks whether to allow USB debugging
   from this computer; tap **Allow**. The phone needs Android 12 or newer.

Give both keys to your agent, or paste them into `.env` yourself (step 2 below).

## What the agent does

1. **Install the build tools** with Homebrew, skipping any that are present:
   `openjdk@17`, `uv`, the `android-platform-tools` cask (for `adb`) and the
   `android-commandlinetools` cask. With `sdkmanager`, install
   `platforms;android-37` and `build-tools;37.0.0` and accept the licences. Set
   `JAVA_HOME` to the JDK 17 home and `ANDROID_HOME` to the SDK folder, or write
   `sdk.dir=<SDK folder>` into the ignored `local.properties`.
2. **Write `.env`** at the repository root with the reader's keys. It is
   ignored by Git.

   ```
   OPENROUTER_API_KEY=<OpenRouter key>
   YOUTUBE_API_KEY=<YouTube Data API key, or leave empty>
   ```
3. **Build and install the app.** Run `./gradlew assembleDebug`, then
   `adb install -r app/build/outputs/apk/debug/app-debug.apk`. The key is read
   from `.env` at build time, so rebuild and reinstall after changing it.
4. **Open the app once on the phone** (`adb shell am start -n
   com.alejoacelas.morningreader/.MainActivity`). This creates the folder the
   app reads books from. A folder created by `adb` instead belongs to another
   user and the app can't read it.
5. **Build books.** `./pack search "<title>"` lists Project Gutenberg matches
   with their ids. `./pack add <id> --no-push` builds a book into `packs/`.
   `./pack starter --no-push` builds the author's eight-book first shelf (listed
   as `STARTER` in `packer/__main__.py`). If YouTube's daily quota runs out, the
   book is built without videos and `./pack videos` adds them the next day.
6. **Copy the books to the phone:**
   `adb push packs/<file>.json /sdcard/Android/data/com.alejoacelas.morningreader/files/packs/`.
   The app imports them when it opens or when the reader taps refresh.
   (`./pack` can push by itself, but only through a helper script on the
   author's machine; `--no-push` plus `adb push` works everywhere.)

## Adding blog feeds

On the phone, Settings → Blog feeds: **Import OPML** loads an export from Feedly
or another feed reader, and **Add feed URL** adds one feed. Posts appear after
the next check, which runs every 12 hours, whenever the app opens with feeds
more than 6 hours stale, or on **Check now**.

## If something goes wrong

- **Explain or blog hooks fail with an "OpenRouter" error:** the app was
  probably built without a valid key or the account is out of credit. Fix `.env`, then rebuild and reinstall.
- **Books don't appear:** check that the files are in the app's `packs` folder
  on the phone and that the folder was created by opening the app (step 4).
- **`adb` sees no device:** unplug and replug the phone, and check the phone for
  the "Allow USB debugging" prompt.
