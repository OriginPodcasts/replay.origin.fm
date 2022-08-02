# About Replay

A Podcast feed is a document that lists the episodes
in a given podcast. Each entry in the feed has a
title, a date, and an ddress for the audio file.

Replay makes a few tweaks to a podcast feed, to
change the dates so that the first few episodes can
be heard instantly, with subsequent episodes
delivered in the original cadence.

That means if you rewind a daily podcast, you'll get
an archived episode every day, starting from episode
one. If you rewind a wekly podcast, you'll get each
episode in order, week by week.

We use today's date as the new starting point for
episdoe one, and actually fast-forward a couple of
weeks from that point, so you'll get the first two
episodes (or more if the show is more frequent). That
way you can evaluate the podcast over a few episodes
before deciding to stick with it or not.

## Who made this and why

I made this! Hi, I'm
[Mark Steadman](https://twitter.com/amarksteadman/).
I run a company called [Origin](https://origin.fm/).
I provide support for podcasters and the podcast
industry.

I built Replay to keep my coding muscles toned, and
because it's the sort of obscure-but-useful tool I
like to see exist in the world.

## Points of order

* Rewind does not alter the original feed (there's
  no way for it to do that). It doesn't re-host any
  media, so if you're a podcaster, your stats will
  show normal listening activity.

* The tool doesn't rewrite the feed completely; it
  just changes a few things. An `<itunes:block>` tag
  is added so that the feed can't be indexed by Apple
  Podcasts, and email addresses are removed from the
  `<itunes:owner>` and `<managingEditor>` tags where
  possible.

* There are no user accounts and no statistics being
  gathered about subscribers or feed owners. There
  isn't much of a database powering it, either. I
  list the feeds that have been rewound and the date
  the feed was requested, but no user activity is
  logged at all.

* If you have any questions or concerns (or if, for
  some reason you want to block a feed from being
  rewound), you can email
  [mark@origin.fm](mailto:mark@origin.fm?subject=About%20replay.origin.fm).
