

class vibration_event:
    def __init__(self, amp, freq, duration, controller_hand, time_stamp):
        self.amplitude = amp
        self.frequency = freq
        self.duration = duration
        self.controller_hand = controller_hand
        self.time_stamp = time_stamp


class all_vibration_list:
    def __ini__(self, time_stamp, per_vibration_list, controller_hand):
        self.time_stamp = time_stamp
        self.per_vibration_list = per_vibration_list



