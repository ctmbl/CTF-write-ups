**[TO BE IMPROVED]**

it's UAF exploit

 - we will redirect the exec flux to the execl call in the admin function
 - we need:
  - to control rip
  - to leak PIE (but not ASLR)
 - we can control rip by:
  - creating a robot
  - destroying the robot
  - writing a user guide (payload)
  - making the robot speak (UAF of robot pointing to userguide)
 - we leak PIE by:
  - creating a robot
  - destroying it
  - writing an empty user guide
  - reading user guide (this leaks bleep and roll addresses)
