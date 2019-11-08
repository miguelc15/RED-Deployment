from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

import argparse



print 'Connecting to vehicle on '
vehicle = connect('/dev/ttyS0', wait_ready=True, baud=921600)



def get_location_metres(original_location, dNorth, dEast):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the
    specified `original_location`. The returned Location has the same `alt` value
    as `original_location`.
    The function is useful when you want to move the vehicle around specifying locations relative to
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt)






def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.
    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5



def distance_to_current_waypoint():
    """
    Gets distance in metres to the current waypoint.
    It returns None for the first waypoint (Home location).
    """
    nextwaypoint = vehicle.commands.next
    if nextwaypoint==0:
        return None
    missionitem=vehicle.commands[nextwaypoint-1] #commands are zero indexed
    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z
    targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint


def download_mission():
    """
    Download the current mission from the vehicle.
    """
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready() # wait until download is complete.



def adds_square_mission(aLocation, aSize):
    """
    Adds a takeoff command and four waypoint commands to the current mission.
    The waypoints are positioned to form a square of side length 2*aSize around the specified LocationGlobal (aLocation).
    The function assumes vehicle.commands matches the vehicle mission state
    (you must have called download at least once in the session and after clearing the mission)
    """

    cmds = vehicle.commands
    #cmds.wait_ready()
    print " Clear any existing commands"
    cmds.clear()
    
    print " Define/add new commands."
    # Add new commands. The meaning/order of the parameters is documented in the Command class.
     
    #Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
    cmd1 =  Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10)
    cmds.add(cmd1)

    #Define the four MAV_CMD_NAV_WAYPOINT locations and add the commands
    point1 = get_location_metres(aLocation, aSize, -aSize)
    point2 = get_location_metres(aLocation, aSize, aSize)
    point3 = get_location_metres(aLocation, -aSize, aSize)
    point4 = get_location_metres(aLocation, -aSize, -aSize)
    cmd2 = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point1.lat, point1.lon, 11)
    cmds.add(cmd2)
    bHlat = 28.0637535
    bHlon = -80.6279969
    back_boi_lat = 28.0620180
    back_boi_lon = -80.6281505
    cmd3 = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, bHlat, bHlon, 12)
    cmds.add(cmd3)
    
    cmd_flyhome = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, back_boi_lat, back_boi_lon, 13)
    cmds.add(cmd_flyhome)
   
    cmd7 = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, back_boi_lat, back_boi_lon, 0)
    cmds.add(cmd7)
    
    
    cmd13 =  Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, back_boi_lat, back_boi_lon, 10)
    cmds.add(cmd13)
    
    cmd4 = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point3.lat, point3.lon, 13)
    cmds.add(cmd4)
    
    cmd5 = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14)
    
    cmds.add(cmd5)
    #add dummy waypoint "5" at point 4 (lets us know when have reached destination)
    cmd6 = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14)
    cmds.add(cmd6)

    print(" Upload new commands to vehicle")
    cmds.upload()


def arm_and_takeoff(aTargetAltitude):
    print "Basic pre-arm checks"
  #  while not vehicle.is_armable:
   #     print " Waiting for vehicle to initialise..."
    #    time.sleep(1)
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    #while not vehicle.armed:
        #print " Waiting for arming..."
       # time.sleep(1)
    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to ta$
    # Check that vehicle has reached takeoff altitude
    while True:
        print " Altitude: ", vehicle.location.location.global_relative_frame.lat, vehicle.location.global_relative_frame.alt,
              vehicle.location.global_relative_frame.lon
                #, vehicle.location.global_relative_frame.lat
        # Break and return from function just below target al$
#       print " Battery: %s" % vehicle.battery
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95
            print "Reached target altitude"
            break
        time.sleep(1)

  

print ('Create a new mission (for current location)')
adds_square_mission(vehicle.location.global_frame,30)


# From Copter 3.3 you will be able to take off using a mission item. Plane must take off using a mission item (currently).
arm_and_takeoff(10)

print("Starting mission")
# Reset mission set to first (0) waypoint
vehicle.commands.next=0

# Set mode to AUTO to start mission
vehicle.mode = VehicleMode("AUTO")





# Monitor mission.
# Demonstrates getting and setting the command number
# Uses distance_to_current_waypoint(), a convenience function for finding the
#   distance to the next waypoint.

while True:
    nextwaypoint=vehicle.commands.next
    print('Distance to waypoint (%s): %s' % (nextwaypoint, distance_to_current_waypoint()))
  
    if nextwaypoint==2:
        time.sleep(1)
    if nextwaypoint==3: #Skip to next waypoint
        print('Skipping to Waypoint 5 when reach waypoint 3')
        vehicle.commands.next = 5
    if nextwaypoint==5: #Dummy waypoint - as soon as we reach waypoint 4 this is true and we exit.
        print("Exit 'standard' mission when start heading to final waypoint (5)")
        break;
    time.sleep(1)

print('Return to launch')
vehicle.mode = VehicleMode("RTL")
print("Now let's land")
vehicle.mode = VehicleMode("LAND")


#Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
