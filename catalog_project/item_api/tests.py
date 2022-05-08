from django.test import TestCase
from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/api/items/create/',{
    "name": "Some random request",
    "owner": 10,
    "type": "Theoretical",
    "field": "Computer Science",
    "keyword_list": "ResearchGate",
    "content": "Documenting a REST API is important for its successful adoption. APIs expose data and services that consumers want to use. An API should be designed with an interface that the consumer can understand. API documentation is key to the app developers comprehending the API. The documentation should help the developer to learn about the API functionality and enable them to start using it easily. This chapter looks at the aspects of documenting an API and some of the tools and technologies available for API documentation, including RAML, Swagger, API Blueprint, and others.",
    "url": "https://www.researchgate.net/publication/315468327_API_Documentation",
    "status": "Completed"
},)