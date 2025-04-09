# import pytest as pytest
# import pytest
# import os
# import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from web_app.app import app


# @pytest.fixture
# def client():
#     app.config["TESTING"] = True
#     with app.test_client() as client:
#         yield client


# def test_home_page_status_code(client):
#     response = client.get("/")
#     assert response.status_code == 200


# def test_home_filter_silence(client):
#     params = {"type": "silence"}
#     response = client.get("/", query_string=params)
#     assert response.status_code == 200
#     assert b"Silence" in response.data


# def test_home_filter_speech(client):
#     params = {"type": "speech"}
#     response = client.get("/", query_string=params)
#     assert response.status_code == 200
#     assert b"Speech" in response.data
