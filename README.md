# sorter-2

Documentation of I2C Commands (so I dont have to look them up every time):

step(int drv, int steps, int dir, int ms)
  uses the ms multiplier to make as many steps as needed. 1 step = 1x/1y/1z

step2(int drv1, int drv2, int steps, int dir, int ms)
  same as step but does it for 2 drvs at the same time
  
