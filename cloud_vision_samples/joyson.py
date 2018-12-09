from enum import Enum


class Joyson:
    def __init__(self, action=None, index_key_filter=None):
        if not callable(action):
            raise ValueError("action must be callable.")
        if index_key_filter is not None and type(index_key_filter) is not list:
            raise ValueError("index_key_filter must be list.")
        self._action = action
        self._filter = index_key_filter
        self._has_action = action is not None
        self._has_filter = index_key_filter is not None
        self._depth = 0
        self._depth_filtered = 0

    class Phase(Enum):
        WHOLE = 0
        INDEX = 1
        KEY = 2
        VALUE = 3

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
        action = self._action
        depth = self._depth
        depth_filtered = self._depth_filtered
        if can_action:
            ret = action(Joyson.Phase.WHOLE, depth, depth_filtered, element)
            if ret == Joyson.Termination.RETURN:
                self._change_depth(filtered, -1)
                return
        #
        type_elm = type(element)
        if type_elm is dict:
            for key in element:
                termination = Joyson.Termination.NONE
                if can_action:
                    termination = action(Joyson.Phase.KEY, depth, depth_filtered, key)
                if termination == Joyson.Termination.CONTINUE:
                    continue
                self._accept(element, key)
                if termination == Joyson.Termination.BREAK:
                    break
        elif type_elm is list:
            for idx, _ in enumerate(element):
                termination = Joyson.Termination.NONE
                if can_action:
                    termination = can_action and action(Joyson.Phase.INDEX, depth, depth_filtered, idx)
                if termination == Joyson.Termination.CONTINUE:
                    continue
                self._accept(element, idx)
                if termination == Joyson.Termination.BREAK:
                    break
        else:
            can_action and self._action(Joyson.Phase.VALUE, depth, depth_filtered, element)
        #
        self._change_depth(filtered, -1)

    def _accept(self, element, index_or_key):
        tmp = self._pop_filter() if self._peek_filter() == index_or_key else None
        Joyson.accept(element[index_or_key], self)
        self._push_filter(tmp)

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
