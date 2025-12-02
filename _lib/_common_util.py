import sys


def pr(*arg, **kwargs):
    if not is_frozen():
        try:
            print(*arg, **kwargs)
        except Exception as e:
            try:
                print(f"Error in pr function: {e}")
            except:
                pass

def is_frozen() -> bool:
    return hasattr(sys, 'frozen')


if __name__ == "__main__":
    # Test the is_frozen function
    print(f"is_frozen: {is_frozen()}")
    pr("This is a test message from pr function.")
    # Test the pr function
    pr("Another test message with multiple", "arguments:", 1, 2, 3)