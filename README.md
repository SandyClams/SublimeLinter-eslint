SublimeLinter-eslint (sc)
=========================
this is a fork of the plugin [SublimeLinter-eslint](https://github.com/SublimeLinter/SublimeLinter-eslint). It enables that fatal/breaking errors are only displayed after a delay period specified by the user when running SublimeLinter in "background" mode. The goal is to allow lint results to display immediately if desired, but also to allow that routine typing and continuous, partially-written code doesn't overwhelm the display with irrelevant and disorienting nonsense.

## How to use it
create a top-level folder in Sublime's `Packages` directory called `SublimeLinter-eslint` and copy the files and structure of this repo into the folder. In your user settings for SublimeLinter, wherever you define your `eslint` linter, you may now specify an additional key, `delay_fatal_errors_by`. This key accepts a value in milliseconds, which represents the period of delay before the display is updated after a fatal error is first encountered. If you don't know what these things mean, you can find more introductory info at the original repo.

## Status of the thing
currently it works, and it doesn't break anything, but tweaks and improvements are planned.
