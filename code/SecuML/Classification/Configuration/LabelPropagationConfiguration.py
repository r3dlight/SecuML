## SecuML
## Copyright (C) 2016  ANSSI
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

from SecuML.Classification.Classifiers.LabelPropagation import LabelPropagation
import ClassifierConfFactory
from ClassifierConfiguration import ClassifierConfiguration

class LabelPropagationConfiguration(ClassifierConfiguration):

    def __init__(self, num_folds, families_supervision, alerts_conf = None):
        ClassifierConfiguration.__init__(self, num_folds, False, families_supervision,
                alerts_conf = alerts_conf)
        self.model_class = LabelPropagation

    def getModelClassName(self):
        return 'LabelPropagation'

    def getParamGrid(self):
        return None

    def setBestValues(self, grid_search):
        return

    def getBestValues(self):
        return None

    @staticmethod
    def fromJson(obj, exp):
        conf = LabelPropagationConfiguration(obj['num_folds'], obj['families_supervision'])
        ClassifierConfiguration.setTestConfiguration(conf, obj, exp)
        return conf

    def toJson(self):
        conf = ClassifierConfiguration.toJson(self)
        conf['__type__'] = 'LabelPropagationConfiguration'
        return conf

    def probabilistModel(self):
        return True

    def semiSupervisedModel(self):
        return True

    def featureCoefficients(self):
        return False

ClassifierConfFactory.getFactory().registerClass('LabelPropagationConfiguration',
        LabelPropagationConfiguration)
