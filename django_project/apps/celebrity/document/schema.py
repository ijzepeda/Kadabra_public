from elasticsearch import Elasticsearch
from django.conf import settings


class Faces:
    INDEX = "celebrity"

    def __init__(self):
        self.es = Elasticsearch(
            settings.ELASTICSEARCH_HOST,
            basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PWD),
            verify_certs=settings.ELASTICSEARCH_VERIFY_CERTS
        )

    def __check_index(self):
        if not self.es.indices.exists(index=self.INDEX):
            self.__create_index()

    def __create_index(self):
        index_body = {
            "mappings": {
                "properties": {
                    "face_encoding": {
                        "type": "dense_vector",
                        "dims": 128
                    },
                    "image_id": {
                        "type": "keyword"
                    },
                    "actor_id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "keyword"
                    }
                }
            },
            "settings": {
                "index": {
                    "routing": {
                        "allocation": {
                            "include": {
                                "_tier_preference": "data_content"
                            }
                        }
                    },
                    "number_of_shards": "1",
                    "number_of_replicas": "1"
                }
            }
        }

        print(f"creating '{self.INDEX}' index...")
        self.es.indices.create(index=self.INDEX, body=index_body)

    def update_one(self, row):
        self.__check_index()

        data_dict = {
            "name": row["name"],
            "image_id": row["image_id"],
            "actor_id": row["actor_id"],
            "face_encoding": row["face_encoding"]
        }

        result = self.es.update(index=self.INDEX, id=row["id"], body={"doc": data_dict})
        print(result)

    def insert_one(self, row):
        self.__check_index()

        data_dict = {
            "name": row["name"],
            "image_id": row["image_id"],
            "actor_id": row["actor_id"],
            "face_encoding": row["face_encoding"]
        }
        result = self.es.index(index=self.INDEX, id=row["id"], document=data_dict)
        print(result)

    def insert_many(self, data):
        self.__check_index()

        bulk_data = []

        for index, row in data.iterrows():
            data_dict = {
                "name": row["name"],
                "image_id": row["image_id"],
                "actor_id": row["actor_id"],
                "face_encoding": row["face_encoding"]
            }
            op_dict = {
                "index": {
                    "_index": self.INDEX,
                    "_id": row['id']
                }
            }
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)

        res = self.es.bulk(index=self.INDEX, body=bulk_data)
        print(res)

    def delete_by_document_id(self, document_id):
        return self.es.delete(index=self.INDEX, id=document_id)

    def get_by_document_id(self, document_id):
        return self.es.get(index=self.INDEX, id=document_id)

    def check_by_document_id(self, document_id):
        return self.es.exists(index=self.INDEX, id=document_id)

    def query(self):
        return self.es.search(body={"query": {"match_all": {}}}, index=self.INDEX)

    def query_face(self, face_encoding, size=1):
        query = {
            'function_score': {
                'functions': [
                    {
                        'script_score': {
                            'script': {
                                'source': "cosineSimilarity(params.query_vector, 'face_encoding')",
                                'params': {
                                    'query_vector': face_encoding.tolist()
                                }
                            }
                        }
                    }
                ],
                'query': {
                    'bool': {
                        'must': [{'match_all': {}}]
                    }
                }
            }
        }

        resp = self.es.search(index=self.INDEX, query=query, size=size, _source=["name", "image_id", "actor_id"])
        return resp

    def get_mapping(self):
        return self.es.indices.get_mapping(index=self.INDEX)
