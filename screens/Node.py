class Node:
    def __init__(self, state=None, col=None, val=None, alpha=None, beta=None, parent=None, children=None, type=None):
        self.state = state      # Game state at this node
        self.col = col          # Column played to reach this node
        self.val = val          # Minimax value
        self.alpha = alpha      # Alpha value for alpha-beta pruning
        self.beta = beta        # Beta value for alpha-beta pruning
        self.parent = parent    # Parent node
        self.children = children or []  # Child nodes
        self.x = 0              # X-coordinate for visualization
        self.y = 0              # Y-coordinate for visualization
        self.expanded = False   # Whether this node's children are expanded
        self.label = ""         # Label displayed on the node
        self.content = ""       # Additional information for the node
        self.type = type

    # Getters
    def get_val(self):
        return self.val

    def get_col(self):
        return self.col

    def get_alpha(self):
        return self.alpha

    def get_beta(self):
        return self.beta

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    # Setters
    def set_val(self, val):
        self.val = val

    def set_alpha(self, alpha):
        self.alpha = alpha

    def set_beta(self, beta):
        self.beta = beta

    def set_children(self, children):
        self.children = children

    def set_parent(self, parent):
        self.parent = parent

    def set_col(self, col):
        self.col = col

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def toggle(self):
        """Toggle the expansion state of this node."""
        self.expanded = not self.expanded
