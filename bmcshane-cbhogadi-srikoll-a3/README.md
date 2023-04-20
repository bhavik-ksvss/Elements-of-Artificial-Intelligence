# Assignment 3
### bmcshane, cbhogadi, srikoll

## Part 1 : Part Of Speech Tagging
**Goal:** Mark every word in a sentence with its part of speech (noun, verb, adjective, etc.).

**Approach:**
The Skeletal code provided by the professor returns noun as pos for all the words in a sentence for all three methods.
Here we have a dataset of bc.train on which we need to implement Bayes Nets,Viterbi and MCMC using Gibbs Sampling. Intially we calculated all the prior probabilities and maintained a lookup which had all the word frequencies wrt its pos. Made a list of all the parts of speech and also kept track of their transistions. Here transition_prob is referred to probability from one pos to another.Then calculated all the probabilities of all the combinations of transitions. Emission probabilty is probability of the word given the pos.
 
**Method 1:(SIMPLE)** Here we have implemented BAYES NET to find all the pos for each word in a given sentence.Considering each word, we found out all the probabilties of that with respect to all the Parts of speech and then use the maximum probabilty to make the final pos for respective word. Fortunately, It worked well for the simple model we used here. Achieved an accuracy of 92% on words and 39% on sentences.

**Method 2:(HMM)** Here we have implemented VITERBI algorithm to optimize and improve the accuracy of the simple model.Apart from the initial state probability and emission probability, we also make use of the transition probabilties and by combininig all of it, we get the correct pos of the sentence. It worked pretty well and has good improvement over the accuracy. Accuracy achieved on words is nearly 94% and 47% on sentences.

**Method 3:(MCMC)** Here we implement Gibbs Sampling where in we consider random pos for all the words of the sentence. For each pos, sample a value of pos from the list of 12 pos's and shuffle the sample. Over a huge number of iterations like 5000 in this case, we have got very less accuracy of 25% on words and 0% on sentences.


## Part 2
I imported copy for this part.

So the first thing to to think about when we're starting with the simple bayes net is the emission probabilities, considering we're not implementing a full hmm we don't need to incorporate transition probabilities just yet. We just need to look at the given pixel values and edge strengths and come up with a way to compute P(observed column values | any possible row for the border placement). We're gonna start with the air-ice border, the way I'm calculating emission probabilities is a heuristic of (edge_strength)/(greyscale_value), so the darker the pixel and the stronger the edge the higher a score it gets. Afterwards I'm gonna normalize to 1 to make it feel more like probabilities although that doesn't necessarily do anything. I may need to look at the Q&A and make sure I'm doing this right, and for the air-ice border I'll probably try to factor in distance from the top of the screen into the heuristic (the further from the top the less likely the pixel is going to contain the air-ice border). For the ice-rock border any pixel less than 10 pixels lower than the air-ice border will have a emission probability of 0

For the transition probabilities I'm going to use a makeshit gaussian distribution pdf where the mean is the previous row for the given border and I'll have to play around with the variance (apparently 1-10 is the range we're looking at)


## Part 3
I imported math and copy for this part, hope that's okay.

For this, the emission probabilities are going to be calculated comparing the pixels of the test image with the pixels of the training images for each letter. This is done based off the percentage of pixels that are noisy (essentially inverted), m. m should be somewhere between 2 and 30 ish but I'll either have to play around a little with it or calculate it based off the corpus. The corpus option seems unnecessarily complicated.

The transition probabilities will be calculated through the corpus. Every time a given_word occurs, we'll store the counts of all the words that occur after given_word, in a nested dictionary (dic[given_word][word_that_occurs_after]), and then normalize them to sum to 1 to represent probabilities. 

From there it should just be using emission probabilities to run the simple algorithm, and then both emission and transition probabilities to run Viterbi on the test image

As of now I have my simple method working which means my emission probability method should fine, but my viterbi method is going haywire. I have the same algorithm in part 2 which seems to be doing fine, so I'm thinking it has something to do with my transition_probabilities function I just can't figure it out for the life of me.