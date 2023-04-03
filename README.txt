I like working on random things, so I recently starting making some scripts regarding AI, and just decided to play around with computer vision.
This repository is just a little project of mine, where I played around with the OpenCV python library and made a bot look at a little window of Old School Runescape, an instance of the RuneLite launcher to be specific.
Didn't bother with targeting the window, as that's not the point of the project, so I just shoved in top left of the screen and scaled down the screen capture window in order to maximize the screenshots/second performance.
It simply has a few images of a cow from different angles and a screenshot of a hide drop, it scans the screen for any of those images and then simply clicks at it's location. Had to implement a little algorithm that detects if the cow was hit or not, since it tends to miss them, after discovering that maybe python wasn't the smartest language to code this in, but hey, it works as a proof of concept.

Thinking of improving this project using the pytorch library, but decided not to, as the screenshot perfomance will not be the best anyways.
Feel free to play around with this. Why runescape you may ask, well, I don't really know much about runescape, but found it to be a good game to try running computer vision automation on, and I think I wasn't wrong.
