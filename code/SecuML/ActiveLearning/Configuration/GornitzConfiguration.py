## SecuML
## Copyright (C) 2017  ANSSI
##
## SecuML is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## SecuML is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with SecuML. If not, see <http://www.gnu.org/licenses/>.

import ActiveLearningConfFactory
from ActiveLearningConfiguration import ActiveLearningConfiguration
from SecuML.ActiveLearning.QueryStrategies.Gornitz import Gornitz
from SecuML.Classification.Configuration import ClassifierConfFactory

def gornitzBinaryModelConf():
    classifier_args = {}
    classifier_args['num_folds']            = 4
    classifier_args['sample_weight']        = False
    classifier_args['families_supervision'] = False
    classifier_args['alerts_conf']          = None
    binary_model_conf = ClassifierConfFactory.getFactory().fromParam('Sssvdd', classifier_args)
    binary_model_conf.setUnlabeled(labels_annotations = 'annotations')
    return binary_model_conf

class GornitzConfiguration(ActiveLearningConfiguration):

    def __init__(self, auto, budget, batch):
        ActiveLearningConfiguration.__init__(self, auto, budget)
        self.labeling_method = 'Gornitz'
        self.batch           = batch
        self.setBinaryModelConf()

    def setBinaryModelConf(self):
        conf = {}
        conf['binary'] = gornitzBinaryModelConf()
        ActiveLearningConfiguration.setModelsConf(self, conf)

    def getStrategy(self, iteration):
        return Gornitz(iteration)

    def generateSuffix(self):
        suffix  = ''
        suffix += '__' + str(self.batch)
        return suffix

    @staticmethod
    def fromJson(obj, experiment):
        conf = GornitzConfiguration(obj['auto'], obj['budget'], obj['batch'])
        return conf

    def toJson(self):
        conf = ActiveLearningConfiguration.toJson(self)
        conf['__type__'] = 'GornitzConfiguration'
        conf['batch']    = self.batch
        return conf

    @staticmethod
    def generateParser(parser):
        al_group = ActiveLearningConfiguration.generateParser(parser)
        al_group.add_argument('--batch',
                type = int,
                default = 100,
                help = 'Number of annotations asked from the user at each iteration.')

    @staticmethod
    def generateParamsFromArgs(args):
        params = ActiveLearningConfiguration.generateParamsFromArgs(args)
        params['batch'] = args.batch
        return params

ActiveLearningConfFactory.getFactory().registerClass('GornitzConfiguration',
        GornitzConfiguration)
