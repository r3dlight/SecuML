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

from SecuML.ActiveLearning.Configuration import ActiveLearningConfFactory
from SecuML.Experiment import ExperimentFactory
from SecuML.Experiment.Experiment import Experiment
from SecuML.Classification.Configuration.TestConfiguration import TestConfiguration

class ActiveLearningExperiment(Experiment):

    def __init__(self, project, dataset, db, cursor):
        Experiment.__init__(self, project, dataset, db, cursor)
        self.kind = 'ActiveLearning'
        self.labeling_method = None

    def setValidation(self, validation_dataset):
        self.validation_conf = None
        if validation_dataset is not None:
            self.validation_conf = TestConfiguration()
            self.validation_conf.setTestDataset(validation_dataset, self)

    def setConfiguration(self, conf):
        self.conf = conf
        self.labeling_method = self.conf.labeling_method

    def generateSuffix(self):
        suffix = ''
        suffix += '__' + self.labeling_method
        suffix += self.conf.generateSuffix()
        if self.validation_conf is not None:
            suffix += '__Validation' + self.validation_conf.test_dataset
            suffix += str(self.validation_conf.test_exp.experiment_id)
        return suffix

    @staticmethod
    def fromJson(obj, db, cursor):
        experiment = ActiveLearningExperiment(obj['project'], obj['dataset'], db, cursor)
        Experiment.expParamFromJson(experiment, obj)
        experiment.labeling_method  = obj['labeling_method']
        # Validation configuration
        experiment.validation_conf = None
        if obj['validation_conf'] is not None:
            experiment.validation_conf = TestConfiguration.fromJson(obj['validation_conf'], experiment)
        experiment.conf = ActiveLearningConfFactory.getFactory().fromJson(obj['conf'], experiment)
        return experiment

    def toJson(self):
        conf = Experiment.toJson(self)
        conf['__type__'] = 'ActiveLearningExperiment'
        conf['labeling_method'] = self.labeling_method
        if self.validation_conf is not None:
            conf['validation_conf'] = self.validation_conf.toJson()
        else:
            conf['validation_conf'] = None
        conf['conf'] = self.conf.toJson()
        return conf

    def webTemplate(self):
        return 'ActiveLearning/active_learning.html'

    def getCurrentIteration(self):
        query  = 'SELECT current_iter FROM InteractiveExperiments '
        query += 'WHERE id = ' + str(self.experiment_id) + ';'
        self.cursor.execute(query)
        current_iter = self.cursor.fetchone()[0]
        return current_iter

ExperimentFactory.getFactory().registerClass('ActiveLearningExperiment', ActiveLearningExperiment)
