# python-video-server

Toy python/flask project intended as an experiment.

The app finds appropriate video files and exposes them in a coherent way, with
a list navigation, player manipulation controls and a way to play file formats
not supported by the browser.

While it's a sane idea to just display each directory with video in it as playlist
it might be an overkill to assume each directory tree with playlists to be a course.
That's why instead of guessing, server just looks for course.md files that mark
directories as course roots.

# Inspired by:

1. Player interface of online courses sites.
2. Omni-format-filesystem - idea of telpeloth - keeping media in original
    format, but with means to convert others on request

# Why?

Because I can :)
The interface based on HTML provides flexibility and can include other media easily.
Given that some courses allow downloading their video materials, it just makes sense
to have a way to browse and watch it offline or in LAN.

# Future plans

* allow playback before recoding finishes - or convert on-the-fly right to response
* add possibility to replace original files after recoding has run successfully
  * this might be configured globally or controlled by course.md file
