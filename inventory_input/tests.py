# from django import http
import re
from urllib import response
from xmlrpc.server import list_public_methods
from django.test import TestCase
# from django.urls import resolve
# from django.http import HttpRequest, response
# from django.template.loader import render_to_string
from inventory_input.models import Item, List

#  from inventory_input.views import home_page
# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

#TODO: Is POST test too long?
    

class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = 'The first (ever) inv item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Inv the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) inv item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Inv the second')
        self.assertEqual(second_saved_item.list, list_)

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        response = self.client.post('/inventory_management/new', data={
            'item_text': 'A new inventory item'
        })

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new inventory item')

    def test_redirects_after_POST(self):
        response = self.client.post('/inventory_management/new', data={
            'item_text': 'A new inventory item'
        })
        new_list = List.objects.first()
        self.assertRedirects(response, f'/inventory_management/{new_list.id}/')

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        new_list = List.objects.first()
        response = self.client.get(f'/inventory_management/{new_list.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemy 1', list=correct_list)
        Item.objects.create(text='itemy 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/inventory_management/{correct_list.id}/')

        self.assertContains(response, 'itemy 1')
        self.assertContains(response, 'itemy 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

