# Naive Bayesian classification model for binary vectors.

# The binary vectors basically represent the on/off state of each
# feature within the respective vector,
# based on which, we build our naive bayesian classification model.
#

from __future__ import division
import sys
sys.dont_write_bytecode = True
import math


class naive_bayes(object):

    def __init__(self, data, features_set):
        self.data = data
        self.features = features_set

    """processes and builds prior probabilities, probabilities of evidences and
     probabilities of likelyhood.

    """
    def process(self):
        self.probs = {}
        self.all_labels = list(set([a[0] for a in self.data]))
        print(self.all_labels)
        self.probs['labels_c'] = {}
        self.probs['labels_p'] = {}
        self.probs['features_c'] = {}
        self.probs['features_p'] = {}
        self.probs['likelyhood_p'] = {}
        self.probs['likelyhood_c'] = {}
        # transposed features for calculating evidence probabilities
        k = zip(*map(lambda n: n[1], self.data))

        # calculating prior probabilities
        for a in self.data:
            if self.probs['labels_c'].has_key(a[0]):
                self.probs['labels_c'][a[0]] += 1
            else:
                self.probs['labels_c'][a[0]] = 1
            self.probs['labels_p'][a[0]] = self.probs['labels_c'][a[0]] / len(self.data)

        # calculating evidence probabilities
        for i in range(0, len(k)):
            current_feature = k[i]
            self.probs['features_c'][self.features[i]] = len(filter(lambda q: q > 0, current_feature))
            self.probs['features_c']['not_'+self.features[i]] = len(filter(lambda q: q < 1, current_feature))
            self.probs['features_p'][self.features[i]] = self.probs['features_c'][self.features[i]]/len(self.data)
            self.probs['features_p']['not_'+self.features[i]] = self.probs['features_c']['not_'+self.features[i]]/len(self.data)

        #calculating likelyhood probabilities
        for i in range(0, len(self.features)):
            self.probs['likelyhood_c'][self.features[i]] = {}
            self.probs['likelyhood_p'][self.features[i]] = {}
            self.probs['likelyhood_c']['not_'+self.features[i]] = {}
            self.probs['likelyhood_p']['not_'+self.features[i]] = {}
            for b in self.data:
                if b[1][i] == 1:
                    if self.probs['likelyhood_c'][self.features[i]].has_key(b[0]):
                        self.probs['likelyhood_c'][self.features[i]][b[0]] += 1
                    else:
                        self.probs['likelyhood_c'][self.features[i]][b[0]] = 1
                    self.probs['likelyhood_p'][self.features[i]][b[0]] = self.probs['likelyhood_c'][self.features[i]][b[0]]/self.probs['labels_c'][b[0]]
                else:
                    if self.probs['likelyhood_c']['not_'+self.features[i]].has_key(b[0]):
                        self.probs['likelyhood_c']['not_'+self.features[i]][b[0]] += 1
                    else:
                        self.probs['likelyhood_c']['not_'+self.features[i]][b[0]] = 1
                    self.probs['likelyhood_p']['not_'+self.features[i]][b[0]] = self.probs['likelyhood_c']['not_'+self.features[i]][b[0]]/self.probs['labels_c'][b[0]]

    #predictor method
    #calculates conditional probabilities for all the unique labels and
    #returns the one with max score.
    def predict(self, vector, key_only=False):
        all_features_rep = []
        for i in range(0, len(vector)):
            if vector[i]:
                all_features_rep.append(self.features[i])
            else:
                all_features_rep.append('not_'+self.features[i])

        divisor = 1
        for a in all_features_rep:
            divisor *= self.probs['features_p'][a]

        results = {}
        for i in range(0, len(self.all_labels)):
            t = 1
            for j in range(0, len(all_features_rep)):
                if self.probs['likelyhood_p'][all_features_rep[j]].has_key(self.all_labels[i]):
                    t *= self.probs['likelyhood_p'][all_features_rep[j]][self.all_labels[i]]
                else:
                    t *= 0
            results[self.all_labels[i]] = (self.probs['labels_p'][self.all_labels[i]]*t)/divisor

        if key_only:
            return max(results, key=results.get)
        else:
            return results
