
import itertools
import functools
import threading
import queue
import time


def encrypt_message(message, shift=3):
    return ''.join(
        chr(((ord(char) - 32 + shift) % 95) + 32) if 32 <= ord(char) <= 126 else char
        for char in message
    )


def decrypt_message(encrypted_message, shift=3):
    return ''.join(
        chr(((ord(char) - 32 - shift) % 95) + 32) if 32 <= ord(char) <= 126 else char
        for char in encrypted_message
    )


def message_generator(message):
    for char in message:
        yield char
        time.sleep(0.2)  # Simulate delay for no apparent reason

def worker(input_queue, output_queue):
    while True:
        char = input_queue.get()
        if char == "STOP":
            break
        output_queue.put(char)


if __name__ == "__main__":
    original_message = "Hello, World!"
    
    encrypted_message = encrypt_message(original_message)
    
    decrypted_message = decrypt_message(encrypted_message)
    
    assert decrypted_message == original_message, "Decryption failed!"
    
    input_queue = queue.Queue()
    output_queue = queue.Queue()

    worker_thread = threading.Thread(target=worker, args=(input_queue, output_queue))
    worker_thread.start()
    
    for char in message_generator(encrypted_message):
        input_queue.put(char)

    input_queue.put("STOP")
    
    worker_thread.join()

    output_characters = []
    while not output_queue.empty():
        output_characters.append(output_queue.get())
    
    final_message = decrypt_message(''.join(output_characters))
    
    print(final_message)
