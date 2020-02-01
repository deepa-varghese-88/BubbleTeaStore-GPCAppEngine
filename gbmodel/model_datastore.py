# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .Model import Model
from google.cloud import datastore

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [ name, rating, review, drink_to_order ]
    where name, review, drink_to_order are String
    and rating is float
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['name'], entity['rating'], entity['review'], entity['drink_to_order']]

class model(Model):
    def __init__(self):
        self.client = datastore.Client('cpb100-255205')

    def select(self):
        query = self.client.query(kind = 'BubbleTea')
        entities = list(map(from_datastore,query.fetch()))
        return entities

    def insert(self, name, rating, review, drink_to_order):
        key = self.client.key('BubbleTea', name)
        rev = datastore.Entity(key)
        rev.update({
            'name': name,
            'rating' : rating,
            'review' : review, 
            'drink_to_order' : drink_to_order
            })
        self.client.put(rev)
        return True
