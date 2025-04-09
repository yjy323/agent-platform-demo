from typing import Any, Dict, List, Union


def calculate_sum(numbers: List[Union[int, float]]) -> Union[int, float]:
    total = 0.0
    for num in numbers:
        total = total + num
    return total


def process_data(data_list: List[Any], factor: float = 1.0) -> List[Union[int, float]]:
    processed_data: List[Union[int, float]] = []
    for item in data_list:
        if isinstance(item, (int, float)):
            processed_data.append(item * factor)
        else:
            processed_data.append(0)

    return processed_data


class DataProcessor:
    def __init__(self, name: str) -> None:
        self.name = name
        self.data: List[Union[int, float]] = []

    def add_data(self, value: Union[int, float]) -> None:
        self.data.append(value)

    def get_statistics(self) -> Dict[str, Union[int, float]]:
        if len(self.data) == 0:
            return {"count": 0, "sum": 0, "average": 0}

        total = calculate_sum(self.data)
        return {
            "count": len(self.data),
            "sum": total,
            "average": total / len(self.data),
        }


# Shortened variable name with proper line length
numbers_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# Function call with consistent spacing
result = calculate_sum([1, 2, 3, 4, 5])
