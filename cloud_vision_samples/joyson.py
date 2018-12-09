from enum import Enum


class Joyson:
    def __init__(self, action_object=None, key_index_filter=None):
        if not (callable(action_object) or isinstance(action_object, Joyson.Action)):
            raise ValueError("action must be callable or Jayson.Action class")
        if key_index_filter is not None and type(key_index_filter) is not list:
            raise ValueError("index_key_filter must be list.")
        self._action_object = action_object
        self._filter = key_index_filter
        self._has_action = action_object is not None
        self._has_filter = key_index_filter is not None
        self._depth = 0
        self._depth_filtered = 0

    class Action:
        def action(self, phase, depth, depth_filtered, element):
            pass

    class Phase(Enum):
        WHOLE = 0
        IN_DICT = 1
        OUT_DICT = 2
        IN_LIST = 3
        OUT_LIST = 4
        KEY = 5
        INDEX = 6
        VALUE = 7

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
        if self._action(can_action, Joyson.Phase.WHOLE, depth, depth_filtered, element) == Joyson.Termination.RETURN:
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
        self._change_depth(filtered, -1)

    def _accept(self, element, key_or_index):
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
