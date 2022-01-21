# from django import http
import re
from urllib import response
from django.test import TestCase
# from django.urls import resolve
# from django.http import HttpRequest, response
# from django.template.loader import render_to_string
from inventory_input.models import Item

#  from inventory_input.views import home_page
# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

#TODO: Is POST test too long?
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={
            'item_text': 'A new inventory item'
        })

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new inventory item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={
            'item_text': 'A new inventory item'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='inv1')
        Item.objects.create(text='inv2')

        response = self.client.get('/')

        self.assertIn('inv1', response.content.decode())
        self.assertIn('inv2', response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) inv item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Inv the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) inv item')
        self.assertEqual(second_saved_item.text, 'Inv the second')

