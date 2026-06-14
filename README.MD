# Explanation

# Installation

Requires the packet manager `uv'. Run
> source scripts/install.sh

Download the images
> cd images && hf sync hf://buckets/e-zorzi/coin_challenge_images .
> 
# Oracle

To train/test your questioner, you need an Oracle. You can implement it however you want, but it needs to inherit from the class `QuestionerInterface` (see file `Questioner.py`). We provide two 
