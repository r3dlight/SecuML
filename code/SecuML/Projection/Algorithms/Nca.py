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

import metric_learn
import numpy as np

from SemiSupervisedProjection import SemiSupervisedProjection

class Nca(SemiSupervisedProjection):

    def __init__(self, experiment):
        SemiSupervisedProjection.__init__(self, experiment)
        self.projection = metric_learn.nca.NCA(num_dims = self.num_components)

    def setProjectionMatrix(self):
        self.projection_matrix = np.transpose(
                self.pipeline.named_steps['projection'].transformer())
