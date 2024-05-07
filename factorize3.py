# Напишіть реалізацію функції factorize, яка приймає список
# чисел та повертає список чисел, на які числа з вхідного списку поділяються без залишку.
from datetime import datetime
import logging
from multiprocessing import Process

p_count = 2

def factorize(*numbers):
    result = []
    for number in numbers:
        factors = []
        for x in range(1, number + 1):
            if number % x == 0:
                factors.append(x)
        result.append(factors)
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    start1 = datetime.now()

    a, b, c, d = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    logging.info(f"Час виконання синхронно: {datetime.now() - start1}")

    start2 = datetime.now()
    prs = []
    a, b, c, d = (128, 255, 99999, 10651060)

    for i in range(p_count):
        pr = Process(target=factorize, args = (a, b, c, d))
        pr.start()
        prs.append(pr)
    [pr.join() for pr in prs]    
    
    logging.info(f"Час виконання через процеси в {p_count} потоків: {datetime.now() - start2}")
