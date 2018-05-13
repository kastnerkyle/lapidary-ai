
# Lapidary AI

An AI for the board game
[Splendor](https://boardgamegeek.com/boardgame/148228/splendor), using
a simple neural let trained with reinforcement learning.

This repository includes Python code implementing the mechanics of
Splendor, code for training the AI using Tensorflow, and a standalone
browser-based gui.

You can play against the current version of the AI online at
https://inclement.github.io/lapidary-ai/.

The Lapidary AI currently only supports two players, but only because
this is what I've focused on training so far. I hope to train networks
for three and four players soon.

# AI details

The AI uses a simple neural network with a single hidden layer. It is
trained by reinforcement learning: the network starts with random
parameters, but then plays many games against itself. Its network is
updated along the way based on the results of these games. Essentially,
when it wins its parameters are tweaked to encourage it to play the
same moves in the future, or when it loses those moves are
discouraged.

The current version of the AI is the result of ~10000 self-play
games. At this point, its behaviour is very stable and it learns very
little, but it has become fairly competent at the game. In self-play
games it wins in an average of ~29.3 rounds in 2 player games, about
0.5 rounds longer than the [official app average in human-bot
games](https://cf.geekdo-images.com/original/img/CRMjuJdl5jEWZy8u4f7BjNAt09Y=/0x0/pic2585590.png). That
seems to mean the AI is doing something right, but it's still well
behind strong human play. In particular, it only really learns to
optimise a strategy based on buying many tier 1 cards

The actual training involves a range of tweakable parameters and
choices in network structure. I'm sure there's a lot of room for
improvement on the current version.

# Web gui details

The web gui reimplements all the game logic and neural net evaluations
in javascript. The gui is built using
[Vue.js](https://vuejs.org/). It's a fairly bare bones implementation
of the game for now, but should let you play the game well enough.

Since the web gui is completely standalone, it can be downloaded and
run offline if you like.
