import json
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from tournaments.models import Tournament


class BaseTableViewTest():
    """Base class for testing table views; provides a default fixture and
    methods for setting tournament/clients and validating data"""

    fixtures = ['completed_demo.json']
    view_name = None
    round_seq = None

    def setUp(self):
        self.t = Tournament.objects.first()
        self.client = Client()

    def get_response(self):
        if self.round_seq is not None:
            return self.client.get(reverse(self.view_name, kwargs={
                'tournament_slug': self.t.slug, 'round_seq': self.round_seq}))
        else:
            return self.client.get(reverse(self.view_name, kwargs={
                'tournament_slug': self.t.slug}))

    def validate_table_data(self, r):
        # TODO: this isn't actually checking if the method or context data is present

        if hasattr(r.context, 'tableData') and hasattr(self, 'table_data'):
            print('validating single table data')
            data = len(json.loads(r.context['tableData']))
            self.assertEqual(self.validate_table_data, data)
        if hasattr(r.context, 'tableDataA') and hasattr(self, 'table_data_a'):
            print('validating double table data')
            data_a = len(json.loads(r.context['tableDataA']))
            self.assertEqual(self.validate_table_data_a(), data_a)
            data_b = len(json.loads(r.context['tableDataB']))
            self.assertEqual(self.validate_table_data_b(), data_b)
            print(self.validate_table_data_a(), data_a)
            print(self.validate_table_data_b(), data_b)


class TableViewTest(BaseTableViewTest):
    """For testing a view class that is always available. Inheriting classes
    must also inherit from TestCase"""

    def test(self):
        response = self.get_response()
        # 200 OK should be issued if setting is not enabled
        self.assertEqual(response.status_code, 200)
        self.validate_table_data(response)


class ConditionalTableViewTest(BaseTableViewTest):
    """For testing a view class that is conditionally shown depending on a
    preference being set or not. Inheriting classes must also inherit from
    TestCase and provide a view_toggle as a dynamic preferences path"""

    view_toggle = None

    def test_set_preference(self):
        # Check a page IS resolving when the preference is set
        self.t.preferences[self.view_toggle] = True
        response = self.get_response()

        # 200 OK should be issued if setting is not enabled
        self.assertEqual(response.status_code, 200)
        self.validate_table_data(response)

    def test_unset_preference(self):
        # Check a page is not resolving when the preference is not set
        self.t.preferences[self.view_toggle] = False
        response = self.get_response()

        # 302 redirect shoould be issued if setting is not enabled
        self.assertEqual(response.status_code, 302)
