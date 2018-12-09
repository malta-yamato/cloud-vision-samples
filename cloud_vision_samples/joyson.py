from enum import Enum


class Joyson:
    def __init__(self, action=None, index_key_filter=None):
        if index_key_filter is not None and type(index_key_filter) is not list:
            raise ValueError("index_key_filter must be list")
        self._action = action
        self._filter = index_key_filter
        self._depth = 0
        self._depth_filtered = 0

    class Phase(Enum):
        WHOLE = 0
        INDEX = 1
        KEY = 2
        VALUE = 3

    @staticmethod
    def accept(json_element, jason):
        jason.visit(json_element)

    def visit(self, element):
        filtered = self._check_filter()
        self._depth += 1
        if filtered:
            self._depth_filtered += 1
        if filtered and self._action(Joyson.Phase.WHOLE, self._depth, self._depth_filtered, element):
            return
        type_elm = type(element)
        if type_elm is dict:
            for key in element:
                ret = filtered and self._action(Joyson.Phase.KEY, self._depth, self._depth_filtered, key)
                self._accept(element, key)
                if ret:
                    break
        elif type_elm is list:
            for idx, _ in enumerate(element):
                ret = filtered and self._action(Joyson.Phase.INDEX, self._depth, self._depth_filtered, idx)
                self._accept(element, idx)
                if ret:
                    break
        else:
            if self._action is not None and filtered:
                filtered and self._action(Joyson.Phase.VALUE, self._depth, self._depth_filtered, element)
        self._depth -= 1
        if filtered:
            self._depth_filtered -= 1

    def _accept(self, element, index_or_key):
        tmp = self._pop_filter() if self._peek_filter() == index_or_key else None
        Joyson.accept(element[index_or_key], self)
        self._push_filter(tmp)

    def _check_filter(self):
        return self._filter is None or len(self._filter) == 0

    def _peek_filter(self):
        if self._filter is not None and len(self._filter) > 0:
            return self._filter[-1]
        return None

    def _pop_filter(self):
        if self._filter is not None and len(self._filter) > 0:
            return self._filter.pop()
        return None

    def _push_filter(self, index_or_key):
        if self._filter is not None and index_or_key is not None:
            self._filter.append(index_or_key)
