import random
import threading
import time

class Publisher:
    def __init__(self):
        self.subscribers = []
        self.current_ticker = None
        self.initial_price = None

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify(self, data):
        for subscriber in self.subscribers:
            subscriber.update(data)

    def simulate_real_time_data(self):
        def update_loop():
            while True:
                if self.current_ticker and self.initial_price is not None:
                    simulated_change = random.uniform(-0.99, 0.99)
                    simulated_price = self.initial_price + simulated_change
                    self.notify({'ticker': self.current_ticker, 'price': simulated_price})
                time.sleep(1)  # Simulate real-time updates every six seconds

        threading.Thread(target=update_loop, daemon=True).start()

    def set_ticker(self, ticker, initial_price):
        self.current_ticker = ticker
        self.initial_price = initial_price

class Subscriber:
    def update(self, data):
        raise NotImplementedError("Subscribers must implement the update method.")
