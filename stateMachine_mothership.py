# state machine to represent the requirements of the mothership for
# mission phases
from sys import stdin, stdout

def initialization():
    print("Entering Initialization State")
    # complete setup steps
    if attempt_transition(synchronizedTargetPursuit):
        return synchronizedTargetPursuit

def synchronizedTargetPursuit():
    print("Entering Synchronized Target Pursuit")
    fly_to_target(targetLong, targetLat, targetAlt)
    flying_to_dropoff = True
    while flying_to_dropoff:
        # continue to fly to target
        if is_dropoff_location_reached():
            flying_to_dropoff = False
    prepare_multirotor_release()
    if attempt_transition(deployedTargetPursuit):
        return deployedDockingPursuit


def deployedTargetPursuit():
    print("Entering Deployed Target Pursuit")
    loiter()
    if wait_for_transition_msg("loadDelivery"):
        # change state
        if attempt_transition(loadDelivery):
            return loadDelivery

def loadDelivery():
    print("Entering Load Delivery State")
    if wait_for_transition_msg("deployedDockingPursuit"):
        # change state
        if attempt_transition(deployedDockingPursuit):
            return deployedDockingPursuit

def deployedDockingPursuit():
    print("Entering Deployed Docking Pursuit")
    if wait_for_transition_msg("approximateDocking"):
        # change state
        if attempt_transition(approximateDocking()):
            return approximateDocking()

def approximateDocking():
    print("Entering Approximate Docking")
    # mothership needs to stop loitering and fly straight back
    # to home slowly
    docking_flight()
    if wait_for_transition_msg("preciseDocking"):
        # change state
        if attempt_transition(preciseDocking):
            return preciseDocking

def preciseDocking():
    print("Entering Precise Docking")
    if wait_for_transition_msg("docked"):
        # change state
        if attempt_transition(docked):
            return docked


def docked():
    print("Entering Docked")
    if wait_for_transition_msg("synchronizedHoming"):
        if attempt_transition(synchronizedHoming):
            return synchronizedHoming


def dockingErrorHandling():
    print("Entering Docking Error Handling")


def synchronizedHoming():
    print("Entering Synchronized Homing")
    fly_home()

def contigencyLanding():
    print("Entering Contingency Landing")


def start_rotors():
    print("starting rotors..")
    # start up the rotors to prepare for deployment

def fly_to_target(long, lat, alt):
    # send mothership to location above target GPS location
    # the target altitiude for the mothership is at an altitude
    # higher than the target for load delivery

def is_dropoff_location_reached():
    # checks that gps location is within dropoff location

def attempt_transition(new_state):
    # send message to other raspberry pi that a transition is requested
    return send_transition_message(new_state)



def send_transition_message(state):
    # send message
    returned_msg = "sample"
    success = False
    while not success:
        if returned_msg is state:
            success = True
    return success


def wait_for_transition_msg(state):
    transition_msg = "sample"
    success = False
    while not success:
        # check for new message
        if state is transition_msg:
            success = True
    return success


def prepare_multirotor_release():
    # slow mother ship so that the multirotor can start
    # up and release

def loiter():
    loitering = True
    # mother ship must loiter while drone delivers

def docking_flight():
    # send commands to go slow while multirotor gets ready to dock

def fly_home():
    # send commands to fly home at full speed

print("Enter GPS Location:")
targetLong, targetLat, targetAlt = map(int, stdin.readline().split())

state = initialization
while state: state=state()