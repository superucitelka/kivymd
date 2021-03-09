from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable


class MyDataTable(MDDataTable):
    def __init__(self):
        MDDataTable.__init__(self,
            size_hint=(1, 1),
            use_pagination=True,
            check=True,
            column_data=[],
            row_data=[],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2
        )

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)

    def sort_on_signal(self, data):
        return sorted(data, key=lambda l: l[2])

    def sort_on_schedule(self, data):
        return sorted(data, key=lambda l: sum([int(l[-2].split(":")[0])*60, int(l[-2].split(":")[1])]))

    def sort_on_team(self, data):
        return sorted(data, key=lambda l: l[-1])
