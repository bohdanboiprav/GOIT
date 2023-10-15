from multiprocessing import Pool, current_process, cpu_count
import time


def factorize(*number):
    name = current_process().name
    factors_list = []
    for num in number:
        item_factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                item_factors.append(i)
        factors_list.append(item_factors)
    print(name, *factors_list)
    return factors_list


def callback(result):
    print(*result)


if __name__ == "__main__":
    start_time = time.time()
    with Pool(cpu_count()) as pool:
        pool.map_async(factorize, [128, 255, 99999, 10651060], callback=callback)
        pool.close()
        pool.join()
    end_time = time.time()
    print("Time taken:", end_time - start_time, "seconds")