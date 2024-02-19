import psutil

# -------------------------------------------


class RAM:
    @staticmethod
    def get_available_in_GB(include_swap=False) -> float:
        available_memory = psutil.virtual_memory().available / (1024 ** 3)
        if include_swap:
            swap_memory = psutil.swap_memory().free / (1024 ** 3)
            available_memory += swap_memory
        return available_memory

    @staticmethod
    def get_total_in_GB(include_swap=False) -> float:
        total_memory = psutil.virtual_memory().total / (1024 ** 3)
        if include_swap:
            swap_memory = psutil.swap_memory().total / (1024 ** 3)
            total_memory += swap_memory

        return total_memory



if __name__ == '__main__':
    total = RAM.get_total_in_GB()