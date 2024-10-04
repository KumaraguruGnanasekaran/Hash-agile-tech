from elasticsearch import Elasticsearch
import pandas as pd

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def createCollection(p_collection_name):
    if not es.indices.exists(index=p_collection_name):
        es.indices.create(index=p_collection_name)
        print(f"Collection {p_collection_name} created.")
    else:
        print(f"Collection {p_collection_name} already exists.")

def indexData(p_collection_name, p_exclude_column):
    df = pd.read_csv('"Employee Sample Data 1.csv"')
    df = df.drop(columns=[p_exclude_column])
    
    for index, row in df.iterrows():
        es.index(index=p_collection_name, id=row['EmployeeNumber'], document=row.to_dict())
    print(f"Data indexed to collection {p_collection_name}, excluding column {p_exclude_column}.")

def searchByColumn(p_collection_name, p_column_name, p_column_value):
    query = {
        "query": {
            "match": {
                p_column_name: p_column_value
            }
        }
    }
    result = es.search(index=p_collection_name, body=query)
    return result['hits']['hits']

def getEmpCount(p_collection_name):
    query = {
        "query": {
            "match_all": {}
        }
    }
    result = es.count(index=p_collection_name, body=query)
    return result['count']

def delEmpById(p_collection_name, p_employee_id):
    es.delete(index=p_collection_name, id=p_employee_id)
    print(f"Employee with ID {p_employee_id} deleted from {p_collection_name}.")

def getDepFacet(p_collection_name):
    query = {
        "size": 0,
        "aggs": {
            "by_department": {
                "terms": {
                    "field": "Department.keyword"
                }
            }
        }
    }
    result = es.search(index=p_collection_name, body=query)
    return result['aggregations']['by_department']['buckets']

v_nameCollection = 'Hash_<YourName>'
v_phoneCollection = 'Hash_<YourPhoneLastFourDigits>'

createCollection(v_nameCollection)
createCollection(v_phoneCollection)

print("Initial Employee Count:", getEmpCount(v_nameCollection))

indexData(v_nameCollection, 'Department')
indexData(v_phoneCollection, 'Gender')

delEmpById(v_nameCollection, 'E02003')

print("Employee Count after deletion:", getEmpCount(v_nameCollection))

print("Search by Department (IT):", searchByColumn(v_nameCollection, 'Department', 'IT'))
print("Search by Gender (Male):", searchByColumn(v_nameCollection, 'Gender', 'Male'))

print("Department Facet (Name Collection):", getDepFacet(v_nameCollection))
print("Department Facet (Phone Collection):", getDepFacet(v_phoneCollection))