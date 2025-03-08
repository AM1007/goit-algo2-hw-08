import time
from typing import Dict
import random

class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        """
        Ініціалізує Rate Limiter з алгоритмом Throttling.
        
        Args:
            min_interval: мінімальний інтервал між повідомленнями в секундах
        """
        self.min_interval = min_interval
        # Словник для зберігання часу останнього повідомлення користувача
        self.last_message_time: Dict[str, float] = {}
    
    def can_send_message(self, user_id: str) -> bool:
        """
        Перевіряє, чи може користувач відправити повідомлення на основі часу 
        останнього повідомлення.
        
        Args:
            user_id: ідентифікатор користувача
            
        Returns:
            True, якщо користувач може відправити повідомлення, False інакше
        """
        current_time = time.time()
        
        # Якщо користувач ще не відправляв повідомлень, дозволяємо відправку
        if user_id not in self.last_message_time:
            return True
        
        # Перевіряємо, чи пройшов мінімальний інтервал з моменту останнього повідомлення
        time_since_last = current_time - self.last_message_time[user_id]
        return time_since_last >= self.min_interval
    
    def record_message(self, user_id: str) -> bool:
        """
        Записує нове повідомлення з оновленням часу останнього повідомлення.
        
        Args:
            user_id: ідентифікатор користувача
            
        Returns:
            True, якщо повідомлення було успішно записано, False інакше
        """
        # Перевіряємо, чи може користувач відправити повідомлення
        if not self.can_send_message(user_id):
            return False
        
        # Записуємо час останнього повідомлення
        self.last_message_time[user_id] = time.time()
        return True
    
    def time_until_next_allowed(self, user_id: str) -> float:
        """
        Розраховує час до можливості відправлення наступного повідомлення.
        
        Args:
            user_id: ідентифікатор користувача
            
        Returns:
            Час очікування в секундах. 0, якщо користувач може відправити повідомлення зараз.
        """
        current_time = time.time()
        
        # Якщо користувач ще не відправляв повідомлень, час очікування 0
        if user_id not in self.last_message_time:
            return 0.0
        
        # Розраховуємо, скільки часу залишилося до наступного дозволеного повідомлення
        elapsed_time = current_time - self.last_message_time[user_id]
        remaining_time = self.min_interval - elapsed_time
        
        # Повертаємо залишковий час, але не менше 0
        return max(0.0, remaining_time)


def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Симуляція потоку повідомлень (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        # Випадкова затримка між повідомленнями
        time.sleep(random.uniform(0.1, 1.0))

    print("\nОчікуємо 10 секунд...")
    time.sleep(10)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_throttling_limiter()