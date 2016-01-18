#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2016, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

helpStr = """
Simple script to run a labeled dataset.

Example invocations:

python simple_labels.py -m keywords --dataPath FILE --numLabels 3
python simple_labels.py -m docfp --dataPath FILE
python simple_labels.py -c data/network_configs/sensor_knn.json -m htm -v 2 --dataPath FILE
python simple_labels.py -c data/network_configs/tp_knn.json -m htm --dataPath FILE

"""

import argparse
import numpy
from textwrap import TextWrapper

from htmresearch.support.csv_helper import readDataAndReshuffle
from htmresearch.frameworks.nlp.model_factory import (
  createModel, getNetworkConfig)


wrapper = TextWrapper(width=100)

def instantiateModel(args):
  """
  Return an instance of the model we will use.
  """

  # Some values of K we know work well for this problem for specific model types
  kValues = { "keywords": 21 }

  # Create model after setting specific arguments required for this experiment
  args.networkConfig = getNetworkConfig(args.networkConfigPath)
  args.k = kValues.get(args.modelName, 1)
  model = createModel(**vars(args))

  return model


def trainModel(args, model, trainingData, labelRefs):
  """
  Train the given model on trainingData. Return the trained model instance.
  """
  print
  print "=======================Training model on sample text================"
  for recordNum, doc in enumerate(trainingData):
    document = doc[0]
    labels = doc[1]
    docId = doc[2]
    if args.verbosity > 0:
      print
      print "Document=", wrapper.fill(document)
      print "label=",labelRefs[labels[0]], "id=",docId
    model.trainDocument(document, labels, docId)

  return model


def queryModel(model, queryDocument, documentTextMap,
               labelRefs, documentCategoryMap):
  """
  Demonstrates how querying might be done with the new partitionId scheme. The
  code below assumes a document level classifier, so not appropriate for all
  model types. The implementation should be cleaned up and moved into the
  model, but this provides a basic idea.
  """

  print
  print "=================Querying model on a sample document================"
  print
  print "Query document:"
  print wrapper.fill(queryDocument)
  print

  categoryVotes, idList, distances = model.inferDocument(
                                                queryDocument,
                                                returnDetailedResults=True,
                                                sortResults=True)

  print "Here are some similar documents in order of similarity"
  for i, docId in enumerate(idList[0:10]):
    print distances[i], docId
    print "document=",wrapper.fill(documentTextMap[docId])
    print "Categories=",documentCategoryMap[docId]
    print

  print "Here are some dissimilar documents in reverse order of similarity"
  lastDocIndex = len(idList)-1
  for i in range(lastDocIndex, lastDocIndex-10, -1):
    print distances[i], idList[i]
    print "document=",wrapper.fill(documentTextMap[idList[i]])
    print


def runExperiment(args):
  """
  Create model according to args, train on training data, save model,
  restore model, test on test data.
  """

  # Read in data file
  (trainingData, labelRefs, documentCategoryMap,
   documentTextMap) = readDataAndReshuffle(args,
                         [8,9,10,5,6,11,13,0,1,2,3,4,7,12,14])

  # Create model
  model = instantiateModel(args)

  model = trainModel(args, model, trainingData, labelRefs)

  # Now query the model using some example HR complaints about managers
  queryModel(model,
             "Begin by treating the employees of the department with the "
             "respect they deserve. Halt the unfair practices "
             "that they are aware of doing. There is no compassion "
             "or loyalty to its senior employees",
             documentTextMap, labelRefs, documentCategoryMap,
             )

  queryModel(model,
             "My manager is really incompetent. He has no clue how to "
             "properly supervise his employees and keep them motivated.",
             documentTextMap, labelRefs, documentCategoryMap,
             )

  queryModel(model,
             "I wish I had a lot more vacation and much more flexibility "
             "in how I manage my own time. I should be able to choose "
             "when I come in as long as I manage to get all my tasks done.",
             documentTextMap, labelRefs, documentCategoryMap,
             )

  # Print profile information
  print
  model.dumpProfile()

  return model


if __name__ == "__main__":

  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description=helpStr
  )

  parser.add_argument("-c", "--networkConfigPath",
                      default="data/network_configs/sensor_knn.json",
                      help="Path to JSON specifying the network params.",
                      type=str)
  parser.add_argument("-m", "--modelName",
                      default="htm",
                      type=str,
                      help="Name of model class. Options: [keywords,htm]")
  parser.add_argument("--retinaScaling",
                      default=1.0,
                      type=float,
                      help="Factor by which to scale the Cortical.io retina.")
  parser.add_argument("--numLabels",
                      default=3,
                      type=int,
                      help="Number of unique labels to train on.")
  parser.add_argument("--retina",
                      default="en_associative_64_univ",
                      type=str,
                      help="Name of Cortical.io retina.")
  parser.add_argument("--apiKey",
                      default=None,
                      type=str,
                      help="Key for Cortical.io API. If not specified will "
                      "use the environment variable CORTICAL_API_KEY.")
  parser.add_argument("--modelDir",
                      default="MODELNAME.checkpoint",
                      help="Model will be saved in this directory.")
  parser.add_argument("--dataPath",
                      default=None,
                      help="CSV file containing labeled dataset")
  parser.add_argument("--textPreprocess",
                      action="store_true",
                      default=False,
                      help="Whether or not to use text preprocessing.")
  parser.add_argument("-v", "--verbosity",
                      default=1,
                      type=int,
                      help="verbosity 0 will print out experiment steps, "
                           "verbosity 1 will include results, and verbosity > "
                           "1 will print out preprocessed tokens and kNN "
                           "inference metrics.")
  args = parser.parse_args()

  # By default set checkpoint directory name based on model name
  if args.modelDir == "MODELNAME.checkpoint":
    args.modelDir = args.modelName + ".checkpoint"

  model = runExperiment(args)
