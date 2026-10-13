import json

from classifier import classify_message


def load_test_cases(filename="data/sample_messages.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate():
    test_cases = load_test_cases()

    category_correct = 0
    queue_correct = 0
    urgency_correct = 0
    all_correct = 0

    total = len(test_cases)

    for case in test_cases:
        print(f"\nTesting {case['id']}: {case['message']}")

        try:
            result = classify_message(case["message"])

            category_match = (
                result["category"] == case["expected_category"]
            )

            queue_match = (
                result["queue"] == case["expected_queue"]
            )

            urgency_match = (
                result["urgent"] == case["expected_urgent"]
            )

            if category_match:
                category_correct += 1

            if queue_match:
                queue_correct += 1

            if urgency_match:
                urgency_correct += 1

            if category_match and queue_match and urgency_match:
                all_correct += 1

            print(f"  Expected: {case['expected_category']} / "
                  f"{case['expected_queue']} / "
                  f"urgent={case['expected_urgent']}")

            print(f"  Predicted: {result['category']} / "
                  f"{result['queue']} / "
                  f"urgent={result['urgent']}")

            print(
                f"  Result: "
                f"{'PASS' if category_match and queue_match and urgency_match else 'FAIL'}"
            )

        except Exception as error:
            print(f"  ERROR: {error}")

    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)

    print(f"Total messages: {total}")
    print(
        f"Category accuracy: "
        f"{category_correct / total * 100:.1f}%"
    )
    print(
        f"Queue accuracy: "
        f"{queue_correct / total * 100:.1f}%"
    )
    print(
        f"Urgency accuracy: "
        f"{urgency_correct / total * 100:.1f}%"
    )
    print(
        f"End-to-end accuracy: "
        f"{all_correct / total * 100:.1f}%"
    )


if __name__ == "__main__":
    evaluate()
