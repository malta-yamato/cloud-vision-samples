from enum import Enum


class Joyson:
    def __init__(self, action_object=None, key_index_filter=None, strict_filter=False):
        if not (callable(action_object) or isinstance(action_object, Joyson.Action)):
            raise ValueError("action must be callable or Jayson.Action class")
        if key_index_filter is not None and type(key_index_filter) is not list:
            raise ValueError("index_key_filter must be list.")
        self._action_object = action_object
        self._filter = key_index_filter
        self._strict_filter = strict_filter
        self._filter_missed = False
        self._has_action = action_object is not None
        self._has_filter = key_index_filter is not None
        self._depth = 0
        self._depth_filtered = 0

    class Action:
        def action(self, phase, depth, depth_filtered, element):
            pass

    class Phase(Enum):
        IN_WHOLE = 0
        OUT_WHOLE = 1
        IN_DICT = 2
        OUT_DICT = 3
        IN_LIST = 4
        OUT_LIST = 5
        KEY = 6
        INDEX = 7
        VALUE = 8

    class Termination(Enum):
        NONE = 0
        RETURN = 1
        CONTINUE = 2
        BREAK = 3

    @staticmethod
    def accept(json_element, joyson):
        joyson.visit(json_element)

    def visit(self, element):
        filtered = self._check_filter()
        self._change_depth(filtered, 1)
        #
        can_action = self._has_action and filtered
        depth = self._depth
        depth_filtered = self._depth_filtered
        if self._action(can_action, Joyson.Phase.IN_WHOLE, depth, depth_filtered, element) == Joyson.Termination.RETURN:
            self._change_depth(filtered, -1)
            return
        #
        type_elm = type(element)
        if type_elm is dict:
            self._action(can_action, Joyson.Phase.IN_DICT, depth, depth_filtered, element)
            for key in element:
                termination = self._action(can_action, Joyson.Phase.KEY, depth, depth_filtered, key)
                if termination == Joyson.Termination.CONTINUE:
                    continue
                self._accept(element, key)
                if termination == Joyson.Termination.BREAK:
                    break
            self._action(can_action, Joyson.Phase.OUT_DICT, depth, depth_filtered, element)
        elif type_elm is list:
            self._action(can_action, Joyson.Phase.IN_LIST, depth, depth_filtered, element)
            for idx, _ in enumerate(element):
                termination = self._action(can_action, Joyson.Phase.INDEX, depth, depth_filtered, idx)
                if termination == Joyson.Termination.CONTINUE:
                    continue
                self._accept(element, idx)
                if termination == Joyson.Termination.BREAK:
                    break
            self._action(can_action, Joyson.Phase.OUT_LIST, depth, depth_filtered, element)
        else:
            self._action(can_action, Joyson.Phase.VALUE, depth, depth_filtered, element)
        #
        self._action(can_action, Joyson.Phase.OUT_WHOLE, depth, depth_filtered, element)
        self._change_depth(filtered, -1)

    def _accept(self, element, key_or_index):
        tmp = None
        if self._strict_filter:
            if not self._filter_missed:
                cur_filter = self._peek_filter()
                if cur_filter is not None:
                    if cur_filter == key_or_index:
                        tmp = self._pop_filter()
                    else:
                        self._filter_missed = True
        else:
            tmp = self._pop_filter() if self._peek_filter() == key_or_index else None
        Joyson.accept(element[key_or_index], self)
        self._push_filter(tmp)

    def _action(self, can_action, phase, depth, depth_filtered, element):
        if not can_action:
            return Joyson.Termination.NONE
        action = self._action_object
        if callable(action):
            return action(phase, depth, depth_filtered, element)
        elif isinstance(action, Joyson.Action):
            return action.action(phase, depth, depth_filtered, element)
        else:
            raise ValueError("Invalid action")

    def _change_depth(self, filtered, num):
        self._depth += num
        if filtered:
            self._depth_filtered += num

    def _check_filter(self):
        return not self._has_filter or len(self._filter) == 0

    def _peek_filter(self):
        if self._has_filter and len(self._filter) > 0:
            return self._filter[-1]
        return None

    def _pop_filter(self):
        if self._has_filter and len(self._filter) > 0:
            return self._filter.pop()
        return None

    def _push_filter(self, index_or_key):
        if self._has_filter and index_or_key is not None:
            self._filter.append(index_or_key)


def extract(json_data, key_index_filter=None, strict_filter=False):
    extracted = []

    # noinspection PyUnusedLocal
    def action(phase, depth, depth_filtered, element):
        if phase == Joyson.Phase.IN_WHOLE:
            extracted.append(element)
            return Joyson.Termination.RETURN

    Joyson.accept(json_data, Joyson(action, key_index_filter, strict_filter))
    return extracted


def structure(json_data, key_index_filter=None, strict_filter=False, writer=None):
    class ActionClass(Joyson.Action):

        # noinspection PyShadowingNames
        def __init__(self, writer=None):
            self._writer = writer
            self._current_dict = []
            self._current_list = []
            self._indent_unit = "  "
            self._reduce_indent_level = 0

        def action(self, phase, depth, depth_filtered, element):
            indent = self._indent_unit * (depth_filtered - self._reduce_indent_level - 1)
            if phase == Joyson.Phase.IN_DICT:
                self._current_dict.append(element)
            elif phase == Joyson.Phase.OUT_DICT:
                self._current_dict.pop()
            if phase == Joyson.Phase.IN_LIST:
                self._current_list.append(element)
                self._reduce_indent_level += 1
            elif phase == Joyson.Phase.OUT_LIST:
                self._current_list.pop()
                self._reduce_indent_level -= 1
            elif phase == Joyson.Phase.KEY:
                child = self._current_dict[-1][element]
                if type(child) is dict:
                    self._print(indent + str(element) + ": ")
                elif type(child) is list:
                    self._print(indent + str(element), end="")
                else:
                    self._print(indent + str(element) + ": ", end="")
            elif phase == Joyson.Phase.INDEX:
                child = self._current_list[-1][element]
                if type(child) is dict:
                    self._print('[' + str(element) + "]" + ": ")
                elif type(child) is list:
                    self._print('[' + str(element) + "]", end="")
                else:
                    self._print('[' + str(element) + "]" + ": ", end="")
                if element == 0:
                    return Joyson.Termination.BREAK
            elif phase == Joyson.Phase.VALUE:
                self._print(str(type(element)).replace("class ", "").replace("'", ""))

        def _print(self, values, end=None):
            if self._writer is None:
                if end is None:
                    print(values)
                else:
                    print(values, end=end)
            else:
                if end is None:
                    self._writer.write(values + "\n")
                else:
                    self._writer.write(values + end)

    Joyson.accept(json_data, Joyson(ActionClass(writer), key_index_filter, strict_filter))
