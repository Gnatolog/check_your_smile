class Vieweresulter:
    """

    Viewer result for client

    """

    # region field

    def __init__(self):
        self.template = {}

    # endregion

    # region method

    def get_result_view(self):
        self.template['name'] = ''
        self.template['result_front_vertical'] = ''
        self.template['result_front_hor'] = ''
        self.template['result_lateral_vert'] = ''
        self.template['result_lateral_sag'] = ''
        self.template['preliminary diagnosis'] = ''
        self.template['recommendation'] = ''
        return self.template

    # endregion



