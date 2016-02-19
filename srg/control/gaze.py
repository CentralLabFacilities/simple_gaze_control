"""

Copyright(c) <Florian Lier>


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

# STD IMPORTS
import time
import threading

# SELF
from srg.utils.colors import BColors as c

class GazeController(threading.Thread):
    """
    The GazeController receives person messages (ROS) and derives
    the nearest person identified. Based on this, the robot's
    joint angle target's are derived using the transformation
    class below
    """
    def __init__(self, _robot_controller, _mw, _lock, _closed_loop):
        threading.Thread.__init__(self)
        self.lock         = _lock
        self.mw           = _mw
        self.run_toggle   = True
        self.acquire_prio = False
        self.lastdatum    = time.time()
        self.rc           = _robot_controller
        self.closed_loop_informer  = _closed_loop
        self.closed_loop_timeout   = 2.0
        self.target_tolerance = 5.0
        self.loop_speed   = 1.0

    def run(self):
        print ">>> Initializing Gaze Controller for: %s --> %s" % (self.mw.inscope.strip(), self.rc.outscope.strip())
        loop_count = 0
        init_time = time.time()
        while self.run_toggle is True:
            then = time.time()
            tick = time.time()
            self.lock.acquire(1)
            if self.mw.current_robot_gaze is not None and self.lastdatum != self.mw.current_robot_gaze_timestamp:
                self.lastdatum = self.mw.current_robot_gaze_timestamp
                if self.acquire_prio:
                    try:
                        current_target = self.mw.current_robot_gaze
                        self.rc.robot_controller.set_gaze_target(current_target, True)
                        if self.closed_loop_informer is not None:
                            pan, tilt = self.closed_loop_informer.get_current_head_state()
                            if self.mw.mode == "absolute":
                                while abs(pan - current_target.pan*-1) >= self.target_tolerance:
                                    time.sleep(0.025)
                                    pan, tilt = self.closed_loop_informer.get_current_head_state()
                                    # TODO FIX -1
                                    if time.time() - tick >= self.closed_loop_timeout:
                                        print c.WARNING + ">>> WARN: %s" % self.mw.inscope + c.ENDC
                                        print c.WARNING + ">>> Target Offset too high (> %d degree) --> %.2f" % (self.target_tolerance, abs(pan - current_target.pan*-1)) + c.ENDC
                                        print c.WARNING + ">>> Absolute target [%.2f | %.2f] NOT reached in %.2f sec --> Current pos. [%.2f | %.2f] " \
                                                          % (current_target.pan*-1, current_target.tilt, self.closed_loop_timeout, pan, tilt) + c.ENDC
                                        break
                    except Exception, e:
                        print ">>> ERROR (set_gaze): %s" % str(e)
                    loop_count += 1
                self.lock.release()
            else:
                self.lock.release()
            now = time.time()
            # Running with maximum frequency of 50 Hz
            hz = 0.02-(now-then)
            if tick - init_time >= 1.0:
                self.loop_speed = loop_count
                loop_count = 0
                init_time = time.time()
            if hz > 0:
                time.sleep(hz)
        print ">>> Deactivating Gaze Controller for: %s" % self.rc.outscope.strip()
