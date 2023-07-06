# @author  : Zhu ZhenDong
# @time    : 2023-07-03 10-59-01
# @function:
# @version :

from pathlib import Path
from pymycobot import MyCobot
import json
from datetime import datetime


class Tester:

    """Tester for robot parameters."""

    def __init__(self, serial, robot_name, model_name) -> None:
        self.json_data = {}
        self.load_json(Path("tests/data"), "firmware_version")
        self.load_json(Path("tests/data"), model_name)
        self.serial: MyCobot = serial
        self.robot_name: str = robot_name
        self.servo_count: int = self.json_data[model_name]["joint_n"]
        self.test_log: list = []

    def load_json(self, path: Path, name):
        with open(f"{path/name}.json", "r") as f:
            data = json.loads(f.read())
            self.json_data[name] = data

    # decorator for penetrate mode
    def penetration_mode(func):
        def wrapper(self, *args, **kw):
            self.serial.set_communicate_mode(1)
            res = func(self, *args, **kw)
            self.serial.set_communicate_mode(0)
            return res

        return wrapper

    def clear_test_log(self):
        self.test_log.clear()

    def get_test_log(self):
        return self.test_log

    def make_log(self, success: bool, msg: str):
        log_template: str = "[{status}] {time} {msg}"
        status = "PASS" if success else "FAIL"
        log_time = datetime.now()
        log_str = log_template.format(status=status, time=log_time, msg=msg)
        self.test_log.append(log_str)

    @penetration_mode
    def test_servo(self) -> bool:
        success = True

        # test for servo communication
        for servo_id in range(1, self.servo_count + 1):
            if self.serial.search_servo(servo_id) != 0:
                success = False
                self.make_log(False, f"Servo {servo_id} is not found.")
            else:
                self.make_log(True, f"Servo {servo_id} found.")

        if not self.serial.is_controller_connected():
            success = False
            self.make_log(False, f"Atom is not connected.")
        else:
            self.make_log(True, f"Atom is connected.")

        return success

    @penetration_mode
    def test_firmware_version(self):
        data = self.json_data["firmware_version"][self.robot_name]
        success = True

        running_basic_v = self.serial.get_basic_version()
        latest_basic_v = data["basic"]
        if running_basic_v != latest_basic_v:
            success = False
            self.make_log(
                False, f"Basic firmware version is not latest. latest version is {latest_basic_v}, your version is {running_basic_v}")
        else:
            self.make_log(
                True, f"Basic firmware version is latest ({latest_atom_v}).")

        running_atom_v = self.serial.get_atom_version()
        latest_atom_v = data["atom"]
        if running_atom_v != latest_atom_v:
            success = False
            self.make_log(
                False, f"Atom firmware version is not latest. latest version is {latest_atom_v}, your version is {running_atom_v}")
        else:
            self.make_log(
                True, f"Atom firmware version is latest ({latest_atom_v}).")
        # TODO: add pico firmware

        return success

    @penetration_mode
    def test_servo_status(self):
        success = True
        for servo_id in range(1, self.servo_count + 1):
            if self.serial.get_servo_error(servo_id) != 0:
                success = False
                self.make_log(False, f"Servo {servo_id} error.")
            else:
                self.make_log(True, f"Servo {servo_id} found no error.")
        return success

    def test_running_params(self):
        success = True
        serie_name = self.robot_name.split(" ")[0]

        # reference frame requires multiple time check
        if serie_name not in ["ultraArm", "myPalletizer"]:
            ok = False
            for i in range(10):
                if self.serial.get_reference_frame() == 0:
                    ok = True
                    break

            if not ok:
                success = False
                sample = self.serial.get_reference_frame()
                self.make_log(
                    False, f"Default reference frame is base frame (0), running reference frame is ({sample})")
            else:
                self.make_log(
                    True, f"Running reference frame is the same as default (0).")

        # check end type
        if serie_name not in ["ultraArm", "myPalletizer"]:
            end_type = self.serial.get_end_type()
            if end_type != 0:
                success = False
                self.make_log(
                    False, f"Default end type is Flange ({end_type})")
            else:
                self.make_log(
                    True, f"Running end type is the same as default ({end_type}).")

        # check fresh mode
        if self.robot_name.startswith("myCobot 280") or self.robot_name.startswith(
            "mechArm 270"
        ):
            fresh_mode = self.serial.get_fresh_mode()
            if fresh_mode != 1:
                success = False
                self.make_log(
                    False, f"{serie_name}'s default fresh mode is fresh(1), running fresh mode is {fresh_mode}")
            else:
                self.make_log(
                    True, f"Running fresh mode is the same as default.")

        if self.robot_name.startswith("myCobot 320"):
            fresh_mode = self.serial.get_fresh_mode()
            if self.serial.get_fresh_mode() != 0:
                success = False
                self.make_log(
                    False, f"{serie_name}'s default fresh mdoe is interpolation(0), running fresh mode is {fresh_mode}")
            else:
                self.make_log(
                    True, f"Running fresh mode is the same as default.")

        # check MOVL or MOVP
        if serie_name not in ["ultraArm", "myPalletizer"]:
            fresh_mode = self.serial.get_fresh_mode()
            move_type = self.serial.get_movement_type()
            if fresh_mode == 0 and move_type != 1:
                success = False
                self.make_log(
                    False, f"When fresh mode is interpolation(0), movement type should be MOVL(1), got {move_type} instead.")
            elif fresh_mode == 1 and move_type != 0:
                success = False
                self.make_log(
                    False, f"When fresh mode is fresh(1), movement type should be MOVJ(0), got {move_type} instead.")
            else:
                self.make_log(
                    True, f"Fresh mode({fresh_mode}) and movement type ({move_type}) matched.")

        return success

    # check servo parameters
    @penetration_mode
    def test_servo_params(self):
        model_name = self.robot_name.split("-")[0].strip()
        servo_param_data: dict = self.json_data[model_name]
        joint_n = self.servo_count
        serial = self.serial
        servo_params_table = {
            "baud": (serial.get_servo_baud, serial.set_servo_baud),
            "reserved_addr": (
                serial.get_servo_response_speed,
                serial.set_servo_response_speed,
            ),
            "max_voltage": (serial.get_servo_max_voltage, serial.set_servo_max_voltage),
            "max_temp": (
                serial.get_servo_max_temperature,
                serial.set_servo_max_temperature,
            ),
            "PID": (serial.get_servo_pid, serial.set_servo_pid),
            "min_start_force": (serial.get_servo_min_start, serial.set_servo_min_start),
            "clockwise_insensitive_area": (
                serial.get_servo_clockwise,
                serial.set_servo_clockwise,
            ),
            "counter_clockwise_insensitive_area": (
                serial.get_servo_counter_clockwise,
                serial.set_servo_counter_clockwise,
            ),
        }

        def test_param(tag, getter) -> bool:
            success = True
            for i in range(1, joint_n + 1):
                running_param = getter(i)
                test_param = servo_param_data["servo_params"][i - 1][tag]
                if running_param != test_param:
                    success = False
                    self.make_log(False,
                                  f"{tag}, joint {i}, default value: {test_param}, real value: {running_param}")
                else:
                    self.make_log(True, f"{tag} test for joint {i} passed.")
            return success

        success = True
        for k, (getter, setter) in servo_params_table.items():
            if test_param(k, getter) is False:
                success = False

        return success
