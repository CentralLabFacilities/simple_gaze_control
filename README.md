# Simple Robot Gaze Config File

The Simple Robot Gaze component coordinates a Robot's gaze direction.
This can be done by a) providing (multiple) input sources and by b) prioritizing them.
For now, the component accepts ROS People messages [1] and ROS RegionOfInterest messsages [2]
then derives the corresponding robot joint angle configuration using the HLRC [3] library.
This is accomplished by mapping from the region of interest (faces, ittikoch...) to the camera's
field of view, robot joint angles respectively.

This file must reside in ~/.config/simplerobotgaze.yaml

In order to pause robot gaze from controlling the robot simply send "true" (bool msg) to:

    $prefix/robotgaze/set/pause using either RSB or ROS.


In order to directly send gaze targets send PointStamped msgs (ROS) or SphericalDirectionFloat (RSB) to:

    $prefix/robotgaze/set/gaze


# ROS remote control support is enabled by default, if you wish to control Gaze remotely via
# RSB set this to "1"
enable_rsb_remote_control:
  - 0


The priority of input data streams, the first entry has the highest priority

    priorities:
        - /robotgazetools/faces
        - /robotgazetools/saliency

This client features various remote control functions, these are usually available
under /$scope_topic_prefix/robotgaze/something. The default is /robot/robotgaze/something

    scope_topic_prefix:
        - robot


What kind of data are you sending in your input stream, corresponds to priorities. Currently implemented:
ROS: ros:People, ros:PointStamped
RSB: rsb:faces, rsb:SphericalDirectionFloat

    datatypes:
    - ros:People
    - rsb:SphericalDirectionFloat


Resolution of the source camera image, corresponds to the priorities

    resolution:
        - 320x240
        - 320x240

Camera field of view horizontal and vertical (in degree), also corresponds to the priorities.

    fov:
        - 66.0x40.0
        - 66.0x40.0

Gaze strategy: relative for moving cameras, absolute for fixed setups, corresponds to the priorities

    modes:
        - relative
        - absolute

Skip stimulus input x for n seconds. For example: only react every three seconds on stimulus input would be "3.0"
This corresponds to priorities. The highest allowed value _must_ be less than "boring_timeout" (see below).

    stimulus_timeout:
        - 0.0
        - 0.0

Based on the input streams (see: priorities). When is a stimulus considered "boring", e.g., no new messages for n
seconds. The last received timestamp is always evaluated.
For example: time.now() - timestamp_last_message >= boring_timeout: proceed to the next priority level.

    boring_timeout:
        - 1.0

See "peak_override"

    allow_peak_override:
        - 1

Peak override: Provide a value that is encoded in your stimulus input messages, e.g, size of face in pixels in order
to override the base priotrity. This field is only evaluated if allow_peak_override is "1" (see above).
Example: your first priority is facedetection. However, if there is massive motion detected in the second priority,
override the first priority. Corresponds priorities.

    peak_overrides:
        - 100.0
        - 10.0