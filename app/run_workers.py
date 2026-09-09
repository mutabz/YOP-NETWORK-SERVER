import multiprocessing
import subprocess


workers = [
    ("critical", 4),
    ("high_priority", 8),
    ("medium_priority", 4),
    ("low_priority", 2),
]


def run_worker(queue, concurrency):

    subprocess.run(
        [
            "python",
            "-m",
            "/worker",
            queue,
            str(concurrency)
        ]
    )


if __name__ == "__main__":

    processes = []

    for queue, concurrency in workers:

        p = multiprocessing.Process(
            target=run_worker,
            args=(queue, concurrency)
        )

        p.start()

        processes.append(p)

    for p in processes:
        p.join()