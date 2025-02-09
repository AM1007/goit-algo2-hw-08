# Homework on "Flow Control Algorithms and Rate Limiting"

Greetings 🌞

Today, you will practice applying data flow control algorithms to solve practical problems.

Imagine that a chat system requires a mechanism to limit the frequency of user messages to prevent spam. You need to implement this in two ways:

  - Using the Sliding Window algorithm for precise control of time intervals, allowing you to track the number of messages within a given time window and restrict users from sending messages if the limit is exceeded.
  - Using the Throttling algorithm to control time intervals between messages, ensuring a fixed waiting period between messages and limiting message frequency if the interval is not met.

Ready? Let's get to work!

Good luck! 😎


### Task 1: Implementing a Rate Limiter using the Sliding Window Algorithm

In the chat system, a mechanism must be implemented to limit the frequency of user messages to prevent spam. The implementation should use the Sliding Window algorithm for precise time interval control, allowing you to track the number of messages in a given time window and restrict users if the limit is exceeded.

# Technical Requirements

1. The implementation must use the Sliding Window algorithm for accurate time interval control.

2. System parameters:
Window size (window_size): 10 seconds
Maximum messages per window (max_requests): 1

3. Implement the class SlidingWindowRateLimiter.

4. Implement the following methods:
  - `_cleanup_window` – removes outdated requests from the window and updates the active time window.
  - `can_send_message` – checks whether a message can be sent within the current time window.
  - `record_message` – records a new message and updates the user's message history.
  - `time_until_next_allowed` – calculates the wait time until the next allowed message.

5. The data structure for storing message history: collections.deque.

**Acceptance Criteria**

📌 Meeting these criteria is mandatory for mentor review. If any criterion is not met, the mentor will return the homework for revision without evaluation. If you need clarification 😉 or get stuck at any step, feel free to ask your mentor in Slack.

1. If a message is sent before 10 seconds have passed, the can_send_message method should return False.
2. For a user's first message, the method should always return True.
3. When all messages are removed from a user’s window, the user’s record should be deleted from the data structure.
4. The time_until_next_allowed method should return the wait time in seconds.
5. The test function runs according to the provided example and behaves as expected.


Task template

```python
import random
from typing import Dict
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        pass

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        pass

    def can_send_message(self, user_id: str) -> bool:
        pass

    def record_message(self, user_id: str) -> bool:
        pass

    def time_until_next_allowed(self, user_id: str) -> float:
        pass

# Demonstration of functionality
def test_rate_limiter():
    # Create a rate limiter: 10-second window, 1 message allowed
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    # Simulate a stream of messages from users (sequential IDs from 1 to 20)
    print("\n=== Simulating message stream ===")
    for message_id in range(1, 11):
        # Simulate different users (IDs from 1 to 5)
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}")

        # Small delay between messages for realism
        # Random delay between 0.1 and 1 second
        time.sleep(random.uniform(0.1, 1.0))

    # Wait for the window to clear
    print("\nWaiting for 4 seconds...")
    time.sleep(4)

    print("\n=== New batch of messages after waiting ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}")
        # Random delay between 0.1 and 1 second
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_rate_limiter()

```


Expected output

```python
=== Message flow simulation ===
Messages  1 | User 2 | ✓
Messages  2 | User 3 | ✓
Messages  3 | User 4 | ✓
Messages  4 | User 5 | ✓
Messages  5 | User 1 | ✓
Messages  6 | User 2 | × (expectation 7.0с)
Messages  7 | User 3 | × (expectation 6.5с)
Messages  8 | User 4 | × (expectation 7.0с)
Messages  9 | User 5 | × (expectation 6.8с)
Messages 10 | User 1 | × (expectation 7.4с)

Waiting 4 seconds...

=== New series of messages after expectation ===
Messages 11 | User 2 | × (expectation 1.0с)
Messages 12 | User 3 | × (expectation 0.7с)
Messages 13 | User 4 | × (expectation 0.4с)
Messages 14 | User 5 | × (expectation 0.0с)
Messages 15 | User 1 | ✓
Messages 16 | User 2 | ✓
Messages 17 | User 3 | ✓
Messages 18 | User 4 | ✓
Messages 19 | User 5 | ✓
Messages 20 | User 1 | × (expectation 7.0с)
```


## Task 2. Implementing a Rate Limiter Using the Throttling Algorithm to Restrict Message Frequency in a Chat

A chat system requires a mechanism to limit the frequency of user messages to prevent spam. The implementation should use the Throttling algorithm to control the time intervals between messages, ensuring a fixed wait time between messages and restricting the sending frequency if this interval is not met.

### Technical Requirements

1. The implementation must use the Throttling algorithm to control time intervals.
2. The system's base parameter: minimum interval between messages (`min_interval`) — 10 seconds.
3. Implement the `ThrottlingRateLimiter` class.
4. Implement the following methods:
  - `can_send_message(user_id: str) -> bool` — checks whether a message can be sent based on the time of the last message.
  - `record_message(user_id: str) -> bool` — records a new message and updates the last message timestamp.
  - `time_until_next_allowed(user_id: str) -> float` — calculates the time remaining until the next allowed message.
Use a dictionary (Dict[str, float]) to store the last message timestamp.

### Acceptance Criteria

1. If a user attempts to send a message less than 10 seconds after the previous one, `can_send_message` must return `False`.
2. The first message from a user should always return `True`.
3. The `time_until_next_allowed` method must return the waiting time (in seconds) until the next allowed message.
4. The provided test function should run and work as expected.

Task template
```python
import time
from typing import Dict
import random

class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        pass

    def can_send_message(self, user_id: str) -> bool:
        pass

    def record_message(self, user_id: str) -> bool:
        pass

    def time_until_next_allowed(self, user_id: str) -> float:
        pass

def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Simulating message flow (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'× (waiting {wait_time:.1f}s)'}")

        # Random delay between messages
        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting for 10 seconds...")
    time.sleep(10)

    print("\n=== New message series after waiting ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'× (waiting {wait_time:.1f}s)'}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_throttling_limiter()

```


Expected output
```python
=== Message flow simulation (Throttling) ===
Message  1 | User 2 | ✓
Message  2 | User 3 | ✓
Message  3 | User 4 | ✓
Message  4 | User 5 | ✓
Message  5 | User 1 | ✓
Message  6 | User 2 | × (expectation 7.4с)
Message  7 | User 3 | × (expectation 7.6с)
Message  8 | User 4 | × (expectation 7.6с)
Message  9 | User 5 | × (expectation 7.6с)
Message 10 | User 1 | × (expectation 7.4с)

Waiting 4 seconds...

=== New series of messages after expectation ===
Message 11 | User 2 | × (expectation 0.7с)
Message 12 | User 3 | × (expectation 0.6с)
Message 13 | User 4 | × (expectation 0.5с)
Message 14 | User 5 | ✓
Message 15 | User 1 | ✓
Message 16 | User 2 | ✓
Message 17 | User 3 | ✓
Message 18 | User 4 | ✓
Message 19 | User 5 | × (expectation 7.9с)
Message 20 | User 1 | × (expectation 7.7с)

```
