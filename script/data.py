import json
import bisect

DataType = list[tuple[str, int | float]]


def get_data(file: str) -> DataType:
    with open(f"resource/save/{file}.json", 'r') as f:
        data: dict[str, int | float] = json.load(f)
    return [*sorted(data.items(), key=lambda x: x[1])]


def check_data(file: str, score: int | float) -> int:
    data = get_data(file)
    return bisect.bisect_right(data, score, key=lambda x: x[1])


def save_data(file: str, name: str, score: int | float):
    data = get_data(file)
    duplicated = False
    data = {k: v for k, v in data}
    if name in data:
        duplicated = True
        data[name] = min(data[name], score)
    data = [*sorted(data.items(), key=lambda x: x[1])]
    if not duplicated:
        bisect.insort_right(data, (name, score), key=lambda x: x[1])
    data = data[:10]
    with open(f"resource/save/{file}.json", 'w') as f:
        json.dump({k: v for k, v in data}, f)
