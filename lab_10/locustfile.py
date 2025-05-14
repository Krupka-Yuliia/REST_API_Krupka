import random
from locust import HttpUser, task, between


class LibraryAPIUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_book_by_id(self):
        book_id = random.randint(1, 10)

        url = f"/v1/api/books/{book_id}"

        with self.client.get(url, catch_response=True, name=f"GET /v1/api/books/{book_id}") as response:
            if response.status_code != 200:
                response.failure(f"Request returned {response.status_code}")
            else:
                if not response.json().get("id") == book_id:
                    response.failure(f"Wrong book data: {response.text}")

    @task(2)
    def get_book_by_invalid_id(self):
        invalid_book_id = random.randint(100, 200)

        url = f"/v1/api/books/{invalid_book_id}"

        with self.client.get(url, catch_response=True, name=f"GET /v1/api/books/{invalid_book_id}") as response:
            if response.status_code == 404:
                response.success()
            else:
                response.failure(f"Expected 404, returned {response.status_code}")
