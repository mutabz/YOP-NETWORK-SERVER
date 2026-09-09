import sys

from app.core.celery_app import celery_app


def start_worker(queue="medium_priority", concurrency=4):

    celery_app.worker_main(
        [
            "worker",
            f"--queues={queue}",
            f"--concurrency={concurrency}",
            "--loglevel=info",
        ]
    )


if __name__ == "__main__":

    queue = "medium_priority"

    concurrency = 4

    if len(sys.argv) > 1:
        queue = sys.argv[1]

    if len(sys.argv) > 2:
        concurrency = int(sys.argv[2])

    start_worker(
        queue=queue,
        concurrency=concurrency
    )