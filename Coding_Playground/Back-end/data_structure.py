from data_base import get_users, post_user, get_project_history, post_project_history

# Import functions for interacting with the database.
# get_users retrieves user data, post_user adds new user data,
# get_project_history retrieves project history, and post_project_history adds new project history.

# Define a class for a linked list node.
class LLNode:
    # Constructor for the LLNode class.
    def __init__(self, data):
        # The data to be stored in the node.
        self.data = data
        # Pointer to the next node in the list, initialized to None.
        self.next = None

# Define a class for a linked list.
class LinkedList:
    """
    Linked list for storing login information.
    This version integrates with the database.
    """
    # Constructor for the LinkedList class.
    def __init__(self):
        # Head of the linked list, initially None.
        self.head = None

    # Method to insert a new node at the beginning of the list.
    def insert(self, data):
        """Insert new data at the beginning (for O(1) insertion) 
           and save to DB."""
        # Create a new node with the given data.
        new_node = LLNode(data)
        # Set the next of the new node to the current head.
        new_node.next = self.head
        # Set the head to the new node.
        self.head = new_node
        # Post new user to database
        # Assuming data is a dict with username and password_hash keys.
        post_user(data.get("username"), data.get("password_hash"))
        
    # Method to find a node with a given key.
    def find(self, key, key_func=lambda x: x):
        """Traverse the list to find a node matching the key.
           key_func defines how to extract the value from stored data."""
        # Start at the head of the list.
        current = self.head
        # Traverse the list.
        while current:
            # If the key matches the current node's data, return the data.
            if key_func(current.data) == key:
                return current.data
            # Move to the next node.
            current = current.next
        # If the key is not found, return None.
        return None

    # Method to traverse the list and return all elements.
    def traverse(self):
        """Return all elements in the list."""
        # Initialize an empty list to store the elements.
        elements = []
        # Start at the head of the list.
        current = self.head
        # Traverse the list.
        while current:
            # Append the current node's data to the list.
            elements.append(current.data)
            # Move to the next node.
            current = current.next
        # Return the list of elements.
        return elements

    # Method to retrieve all users from the database.
    def get_from_db(self):
        """Retrieve all users from the database."""
        return get_users()

    # Method to insert new login data into the database.
    def post_to_db(self, data):
        """Insert new login data into the database."""
        return post_user(data.get("username"), data.get("password_hash"))

# Define a class for a stack.
class Stack:
    """
    Stack for project history and autosave version control.
    Integrates with the database for persistent storage.
    """
    # Constructor for the Stack class.
    def __init__(self):
        # Use a list for internal storage.
        self.items = []  # using list for internal storage

    # Method to add an item to the stack.
    def push(self, item):
        """
        Add item to the stack and save to database.
        Here item is expected to be a dict with keys 'user_id', 'project_name', and 'data'.
        """
        # Append the item to the list.
        self.items.append(item)
        # Save new project history / autosave record to DB.
        post_project_history(item.get("user_id"), item.get("project_name"), item.get("data"))

    # Method to remove and return the top item from the stack.
    def pop(self):
        # If the stack is empty, return None.
        if self.is_empty():
            return None
        # Remove the last item from the list.
        item = self.items.pop()
        # Optionally, update the database state if you wish to remove the latest version.
        return item

    # Method to return the top item from the stack without removing it.
    def top(self):
        # If the stack is empty, return None.
        if self.is_empty():
            return None
        # Return the last item in the list.
        return self.items[-1]

    # Method to check if the stack is empty.
    def is_empty(self):
        # Return True if the list is empty, False otherwise.
        return len(self.items) == 0

    # Method to traverse the stack and return a copy of the items.
    def traverse(self):
        """Return a copy of the current stack (top at the end of list)."""
        # Return a copy of the list.
        return self.items.copy()

    # Method to retrieve all project history records for a given user from the database.
    def get_from_db(self, user_id):
        """
        Retrieve all project history records for the given user.
        This can be used to initialize the stack.
        """
        return get_project_history(user_id)

    # Method to persist the given item to the database.
    def post_to_db(self, item):
        """
        Persist the given item to the database.
        Same as push but provided as a separate method if needed.
        """
        return post_project_history(item.get("user_id"), item.get("project_name"), item.get("data"))
