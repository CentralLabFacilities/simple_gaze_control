"""

This file is part of FINITE STATE MACHINE BASED TESTING.

Copyright(c) <Florian Lier, Simon Schulz>
http://opensource.cit-ec.de/fsmt

This file may be licensed under the terms of the
GNU Lesser General Public License Version 3 (the ``LGPL''),
or (at your option) any later version.

Software distributed under the License is distributed
on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
express or implied. See the LGPL for the specific language
governing rights and limitations.

You should have received a copy of the LGPL along with this
program. If not, go to http://www.gnu.org/licenses/lgpl.html
or write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

The development of this software was supported by the
Excellence Cluster EXC 277 Cognitive Interaction Technology.
The Excellence Cluster EXC 277 is a grant of the Deutsche
Forschungsgemeinschaft (DFG) in the context of the German
Excellence Initiative.

Authors: Florian Lier, Simon Schulz
<flier, sschulz>@techfak.uni-bielefeld.de

"""

# STD
import time
import threading

# PyQT
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot


class Viz(QtGui.QWidget):
    def __init__(self, _input_source, _gaze_controller, _arbitration):
        super(Viz, self).__init__()
        self.run = True
        self.layout = QtGui.QHBoxLayout(self)
        self.label = QtGui.QLabel("Current Stimulus:")
        # self.label.setFixedWidth(200)
        self.layout.addWidget(self.label)
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)
        self.layout.addWidget(self.textbox)
        self.button = QPushButton('click.', self)
        self.button.move(20, 80)
        self.layout.addWidget(self.button)
        self.arbitration  = _arbitration
        self.input_sources   = _input_source
        self.gaze_controller = _gaze_controller
        self.init_ui()

    def run(self):
        t = threading.Thread(target=self.get_winning_stimulus)
        t.start()

    def get_winning_stimulus(self):
        while self.run:
            if self.arbitration.winner is not None:
                self.textbox.setText(self.input_sources[self.arbitration.winner].inscope)
            time.sleep(0.1)

    @pyqtSlot()
    def on_click(self):
            pass

    def init_ui(self):
        self.setGeometry(100, 100, 640, 480)
        self.setWindowTitle(":: Florian's Simple Robot Gaze ::")
        self.button.clicked.connect(self.on_click)
        self.show()