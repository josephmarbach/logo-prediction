# Predict Analysis Plan

## Image Analysis Plan
* Time on screen (number of unique frames/images the logo appears in)
* Number of time the logo appears

## Logo Analysis Plan
* Size of logo on Screen

    ***NOTE*** This could be odd if the assumption that the logos are the same size does not hold true.

* Straightness of logo
* Clarity of logo

## Opportunistic Analysis
* Amount of time player or focal point of image is near logo
  * This could also be done assuming center of screen is focal point.
* Amount of time logo is blocked by ball person
  * This will likely be based on when the other logos are visible and ours is not and a person is detected.
* Movement detection and logo proximity to this movement

## Notables/Quality Control
* ***Note:*** The prompt only asks if we should favor someone else's positions therefore doing this at a "brand level" and not differentiating the individual locations.
* ***Note:*** Some of the logos have a different number of positions so this should be normalized in the image level analysis.
* ***Note:*** A small US Logo also appears in some close up images.  Only appears in ~1% of sampled data but if STATS are very close may need to implement correction.
* ***Note:*** The Emirates Airlines is double counted in some images.  Only occurs in ~1% of sampled data but if STATS are very close may need to implement correction.
