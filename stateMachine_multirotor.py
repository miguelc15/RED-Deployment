# state machine to represent the requirements of the multirotor for
# mission phases
from sys import stdin, stdout


def initialization():
    print("Entering Initialization State")
    # complete setup steps
    # change state
    if attempt_transition(synchronizedTargetPursuit):
        return synchronizedTargetPursuit


def synchronizedTargetPursuit():
    print("Entering Synchronized Target Pursuit")
    # wait for mothership to get to location above target
    if wait_for_transition_msg("deployedTargetPursuit"):
        # change state
        if attempt_transition(deployedTargetPusuit):
            return deployedDockingPursuit


def deployedTargetPusuit():
    print("Entering Deployed Target Pursuit")
    start_rotors()
    release_multirotor()
    if attempt_transition(loadDelivery):
        return loadDelivery

def loadDelivery():
    print("Entering Load Delivery State")
    if fly_to_target():
        release_load()
    if attempt_transition(deployedDockingPursuit):
        return deployedDockingPursuit

def deployedDockingPursuit():
    print("Entering Deployed Docking Pursuit")
    if fly_back_to_mothership():
        if attempt_transition(approximateDocking):
            return approximateDocking


def approximateDocking():
    print("Entering Approximate Docking")
    if dock_ready():
        if attempt_transition(preciseDocking):
            return preciseDocking

def preciseDocking():
    print("Entering Precise Docking")
    if dock():
        if attempt_transition(docked):
            return docked
    else:
        if attempt_transition(dockingErrorHandling):
        return dockingErrorHandling

def docked():
    print("Entering Docked")
    turn_off_rotors()
    if attempt_transition(synchronizedHoming):
        return synchronizedHoming

def synchronizedHoming():
    print("Entering Synchronized Homing")

def dockingErrorHandling():
    print("Entering Docking Error Handling")


def synchronizedHoming():
    print("Entering Synchronized Homing")


def contigencyLanding():
    print("Entering Contingency Landing")

def start_rotors():
    print("starting rotors..")
    # start up the rotors to prepare for deployment


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

def release_multirotor():
    # send command to have mothership release the multirotor

def fly_to_target():
    # send drone to target location
    reached = False
    while not reached:
        # check if GPS location is target location
        if ready_to_deliver():
            reached = True
    return reached

def ready_to_deliver():
    # check target location with multirotor GPS location
    in_delivery_position = False
    while not in_delivery_position:
        # check
        # if yes
        # in_delivery_position = True
    return in_delivery_position

def release_load():
    # release payload


def fly_back_to_mothership():
    # command the multirotor to go to a docking position
    # which should be at an altitude lower than the
    # GPS location that it was released from
    in_docking_position = False
    while not in_docking_position:
        # check if it is in docking position
        # if it is
        # in_docking_position = True
    return in_docking_position


def dock_ready():
    # image tracking
    ready_to_dock = False
    while not ready_to_dock:
        # check that the multirotor is ready to dock
        # if it is
        # ready_to_dock = True
    return ready_to_dock


def dock():
    # send commands to send multirotor into the docking mechanise
    success = False
    # wait for signal that docking was successful
    # if it is
    # success = true
    return success

def turn_off_rotors():
    # turn off the rotors


print("Enter GPS Location:")
targetLong, targetLat, targetAlt = map(int, stdin.readline().split())

state = initialization
while state: state=state()