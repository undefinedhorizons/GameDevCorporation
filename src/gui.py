from kivy.uix.boxlayout import BoxLayout

from utils import ButtonClick, get_game


class SelectWorkerButton(ButtonClick):
    def __init__(self, worker_name='worker', **kwargs):
        self.worker_name = worker_name
        super().__init__(**kwargs)

    def on_press(self):
        super().on_press()
        get_game().current_worker = self.worker_name


class SelectOfficeButton(ButtonClick):
    def __init__(self, office_name='office', **kwargs):
        self.office_name = office_name
        super().__init__(**kwargs)

    def on_press(self):
        super().on_press()
        get_game().current_office = self.office_name


class RoomButton(ButtonClick):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Rooms'
        self.size_hint = (.2, .2)
        self.pos_hint = {'x': .01, 'y': .79}

    def on_press(self):
        super().on_press()
        get_game().switch_state('office')
        if not get_game().is_office_opened:
            if get_game().is_worker_opened:
                get_game().gui.remove_widget(get_game().layout_worker)
                get_game().is_worker_opened = False
            layout_office = BoxLayout(orientation='horizontal', size_hint=(.5, .6))
            Office = SelectOfficeButton(office_name='office', text='Office', size_hint=(.2, .2),
                                        pos_hint={'x': .22, 'y': .79})
            Toilet = SelectOfficeButton(office_name='toilet', text='Toilet', size_hint=(.2, .2),
                                        pos_hint={'x': .22, 'y': .79})
            layout_office.add_widget(Office)
            layout_office.add_widget(Toilet)
            get_game().gui.add_widget(layout_office)

            get_game().layout_office = layout_office
            get_game().is_office_opened = True
        else:
            get_game().gui.remove_widget(get_game().layout_office)
            get_game().is_office_opened = False


class WorkerButton(ButtonClick):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Worker'
        self.size_hint = (.2, .2)
        self.pos_hint = {'x': .24, 'y': .79}

    def on_press(self):
        super().on_press()
        get_game().switch_state('worker')
        if not get_game().is_worker_opened:
            if get_game().is_office_opened:
                get_game().gui.remove_widget(get_game().layout_office)
                get_game().is_office_opened = False
            layout_worker = BoxLayout(orientation='horizontal', size_hint=(.5, .6))
            build_worker1 = SelectWorkerButton(worker_name='worker',
                                               text='Worker',
                                               size_hint=(.2, .2),
                                               pos_hint={'x': .22, 'y': .79})
            build_worker2 = SelectWorkerButton(worker_name='repairman',
                                               text='RepairMan',
                                               size_hint=(.2, .2),
                                               pos_hint={'x': .22, 'y': .79})
            layout_worker.add_widget(build_worker1)
            layout_worker.add_widget(build_worker2)
            get_game().gui.add_widget(layout_worker)

            get_game().layout_worker = layout_worker
            get_game().is_worker_opened = True
        else:
            get_game().gui.remove_widget(get_game().layout_worker)
            get_game().is_worker_opened = False
